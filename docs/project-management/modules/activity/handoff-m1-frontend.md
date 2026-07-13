# 活动板块 V3.0 M1 前端 Handoff

- work item：`AIW-20260713-ACTIVITY-V3-M1-FRONTEND`
- record：`IR-20260713-ACTIVITY-V3-M1-FRONTEND`
- branch：`codex/activity-v3-m1-frontend`
- base：`7177419a65634017844ee3a2ddf88b6ea17e7948`
- status：`Frontend candidate ready for independent acceptance`
- verdict：`Frontend Candidate Go / M1 Full No-Go`

## 本检查点交付

在 `app/src/modules/activity/**` 内新增活动 M1 的独立、未挂载前端模块：

- 严格 DTO 适配器，只接受 `mock-only`、非生产资料；未知字段失败关闭。
- 公开活动必须同时满足俱乐部批准、平台审核、报名开放和可发现时间窗。
- M1 只接受免费活动；任何非零金额或支付扩展字段均被拒绝。
- 详情目标必须是 `/services/activity/<id>` 内部路由；时间必须可解析。
- 报名状态与剩余名额必须一致；只有显式注入 `onRegister` 且状态为 available 时才呈现用户确认按钮。
- 本人提案显示俱乐部审核状态，并强制 `proposer_can_approve=false`。
- 页面明确展示非生产合成资料和 M1 隔离边界，不调用 AI、关系推荐、消息、商城、订单或支付。
- 提供 loading、ready、empty、unauthorized、error 和 available/registered/full/ineligible 状态。
- 提供 479px 与 720px 响应式规则和 `:focus-visible` 键盘焦点。

## 验证

- governance checklist：completed。
- governance exam：100/100，attempt 1。
- `npm test -- activityAdapter.test.ts ActivityM1.test.tsx`：2 files、25/25 passed。
- `npm test`：25 files、256/256 passed。
- `npm run build`：通过，68 modules transformed。
- `python contracts/modules/activity/v3/validate_activity_v3_contracts.py`：15 JSON files、72 oracle cases、6 dependency schemas passed。
- 前端依赖：锁文件哈希一致，使用 `C:/Users/shugo/Documents/APP系统/app/node_modules` 的本地 junction；该 junction 不进入 Git。

## 边界与未完成

- 没有修改 `app/src/App.tsx`，因此没有共享路由挂载。
- 没有后端、API、数据库、网络、真实鉴权、真实会员或环境操作。
- 没有发送验证码、消息，没有 AI 外部动作、商城、订单、支付或生产变更。
- Club Alliance 与 Auth/Privacy 的真实依赖签署仍是后端和真实闭环前置。
- Mock-only 组件和测试不得冒充 M1 真实闭环或部署 Go。

## 下一门禁

由独立验收负责人复跑活动专属测试、全量前端测试、构建、M0 合同、治理、UTF-8、范围和敏感扫描。独立验收 Go 后，平台才能激活 `AIW-20260713-ACTIVITY-V3-M1-SHARED-ROUTE`；后端仍需满足任务单列出的依赖签署条件后单独激活。
