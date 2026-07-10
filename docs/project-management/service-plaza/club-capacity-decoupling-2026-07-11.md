# 标准俱乐部与家庭容量配置依赖解耦

- 日期：2026-07-11
- 工作项：`AIW-20260711-CLUB-CAPACITY-GOVERNANCE` / `AIW-20260711-CLUB-CAPACITY-BACKEND`
- 实现记录：`IR-20260711-CLUB-CAPACITY-DECOUPLING`
- 后端提交：`b8996793`
- 当前结论：本地实现与回归 Go；测试环境未部署，俱乐部 M2 仍 No-Go

## 根因

普通非幂等加入路径已经只在 `type=family` 时解析 `club.family.member_capacity`，但幂等申请路径在识别俱乐部类型前无条件解析家庭容量；审核批准路径也在读取 application 和 club type 前无条件解析。家庭配置初始化或解析失败因此会错误阻塞 `standard` 自建俱乐部。

## 修复

新增按俱乐部类型解析容量的内部边界：

- standard/direct 返回零容量占位，不读取家庭业务变量；
- family 调用既有版本化业务变量解析器；
- family 配置不可用继续返回 `ErrBusinessVariableUnavailable`，不提供猜测默认值；
- 申请幂等事务和审核原子事务保持原结构。

## 验证

- 强制设置家庭配置初始化错误时，standard 幂等申请仍创建 pending；
- 同一错误下 standard 批准仍写入成员并将申请改为 approved；
- family 幂等申请失败关闭；
- family 批准失败且申请保持 pending；
- `go test -count=1 ./plugins/club-plugin` 通过；
- `go test -count=1 ./...` 通过；
- `go vet ./...` 与 `git diff --check` 通过。

第一次格式化命令因当前目录已是 `backend-go` 却重复传入 `backend-go/plugins/...` 而未执行；改为 `plugins/...` 后完成。该失败未计为测试成功。

## 未关闭

- 测试环境 HTTP 级 standard/family 验收；
- 本人申请状态接口；
- 审核写入 Idempotency-Key 与并发相反决定；
- 跨俱乐部越权、错配 application ID 和全部事务故障证据；
- 稳定 400/403/404/409 机器错误矩阵。

