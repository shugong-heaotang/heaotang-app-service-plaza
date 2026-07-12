# CA-SC 首个会员侧闭环 Handoff

- from：平台集成负责人（CA-SC T0 验收执行）
- to：服务广场权威集成基线
- date：2026-07-12
- work item：`AIW-20260712-CLUB-SC-T0-REMEDIATION`
- status：R4 remediation complete / controlled integration pending
- upstream APP / backend：`2c4b295e6fd625a2df24957f7b8becbc28ad1dcf` / `98426ff83a1218080019faa377c152a81ecca437`
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

## R4 根因关闭（2026-07-12）

- 后端安全 DTO 实现提交 `df0575a05c8f75d927d079dc8c662e2cd25b9e55` 已经独立复核，并受控集成为 backend `98426ff83a1218080019faa377c152a81ecca437`；定向、全量 Go tests 与 `go vet` 通过。
- 测试环境部署 binary SHA-256 `fec7bcbb58d6186d9c384b1b837479f592d978c145ce09c46e002763d9c565f1`；部署前远端备份 `/root/heaotang-backups/20260712-095800.tar.gz`，本地备份 SHA-256 `2b24a9d07588eace04ae4bbfa448e6a9ace23da0ddd064c0f90945acf8306f1f`；ready/db 均通过。
- 唯一 run `club-sc-t0-20260712-100100` 完成 10 条混合数据验收。search total=5 且零串类；列表/详情字段白名单通过、禁止字段 0；加入首次/重放/冲突、并发单 pending、跨用户隔离通过。
- cleanup 后 run-owned clubs、applications、members、`api_idempotency_keys` 均为 0；SQLite 在线备份已恢复到隔离临时库，完整性 ok、schema 400、dump SHA 匹配、在线库未变。
- 真实刷新 DOM 同时证明 URL、heading、认证状态和主导航。Enter 经现有 in-app 与 Windows 原生控制通道仍不能可靠传递，依规则停止扩大尝试并保留为 control-channel Unverified；这不是环境 Enter Pass，也不是产品 No-Go。
- 治理时序偏差已透明记录：数据库恢复证据曾在 remediation R1 检查单/考试前写入；发现后立即停止后续实现，完成 preflight、R1 逐项阅读和 100 分考试后才继续。未在考试前修改业务代码，不删除历史快照。

## 未完成/禁止推断

原四项 Blocker/Major 已关闭；最终 current checklist、100 分考试、IR、再次独立复核与受控集成仍是最后门禁。创建、审核、成员管理、资金、生产与真实数据仍未授权。

## 请求

请平台独立复跑最终门禁并受控集成；集成完成后关闭 SP-H036 和三个 remediation/safe-DTO 工作项。
