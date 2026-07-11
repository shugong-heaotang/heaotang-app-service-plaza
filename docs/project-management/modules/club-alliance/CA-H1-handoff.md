# 俱乐部联盟 CA-H1 Handoff

## H1-M1 共享动作适配器检查点

- 日期：2026-07-11
- 工作项：`AIW-20260711-CLUB-ALLIANCE-H1-HOMEPAGE`
- 上游：`SP-H029`，权威激活修正 HEAD `07bb839014add1c4ea3e635b038b00fb7c105d5b`
- 实施记录：`IR-20260711-CLUB-ALLIANCE-H1-M1`
- 当前结论：模块自验通过，等待平台检查点验收

### 已完成

1. current checklist `28/28`，当前治理 SHA mismatch `0`；随机治理考试 attempt 1 为 `100`。
2. 冻结 TypeScript 首页合同：根路由、返回路由、四入口、管理附属入口、精确八态和稳定错误 ID。
3. 新增纯共享 action adapter，只从上游动作对象派生展示字段；打乱输入后仍按上游 `sort_order` 排序。
4. `club-manage` 明确作为附属入口返回，不进入四分类数组；额外第五分类失败关闭。
5. 缺失、重复、错误作用域和非法 target 稳定失败关闭。
6. `category` query 从上游 action target 解析为 `selected_action_id`；无 query 为 home，空白、未知、多值/多义分别稳定失败关闭。
7. M1 没有路由、页面、公共 repository/evaluator/telemetry、后端、Schema、部署或任何俱乐部业务 API 变更。

### 验证证据

- 定向 Vitest：2 files、9 tests，全通过。
- TypeScript + Vite production build：通过。
- 检查单 validator：通过；`28/28`、SHA mismatch `0`。
- 治理考试：`EX-20260711-CLUB-ALLIANCE-H1-M1-1`，score `100`。
- implementation record、治理考试、UTF-8、Git diff 和范围门禁在提交前复跑。

### 未完成与边界

- H1-M2 独立路由、首页组件、八态渲染、权限/生命周期/遥测复用和响应式尚未开始，等待 M1 平台 Go。
- H1-M3 全量前端与零业务 API 网络 allowlist/denylist 尚未开始。
- H1-M4 测试环境部署与浏览器 UAT 未授权。
- CA-SC/FC/PC/UF 业务、selector 执行、backend、deploy、production 均保持禁止。

### 请求平台验收

请平台复核 M1 的单一真相源、失败关闭错误 ID、管理入口排除、query 映射、变更范围和自动化证据；平台 Go 后再进入 H1-M2。

## H1-M1 平台验收结论

- 平台于 2026-07-11 对 `e87feecd0dbfd53cd9e5e6e48f80eee650562839` 独立复核为 Go。
- 平台验收及权威集成 HEAD：`7c987ff4a62eff8b383ccf15b4cf4e5700a4c2e6`。
- `SP-H029` 已记录 M1 Go，并正式授权进入 H1-M2。

## H1-M2 精确路由与八态页面壳检查点

- 日期：2026-07-11
- 实施记录：`IR-20260711-CLUB-ALLIANCE-H1-M2`
- 当前结论：模块自验通过，等待平台检查点验收

### 已完成

1. 新增 `/services/club-alliance` 精确模块路由，优先于 `/services/:serviceKey`，不再进入包含俱乐部查询/加入提交的 `CoreServicePage`。
2. `ServicePlazaPage` 与俱乐部联盟首页共同调用 M1 `deriveClubAllianceActions`，服务广场不再维护第二套四入口数组。
3. `ClubAllianceRoute` 只读取版本化 catalog/actions，并从真实目录、query、权限和生命周期派生 `home/focused/loading/empty/error/unauthorized/maintenance/offline` 精确八态。
4. 四入口继承上游 label/target/sort/access/lifecycle/telemetry；`club-manage` 单独作为管理附属入口，不进入四分类。
5. 通过 `ActionControl` 复用权限、生命周期和 activated/blocked 遥测；页面不自行放宽 scope。
6. `category` query 只产生 `selected_action_id` 页面状态，不触发业务 API；非法 query 显示稳定 error ID。
7. 增补 missing/malformed category target 显式负例并稳定返回 `CAH1_ACTION_TARGET_INVALID`。
8. 建立网络 allowlist：仅 `/api/v1/service-plaza/catalog` 与 `/api/v1/service-plaza/actions`；测试对 club search/create/join/review/member/payment/charity/federation 请求失败关闭。
9. 页面提供 320/360 单列、560+ 双列、900+ 有界布局，无固定内容宽度；交互控件具备键盘焦点、aria label/status/alert 和恢复路径。

### 验证证据

- M2 定向测试：ClubAlliance、ServicePlaza 与 App 路由测试通过。
- 前端全量：18 files、117 tests，全通过。
- production build 与 test-server build：通过。
- current checklist：28/28、SHA mismatch 0；考试 `EX-20260711-CLUB-ALLIANCE-H1-M2-1` score 100。
- 总合同、checklist/exam/IR/collaboration、UTF-8、Git diff 与精确路径门禁在提交前复跑。

### 未完成与边界

- M2 只证明实现检查点；测试环境浏览器布局、直达/刷新/后退、真实权限和网络证据仍属于 M3/M4。
- H1-M4 部署和浏览器 UAT 未授权。
- CA-SC/FC/PC/UF 业务、selector 执行、backend、Schema、deploy、production 均保持禁止。

### 请求平台验收

请平台独立复核精确路由、单一 adapter、八态、ActionControl 复用、网络 allowlist/denylist、响应式/可访问性和变更范围；M2 Go 后再进入 H1-M3。

## H1-M2 平台 No-Go 与 R1 根因修复

- 平台对 `1e7d46d335e5dc26ea9c5894b8a940a63fc02f1e` 独立复核后暂判 No-Go：无 query 首页的 catalog 派生未验证四分类 target，原负例只覆盖 query resolve；allowed ActionControl 也缺少模块级 `activated` 遥测断言。
- 根因：`categoryFromTarget()` 只在 `resolveClubAllianceQuery()` 有 category query 时调用，`deriveClubAllianceActions()` 在 home/Service Plaza 渲染前仅验证数量与 scope，导致错误 target 可泄漏为不可用链接。
- R1 修复在派生阶段验证每个分类 target 必须可解析、仅含一个非空 category，并强制不同 action 的 category 一对一；缺失、空白、重复、多值、不可解析和跨 action 重复映射统一稳定失败关闭为 `CAH1_ACTION_TARGET_INVALID`。
- 首页无 query 与 Service Plaza 均新增完整负例矩阵；Service Plaza 错误面保留稳定 error ID，且错误目录不渲染俱乐部链接。
- 新增 allowed 公益入口点击断言，证明复用 `ActionControl` 上报 `activated/none`；既有拒绝路径继续证明 `blocked/authentication_required`。
- 首次 R1 检查单使用了非合同固定 attestation，试卷虽答题 100 但不能授权实现；两份快照已原样保留在各自 `invalidated/` 子目录，未改写为通过。
- R2 current checklist：`28/28`、当前 SHA mismatch `0`；考试 `EX-20260711-CLUB-ALLIANCE-H1-M2-R2-1` score `100`；实施记录 `IR-20260711-CLUB-ALLIANCE-H1-M2-R2`。
- 定向：3 files、43 tests；全量：18 files、136 tests；production 与 test-server build 均通过。
- 当前结论：M2 R2 模块复验通过，等待平台重新独立验收；M3、业务、后端、部署和生产仍未启动。
