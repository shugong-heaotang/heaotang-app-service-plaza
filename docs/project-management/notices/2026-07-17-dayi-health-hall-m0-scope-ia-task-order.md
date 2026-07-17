# 大医健康馆 M0 非医疗范围与信息架构冻结任务令

- work_id：`AIW-20260717-DAYI-HEALTH-HALL-M0-SCOPE-IA`
- record_id：`IR-20260717-DAYI-HEALTH-HALL-M0-SCOPE-IA-C1`
- owner：`Dayi Health Hall continuous development agent`
- owner_role：`健康大管家负责人`
- base：`02f16fb6451ef23cc3da6da2a360f3b1efe67b60`
- branch：`codex/dayi-health-hall-m0-scope-ia`
- worktree：`C:/Users/shugo/Documents/项目最高负责人/worktrees/heaotang-dayi-health-hall-m0-scope-ia`
- status：`active after controlled authority activation`

## 目标

把最高负责人 2026-07-17 的范围变化正式冻结为治理仓库中的 M0 非医疗合同：大医健康馆只建设组织、馆生命周期预览、角色/权限边界、会员服务关系、非医疗服务目录，以及学习广场/俱乐部联盟的权威跳转。

## 当前检查点 C1

只推进以下顺序，不提前实现运行时：

1. ownership/preflight；
2. 使用 `health-manager` overlay 建立同 record_id current checklist，并逐项真实阅读、记录当前 SHA；
3. 随机治理考试 100；
4. 在允许路径内重新实现 M0 Contract、Schema、正负 conformance、说明、IR 和 Handoff；
5. 运行依赖、协作、范围、UTF-8、秘密与医疗暂停门禁；
6. commit/push 后交由独立 reviewer 验收，Go 后受控集成。

`C:/Users/shugo/Documents/项目最高负责人/health-cross-module-requirements/m0-prereg/` 中的预登记合同、fixtures、页面矩阵和机器验收只能作为不可信设计输入；不得复制其“pass”结论，也不得把预登记证据冒充 current checklist、考试、IR 或正式独立验收。

## 必须冻结

- 平台 → 区域 → 健康馆三级组织边界；
- 健康馆申请、审核、入驻、暂停、退出的失败关闭状态；
- 馆负责人、工作人员、会员和审计角色的最小权限与职责分离；
- 会员本人控制服务关系确认、纠错和退出；工作人员或系统不得代确认；
- 学习广场/俱乐部联盟仅“最小摘要 + 跳转权威模块 + 会员确认回传”，禁止直接写库；
- 页面未登录、越权、空、暂停、退出、不可用的明确状态；
- `synthetic_only=true`、`executable=false` 和非医疗安全提示。

## No-Go

不得新增或启用真实身份、真实健康数据、病历、诊断、治疗、处方、用药、医生推荐、在线咨询、第二意见、病例征集、MDT、医疗机构承接、收费、支付、测试服、部署、生产或不可逆操作。不得把健康馆、负责人或工作人员描述为医疗机构、医生或具备诊疗权限的主体。

## blocks / does_not_block

- `blocks`：M0 runtime、M1、真实数据、医疗、收费、部署、生产。
- `does_not_block`：本工作项的离线合成合同、Schema、正负测试、说明、IR、Handoff 和独立验收。

## 完成条件

本工作项只有在 current checklist、Exam100、实现、正负测试、同 record_id IR、Handoff、commit/push 和独立验收/受控集成全部完成后，才能标记 `integrated`。工作树存在、预登记测试通过或代码文件存在均不等于 Go。
