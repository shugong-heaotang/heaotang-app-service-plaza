# 单一产品主线 S2B 生命导航申请历史构建测试任务书

- work_id：`AIW-20260718-SINGLE-MAINLINE-S2B-LIFE-APPLICATION-HISTORY-BUILD-TEST`
- record_id：`IR-20260718-SINGLE-MAINLINE-S2B-LIFE-APPLICATION-HISTORY-BUILD-TEST-C1`
- actor：`Codex highest owner / thread 019f72ee-3907-7b21-9498-8e918ac53aac`
- independent reviewer：`Project Brain / thread 019f53cf-af43-7311-8e3c-bff5e0e187f2`
- branch/worktree：`codex/single-mainline-s2b-life-r1` / `C:/Users/shugo/Documents/worktrees/heaotang-single-mainline-s2b-life-r1`
- accepted base：`9a4fc29837d80cc3d3856056a5c97fb13b83a3c2`
- G1 expiry：`2026-07-18T15:30:00+08:00`

## 唯一产品主通道

后续 G2 只验证既有链路：`服务广场 → 生命导航 → 登录态 → 提交导航需求 → created/replayed → 我的申请记录 → 错误恢复/重试 → 返回服务广场`。沿用现有 `application-history`，`D-LN-S2-001` 维度选择器仍 Pending 且排除。

## G1 当前授权与范围

G1 只建立真实 S2B 治理身份：registry、任务理解、life-navigation current checklist 31/31、same-record random Exam100、IR、Handoff、治理门禁和一个本地提交。允许路径为 registry、本任务书、comprehension、Handoff、S2B checklist/exam/IR globs 七类。

`app/node_modules/**`、`app/dist/**` 仅为未来 G2 声明，不授予创建权。G1 不运行 npm/network/test/build，不创建 runtime evidence，不改产品/backend/schema/scripts/workflow/旧证据，不 push/merge/integrate/deploy，不触碰测试服、生产、真实数据、OTP 或 payment。

## 门禁与停止

collaboration validator 0 → preflight ready → 全读 26 core + 5 overlay → checklist 31/current → attempt 1 Exam100 → IR/Handoff/UTF-8/diff/path gates → one commit → independent Acceptance。任一失败立即停止，不清理 worktree、不同轮修补或重跑。
