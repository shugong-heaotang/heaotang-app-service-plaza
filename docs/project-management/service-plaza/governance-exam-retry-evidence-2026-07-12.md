# 治理考试重试证据根因修复（2026-07-12）

## Identity

- pattern_id：`GOV-EXAM-RETRY-EVIDENCE-NOT-PERSISTED`
- title：治理考试重试无法证明前序失败试卷与补课重读
- owner：平台集成负责人 / Platform governance tooling agent
- first_seen / recurrence_count：2026-07-12 / 1
- affected_checkpoint：Project Brain M1-R3

## Evidence

- symptom：attempt 2 只记录递增编号，未持久化 `previous_attempt_path`、上一试卷 SHA-256 或补课来源重读证据；IR 的 `PreviousAttemptPath generation` 声明无法从提交复现。
- exact_stop：Project Brain source `b33068018a7db7097225952ce0f7ec480e2bc251` 保持 No-Go，不改写旧 R2/R3 考试。
- reproduction：审查 `New-AgentGovernanceExam.ps1` 可见 `PreviousAttemptPath` 仅用于即时校验后即丢弃；validator 只按同目录和 attempt_number 推断前一场失败，手工构造的 retry 无显式证据链也可通过。
- expected / actual：重考必须证明紧邻失败试卷、不可变哈希及其全部 remediation sources 在重考前已按当前 SHA 重读；实际只能证明目录里碰巧存在编号较小的失败记录。
- product_evidence：不影响业务产品运行时。
- tool_or_environment_evidence：共享 L0 治理认证证据缺口，直接阻塞依赖重考链的 Project Brain M1-R3。

## Causal chain

1. 因为生成器把 `PreviousAttemptPath` 当作临时参数而不是试卷合同字段，所以提交后无法定位重考引用的失败快照。
2. 因为试卷没有保存前序 SHA，所以无法证明前序失败快照没有被替换。
3. 因为补课只由提示文字要求而无路径、时间、当前 SHA，所以无法证明 remediation sources 真正重读。
4. 因为 Schema 和 validator 没有上述字段与条件约束，所以手工构造 retry 仍可通过。最早可控根因是 retry evidence 未进入版本化考试合同。
5. 首轮修复 `a8106033` 虽补齐路径、SHA 和时间，却由生成器静默读取文件并自行生成“已重读”证据；Agent 没有看到完整内容，也没有逐来源明确确认。独立复核据此 No-Go。R2 改为完整输出每份补课源，并要求显式提供与失败试卷完全一致、无遗漏/无重复的来源路径确认，才生成带确认人和确认方式的重读证据。

## Impact

- affected_modules_and_paths：所有未来 `attempt_number > 1` 治理考试；当前直接影响 Project Brain M1-R3。
- security_data_release_impact：不接触生产、真实数据或资金；影响治理证据可信度。
- blocks：Project Brain M1-R4 之前的平台治理基础设施 Go。
- does_not_block：无重考链的既有 attempt 1 快照、其他非重叠业务和文档工作。

## Resolution

- rejected_workaround_and_reason：不允许在 Project Brain IR 中补一句说明，也不允许修改旧 R3 试卷；聊天或文件名推断不能替代机器证据。
- systemic_fix：为 retry 增加前序路径、前序 SHA 与逐来源重读证据；生成器完整展示每份来源并要求精确来源路径确认后记录确认人、确认方式、时间和当前 SHA；Schema 对 attempt>1 条件强制；validator 校验同 record、连续编号、上一场 failed、精确哈希、来源集合、确认人/方式、当前 SHA 和时间窗口。
- changed_contracts_code_tools：`governance-exam.v1.schema.json`、`New-AgentGovernanceExam.ps1`、`validate_governance_exams.py` 及回归测试。
- compatibility_or_migration：attempt 1 和全部既有已集成快照保持有效；权威基线中没有 attempt_number>1，旧 Project Brain R3 保留为未集成历史，修复后从新基线生成 R4。
- rollback：回退本切片提交即可恢复旧工具；不得回写或迁移历史试卷。

## Prevention and proof

- prevention_gate：attempt>1 缺任一字段即 Schema/validator 失败；引用越界、非紧邻失败、错误 SHA、缺/多/重复补课确认、确认人不符、确认方式不符、来源 SHA 漂移和时间越界均失败。
- positive_test：failed attempt 1 → 全文展示并逐来源明确确认 → passed attempt 2，提交后字段完整保留。
- negative_test：missing/wrong previous path/hash、nonconsecutive、path escape、missing/duplicate/stale reread 与时间边界。
- regression_set：legacy attempt 1、全仓治理试卷、检查单、IR、总合同与 UTF-8。
- environment_retest：不适用；纯仓库治理工具。
- evidence_paths_and_exact_commits：本报告、R1 checklist/exam/IR、脚本测试和后续受控集成提交。

## Verdict

- 当前：R1 source `a8106033` 因静默自动重读证据被独立复核 No-Go；R2 source `f61f0eed` 因新 JSON 末尾空行被 diff 门禁拒绝；R3 source `406b5f30` 因确认参数可在全文展示前预传而被独立复核 No-Go。三者 Git 历史保留，最终树由 R4 的“全文展示→路径+nonce交互确认→记录时间/SHA”强制顺序证据取代。
- unresolved_risk：Project Brain 需在新权威基线生成 M1-R4；首试100不人为制造 retry。
- next_authorization：平台集成后通知 Project Brain 重新生成当前治理证据。
