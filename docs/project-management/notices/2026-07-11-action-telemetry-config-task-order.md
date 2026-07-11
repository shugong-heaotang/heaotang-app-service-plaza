# 动作遥测功能开关双人审批根因修复任务通知

- 通知编号：`SP-ACTION-TELEMETRY-CONFIG-TASK-20260711-001`
- 状态：正式下达；待平台治理提交集成后激活后端工作项
- 阻断：`CA-H1-M4-B001`
- 后端 work_id：`AIW-20260711-ACTION-TELEMETRY-BUSINESSCONFIG-BACKEND`
- 伴随证据 work_id：`AIW-20260711-ACTION-TELEMETRY-BUSINESSCONFIG-EVIDENCE`
- repository：`C:/Users/shugo/Documents/heaotang-main`
- branch/worktree：`codex/action-telemetry-businessconfig` / `C:/Users/shugo/Documents/worktrees/heaotang-action-telemetry-businessconfig`
- base：`47ef91bb5ca6774c40f6c4301ba3f25e224a4bd9`

## 授权范围

仅允许修改：

- `backend-go/internal/businessconfig/businessconfig.go`
- `backend-go/internal/businessconfig/businessconfig_test.go`
- `backend-go/plugins/config-plugin/plugin_test.go`
- `backend-go/plugins/service-plaza-plugin/infrastructure.go`
- `backend-go/plugins/service-plaza-plugin/infrastructure_test.go`

后端 Git 根只承载上述五个 Go 路径。当前检查单、随机治理考试和 implementation record 由 APP 治理仓库的独立伴随证据工作项在 `codex/action-telemetry-businessconfig-evidence` 工作树生成；两项使用同一 record_id，禁止把 APP 的 `contracts/` 目录复制到后端仓库，禁止无归属跨仓写入。

机器映射必须固定：权威 variable=`service-plaza.action-telemetry.enabled`；兼容 consumer endpoint/key=`GET /api/v1/service-plaza/feature-flags` / `action_telemetry`；legacy table=`service_plaza_feature_flags` authority=`forbidden`、role=`compatibility_only`。实现 boolean kind 和权威变量定义；Service Plaza 的 `action_telemetry` 只适配权威批准版本，未配置/失败关闭。复用现有配置插件提案/审核 API，不新增第二套审批，不改数据库、不修改前端、俱乐部业务或生产。

## 验收

必须覆盖：boolean true/false；字符串/数字/null/对象/数组/尾随值拒绝；unknown key；未配置/读取失败 false；同人审核 403；同键同载荷重放；异载荷 409；批准 true 后 action event accepted+stored；批准 false 后回滚；历史/审计可查；事件严格字段和敏感字段拒绝。还必须证明 legacy enabled=1+未配置=false、legacy enabled=1+approved false=false、legacy enabled=0+approved true=true，且旧 history 不得冒充批准历史，必须 superseded 或映射权威 versions。运行定向 Go tests、相关插件回归、`go test ./...`、`go vet ./...`、gofmt 和 diff 门禁。

后端提交与平台复核 Go 后才允许受控集成和测试环境部署。测试环境启用必须预先核验两个不同 `user_id`、角色等级不低于 2 的合成管理员；报告只记录角色满足和身份不同的事实，不保留凭据或完整 user_id。使用两名不同批准身份保留提案/审核/true/false 回滚证据；禁止直接 SQL。
