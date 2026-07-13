# 健康大管家 M1 专业会签材料包任务通知书

- notice_id：`HM-M1-PROFESSIONAL-SIGNOFF-TASK-20260712-001`
- work_id：`AIW-20260712-HEALTH-M1-PROFESSIONAL-SIGNOFF`
- decision_thread：`019f54a1-2847-7a71-b0ea-ee1ec403f29b`
- owner：和奥堂医生集团专业负责人会签协调
- signer：和奥堂医生集团专业负责人
- 状态：正式派发后由 planned 转 active；协调 Agent 不具有签字权

## 目标

形成两份可由真实专业负责人逐项签署的决策：

1. `C4-H01`：AI、健康管理师、医生的允许动作、禁止动作、转介责任、不可替代边界。
2. `M1-LIFESTYLE-TEMPLATE`：仅限成年合成会员 M1 纵切使用的安全生活方式模板，覆盖适用/不适用人群、禁忌、停止条件、转人工条件、模板版本、审核人和复审触发。

第二项只关闭 M1 所需的窄模板门禁，不得把全部 `C4-H06` 改为 Accepted。

## 工作区与允许路径

- branch：`codex/health-m1-professional-signoff`
- worktree：`C:/Users/shugo/Documents/worktrees/heaotang-health-m1-professional-signoff`
- registration base：`ef66b98113862d4b75bfe96df2966db52d65fddf`
- 最终 base：派发集成后的 exact APP HEAD

只允许修改 registry 中本工作项列明的 decision packet、receipt、专属 checklist/exam/IR，以及 `readiness/` 下精确枚举的 C4-H01 动作边界、M1 窄模板和 15 场景专业复核 JSON/Schema。禁止修改 M0 合同、M1 实现合同、前后端、环境、部署和真实健康数据。

## 决策包必备字段

- decision_id、decision_maker、decision_date、scope、version；
- `Accepted | Exact revision | Pending with owner`；
- premise、falsification evidence、review trigger/date；
- allowed actions、forbidden actions、required human review；
- transfer/escalation responsibility、stop condition、non-substitutable boundary；
- evidence references、signer role、signature/书面确认引用。

## C4-H01 动作矩阵

至少逐项审查：资料整理、评估草案、目标/计划草案、计划复核与生效、任务解释、反馈记录、计划调整、成长记录、风险识别、风险关闭、紧急处置、诊断、处方、治疗建议、转介和专业复核。

每项必须分别给出 AI、管理师、医生的 `allow | deny | draft-only | review-required | transfer-only`，并说明资源范围、前置授权和失败关闭结果。不得用“辅助”“按需”等模糊词代替逐动作结论。

机器记录必须以 `additionalProperties=false` 的 Schema 拒绝缺动作、缺裁决人、缺版本、缺场景覆盖或把 Pending 标成 executable 的输入。

## 窄模板会签

模板不得包含疾病诊断、药物调整、治疗方案、疗效保证、未审核运动强度或营养处方。任何禁忌、资料不足、不适反馈、风险提示、撤权或模板过期均必须停止生成/执行并转人工或保持 No-Go。

## 验收与签署规则

- 协调 Agent 可以预填现有技术/产品边界，但不得填写真实 signer 决策。
- `Accepted` 必须有专业负责人姓名/角色、日期、版本和书面引用。
- `Exact revision` 必须列 exact section、替换文本、理由和复验条件。
- `Pending with owner` 必须列唯一 owner、缺失证据和下一检查点。
- 未签署时 receipt 必须保持 Pending，M1 继续 planned。
