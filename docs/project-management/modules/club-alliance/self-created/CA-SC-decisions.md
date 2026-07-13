# CA-SC 决策记录

## D-CA-SC-001 精确分类

- status：Accepted
- decision maker：项目负责人
- date：2026-07-11
- decision：SC = `type=standard AND category=general`，服务端组合筛选为唯一权威。
- premises：Club 模型能够稳定表达 type/category；服务端分页前完成组合筛选。
- falsification：历史 standard 无法迁移到 general、category 变为多值/层级、或索引与组合筛选不一致。
- review trigger：任一 falsification evidence 出现时。
- compatibility：旧 type-only selector 被取代；迁移必须有混合数据回归。
- forbidden alternatives：type-only、前端本地筛选、新增 SC ClubType。

## D-CA-SC-002 首闭环范围

- status：Accepted
- decision maker：平台集成负责人
- date：2026-07-12
- decision：首闭环只包含会员侧 list/detail/join/my，审核与管理严格后置。
- premises：已有 search/join/my 事实可作为后续实现输入，详情缺口由独立后端切片关闭。
- review trigger：若首闭环不能在不引入管理能力的情况下完成本人状态闭环。
- forbidden alternatives：把审核视为首闭环完成条件、复用旧通用 CoreServicePage、夹带资金或生产。

## 可变政策

免审、审批时限、撤回、冷却期、容量、费用均未冻结；缺失时不得猜测或硬编码。本 P0/P1 合同不执行这些政策。
