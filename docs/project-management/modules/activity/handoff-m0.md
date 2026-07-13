# 活动板块 V3.0 M0 Handoff

状态：实施候选完成，等待独立验收。

## 已完成

- 固定V3.0基线哈希和模块版本入口。
- 将36条验收标准逐条绑定原文、合同、API、正反fixture与断言。
- 固定俱乐部主办、会员提案、AI人工确认、隐私分层、双方同意、商城复用、单次订单归因和幂等边界。
- 建立可实例验证的依赖schema、领域模型、完整状态转换与guard、语义API、错误语义、安全矩阵、严格schema、72个oracle执行fixtures及输入变异测试。
- 建立“活动→俱乐部→商城”3段合成事件链，执行1个零资金允许场景和2个拒绝场景；事件字段显式禁止金额、币种、价格、订单、支付、退款和结算。
- current checklist 28/28，治理考试100分。

## 验证入口

`python contracts/modules/activity/v3/validate_activity_v3_contracts.py`

当前通过摘要：17个JSON、72个验收场景、3个跨域事件场景、6组依赖schema及语义/变异门禁全部通过。

## No-Go 边界

- 未修改任何前后端业务代码。
- 未连接数据库、网络、真实鉴权、真实消息、真实商城、支付或生产环境。
- 六个跨模块接口均为 `provisional`，不能据此宣称M1真实闭环完成。
- 跨域事件仅为合成、mock-only、non-production 合同证据，不创建购物车、订单、支付、退款或结算。
- M1、测试服部署和生产上线均未授权。

## 登记偏差与解除条件

- `blocks`: M0 独立验收与集成。
- `owner`: 平台集成负责人。
- `symptom`: 权威 registry 登记的 `base_commit=485601ce10ad4d3ac7d9db655465754ad5ac0032` 不存在于当前仓库对象库。
- `verified activation base`: `5d6d22b51b65abf87a5f7c9b9bdd419ce04dfd40`；平台激活提交为 `750eaf7e25951c2478a25523b28eb3f39e45c0b4`。
- `clearance`: 平台集成负责人修正 registry，或以审计记录明确裁决验收基线后，由独立验收负责人对精确候选提交给出 Go/No-Go。
- `does_not_block`: 当前 M0 授权路径内的合同验证、合成fixture和证据修复；不授权 M1、部署、真实触达或交易。

## 独立验收请求

请独立验收负责人复核：基线哈希、36条追踪、schema、fixtures、负面权限、安全边界、依赖readiness、范围差异、UTF-8、checklist及考试。只有 exact candidate commit 验收 Go 后才可申请 M1；不得自动扩权。
