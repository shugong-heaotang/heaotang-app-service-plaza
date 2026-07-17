# Project Brain v2 M2 G0 remediation 激活任务令

- 日期：2026-07-17
- exact authority/base：`6ad2e7e1930f60dfe174397c480a9feefdd53c93`
- R1 `4221004dddf75ce6e9eb6b26e61849652cd2f6b9`因freshness漂移独立验收No-Go，保持原证据且未推送、未集成；本次为R2重建。
- branch：`codex/project-brain-v2-m2-g0-remediation-activation`
- workspace：`C:/Users/shugo/Documents/APP系统/.codex-worktrees/project-brain-v2-m2-g0-remediation-activation`

## 目标

只激活`PBV2-M2-G0-PRIVACY-THRESHOLD-001`的独立根因修复工作项。合法G0 Trusted当前被M2错误套用G1 standard sample threshold，导致两个核心治理事实无法生成snapshot并阻塞M3整体Acceptance。

本activation不修改runtime。它只登记activation与formal remediation两项，冻结两文件runtime范围、G0/G1防复发标准和下游复验顺序。

## 修复验收合同

- 合法G0 Trusted：`sample_size=null`、`privacy_threshold=not_applicable`，可生成immutable snapshot、run、audit和last-trusted pointer。
- 非法G0：任何sample size、`pass`/`fail` privacy result或G1阈值伪装均失败关闭。
- G1：high/standard minimum group size、rounding_base、authorization、quality、freshness和fail-closed语义不变。
- 历史错误No-Go证据不可改写；只影响新run。
- M1合同、M3 candidate、v1和源系统保持不变。

## Activation 7类路径

1. collaboration registry；
2. 本任务令；
3. activation理解回执；
4. activation Handoff；
5. activation checklist wildcard；
6. activation Exam wildcard；
7. activation IR wildcard。

## Formal remediation 8类路径

只允许`engine.py`、`runtime/tests/test_engine.py`、formal任务令、formal理解回执、formal Handoff及其checklist/Exam/IR wildcard。

## 停止条件

authority漂移、registry overlap、第三个work item、activation第八类路径、formal第九类路径、M1/M3/v1/App/环境修改、真实数据/凭据/网络/部署/timer/production能力或任何门禁失败均No-Go。activation exact candidate独立Go并受控集成前，不得创建formal runtime工作树或修改代码。
