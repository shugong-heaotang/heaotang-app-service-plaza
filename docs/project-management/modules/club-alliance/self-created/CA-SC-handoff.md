# CA-SC 首个会员侧闭环 Handoff

- from：平台集成负责人（CA-SC T0 验收执行）
- to：服务广场权威集成基线
- date：2026-07-12
- work item：`AIW-20260712-CLUB-SC-T0-ACCEPTANCE`
- status：Independent Review No-Go / remediation active
- upstream APP / backend：`2c4b295e6fd625a2df24957f7b8becbc28ad1dcf` / `a998812cf44dc449d85b726706d4ae2573179860`
- latest historical checklist：`FC-20260712-CLUB-SC-T0-ACCEPTANCE-R3`（28/28；修复改动后不再 current）
- latest historical exam：`EX-20260712-CLUB-SC-T0-ACCEPTANCE-R3-1`（100）
- latest historical IR：`IR-20260712-CLUB-SC-T0-ACCEPTANCE-R3`

## 完成

- 冻结 list/detail/join/my、`standard+general` 与详情 active guard。
- 建立合同、Schema、稳定错误、固定 seed 合成 fixtures 和 conformance。
- 建立子项目两层依赖、验收矩阵、回执、R2 current 治理证据与 IR。
- conformance 17/17 通过；`intro` 为权威 Club 文本字段，`description` 负例被拒绝。

## T0 前置勘误（2026-07-12）

- 访问合同统一为 `shared_session`；guest 由父首页承接登录，不调用 SC 业务 API。
- 详情边界资源统一 404 `CLUB_NOT_FOUND`；内部详情/加入失败分别为 500 `CLUB_DETAIL_UNAVAILABLE`/`CLUB_JOIN_UNAVAILABLE`。
- category 输入错误统一使用平台权威 `CLUB_FILTER_CATEGORY_INVALID`。
- 固定 seed 生成器与 committed fixture 已重新统一，conformance 升为 17/17。
- 独立后端复核发现共享 `/clubs/:id` 被 SC 收窄的破坏性回归；合同改用专用 `/clubs/self-created/:id` 并要求通用详情保持兼容。
- 独立前端复核发现 `Number(clubId)` 会把科学计数/十六进制/前导零重解释为其他资源；合同增加 canonical route ID 与零请求失败关闭。
- 测试包显式生成 list/applications 固定深链；动态 `:clubId` 由测试环境 SPA fallback 在 T0 真实验证。

## T0 测试环境验收（2026-07-12）

- APP source `2c4b295e6fd625a2df24957f7b8becbc28ad1dcf`，backend source `a998812cf44dc449d85b726706d4ae2573179860`。
- 固定 seed `HEAOTANG-CA-SC-20260712-V1` 创建 10 个混合俱乐部、5 个有效自建样本和 2 个合成账号；列表零串类。
- 真实 HTTP：未登录401、列表5、详情200/非自建404、加入201/重放200/冲突409、并发单 pending、跨用户隔离全部通过。
- 浏览器：列表、详情、加入重放、本人申请、刷新、后退、上下返回、320/360/768/1280、Tab/focus-visible/ARIA 通过；Enter 注入因浏览器控制通道限制保留 Unverified，不作为产品失败。
- 前端全量 22 files / 204 tests、双构建、17/17 conformance、总合同、静态安全通过。
- 后端与前端失败注入回滚均恢复原哈希，测试环境 ready；固定前缀 fixture、关联申请和成员已清理为 0。
- current checklist `FC-20260712-CLUB-SC-T0-ACCEPTANCE-R3` 28/28；exam `EX-20260712-CLUB-SC-T0-ACCEPTANCE-R3-1` 100；IR `IR-20260712-CLUB-SC-T0-ACCEPTANCE-R3`。

## 独立复核 No-Go（2026-07-12）

- 列表响应未使用合同字段白名单安全 DTO，部署版本会序列化 `owner_id` 等禁止字段；已登记独立后端根因修复工作项。
- fixture 必须升级为唯一 run，并在清理时精确删除本轮 `api_idempotency_keys`。
- 数据库恢复演练、刷新后 DOM 和环境 Enter 证据尚未关闭。
- R3 作为历史检查点保留；修复完成后必须生成 R4 current checklist、100 分考试和新 IR。

## 未完成/禁止推断

上述 Blocker/Major、R4 治理、再次独立复核和受控集成均未关闭。创建、审核、成员管理、资金、生产与真实数据仍未授权；既有部署和局部通过证据不代表 T0 Go。

## 请求

先完成安全 DTO、唯一 run/幂等清理、数据库恢复与真实浏览器证据，再由平台独立复跑并关闭 SP-H036。
