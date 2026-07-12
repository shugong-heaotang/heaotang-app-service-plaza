# 健康大管家 MVP-90 M1 专业会签决策包（Proposed）

- work_id：`AIW-20260712-HEALTH-M1-PROFESSIONAL-SIGNOFF`
- decision thread：`019f54a1-2847-7a71-b0ea-ee1ec403f29b`
- signer：和奥堂医生集团专业负责人
- packet version：`v1-proposed`
- packet status：`Pending with owner`
- executable：`false`

## 1. 决策范围

本包只请求两项正式决定：

1. `C4-H01`：HM-MVP90-M1 成年合成会员 PDCAR 纵切内，AI、健康管理师、医生的逐动作边界。
2. `M1-LIFESTYLE-TEMPLATE`：仅用于上述 M1 纵切的安全生活方式窄模板。

本包不关闭 HM-R0 全量专业冻结，不接受全部 `C4-H06`，不授权真实会员、真实健康数据、业务代码、环境、部署、诊断、处方、治疗或收费。

## 2. 请专业负责人选择唯一回复

请对 `C4-H01`、`M1-LIFESTYLE-TEMPLATE` 以及 15 个场景逐项给出以下一种书面结论：

- `Accepted`：填写真实姓名、角色、日期、接受版本及书面确认引用。
- `Exact revision`：列明 exact section/action/scenario、替换文本、专业理由和复验条件。
- `Pending with owner`：列明唯一 owner、缺失证据和下一检查点。

协调 Agent 不能替您填写签字、姓名、日期或 Accepted。

## 3. C4-H01 Proposed 动作矩阵

机器全文：`contracts/modules/health-manager/mvp90-m1/readiness/c4-h01-action-boundary-decision.v1.json`

| 动作 | AI Proposed | 管理师 Proposed | 医生 Proposed |
| --- | --- | --- | --- |
| 资料整理 | draft-only | allow | allow |
| 评估草案 | draft-only | review-required | review-required |
| 目标/计划草案 | draft-only | review-required | review-required |
| 计划复核与生效 | deny | review-required | review-required |
| 任务解释 | allow（仅已确认普通任务） | allow | allow |
| 反馈记录 | draft-only | allow | allow |
| 计划调整 | draft-only | review-required | review-required |
| 成长记录 | draft-only | allow | allow |
| 风险识别 | transfer-only | review-required | allow |
| 风险关闭 | deny | deny（不得单独关闭） | review-required |
| 紧急处置 | transfer-only | transfer-only | review-required |
| 诊断 | deny | deny | review-required（仅正式医疗范围） |
| 处方 | deny | deny | review-required（仅有处方权的正式医疗范围） |
| 治疗建议 | deny | deny | review-required（仅正式医疗范围） |
| 转介 | transfer-only | allow | allow |
| 专业复核 | deny | transfer-only | allow |
| 普通流程安全恢复 | deny | review-required | allow |

每项机器记录还包含资源范围、前置授权、失败关闭、转介责任、停止条件和不可替代边界。当前全部只是协调方 Proposed，不是专业决定。

## 4. M1 安全生活方式窄模板 Proposed

机器全文：`contracts/modules/health-manager/mvp90-m1/readiness/m1-lifestyle-template-signoff.v1.json`

- 适用：成年合成会员；资料、授权、服务关系和模板版本有效；无已知禁忌；仅普通睡眠、作息、饮水、饮食事实记录、日常活动与自我观察提示。
- 不适用：未成年人、孕产期或需专门专业评估者、急性不适/风险者、需要诊断/药物/治疗/康复处方者、资料或授权不足者。
- 禁止：疾病诊断、处方或改药、治疗方案、疗效保证、未审核运动强度、个体化营养处方、替代急救或医生。
- 停止并转人工：禁忌、资料不足、不适、风险、撤权、关系失效、模板/规则过期或 AI 触及禁止内容。
- 当前 reviewer/effective date/expiry/signature 均为空，`executable=false`。
- 即使本窄模板未来 Accepted，`C4-H06` 其他模板仍保持 Pending。

## 5. 15 场景专业复核

机器全文：`contracts/modules/health-manager/mvp90-m1/readiness/m1-professional-scenario-review.v1.json`

已逐项列出 `MVP-A001`—`MVP-A015` 的专业复核问题、Proposed 安全结果、禁止结果、停止/转人工条件和缺失证据。当前 15/15 均为 `Pending with owner`，不能作为可执行策略。

重点请核验：紧急风险、不适、AI 越权、授权撤回、模板失效、人工消息未送达、数据纠错影响和安全退出后的开放风险责任。

## 6. 可证伪前提和复审触发

以下任一事实出现即推翻当前 Proposed 边界并要求停止/复审：AI 输出被当作诊断/处方/治疗或有效专业结论；风险被非合格人员关闭；模板在不适、撤权、过期或禁忌后继续；窄模板被扩大为全量 C4-H06；范围扩展到真实会员或新群体。

复审触发包括：范围/人群/内容类别变化、安全事件或越权输出、专业或监管前提变化、模板到期、资质/授权模型变化。

## 7. 回执位置

正式书面回复及引用应登记到 `health-manager-mvp90-m1-professional-signoff-receipt.md`。在真实 signer 回执前，该回执必须保持 Pending，M1 模块仍为 planned/No-Go。
