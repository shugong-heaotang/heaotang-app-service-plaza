# NOVA M2 Provider 三包派发报告

日期：2026-07-12

平台工作项：`AIW-20260712-NOVA-M2-PROVIDER-DISPATCH`

起始 APP 基线：`5004cdc45e21604817f809d3b9babe783f0ac40b`

起始 backend 基线：激活时读取 authoritative backend integration，当前候选 `e41265905815082433e040412f3dd6b6b33dfede`

## Outcome

正式拆分三个主业务包：Network Read Provider、Social Write Provider、Migration & Disable Drill。三者无代码路径重叠；P1/P2 使用新 Go 文件且不改 legacy route/service，P3 只做 APP 侧临时数据库演练与兼容合同。

为满足跨 Git 根治理，P1/P2 各配一个 APP companion evidence item。companion 不改变“三个主业务包”的职责划分，也不拥有业务代码。

## 当前门禁

- canonical Owner：integrated。
- tools/callback contract：integrated，全部 executable=false。
- P1/P2/P3：待 activation 后从 P0/C0 开始。
- NOVA M2：No-Go，直到三包独立 Go + 组合测试环境安全验收。

## 平台治理证据

- checklist：`IR-20260712-NOVA-M2-PROVIDER-DISPATCH-R1`，26/26 completed。
- exam：`EX-20260712-NOVA-M2-PROVIDER-DISPATCH-R1-1`，100 分 passed。
- 任何真实会员数据、真实消息或生产迁移均不在授权内。
