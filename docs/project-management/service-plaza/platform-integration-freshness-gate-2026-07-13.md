# 平台 integration 第二次分叉根因与 freshness gate Handoff

## Identity

- pattern_id: `RI-INTEGRATION-AUTHORITY-DIVERGENCE`
- title: 多个平台工作树从过期基线向同一权威集成分支形成分叉
- owner: 平台集成负责人
- first_seen / recurrence_count: 2026-07-13 / 2
- affected_checkpoint: 权威 integration 推送与 HM-R0 F2 freshness 后续平台收口
- current status: gate implemented / reconciliation pending independent review

## Evidence

- first occurrence: 本地保障商城 `7d638e3` 与远端健康 F1 `034e46b` 从 `cd2bbae` 分叉，见 `platform-integration-divergence-reconciliation-2026-07-13.md`。
- second occurrence: 本地活动激活 `bb9e717` 与远端健康 F2 freshness `6f4f904` 从 `e947d70` 分叉；remote-only=6、local-only=1。
- second local changed paths: `contracts/foundation/agent-collaboration.v1.json`、`docs/project-management/notices/2026-07-13-activity-v3-m0-task-order.md`。
- second remote impact: 健康 F2-0、freshness 合同/Schema/治理与平台 acceptance 证据；唯一文件重叠仍为协作 registry。
- exact stop: 旧本地 integration worktree 不得作为权威，也不得直接 push；真实调和等待本工作项独立复核。

## Causal chain

1. 因为多个平台执行者拥有不同干净工作树，因此文件所有权隔离本身不能证明它们共享同一个最新远端父提交。
2. 因为 registry 没有建模“权威分支推送租约”，因此一个执行者可以从 `e947d70` 提交活动激活，而另一执行者已把健康链推进远端。
3. 因为普通 push 前没有强制 fetch、expected remote HEAD、ancestry 和 ahead/behind 校验，因此分叉只能在后续 fast-forward 失败时被发现。
4. **最早可控原因**：仓库没有唯一共享的、失败关闭的 pre-push freshness gate，也没有要求 lease 保护成为权威推送的可执行证据。

## Impact

- affected_modules_and_paths: 平台 registry、健康 F2 freshness、活动 V3 M0 激活通知。
- security_data_release_impact: 无真实数据、环境、资金、部署或生产影响。
- blocks: 旧本地 integration 的继续使用；`bb9e717` 与远端权威的受控调和；任何未经 freshness gate 的权威推送。
- does_not_block: 已集成健康 freshness 的只读使用；健康模块保持 handoff-ready；活动分支只读保全；其他不写权威 integration 的工作。

## Resolution

- rejected workaround: 禁止强推、reset、单边 registry 覆盖、删除本地活动提交或把普通 non-fast-forward push 失败当作充分门禁。
- systemic fix: `integration-push-policy.v1` + `Test-IntegrationPushFreshness.ps1` + policy validator + 8项本地 Git 回归。
- gate behavior: fetch 后要求 caller expected remote HEAD 精确匹配；候选必须在 `codex/` 分支、worktree clean、remote 为候选祖先、behind=0；执行推送前再次读取远端，并使用精确 `--force-with-lease=<ref>:<expected>`；推送后验证远端等于候选。
- compatibility: gate 允许正常 fast-forward 和包含远端父链的调和 merge；拒绝 behind/diverged/stale/race。
- rollback: gate 文件可随提交回退，但权威推送不得绕过 lease；真实调和提交保留两条父历史。

## Prevention and proof

- policy validation: Draft 2020-12 Schema + stable error IDs + fail-closed semantic validator。
- positive tests: fresh candidate ready；lease-protected push 成功并验证远端。
- negative tests: stale expected、diverged candidate、behind candidate、dirty worktree、non-codex branch 全部拒绝。
- regression: 8/8 unittest 通过；policy、recurring issue、collaboration、checklist、exam、IR、Service Plaza 总合同全部通过；R3 最终树 UTF-8 检查 1264 files 通过；`git diff --check` 与敏感凭据模式扫描通过。
- third recurrence: 立即建立 ADR、更新 CONSTRAINTS，并对全部 integration/deploy/push 消费方执行审计。

## Independent review exact revision closeout

- first review source: `057a5b6f41085fe654480528471d5aa465dd0788`。
- exact revision: 原 R2 checklist/exam 保留原字节；其记录的 `recurring-issues.v1.json` 与 `agent-collaboration.v1.json` SHA 在最终状态更新后已不再 current，不作为最终准入证明。
- final certification: 新建 R3 checklist，最终 26 项逐项重读且 current SHA 匹配；R3 exam attempt 1 score=100；R3 IR 单独引用最终证据。
- unchanged stop line: 最终 R4 独立复核 Go 前仍不执行 `bb9e717` 与权威远端的真实调和或推送。
- second exact revision: R3 认证文件名不匹配工作项的 `r2*` 精确授权，因此该检查点仅保留在 Git 历史，不进入最终树。
- authorized final certification: 以 `...freshness-gate-r2-r4...` 路径新建 R4 checklist/exam/IR；26/26 current SHA、exam100，并保持实现和停止线不变。

## Verdict

- Gate implementation checkpoint: `handoff-ready / awaiting independent platform review`。
- Unresolved: 尚未合并真实本地 activity `bb9e717`；尚未逐项调和 registry；尚未用新 gate 推送调和候选。
- Next authorization: 独立复核 Gate Go 后，只允许保留两条历史的受控调和与 lease 推送；其他模块/业务权限不扩大。
