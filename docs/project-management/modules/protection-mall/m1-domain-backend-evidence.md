# 保障商城 M1 纯领域核后端证据

日期：2026-07-13

## 精确实现

- 后端仓库：`C:/Users/shugo/Documents/和奥堂总后端`
- 分支：`codex/protection-mall-m1-domain-backend`
- 基线：`e41265905815082433e040412f3dd6b6b33dfede`
- exact source commit：`5368cc3d`
- 变更路径：`backend-go/plugins/mall-plugin/domain_m1.go`、`backend-go/plugins/mall-plugin/domain_m1_test.go`

## 合同映射

- `responsibility.v1.json`：显式商城类型、销售方、履约方和售后责任；保障权益仅允许保障商城订单完成且售后关闭。
- `state-machines.v1.json`：库存、订单、履约、售后、权益回滚五类状态机；乱序和终态写入失败关闭。
- `api-security.v1.json`：scope 只接受服务端授权登记源；校验资源归属；写操作必须提供幂等键；同键同载荷重放，同键异载荷冲突。

## 验证结果

- `gofmt -w plugins/mall-plugin/domain_m1.go plugins/mall-plugin/domain_m1_test.go`：通过。
- `go test -race ./plugins/mall-plugin`：通过。
- `go test ./...`：通过。
- `go vet ./...`：通过。
- `git diff --check`：通过。
- 两条精确路径秘密模式扫描：通过。

测试覆盖责任主体缺失、俱乐部商城禁止保障权益、无可信 scope、跨资源越权、缺幂等键、同键重放、同键异载荷、五类状态机合法转换、乱序、终态写入、补偿失败后同键重试和 32 并发同键唯一写入。

## 边界

实现只包含 Go 纯领域内存核和单元测试，未挂路由，未连接数据库、网络、支付、回调、真实资金、部署或真实数据。该提交不构成环境、支付或上线 Go。
