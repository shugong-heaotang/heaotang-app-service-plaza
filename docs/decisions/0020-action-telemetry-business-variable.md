# ADR 0020：动作遥测功能开关复用版本化业务变量双人审批

- 状态：Accepted
- 日期：2026-07-11
- 决策者：项目负责人既定双人配置原则、平台集成负责人

## 背景

CA-H1 M4 真实环境验收发现 `action_telemetry=false`。客户端因此失败关闭且不发送 action-events；旧 feature flag 管理写入口无条件返回 `CONFIG_APPROVAL_WORKFLOW_REQUIRED`。直接修改数据库虽然能制造遥测事件，却绕过录入/审核分离、幂等、审计和回滚，禁止采用。

## 决策

新增权威变量 `service-plaza.action-telemetry.enabled`，kind=`boolean`，复用现有 `internal/businessconfig` 的 proposal/review、`proposed_by != reviewed_by`、幂等、有效时间、不可变版本和历史审计。

机器映射固定为：权威 variable=`service-plaza.action-telemetry.enabled`；兼容 consumer endpoint/key=`GET /api/v1/service-plaza/feature-flags` / `action_telemetry`；legacy table=`service_plaza_feature_flags`，authority=`forbidden`，仅作 compatibility-only 证据。公开兼容键的值只从权威变量解析：未配置、未生效、解析失败或依赖不可用均返回 false。旧 PUT 保持 409 锁定并指向通用业务变量审批接口；旧 history 必须明确 superseded，或映射到权威 business-variable versions，不能伪造批准历史。

boolean 仅接受 JSON `true` 或 `false`；字符串、数字、null、对象、数组和额外 JSON 值均拒绝。启用和关闭都必须由两个不同测试管理员完成审批；false 回滚形成新版本，不覆盖历史 true 版本。

## 禁止方案

- 直接 SQL 修改 feature flag；
- 恢复单管理员 PUT；
- 为 service-plaza 再复制一套审批表和审核逻辑；
- 把旧 enabled=1 自动迁移为已批准版本；
- 客户端猜测默认 true 或在读取错误时保持上次 true。

## 单一真相源验收负例

- legacy `enabled=1` 且权威变量未配置，公开 `action_telemetry=false`；
- legacy `enabled=1` 且已批准权威值为 false，公开值=false；
- legacy `enabled=0` 且已批准权威值为 true，公开值=true；
- legacy audit/history 不得作为批准版本历史；接口必须返回 superseded 标识或权威版本引用。

## 可证伪前提与复审

前提：businessconfig 能稳定承载 boolean、两个管理员身份独立、Service Plaza 初始化顺序能访问 businessconfig。测试环境必须存在两个不同 `user_id` 且角色等级不低于 2 的合成管理员；验收报告只记录“角色满足、身份不同”的事实，不记录凭据或完整用户标识。若未来配置服务独立部署、boolean 需要多环境分层、业务变量不可在请求路径安全读取，或无法提供两个独立合成管理员，应升级合同并复审。最迟在功能开关主版本变化或第二个模块提出同类开关时复审。
