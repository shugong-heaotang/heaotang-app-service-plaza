# 治理考试与实施记录跨记录一致性门禁 R1 Handoff

状态：implementation complete; independent review pending

## 结论

实施记录引用的治理考试现已失败关闭：引用必须存在，且必须为相同 `record_id`、`status=passed`、`score=100`。服务广场总门禁会递归发现所有 `contracts/modules/*/implementation-records`；foundation 记录仍执行完整 Schema，模块记录执行共同的 checklist/exam 跨记录证据约束。

## 已完成

- current checklist 26/26，全部哈希匹配；随机治理考试 attempt 1 为 100 分。
- 增加 passed/100 正向、failed/75、record mismatch、missing exam 四项永久回归。
- Service Plaza 总门禁启用模块治理考试与实施记录递归检查；模块考试先按题库重算成绩和状态，再由 IR 门禁核对引用必须同记录 passed/100；当前候选仓库总门禁通过。
- 对 `C:\Users\shugo\Documents\worktrees\heaotang-protection-mall-m2-catalog-evidence` 的九文件脏快照只读执行：门禁以实际 `status=failed, score=75` 失败；前后 dirty count=9、状态完全一致、九文件哈希变化数=0。
- 全量 Python 治理回归执行 79 项：本候选 78 通过、1 项既有 inventory 测试失败；在临时 detached worktree 对 exact base `2535a6bf` 复跑同一测试，也以相同 27 条历史 foundation checklist/registry 对账发现失败。本候选自己的 checklist 通过 `platform_scope_errors=[]`，因此该失败不是本候选引入，也不在本工作项授权范围内；Service Plaza 正式总门禁保持通过。

## 根因闭环记录

### Identity

- pattern_id: `RI-EXAM-IR-CROSS-RECORD-CLAIM`
- title: 失败治理考试可被实施记录的 verified/exam100 声明掩盖
- owner: Platform governance validator repair agent
- first_seen / recurrence_count: 2026-07-13 / 1
- affected_checkpoint: 保障商城 M2 治理证据验收与 Service Plaza 总门禁

### Evidence

- symptom: 商城 R2 IR 为 `status=verified` 并声称 exam100，但其引用考试为同记录 `status=failed, score=75`。
- exact_stop: 旧总门禁只扫描 foundation 实施记录目录，未发现模块 IR；旧 IR 验证器也未被应用到商城模块记录。
- reproduction: 用候选验证器对商城 worktree 执行 `--include-module-records`，精确返回 failed/75 错误和非零退出码。
- expected / actual: expected 为矛盾证据失败关闭；actual 为旧门禁未扫描模块路径。
- product_evidence: 不涉及业务运行或资金；影响治理验收真实性。
- tool_or_environment_evidence: 商城九文件状态及 SHA-256 在只读复现前后完全不变。

### Causal chain

因为总门禁把实施记录路径固定为 foundation 单目录，因此模块 IR 没有进入跨记录检查；因为模块 IR 没有进入检查，因此其文字声明可以与被引用考试事实矛盾；因此失败试卷可能被错误呈现为 verified。最早可控原因是总门禁缺少模块实施记录发现及公共考试链接约束。

### Impact

- affected_modules_and_paths: 所有 `contracts/modules/*/implementation-records/*.json`；已确认实例为 protection-mall M2 R2。
- security_data_release_impact: 无生产、真实数据、支付或部署影响；有错误放行治理证据的发布风险。
- blocks: 保障商城治理证据 acceptance。
- does_not_block: 商城后端精确候选保存、其他隔离业务实现、NOVA 离线回归。

### Resolution

- rejected_workaround_and_reason: 禁止改写失败试卷、删除商城脏文件或只在 Handoff 修正文案；这些做法不能阻止复发。
- systemic_fix: 总门禁递归发现模块 exam 与 IR；考试验证器重算成绩，IR 验证器按引用读取考试事实并要求 same-record passed/100。
- changed_contracts_code_tools: `validate_governance_exams.py`、`validate_implementation_records.py`、`Test-ServicePlazaContracts.ps1`、永久回归测试。
- compatibility_or_migration: foundation IR 保持完整 Schema；模块历史非 canonical 字段不被本修复重写，只增加共同跨记录约束。
- rollback: 回退候选提交即可恢复旧行为；不得删除失败考试或商城现场证据。

### Prevention and proof

- prevention_gate: Service Plaza 总合同门禁的 `--include-module-records`。
- positive_test: same record passed/100。
- negative_test: failed/75、record mismatch、missing exam。
- regression_set: implementation-record 与 governance-exam 定向测试、全量治理测试、Service Plaza 总合同。
- environment_retest: 商城九文件快照只读失败且零文件变化。
- evidence_paths_and_exact_commits: 本 Handoff、implementation record、候选提交（提交后补 exact SHA）。

### Recurrence action

- first: 已建立系统性公共门禁和永久回归；若再次发生，升级 recurring issue 登记与全模块影响审计。

### Verdict

- Conditional Pass：实施与本地证据完成，等待独立测试负责人复跑和裁定。
- unresolved_risk: 尚未独立验收、受控集成。
- next_authorization: 独立 reviewer 只读复验 exact candidate；Go 后交平台集成负责人。

## 变更边界

未修改 registry、NOVA、商城九文件、业务代码、部署、生产、真实用户、支付或资金。实施负责人不执行受控集成。
