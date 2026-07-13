# NOVA M2 人脉工具前置派发报告

日期：2026-07-12

平台工作项：`AIW-20260712-NOVA-M2-PEOPLE-TOOLS-DISPATCH`

起始基线：`15ce1053e1a9173e5a000655167f7d69acac5bcd`

## Outcome

M2 维持 No-Go。平台将前置拆成两个互不重叠的独立工作项：人脉 Owner canonical 决策，以及 NOVA 四工具/callback 契约会签。两项均不授权业务实现或真实数据操作。

## 只读事实

- network 写侧允许正文伪造 from_user_id，状态更新缺资源归属；不得作为 NOVA canonical。
- social 写侧使用服务端身份、接收方绑定状态迁移，暂定为更安全的 canonical persistence 候选，但仍需加固。
- network 和 social 同时建 `introduction_requests`，另有 `introductions`，必须由唯一人脉 Owner 消除双事实源。
- 未集成的 `codex/nova-api-contract-signoff@0dd415d` 只覆盖通用 chat/task/confirm/cancel/retry，不证明 M2 四工具，本任务不复用其未授权结论。

## 两项独立证据

1. Owner evidence：registry 中唯一 owner、branch/worktree/base/allowed paths；canonical decision、迁移/禁用计划、内部依赖、receipt/Handoff、current checklist/exam100/IR。
2. Contract evidence：四工具 + callback 的 JSON/Schema/errors/fixtures/Python tests、会签结论、current checklist/exam100/IR。

## 后续实现拆分

本轮不创建后端实现工作项。后续如获 Go：network search 读侧、social connection 写侧、共享 DB migration 必须拆成三个不同 owner/allowed paths；不得一个 item 同时覆盖 network/social/db/cmd/server。

## 当前治理证据

- platform checklist：`IR-20260712-NOVA-M2-PEOPLE-TOOLS-DISPATCH-R1`，26/26 completed。
- platform exam：`EX-20260712-NOVA-M2-PEOPLE-TOOLS-DISPATCH-R1-1`，100 分 passed。
- collaboration validator：待派发文件落盘后复跑。
- M2 verdict：No-Go，直到两项独立证据均 Go。
