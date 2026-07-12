# 健康大管家 MVP-90 M1 合成 PDCAR 纵切任务通知书

- notice_id：`HM-MVP90-M1-TASK-20260712-001`
- platform_work_id：`AIW-20260712-HEALTH-MVP90-M1-READINESS-DISPATCH`
- module_work_id：`AIW-20260712-HEALTH-MVP90-M1-SYNTHETIC-PDCAR`
- Handoff：`HM-M1-PREAUTH-HANDOFF-20260712-001`
- 下达日期：2026-07-12
- 下达方：平台集成负责人
- 接收方：健康大管家负责人
- 状态：正式预派发；`Pending with owner`，模块工作项保持 `planned` 和只读

## 1. 目标与最小纵切

仅面向成年合成会员，形成一条可验证的 PDCAR 产品纵切：边界与授权 → 档案/测评 → 年度目标与计划草案 → 管理师复核/会员确认 → 每日任务 → 反馈 → 检查/复盘 → Advance/计划版本调整 → 成长记录。

AI 仅可生成草案、提醒和解释；不得诊断、处方、独立生效计划、替代专业人员或关闭专业/紧急风险。

## 2. 已满足前置

- `AIW-20260711-HEALTH-MVP90-M0-CONTRACTS` 已 integrated。
- M0 已形成 16/16 对象、6/6 状态机、6/6 角色、15/15 合成场景及 12/12 conformance。
- 健康平台安全后端实现 `e361a8ac792d1caaa15241062be904a266bf83ea` 已进入 backend integration `e41265905815082433e040412f3dd6b6b33dfede`；仅证明代码集成，不证明测试环境 Go。

## 3. 激活前必须关闭的三项门禁

1. `C4-H01`：和奥堂医生集团专业负责人书面确认 AI、管理师、医生的允许动作、禁止动作、转介责任和不可替代边界。
2. M1 窄模板会签：和奥堂医生集团专业负责人只对本纵切使用的安全生活方式模板确认适用范围、禁忌、停止/转人工条件、版本和审核人。该证据不得把全部 `C4-H06` 模板改为 Accepted。
3. `C4-S04`：平台安全负责人冻结 M1 精确权限、资源级服务端拒绝矩阵、最小审计字段和威胁模型；前端隐藏不是授权证据。

三项证据必须包含 decision maker、date、scope、accepted/revision/pending 状态、可证伪前提、复审触发条件和版本。任何一项缺失，模块不得从 `planned` 转 `active`。

## 4. 唯一工作区与首检查点允许路径

- repository：`C:/Users/shugo/Documents/APP系统`
- branch：`codex/health-manager-mvp90-m1-synthetic-pdcar`
- worktree：`C:/Users/shugo/Documents/worktrees/heaotang-health-mvp90-m1-synthetic-pdcar`
- registration base：`b5d2b635de2cddd71debf76a6c688615b72de2ab`
- activation base：必须在平台派发受控集成后更新为最终权威 integration HEAD，并核验 HEAD/merge-base 一致、worktree clean
- owner：健康大管家负责人

精确允许路径以 `agent-collaboration.v1.json` 为机器真相源。首检查点仅包括 M1 requirements、receipt、Handoff、conformance report、内部依赖、M1 vertical slice/professional boundaries/security authorization/synthetic scenarios 的 JSON 与 Schema、fixtures、Python conformance 以及 M1 专属 checklist/exam/IR。

本通知不授权共享前端、后端、API、数据库或部署路径。需要共享实现时，由平台和后端负责人另建不重叠工作项。

## 5. 两层依赖和失败关闭

- 平台依赖继续使用 `contracts/foundation/module-dependencies/health-manager.v1.json`；代码集成和环境验收分别记录。
- 模块依赖继续使用 `contracts/modules/health-manager/internal-dependencies.v1.json`；M1 节点必须逐项引用 M0、H01、窄模板会签和 S04 证据。
- `HM-R0` 保持 Technical Go / Professional Freeze Pending；其余 27 项 Pending 默认 `executable=false`。
- 价格、供应商、真实试运行等与本首检查点无关的决定不阻塞合同准备。
- `C4-H02/H03/H04`、`C4-O01/O02` 继续失败关闭并后置 M2；M1 不得宣称人工风险接管已经完成。

## 6. 短检查点

1. M1-P0：三项门禁证据完整性和两层依赖图；未满足时只能提交 decision packet，不得生成 executable policy。
2. M1-P1：纵切对象引用、状态迁移、角色动作、拒绝矩阵、审计字段与合成场景合同。
3. M1-P2：固定 seed 的合成 PDCAR conformance；不得使用真实会员或健康数据。
4. M1-P3：平台独立复核 Contract Go 后，才评估拆分前端/后端实现工作项。

每个检查点必须完成 current checklist、随机考试 100、IR、Handoff、范围/UTF-8/diff/敏感扫描并提交推送。聊天确认不能替代仓库证据。

## 7. 明确禁止

- 激活前禁止模块创建 checklist、考试、合同或业务文件。
- 禁止环境、部署、生产、真实会员、真实健康数据、收费和资金操作。
- 禁止 AI 诊断、处方、疗效承诺、独立计划生效或关闭风险。
- 禁止把 M0 Go、PRD C5、技术评审或窄模板会签扩大为 HM-R0 全量专业冻结。
- 禁止以前端本地判断代替服务端权限和资源级拒绝。

## 8. 激活与 Handoff 条件

平台收到三项书面证据后独立复核；全部通过才创建/同步模块工作树、更新 exact base、核验 clean，并以独立 activation commit 将模块工作项从 `planned` 转 `active`。激活通知必须回传 exact commit、权威 integration HEAD、branch、worktree、allowed paths 和三项证据引用。
