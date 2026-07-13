# CA-F0/H0 正式任务通知书

通知编号：`CA-F0-TASK-20260711-001`  
状态：正式下达  
下达人：服务广场平台集成负责人  
承接人：俱乐部联盟负责人  
授权阶段：`CA-F0-M0 + CA-H0`；`CA-H1` 及四类业务严格后置。

## Supersedes

本通知取代旧 `CA-TASK-20260711-001`、旧 `standard-club-join-review` 项目入口、依赖图、回执与 M0-M4 Handoff 作为俱乐部联盟父项目入口。旧证据保留但不得推导本项目 Go。

## 固定边界

根路由 `/services/club-alliance`，返回 `/services`。四入口由上游 `service-plaza-actions.v1` 中 `region=club_alliance`、`service_id=club-alliance`、`action_type=service_variant` 且属于精确 accepted action set 的记录派生，并显式排除 `club-manage`；顺序继承 50/60/70/80：公益、自建、家庭、友联体。`club-manage` 单独解析为附属操作，保持 preview + `club:manage`。

无 query 表示 home。既有中文 `category` query 只兼容解析为唯一 `selected_action_id` 和焦点状态，不调用业务 API；未知、空白或多义参数进入稳定 fail-closed 状态。直达、刷新、浏览器后退和返回 `/services` 必须可重复；CA-H1 前禁止修改上游 target。

首页只负责入口、排序、生命周期、权限、导航、统一状态、响应式和遥测；禁止创建、加入、审核、成员、关系或支付业务 API。CA-H0 不修改前端；CA-H1 必须在平台 H0 Go 后另行授权。

已接受：公益=`standard+charity`；友联体=`relationship_kind=club-federation`。`D-CA-003 standard+general` 保持 Pending：允许 proposed metadata 和 H0 base conformance，不允许 executable selector 或分类业务编码；完整 H0 Go 前必须关闭。

## 本轮交付

1. 顶层需求、四类能力矩阵、递归 P0-P7/G0-G6 计划和可证伪决策记录。
2. `category-registry`、`capability-catalog`、`homepage`、`relationship` 的 JSON、Schema、fixtures 和批准 Python conformance。
3. 在 `docs/project-management/modules/club-alliance/CA-H0-acceptance-matrix.md` 完整落盘 H0-C01 至 C12、H0-B001 至 B033、expected 和 error_id；该文件完成前编号不得被当作权威验收证据。
4. 稳定、版本化 error catalog。
4. 新 CA-F0/H0 internal dependencies、receipt、实现记录和 Handoff。

能力状态使用 `planned | code-present-unverified | standardized | implemented | test-verified | release-go | operations-go | forbidden`。商业、支付、提现、退款和订阅首期只能 forbidden。

## 允许路径与禁止项

模块工作项只允许 `agent-collaboration.v1` 中逐文件列出的 README、requirements、decisions、acceptance、依赖、receipt、checklist/exam/IR/Handoff、四组 JSON+Schema 及 conformance error catalog/validator/fixtures/report。不得修改 CA-H1/frontend/backend/deploy 路径，也不得修改平台合同、上游动作或脚本。

决策记录必须包含 decision maker、date、status、premises、falsification evidence、review trigger/date、compatibility/migration 和 forbidden alternatives；PC、UF、homepage/single-source/order 分别记录，D-CA-003 单列 Pending。

完成 CA-F0/H0 合同证据后提交平台验收；平台 H0 Go 前不得进入 CA-H1。生产、真实资金和不可逆操作不在授权范围。
