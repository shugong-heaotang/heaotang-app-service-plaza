# APP PDCAR Skill 强制接入激活治理任务书

- work_id：`AIW-20260717-PLATFORM-PDCAR-SKILL-ENFORCEMENT-ACTIVATION`
- record_id：`IR-20260717-PLATFORM-PDCAR-SKILL-ENFORCEMENT-ACTIVATION-C1`
- actor：`APP PDCAR enforcement activation owner`
- decision owner：项目最高负责人
- independent reviewer：Project Brain 独立审核负责人
- repository：`C:/Users/shugo/Documents/APP系统`
- branch：`codex/platform-pdcar-skill-enforcement-activation`
- worktree：`C:/Users/shugo/Documents/worktrees/heaotang-platform-pdcar-skill-enforcement-activation`
- authority/base：`09cd00a429da37a87d26870310617b928d0894a7`
- due：`2026-07-17T12:30:00+08:00`
- expiry：`2026-07-17T13:00:00+08:00`

## 唯一目标

完成正式实施工作项之前的激活治理证据：任务理解、当前开发清单、随机治理考试 100 分、activation implementation record 和 Handoff，交 Project Brain 独立验收。该切片不实施 APP PDCAR 强制接入。

## 精确允许范围

1. `contracts/foundation/agent-collaboration.v1.json`
2. `docs/project-management/notices/2026-07-17-platform-pdcar-skill-enforcement-activation-task-order.md`
3. `docs/project-management/pdcar/task-comprehension-platform-pdcar-skill-enforcement-activation.md`
4. `docs/project-management/pdcar/handoff-platform-pdcar-skill-enforcement-activation.md`
5. `contracts/foundation/development-checklists/2026-07-17-platform-pdcar-skill-enforcement-activation*.json`
6. `contracts/foundation/governance-exams/2026-07-17-platform-pdcar-skill-enforcement-activation*.json`
7. `contracts/foundation/implementation-records/2026-07-17-platform-pdcar-skill-enforcement-activation*.json`

本检查点不需要修改 registry；registry 路径仅保留给后续独立批准的生命周期变更。

## 禁止范围

- 不修改 `AGENTS.md`、`README.md`、`.github/workflows/**`、`scripts/**`、schema、正式 PDCAR 实施文件或任何业务代码。
- 不创建或登记正式实施工作项，不创建正式实施工作树。
- 不 push、不集成、不部署，不触碰真实数据、支付或生产。
- 不把 preflight、checklist、Exam100、自测或本候选提交解释成正式实施授权。

## 检查点和证据

1. 从 authority `09cd00a...` 的 clean 专用工作树运行 preflight，状态必须为 `ready`。
2. 创建同一 record_id 的 current checklist，逐项全文读取并记录当前 SHA-256。
3. checklist 验证通过后生成随机 attempt 1；按题面作答，必须 8/8、100 分、`passed`。
4. 形成 activation implementation record 和 Handoff，记录实际命令、结果、changed paths、残余风险和独立验收条件。
5. 运行 JSON/schema、collaboration、checklist、exam、implementation-record、UTF-8、`git diff --check` 和 allowed-path 检测。
6. 提交 activation governance candidate 后立即停止，等待 Project Brain 独立审核。

## 停止与升级条件

authority 漂移、工作树不 clean、active overlap、checklist 不完整、考试非 100、任一越界路径或第二次同类失败均立即停止，并向项目最高负责人和 Project Brain 报告。does_not_block：所有既有非重叠板块工作。
