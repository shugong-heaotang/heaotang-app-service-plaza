# CA-SC F0 前端检查点 Handoff

- from：俱乐部联盟自建俱乐部前端负责人
- to：服务广场平台集成负责人
- date：2026-07-12
- work item：`AIW-20260712-CLUB-SC-FIRST-CLOSURE-FRONTEND`
- branch：`codex/club-sc-first-closure-frontend`
- base：`6149504959ea779102022d6b6e172fe0999dcaec`
- activation HEAD：`73b21bb15fcefa5aad4140619e9661216aca54c7`
- implementation commit：`4ae2b8f17ffab4bc131a3f67f13873eb02d080f9`
- status：handoff-ready / local F0 Go candidate / T0 No-Go

## 治理证据

- checklist：`FC-20260712-CLUB-SC-FRONTEND`，28/28 completed
- exam：`EX-20260712-CLUB-SC-FRONTEND-1`，score=100
- IR：`IR-20260712-CLUB-SC-FRONTEND`
- dependency bootstrap：`app/node_modules` 使用与本工作树 `package-lock.json` 哈希兼容的共享 junction；未安装、复制或升级依赖，未修改 lock
- preflight：ready

## 完成

- H1 自建 focused CTA 与独立 SC 路由。
- 登录前零业务请求；登录后服务端权威 `standard+general` 搜索。
- 列表、详情、加入、本人申请状态与稳定失败反馈。
- `intro` 投影、敏感字段排除、Idempotency-Key、重复点击防护和 replay 状态。
- loading/empty/error/auth/submitting/success、分页、返回路径、移动端、键盘和 aria 自动化。
- 定向、全量、双构建、合同、conformance、治理门禁通过。

## 未完成/阻塞

- `F0-CORR-001`：guest access 文档合同必须改为 shared-session。
- `F0-CORR-002`：category 错误目录必须采用权威 `CLUB_FILTER_CATEGORY_INVALID`。
- `F0-CORR-003`：详情/加入内部不可用的 HTTP 500 与 error catalog 404/409 必须统一。
- 后端检查点尚由独立负责人完成；测试环境 T0 尚未授权/执行。
- 未执行生产、真实数据、创建、审核、成员、资金或其他三类业务。

## 平台验收请求

1. 独立复跑 current checklist/exam、定向/全量测试、双构建、总合同、UTF-8、scope 和敏感扫描。
2. 核对新模块只使用四个 SC 接口，guest 时业务请求为零，`/api/v1/clubs` 全量接口不可达。
3. 对 `F0-CORR-001/002` 建立最小受控合同修正并集成；修正前不得进入 T0。
4. 前端 F0 Go 后，与独立后端检查点在测试环境按 SP-H034 执行 T0。
