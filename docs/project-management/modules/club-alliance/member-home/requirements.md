# H2-M0 会员首页需求与数据责任

## 用户目标

普通会员进入联盟首页后，应先看见自己的俱乐部、待办和活动，再探索公益、自建、家庭与友联体入口。管理中心为附属能力，不干扰普通会员。

## 数据责任

| 区域 | 权威来源 | 当前 readiness | M0 结论 |
| --- | --- | --- | --- |
| 会员摘要 | 新聚合能力 | gap | M2 前必须独立派发，禁止前端拼接猜测 |
| 我的俱乐部 | `GET /api/v1/clubs/my` | code-present-unverified | M2 前做 DTO、本人归属、状态与测试服验证 |
| 今日待办 | 新聚合能力 | gap | 只聚合本人可见事项；需要稳定 source kind 和 target |
| 最近活动 | 新本人活动聚合 | gap | 现有按俱乐部活动接口不能直接证明本人报名视图 |
| 联盟动态 | 新受控 feed | gap | 非关键；无权威来源时隐藏或空态，不伪造推荐 |
| 探索更多 | `service-plaza.action.v1` | verified | 继续复用 H1 action adapter 与上游排序 |

## 隐私与授权

- 会员摘要、我的俱乐部、待办、活动均为 self-only；身份只来自共享会话。
- 首页 DTO 禁止手机号、证件、健康明细、家庭隐私记录、收款账号和原始 Token。
- `club:manage` 只控制附属管理入口；前端隐藏不能替代服务端授权。
- 局部错误不得用空数组伪装成功；运行时不得回退到 mock。

## 状态

页面八态为 loading/ready/empty/partial-error/error/unauthorized/maintenance/offline。会员关系至少覆盖 active/pending/rejected/left/suspended/dissolved。关键“我的俱乐部”失败进入页面错误；待办或活动失败保留其他已证实区域并显示局部错误；推荐失败可隐藏。

## 排序

页面区域按合同固定；俱乐部列表由服务端权威排序；待办按优先级后截止时间；活动按开始时间；动态按发布时间；探索入口继承上游 sort_order。

## 非目标

本检查点不实现页面、聚合 API、数据库、创建/审核/成员管理、资金、部署、生产或真实用户数据。
