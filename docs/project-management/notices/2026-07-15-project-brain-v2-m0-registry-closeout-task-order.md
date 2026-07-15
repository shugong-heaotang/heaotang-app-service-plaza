# Project Brain v2 M0 registry 收口任务令

- 日期：2026-07-15
- work item：`AIW-20260715-PROJECT-BRAIN-V2-M0-REGISTRY-CLOSEOUT`
- exact base：`9b221a8a2a4de7c70ef9d1f86a55656b2c0d2757`
- branch：`codex/project-brain-v2-m0-closeout`
- workspace：`C:/Users/shugo/Documents/APP系统/.codex-worktrees/project-brain-v2-m0-closeout`

## 目标

仅对 Project Brain v2 自身进行平台 registry 收口：把 `AIW-20260714-PROJECT-BRAIN-V2-OPERATIONS` 从 `active` 准确登记为 `integrated`，登记本收口工作项，并新增 M1 经营事实合同工作项为 `planned`。M1 不得激活，不得创建运行工作树，不得编写合同或实现。

## exact allowed path classes

1. `contracts/foundation/agent-collaboration.v1.json`
2. `docs/project-management/notices/2026-07-15-project-brain-v2-m0-registry-closeout-task-order.md`
3. `docs/project-management/project-brain-v2/task-comprehension-receipt-m0-registry-closeout.md`
4. `contracts/foundation/development-checklists/2026-07-15-project-brain-v2-m0-registry-closeout*.json`
5. `contracts/foundation/governance-exams/2026-07-15-project-brain-v2-m0-registry-closeout*.json`
6. `contracts/foundation/implementation-records/2026-07-15-project-brain-v2-m0-registry-closeout*.json`
7. `docs/project-management/project-brain-v2/handoff-m0-registry-closeout.md`

上述为 7 类受控路径。首次准入证据在 registry 最终化后变旧，必须原样保留为历史；current R2 checklist、exam 与 IR 作为同类追加证据，因此候选实际包含 10 个文件。不得增加第八类路径。

## 状态语义

候选内 `operations=integrated`、`closeout=integrated`、`M1=planned` 仅在本 exact candidate 经过独立 reviewer 判定 Go，并由平台集成负责人以普通 fast-forward 纳入 authority 后生效。候选分支、提交、自测或 Handoff 均不得冒充权威集成。

M1 的 `planned` 只表示满足 M0 后可另行发起准入；不授予 active、工作树、contracts、App、scripts、真实数据、凭据、环境、部署或 production 权限。M2-M5 继续 No-Go。

## 角色分离

- developer：Project Brain v2 M0 registry closeout platform governance owner
- reviewer：independent platform reviewer
- approver：项目最高负责人
- integration owner：平台集成负责人

## 完成门禁

current R2 checklist、随机考试 100、任务理解回执、verified R2 IR、协作 registry 校验、总合同、UTF-8、secret 0、7/7 allowed path classes、实际 10 个文件、其他 work items 逐项序列化语义不变和 authority freshness 全部通过。只形成 clean candidate，不 push；独立 Go 后才允许普通 fast-forward 集成。

## 禁止范围

禁止触碰 R4、Mall、NOVA、Club、Activity、Health、SC remediation、Project Brain v1、业务代码、运行脚本、真实数据、凭据、环境、部署与 production。任一越界、基线漂移或未验证证据均失败关闭。
