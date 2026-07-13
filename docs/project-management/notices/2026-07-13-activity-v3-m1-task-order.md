# 活动板块 V3.0 M1 最小真实闭环任务单

签发日期：2026-07-13（Asia/Shanghai）
批准角色：项目最高负责人
唯一需求基线：`和奥堂APP活动板块统一需求说明书-V3.0.md`
基线 SHA-256：`838C54AE895D223E66FCA8BE8BB54D588DC3F83234B430B91073B8454E2975E6`

## 授权

M1 已批准，目标是“俱乐部主办/会员提案 + 平台公开活动发现 + 免费自主报名”的最小真实闭环。不得部署、上线、触达真实会员、发送验证码或外部消息、调用商城/订单/支付、修改生产数据或启用 AI 外部动作。

## 产品裁决

1. 已认证且状态有效的俱乐部会员可向所属俱乐部提交提案；非会员、失效或受限会员拒绝。
2. 提案只进入俱乐部待审；提案人不得成为唯一审批人，必须由不同的授权运营者审批。
3. 平台公开发现必须同时满足俱乐部批准、平台公开审核通过、未取消/下架和仍在可发现时间窗。
4. 免费报名使用真实认证 subject、资源归属、服务端 scope、容量/资格、同意版本和幂等键；报名状态仅本人及授权角色可见。
5. AI、关系推荐、消息、商城、订单、支付全部隔离，不进入 M1 验收。

## 工作项

- Frontend：`AIW-20260713-ACTIVITY-V3-M1-FRONTEND`，只允许 `app/src/modules/activity/**` 和本工作项专属治理证据。
- Backend：`AIW-20260713-ACTIVITY-V3-M1-BACKEND`，只允许 canonical backend 的 `backend-go/plugins/activity-plugin/**`，强依赖回执 Go 前保持 planned。
- Shared route：`AIW-20260713-ACTIVITY-V3-M1-SHARED-ROUTE`，只允许 `app/src/App.tsx` 与 `app/src/App.test.tsx`，等待 frontend Handoff 后激活。

## Frontend does_not_block

允许在真实依赖签字期间完成严格 DTO/adapter、mock-only/non-production fixtures、公开列表/详情、本人提案状态、审批状态、免费报名状态组件和正负自动测试。Mock 不得冒充真实闭环。

## Go 条件

- M0 已受控集成并在 registry 中为 integrated。
- 三工作项 branch/worktree/base/allowed paths/角色分离可追溯。
- Club Alliance、Auth/Privacy 签署 go；其余四个 owner 签署 go 或 isolated-not-called。
- 提案人与审批人分离、平台公开审核、隐私 DTO、容量、资格、同意版本、幂等和无支付/消息副作用的正负测试通过。
- 前后端、合同、安全、UTF-8、范围、Handoff 和独立验收完整。
