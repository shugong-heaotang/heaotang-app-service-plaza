# 活动板块 V3.0 M0 Handoff

状态：实施候选完成，等待独立验收。

## 已完成

- 固定V3.0基线哈希和模块版本入口。
- 将36条验收标准逐条绑定原文、合同、API、正反fixture与断言。
- 固定俱乐部主办、会员提案、AI人工确认、隐私分层、双方同意、商城复用、单次订单归因和幂等边界。
- 建立结构化依赖schema、领域模型、完整状态转换与guard、API、错误语义、安全矩阵、严格schema、72个确定性fixtures及变异测试。
- current checklist 28/28，治理考试100分。

## 验证入口

`python contracts/modules/activity/v3/validate_activity_v3_contracts.py`

## No-Go 边界

- 未修改任何前后端业务代码。
- 未连接数据库、网络、真实鉴权、真实消息、真实商城、支付或生产环境。
- 六个跨模块接口均为 `provisional`，不能据此宣称M1真实闭环完成。
- M1、测试服部署和生产上线均未授权。

## 独立验收请求

请独立验收负责人复核：基线哈希、36条追踪、schema、fixtures、负面权限、安全边界、依赖readiness、范围差异、UTF-8、checklist及考试。只有 exact candidate commit 验收 Go 后才可申请 M1；不得自动扩权。
