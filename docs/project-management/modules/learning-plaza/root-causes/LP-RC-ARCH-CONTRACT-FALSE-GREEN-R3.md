# LP-RC-ARCH-CONTRACT-FALSE-GREEN-R3

## Identity

- pattern_id：`LP-RC-ARCH-CONTRACT-FALSE-GREEN`
- title：关键架构语义变异未被 Schema、验证器和 fixtures 拒绝
- owner：学习广场持续开发负责人
- first_seen / recurrence_count：M0-R2 首次发现；M0-R3 独立复验第二次发现同类假绿
- affected_checkpoint：M0-R2、M0-R3 架构冻结

## Evidence

- symptom：替换外部项目、对调目录 owner、取消双关审计、提前验证端口或修改端口 ID 时，原门禁仍全部通过。
- exact_stop：架构合同无法证明被冻结，独立验收 `No-Go`。
- reproduction：对内存合同逐项变异并分别运行 Draft 2020-12 Schema、`validate_contract` 和 fixtures。
- expected / actual：预期每类非法变异至少产生 Schema、invariant 与 fixture 失败；实际三类失败数均为 0。
- product_evidence：会重新引入项目层级、商城边界、审核治理和跨项目端口漂移。
- tool_or_environment_evidence：工具运行正常，缺陷来自约束覆盖不足。

## Causal chain

M0-R2 的最早可控原因是机器契约没有把已冻结的 v3.0 决策编码为精确常量与变异测试。M0-R3 虽补齐精确 Schema、fixtures 和 mutation gate，但 `validate_contract()` 把 Schema 与手写 invariant 错误合并返回；mutation gate 又把这个混合结果当成独立 `invariant_errors`，造成四类变异只有 Schema 和 fixture 拒绝却显示三层通过。第二次最早可控原因是验证层没有类型隔离，计数名称与实际数据来源不一致。

## Impact

- affected_modules_and_paths：v3 architecture Schema、validator、fixtures、IR 与 conformance。
- security_data_release_impact：无真实环境影响；若带入 M1 会扩大为权限、数据所有权和审核风险。
- blocks：M0-R2 Go 与 M1。
- does_not_block：离线强化和旧 M0 回归。

## Resolution

- rejected_workaround_and_reason：不依赖人工阅读替代机器门禁，不只新增文字说明。
- systemic_fix：保留精确 Schema 与 fixtures；新增只返回手写规则的 `validate_invariants()`，`validate_contract()` 仅负责组合 Schema 与 invariant；mutation gate 分别计算两层，并为外部项目精确集合、目录 owner、双关策略、五端口 ID/direction/readiness 建立独立 invariant。
- changed_contracts_code_tools：`learning-plaza-architecture.v3.schema.json`、`validate_learning_plaza_m0_r2.py`、`cases.v3.json`。
- compatibility_or_migration：不改变当前合法 v3 实例，只拒绝此前误放行的非法变异。
- rollback：回退会恢复假绿，禁止。

## Prevention and proof

- prevention_gate：有效实例 0 Schema errors、34 条 fixtures；5 类变异的 Schema、独立 invariant、fixture 计数分别非零，禁止混合计数。
- positive_test：当前 v3 合同通过。
- negative_test：外部项目、目录 owner、双关策略、端口 readiness、端口 ID 五类变异。
- regression_set：旧 M0 16 条 fixtures。
- environment_retest：不涉及环境。
- evidence_paths_and_exact_commits：M0-R3 conformance、Handoff；精确候选在提交后填写。

## Verdict

- 当前：M0-R4 分层修正实施中，等待新独立验收。
- unresolved_risk：未来新增应用或端口必须同步升级 Schema 与 mutation gate。
- next_authorization：R4 独立验收。
