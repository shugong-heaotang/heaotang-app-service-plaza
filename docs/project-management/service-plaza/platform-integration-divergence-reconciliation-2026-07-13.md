# 平台集成分叉根因与调和报告

## Identity

- pattern_id: `PLATFORM-INTEGRATION-AUTHORITY-DIVERGENCE-001`
- title: 本地商城集成链与远端健康权威链分叉
- owner: 平台集成负责人
- first_seen / recurrence_count: 2026-07-13 / 1
- affected_checkpoint: HM-R0 F2 激活前置

## Evidence

- symptom: `C:/Users/shugo/Documents/worktrees/heaotang-app-integration` 位于 `7d638e3c7b4ec1b916662c3323bd2549c0e1820f`，远端权威位于 `034e46beae3dd30d5616c873d596e9c591c8d797`，两者互不为祖先。
- exact_stop: HM-R0 F2 不得从本地 `7d638e3` 的旧 registry 激活。
- reproduction: 两链 merge-base=`cd2bbae681767262994f53cd1fecd3c2e35bdd1d`，远端独有 5 个健康 F1 提交，本地独有 6 个保障商城 M1 提交。
- expected / actual: 期望平台权威集成分支只有一个可追溯 HEAD；实际本地集成工作树没有 upstream，商城链未推送时，健康链由另一干净工作树推进远端。
- product_evidence: 两链产品/模块文件互不覆盖；仅 `contracts/foundation/agent-collaboration.v1.json` 重叠。
- tool_or_environment_evidence: 本地分支未配置 upstream，无法用普通状态输出提示远端漂移。

## Causal chain

1. 因为本地集成工作树未配置 upstream，且本地商城链在未推送状态继续形成提交，因此本地状态无法自动显示远端健康链已经前进。
2. 因为健康 F1 由另一干净受控工作树直接推进远端权威，因此本地商城链与远端健康链从共同基线分开。
3. **最早可控原因**：权威推送前没有统一执行“远端精确 HEAD + 本地候选 ancestry + 未推送提交”三项 freshness 门禁。

## Impact

- affected_modules_and_paths: 健康 HM-R0 F1、保障商城 M1 及协作 registry。
- security_data_release_impact: 无业务运行、真实数据、环境、资金、部署或生产影响。
- blocks: HM-R0 F2 正式激活；任何基于 `7d638e3` registry 的新派发。
- does_not_block: 两条已提交历史的只读验证；其他不依赖 registry 的只读工作。

## Resolution

- rejected_workaround_and_reason: 禁止强推任一链、禁止把一边 registry 整体覆盖另一边、禁止删除本地商城提交。
- systemic_fix: 从远端健康权威链创建独立调和工作树，三方合并本地商城链；保留健康 F1 状态，吸收商城 M0/M1 的真实 integrated 状态与证据。
- changed_contracts_code_tools: 仅合并既有商城证据、更新协作 registry，并新增本报告及治理证据；无业务代码修改。
- compatibility_or_migration: 两条原提交链均保留为合并父历史。
- rollback: 调和提交可通过其第一父提交回到健康权威链；不删除第二父商城历史。

## Prevention and proof

- prevention_gate: 今后权威推送前必须核对 `git ls-remote`、候选与远端 `merge-base --is-ancestor`、本地集成工作树未推送提交和 clean status；发现分叉必须独立调和，不允许直接强推。
- positive_test: 两条父链均为最终调和提交祖先；健康与商城关键工作项同时存在且状态正确。
- negative_test: 以任一单边 registry 替换调和结果会丢失另一边工作项，禁止接受。
- regression_set: collaboration、checklist、exam、IR、Service Plaza 总合同、UTF-8 和 diff 门禁。
- environment_retest: 不适用；无环境变更。
- evidence_paths_and_exact_commits: 远端健康 `034e46b`，本地商城 `7d638e3`，本报告与最终权威 HEAD。

## Verdict

- Pass：两条链均保留并在受控合并中调和，唯一 registry 重叠已验证。
- unresolved_risk: 本地旧集成工作树必须在最终远端推送后安全快进到新权威 HEAD。
- next_authorization: 完成本工作项收口后，平台可独立派发 HM-R0 F2 文档/决策审计；不得自动进入 F3/P3 或业务实现。
