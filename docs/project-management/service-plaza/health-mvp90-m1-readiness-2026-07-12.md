# 健康大管家 MVP-90 M1 准入与派发报告

- Handoff：`HM-M1-PREAUTH-HANDOFF-20260712-001`
- 平台工作项：`AIW-20260712-HEALTH-MVP90-M1-READINESS-DISPATCH`
- 模块工作项：`AIW-20260712-HEALTH-MVP90-M1-SYNTHETIC-PDCAR`
- 通知：`HM-MVP90-M1-TASK-20260712-001`
- 结论：`Pending with owner`；工作包已正式预登记，模块保持 `planned` 和只读

## 已核验证据

- APP 派发基线：`b5d2b635de2cddd71debf76a6c688615b72de2ab`。
- 后端权威基线：`e41265905815082433e040412f3dd6b6b33dfede`。
- M0 合同工作项已 integrated；M0 数量门禁为对象 16/16、状态机 6/6、角色 6/6、合成场景 15/15、conformance 12/12。
- 健康安全后端提交 `e361a8ac792d1caaa15241062be904a266bf83ea` 是后端权威基线祖先，精确修改三条允许路径；定向 health-plugin test 和 vet 通过，分支、远端及工作树一致且 clean。
- 该后端尚未部署测试环境，因此只关闭陈旧 registry 占用，不把它提升为环境 Go。
- 最终治理证据为 R3 checklist 28/28、current SHA mismatch 0 和 R3 governance exam score 100。R1/R2 使用了不符合实现记录统一标识规则的 `FC-...` record_id，且其注册表 SHA 已过期；原字节保存在 `contracts/foundation/invalidated-snapshots/health-mvp90-m1-readiness-dispatch/`，不修改、不用于最终授权。

## 阻塞与唯一责任人

| 门禁 | 当前状态 | 唯一责任人 | 关闭证据 |
| --- | --- | --- | --- |
| C4-H01 专业动作边界 | Pending | 和奥堂医生集团专业负责人 | AI/管理师/医生允许与禁止动作、转介责任、版本化书面会签 |
| M1 窄模板专业会签 | Pending | 和奥堂医生集团专业负责人 | 适用范围、禁忌、停止/转人工条件、版本、审核人；不得扩大为全量 H06 |
| C4-S04 安全冻结 | Pending | 平台安全负责人 | 精确权限、服务端拒绝矩阵、审计字段、威胁模型及复审条件 |

平台集成负责人负责验证证据、更新机器登记和执行 activation，但无权替上述责任人签字。

## 不阻塞项

价格、外部供应商、真实试运行、容量数值和收费策略不影响 M1 合同准备；它们继续 Pending 且不可执行。风险值班、专业资格容量和运营接管仍失败关闭并后置 M2。

## planned 工作包

- branch：`codex/health-manager-mvp90-m1-synthetic-pdcar`
- worktree：`C:/Users/shugo/Documents/worktrees/heaotang-health-mvp90-m1-synthetic-pdcar`
- registration base：`b5d2b635de2cddd71debf76a6c688615b72de2ab`
- 激活时必须改为包含本通知和本报告的最终 integration HEAD。
- 首检查点只允许合同、Schema、合成 fixtures/conformance 与治理证据；共享代码另立工作项。

## 下一检查点

三位责任角色提交书面证据后，平台执行一次联合门禁复核。全部 Accepted 才进行独立 activation；任一 Exact revision 或 Pending 都保持模块只读，并只退回对应责任人，不让无关决定扩大为全项目停工。
