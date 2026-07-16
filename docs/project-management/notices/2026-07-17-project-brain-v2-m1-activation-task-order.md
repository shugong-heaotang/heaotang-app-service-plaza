# Project Brain v2 M1 激活治理任务令

- 日期：2026-07-17
- work item：`AIW-20260717-PROJECT-BRAIN-V2-M1-ACTIVATION`
- target item：`AIW-20260716-PROJECT-BRAIN-V2-M1-FACT-CONTRACTS`
- exact authority base：`86ab20f8928a6d70195edb3879fbe7083c20a0f9`
- activation branch：`codex/project-brain-v2-m1-activation`
- activation workspace：`C:/Users/shugo/Documents/APP系统/.codex-worktrees/project-brain-v2-m1-activation`
- M1 branch：`codex/project-brain-v2-m1-fact-contracts`
- M1 workspace：`C:/Users/shugo/Documents/APP系统/.codex-worktrees/project-brain-v2-m1-fact-contracts`

## 目标

只完成 Project Brain v2 M1 的合法激活治理：登记一个 PB-only activation 工作项，把 M1 的预留 base 刷新为当前 exact authority，证明唯一 owner、无活动路径冲突、两个工作树均从同一 authority 创建且干净，生成当前 checklist、随机考试 100、实现记录和 Handoff，并交独立 reviewer。M1 从 `planned` 到 `active` 仅在本 exact candidate 获得独立 Go 且由平台集成负责人普通 fast-forward 进入 authority 后生效。

## exact allowed path classes

1. `contracts/foundation/agent-collaboration.v1.json`
2. `docs/project-management/notices/2026-07-17-project-brain-v2-m1-activation-task-order.md`
3. `docs/project-management/project-brain-v2/task-comprehension-receipt-m1-activation.md`
4. `docs/project-management/project-brain-v2/handoff-m1-activation.md`
5. `contracts/foundation/development-checklists/2026-07-17-project-brain-v2-m1-activation*.json`
6. `contracts/foundation/governance-exams/2026-07-17-project-brain-v2-m1-activation*.json`
7. `contracts/foundation/implementation-records/2026-07-17-project-brain-v2-m1-activation*.json`

首次准入证据在 registry 最终化后会因 registry 哈希变化而成为历史快照，必须原样保留；以 `R2` 生成 current checklist、exam 与 IR。因此候选预计包含 10 个文件，且不得新增第八类路径。

## 激活边界

- activation developer：Project Brain v2 M1 activation governance owner
- M1 developer：Project Brain v2 M1 project owner
- reviewer：independent Project Brain v2 M1 activation reviewer
- approver：项目最高负责人（本任务已于 2026-07-17 明确授权进入 M1 激活治理）
- integration owner：平台集成负责人

本任务只使 M1 具备进入第一个合同检查点的资格，不完成任何 M1 合同，不触碰 `contracts/project-brain/v2/**` 或 `source-map-v2.md`。激活后第一个实施检查点仍须在 M1 自己的 current checklist、exam 100 和任务令约束下，仅完成去标识事实合同与来源映射。

## 完成门禁

1. 远端 authority 在提交、review 和集成前均为 exact fresh；
2. activation 与 M1 工作树均从 exact base 创建、分支匹配且 clean；
3. registry 只有 activation 新增和 M1 激活字段变化，其他 140 个基线 work items 序列化语义不变；
4. current R2 checklist 26/26、随机考试 100、R2 IR verified；首次证据保持不可修改；
5. collaboration、checklist、exam、IR、总合同、UTF-8、diff-check、secret 0 和 exact scope 全部通过；
6. independent reviewer 文件化判定 Go 后，才允许普通 fast-forward；禁止 force push。

## 持续 No-Go

M2-M5、App、运行 scripts、scheduler、snapshot、dashboard、通知、导出、真实数据、凭据、环境、部署与 production 全部继续 No-Go。禁止行级会员、健康、订单、支付、客服、人脉数据以及可重识别或小样本聚合。禁止修改 R4、Mall、NOVA、Club、Activity、Health、SC remediation 与 Project Brain v1。任一 Unknown、漂移、越界或冲突均失败关闭。
