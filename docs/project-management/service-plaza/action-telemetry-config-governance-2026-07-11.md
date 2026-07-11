# 动作遥测功能开关根因修复治理报告

CA-H1 M4 已确认平台阻断 `CA-H1-M4-B001`：测试环境 `action_telemetry=false`，旧写入口正确失败关闭，但缺少可执行的双人审批接入。该问题属于 foundation/config，不属于俱乐部页面缺陷。

采用 ADR 0020：复用 `internal/businessconfig`，新增 boolean 权威变量 `service-plaza.action-telemetry.enabled`；兼容 consumer 固定为 `GET /api/v1/service-plaza/feature-flags` 的 `action_telemetry`。`service_plaza_feature_flags` 是 authority=forbidden 的 compatibility-only legacy table，不能覆盖权威版本，也不能把旧 history 冒充批准历史。未配置、依赖失败和非法值全部 false。禁止 SQL 捷径、单管理员写入口和第二套审批系统。

平台治理工作项：`AIW-20260711-ACTION-TELEMETRY-CONFIG-GOVERNANCE`。后端实现工作项：`AIW-20260711-ACTION-TELEMETRY-BUSINESSCONFIG-BACKEND`。平台 checklist 26/26、考试 `EX-20260711-ACTION-TELEMETRY-CONFIG-GOVERNANCE-1` score 100。

后端验收必须含 legacy=1/未配置=>false、legacy=1/approved false=>false、legacy=0/approved true=>true 三个冲突负例。测试环境执行前须核验两个不同 user_id、角色等级不低于 2 的合成管理员，报告仅记录角色和身份不同的事实。后端实现、测试环境双人启用、true/false 回滚和 M4 三类遥测复测全部完成前，CA-H1 M4 保持 No-Go；其余导航/query/layout 证据不受阻塞。
