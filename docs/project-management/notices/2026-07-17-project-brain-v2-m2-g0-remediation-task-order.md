# Project Brain v2 M2 G0 remediation task order

- authority/base：`16d538c9f8f12dacfd9dba1ad82400f9724e9d94`
- work item：`AIW-20260717-PROJECT-BRAIN-V2-M2-G0-REMEDIATION`
- 缺陷：`PBV2-M2-G0-PRIVACY-THRESHOLD-001`

## 目标

修复 `RefreshEngine._evaluate` 对所有 Trusted 结果统一执行 G1 样本阈值的错误。合法 G0 结果必须要求 `sample_size=null`、`privacy_threshold=not_applicable`，且不得执行 G1 minimum group size；G1 high/standard 阈值、rounding、失败关闭与不可变证据语义必须保持。

## 唯一允许范围

- `project_brain_v2/runtime/engine.py`
- `project_brain_v2/runtime/tests/test_engine.py`
- 本工作项自己的 task order、comprehension、Handoff、checklist、Exam、IR

不得修改 M1/M3/v1、registry、合同 fixture、App、环境、真实数据、网络、部署、timer 或 production 能力。

## 必须证明

- 两个 G0 治理事实的合法 Trusted 结果均可创建 snapshot、pointer、audit 与 run record；
- G0 携带任何 sample size 或把 privacy threshold 伪造为 pass/fail 时失败关闭；
- G1 high/standard minimum group size 与 rounding 不回归；
- M2、M1、M3 相关回归全部通过；
- 历史 No-Go 不改写，M3 overall Acceptance 仍须独立复验。

任何越界、freshness 漂移、失败门禁或 reviewer 发现均 No-Go。
