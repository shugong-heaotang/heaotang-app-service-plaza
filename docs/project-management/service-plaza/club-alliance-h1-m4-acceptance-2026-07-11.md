# 俱乐部联盟 CA-H1 M4 验收执行记录

- work_id：`AIW-20260711-CLUB-ALLIANCE-H1-M4-ACCEPTANCE`
- branch/worktree：`codex/club-alliance-h1-m4-acceptance` / `C:/Users/shugo/Documents/worktrees/heaotang-club-h1-m4-acceptance`
- base：`91547b3db4a8a92537ff19193f2e2a6740318ccd`
- 当前阶段：部署 Pass；浏览器 UAT No-Go。
- 证据：`docs/project-management/modules/club-alliance/acceptance/CA-H1-M4-frontend-uat.md`。

本工作项只验收标准首页/页面壳，不调用 club search/create/join/member 等业务 API。网络证据分别记录模块 catalog/actions、APP 公共 feature-flags 和业务 denylist；部署、备份、回滚、浏览器、权限、遥测和八态未全部闭环前不得判 M4 Go。

当前根因阻断 `CA-H1-M4-B001`：测试环境 `action_telemetry=false`，旧功能开关写入口正确失败关闭为 `CONFIG_APPROVAL_WORKFLOW_REQUIRED`，但功能开关尚无已接入的双人提案/审核流程。平台必须先完成该公共依赖，禁止直接改库或以单管理员启用。
