# LP-RC-GOV-EVIDENCE-INTEGRITY-R3

## Identity

- pattern_id：`LP-RC-GOV-EVIDENCE-INTEGRITY`
- title：候选基线漂移与治理考试时序失真
- owner：学习广场持续开发负责人
- first_seen / recurrence_count：独立验收首次发现；影响 M0 与 M0-R2 两组历史证据
- affected_checkpoint：M0-R2 独立验收

## Evidence

- symptom：候选合入目标基线后旧 checklist 不再 current；历史考试时间早于 checklist 完成时间。
- exact_stop：独立验收 `No-Go`，禁止合并与激活 M1。
- reproduction：在目标合并树运行 `validate_development_checklists.py --require-current`；比较 checklist `completed_at` 与 exam `generated_at/completed_at`。
- expected / actual：预期治理 SHA 当前且考试在清单完成后生成；实际旧 SHA 漂移，M0/M0-R2 分别存在倒序。
- product_evidence：不影响 v3.0 产品语义本身，但使其工程准入证据不可信。
- tool_or_environment_evidence：目标 integration 已从 `029650f` 前进到 `4432531`，旧候选未包含最新权威历史。

## Causal chain

因为模块候选从旧集成基线长期前进，因此平台治理文件在目标分支发生漂移；因为旧 checklist 仍留在 active 验证目录，因此合并后 current 门禁必然失败。因为 R2 checklist 人工填写的完成时间晚于实际考试时间，因此最终 SHA 正确仍不能证明 ADR 0017 的因果顺序。最早可控原因是：未在独立验收前同步最新权威基线并用真实生成顺序建立最终治理快照。

## Impact

- affected_modules_and_paths：学习广场历史 M0/M0-R2 checklist、exam、IR。
- security_data_release_impact：无真实数据、环境、支付或发布影响。
- blocks：M0-R2 Go、受控集成、M1 激活。
- does_not_block：离线修正、历史证据保留、其他隔离模块。

## Resolution

- rejected_workaround_and_reason：不修改历史时间戳，不关闭 current 门禁，不把开发者自测改称独立验收。
- systemic_fix：先合并最新权威 integration；历史证据原字节移入 invalidated snapshot；生成 R3 checklist，完成后再生成并提交 R3 exam。
- changed_contracts_code_tools：仅学习广场治理证据和 Handoff。
- compatibility_or_migration：旧 M0/M0-R2 仍可追溯，但不再授权当前任务。
- rollback：回退 R3 会恢复 No-Go，不得恢复旧证据为 active。

## Prevention and proof

- prevention_gate：current checklist SHA、真实 `completed_at < generated_at < exam.completed_at`、integration ancestry。
- positive_test：R3 checklist 28/28、hash mismatch 0、exam 100。
- negative_test：active 目录不再包含旧 stale checklist；历史文件仍在 invalidated snapshot。
- regression_set：旧 M0 合同回归继续执行，但旧治理证据不参与准入。
- environment_retest：不涉及环境。
- evidence_paths_and_exact_commits：R3 checklist、R3 exam、M0-R2 Handoff；精确候选在提交后填写。

## Verdict

- 当前：修正实施中。
- unresolved_risk：权威 integration 在最终验收前继续前进时必须再次同步并重建 current 证据。
- next_authorization：R3 独立验收。
