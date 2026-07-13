# LP-RC-ARCH-CONTRACT-FALSE-GREEN-R3

## Identity

- pattern_id：`LP-RC-ARCH-CONTRACT-FALSE-GREEN`
- title：关键架构语义变异未被 Schema、验证器和 fixtures 拒绝
- owner：学习广场持续开发负责人
- first_seen / recurrence_count：独立验收首次发现，五类可复现变异
- affected_checkpoint：M0-R2 架构冻结

## Evidence

- symptom：替换外部项目、对调目录 owner、取消双关审计、提前验证端口或修改端口 ID 时，原门禁仍全部通过。
- exact_stop：架构合同无法证明被冻结，独立验收 `No-Go`。
- reproduction：对内存合同逐项变异并分别运行 Draft 2020-12 Schema、`validate_contract` 和 fixtures。
- expected / actual：预期每类非法变异至少产生 Schema、invariant 与 fixture 失败；实际三类失败数均为 0。
- product_evidence：会重新引入项目层级、商城边界、审核治理和跨项目端口漂移。
- tool_or_environment_evidence：工具运行正常，缺陷来自约束覆盖不足。

## Causal chain

因为 Schema 主要限制数组数量而未锁定成员和值，因此语义替换仍合法；因为验证器对目录 owner 和端口 readiness 使用 case 常量而不是合同字段，因此合同漂移不影响判定；因为 fixtures 未逐项引用外部项目和端口 ID，因此关键变异没有可观察失败。最早可控原因是机器契约没有把已冻结的 v3.0 决策编码为精确常量与变异测试。

## Impact

- affected_modules_and_paths：v3 architecture Schema、validator、fixtures、IR 与 conformance。
- security_data_release_impact：无真实环境影响；若带入 M1 会扩大为权限、数据所有权和审核风险。
- blocks：M0-R2 Go 与 M1。
- does_not_block：离线强化和旧 M0 回归。

## Resolution

- rejected_workaround_and_reason：不依赖人工阅读替代机器门禁，不只新增文字说明。
- systemic_fix：Schema 精确冻结全部数组、owner、审核策略、事件、课程顺序和五端口；validator 读取合同字段；fixtures 覆盖四个外部项目和每个端口；内置五类 mutation gate。
- changed_contracts_code_tools：`learning-plaza-architecture.v3.schema.json`、`validate_learning_plaza_m0_r2.py`、`cases.v3.json`。
- compatibility_or_migration：不改变当前合法 v3 实例，只拒绝此前误放行的非法变异。
- rollback：回退会恢复假绿，禁止。

## Prevention and proof

- prevention_gate：有效实例 0 Schema errors、34 条 fixtures、5 类变异均同时触发 Schema/invariant/fixture 拒绝。
- positive_test：当前 v3 合同通过。
- negative_test：外部项目、目录 owner、双关策略、端口 readiness、端口 ID 五类变异。
- regression_set：旧 M0 16 条 fixtures。
- environment_retest：不涉及环境。
- evidence_paths_and_exact_commits：M0-R3 conformance、Handoff；精确候选在提交后填写。

## Verdict

- 当前：修正实施中。
- unresolved_risk：未来新增应用或端口必须同步升级 Schema 与 mutation gate。
- next_authorization：R3 独立验收。
