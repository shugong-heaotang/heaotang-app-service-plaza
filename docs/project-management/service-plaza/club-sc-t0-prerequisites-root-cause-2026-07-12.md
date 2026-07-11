# CA-SC T0 前置根因关闭记录

## Identity

- pattern_id：`CA-SC-T0-RC-001`
- title：访问/错误合同漂移与深链打包证据缺口
- owner：平台集成负责人
- first_seen / recurrence_count：2026-07-12 / 1
- affected_checkpoint：`CA-SC-T0`

## Evidence

- symptom：P0/P1 写 guest 可浏览、错误目录使用旧 error id/HTTP；现有 action/backend 要求认证并使用另一组稳定语义。测试包只显式生成父路由静态入口。
- exact_stop：后端与前端可以继续实现，但在合同统一和深链包装回归前不得进入 T0。
- reproduction：对照 `service-plaza-actions.v1.json`、后端 `Auth:true`、`club-category-filter.v1.json`、CA-SC error catalog 和 `Build-ServicePlazaTestPackage.ps1`。
- expected / actual：期望单一访问/错误真相源和可验证深链包；实际存在双口径和缺失的子路由清单。
- product_evidence：现有父入口为 `shared_session`；后端 search/detail 为认证路由。
- tool_or_environment_evidence：测试环境 Nginx 当前对 list/applications/任意 detail 深链均返回 SPA index 200；构建包仍需显式携带固定 list/applications 路由，动态 `:clubId` 由环境 SPA fallback 在 T0 真实刷新验证。

## Causal chain

因为 P0/P1 依据目标文字推断 guest 可浏览而未复核既有 action/backend 权限，所以合同与运行事实分叉；因为错误目录在实现前猜测边界状态，所以内部故障与资源隐藏混用；因为构建脚本只登记父路由，所以固定子路由缺少包内回归。最早可控原因是合同冻结和打包测试未交叉读取既有权威依赖。

## Impact

- affected_modules_and_paths：CA-SC 合同、conformance、测试服前端打包。
- security_data_release_impact：禁止意外开放匿名 club 数据；无生产和真实数据变更。
- blocks：T0 派发与环境 Go。
- does_not_block：已认证的后端/前端本地实现与测试。

## Resolution

- rejected_workaround_and_reason：不通过修改 UAT 预期、前端本地吞错或临时 Nginx 规则绕过。
- systemic_fix：统一 `shared_session`；资源边界统一 404 `CLUB_NOT_FOUND`，内部 detail/join 统一 500；category 使用平台权威 error id；固定子路由进入打包清单和可执行检查。
- changed_contracts_code_tools：CA-SC 合同/错误目录/conformance、构建脚本和打包检查。
- compatibility_or_migration：不开放新权限；保持既有后端安全语义，修正未发布业务合同。
- rollback：回退本工作项提交即可；不触及环境数据。

## Prevention and proof

- prevention_gate：conformance 精确校验 access、error id/HTTP 和完整 fixture replay；包测试校验固定深链 index。
- positive_test：合法合同、固定 seed、list/applications 包入口通过。
- negative_test：anonymous access、旧 error id/409 内部错误、缺路由均失败。
- regression_set：Service Plaza contracts、前端双 build、Test-ServiceIntegrationPackage。
- environment_retest：T0 真实验证 list/applications/合法与非法 `:clubId` 直达和刷新。
- evidence_paths_and_exact_commits：由本工作项 IR 和 SP-H034 在提交后补录。

## Recurrence action

首次发生：登记并在本切片增加交叉依赖与负例门禁；若其他子项目再次出现 access/error/packaging 三者漂移，升级公共影响扫描和共享门禁。

## Verdict

- verdict：Pass（本地合同与固定路由打包前置）；T0 仍未授权。
- unresolved_risk：前后端尚待独立集成；动态详情深链仍需环境 SPA fallback 真实证据。
- next_authorization：本工作项全门禁通过并受控集成后，平台才能派发 CA-SC T0。
