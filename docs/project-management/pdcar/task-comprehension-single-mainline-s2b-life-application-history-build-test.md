# 单一产品主线 S2B 任务理解回执

- work_id：`AIW-20260718-SINGLE-MAINLINE-S2B-LIFE-APPLICATION-HISTORY-BUILD-TEST`
- record_id：`IR-20260718-SINGLE-MAINLINE-S2B-LIFE-APPLICATION-HISTORY-BUILD-TEST-C1`
- received_at：`2026-07-18T13:24:30+08:00`
- actor：`Codex highest owner / thread 019f72ee-3907-7b21-9498-8e918ac53aac`

## 目标

不再摊大饼，只围绕服务广场到生命导航申请历史闭环这一条主通道推进。当前 G1 只完成这条通道的治理准入，不执行产品构建测试。

## 边界

- S2A 以实际 predecessor branch/worktree 记录 integrated；S2B 使用新的全局唯一 successor branch/worktree。
- 旧失败 worktree 原样冻结，不清理、不 reset、不提供当前 authority。
- G1 只写七类治理路径；future node_modules/dist 不可创建。
- 必须重新完成 life-navigation 31 项 current checklist 和同 record Exam100，不复用 S2A 26 项认证。
- D-LN-S2-001 保持 Pending；不运行 npm/test/build，不改产品，不 push、不集成、不部署。

## 顺序与防线

registry transition → collaboration validator → preflight → 全量阅读/checklist → random Exam100 → IR/Handoff → 全门禁 → one local commit → independent Acceptance。单一主线、共享路径唯一 writer；任何失败立即停并发新 revision，不跨阶段修产品。
