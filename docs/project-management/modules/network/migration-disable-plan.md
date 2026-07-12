# 人脉双事实源迁移与 legacy 禁用计划

## 目标

把多写入口收敛到 People/Connection facade 和 canonical `introduction_requests` 生命周期，同时保留可审计迁移、恢复点和明确 Sunset。本文是计划，不授权数据库变更。

## 路由分类

| 路径/能力 | 当前分类 | 目标 |
| --- | --- | --- |
| `GET /api/v1/network/search` | legacy read candidate | 加固后由 facade 适配，隐藏原始身份字段 |
| `POST /api/v1/network/introductions` | unsafe legacy write | 立即禁止 NOVA/新调用方，迁移后 `410 Gone` |
| `PUT /api/v1/network/introductions/:id` | unsafe legacy status | 立即禁止 NOVA/新调用方，迁移后 `410 Gone` |
| `POST /api/v1/network/referral` | unsafe duplicate writer | 立即冻结，迁移后 `410 Gone` |
| `POST/PUT /api/v1/social/introductions` | canonical target candidate | 只允许经 facade，在加固前不开放 NOVA |
| People/Connection facade | 尚未实现 | 唯一新入口 |

## 分阶段计划

### M0 盘点与冻结

- 生成仅含计数、状态分布、tenant 可判定性和哈希的脱敏盘点；不导出正文、手机号或完整用户标识。
- 冻结 network legacy 写路由的新调用方；CI 拒绝任何 NOVA 工具映射。
- 记录每个调用方、Owner、替代路径和 Sunset 版本。

### M1 facade 与 canonical 加固

- trusted server context 提供 actor/tenant；资源级服务端授权失败关闭。
- `connection_draft` 生成不可发送预览；`connection_send` 验证确认票据与幂等键。
- canonical 写入与 outbox 同事务；审计只保留允许字段、hash 和 trace。
- `RowsAffected=0` 必须稳定返回 not-found/conflict，不得伪装成功。

### M2 dry-run 与 tenant 隔离

- 使用备份副本和固定 run id 执行 dry-run，不修改权威数据。
- 仅迁移 actor、target、tenant 和状态均可证明的记录。
- tenant 未知、参与者冲突、非法状态或重复语义进入 quarantine；不得猜测归属。
- 输出 source id 到 canonical id 的不可变映射和校验摘要。

### M3 单向切换

- 先停止 legacy 写入，再切 facade 写侧；禁止双写过渡。
- legacy 读只允许受控兼容窗口，返回 deprecation/Sunset 和 canonical reference。
- 验证状态数、参与者归属、幂等重放、outbox 与审计闭包。

### M4 Sunset

- 在已公告版本把三类 unsafe write 路径改为稳定 `410 Gone`，返回机器可读 successor；不得把请求转发后伪装成功。
- 移除 legacy 写权限和调用配置；保留不可变迁移证据及按政策到期的最小审计。

## 回滚规则

1. 切换前必须有数据库备份、schema/version、制品 hash 和恢复演练。
2. 回滚只允许把 facade 指向切换前 canonical 版本或恢复备份；不得重新开放 network unsafe writes。
3. 已产生 canonical 请求不得反向双写至 legacy。
4. tenant/参与者/状态校验失败立即停止批次并恢复，不继续跳过。

## 验收矩阵

- forged actor/tenant、cross-tenant、opt-out、block relation、hidden field 全部拒绝。
- draft/target/version/disclosure/expiry 票据漂移全部拒绝。
- 同幂等键同载荷重放，同键异载荷冲突。
- canonical status 与 outbox/callback 一致；event id 异载荷冲突。
- legacy route 无 NOVA 映射；Sunset 后稳定 `410`。
- unknown tenant 留在 quarantine，零自动归属；dry-run 后可完整 restore。

## 当前状态

计划已冻结，实际 migration 为 `No-Go`；必须另立后端、数据迁移和环境验收工作项。
