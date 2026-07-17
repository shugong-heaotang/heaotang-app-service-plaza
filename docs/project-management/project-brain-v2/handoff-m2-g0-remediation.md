# Project Brain v2 M2 G0 remediation Handoff

- exact base：`16d538c9f8f12dacfd9dba1ad82400f9724e9d94`
- work item：`AIW-20260717-PROJECT-BRAIN-V2-M2-G0-REMEDIATION`
- 状态：implementation in progress；不是 accepted、integrated 或 production

## 修复边界

只修改 `RefreshEngine._evaluate` 与其回归测试：G0 使用 not-applicable 语义，G1 保留样本阈值与 rounding 语义。历史 M2/M3 验收事实不可改写。

## 独立验收重点

必须攻击合法/伪造 G0、G1 high/standard 边界、boolean 与非整数样本、rounding、失败不覆盖 last-trusted，并复跑 M2/M1/M3 回归。还需验证 exact scope、UTF-8、diff、协作、secret0、clean worktree 与 fresh authority。

## 开发者验证

- M2 runtime：43/43，0 skip；合法 G0、第二个 G0、伪造 G0、G1 high/standard 边界及 boolean 样本均覆盖；
- M1 合同及变异回归：20/20，包含 rounding 与 threshold；
- runtime contract：default disabled、production capabilities false、network imports 0、schemas 6；
- current checklist：26/26；随机治理考试：100。
- collaboration、checklist、Exam、IR、总合同、1618文件UTF-8与diff通过；
- exact scope：8文件/8类登记路径，越界0，secret0；最终fetch时remote authority与merge-base均为`16d538c9f8f12dacfd9dba1ad82400f9724e9d94`。

这些writer证据不构成独立Go；候选冻结后仍须由独立reviewer重新绑定exact commit并复验。在独立 Go 前不得推送或集成。
