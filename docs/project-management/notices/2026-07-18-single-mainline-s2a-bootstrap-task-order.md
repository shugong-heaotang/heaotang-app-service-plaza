# 单一产品主线 S2A 治理启动任务书

- work_id：`AIW-20260718-SINGLE-MAINLINE-S2A-BOOTSTRAP`
- record_id：`IR-20260718-SINGLE-MAINLINE-S2A-BOOTSTRAP-C1`
- actor：`Codex highest owner / thread 019f72ee-3907-7b21-9498-8e918ac53aac`
- decision owner：Codex 项目最高负责人；保留边界事项由张树功决策
- independent reviewer：`Project Brain / thread 019f53cf-af43-7311-8e3c-bff5e0e187f2`
- repository authority：`refs/heads/codex/service-plaza-phase1-integration@126419d9aea93b86a8449fabe7156e03d78572dc`
- branch：`codex/single-mainline-s2-r1`
- worktree：`C:/Users/shugo/Documents/worktrees/heaotang-single-mainline-s2-r1`
- execution activation expiry：`2026-07-18T16:00:00+08:00`

## 唯一目标

从已独立接受的唯一同步锚点建立一条干净主线的治理身份，完成协作登记、任务理解、preflight、current checklist、随机治理考试 100 分、implementation record、Handoff、静态门禁和一个本地候选提交。该检查点不实施业务功能。

## 精确允许范围

1. `contracts/foundation/agent-collaboration.v1.json`
2. `docs/project-management/notices/2026-07-18-single-mainline-s2a-bootstrap-task-order.md`
3. `docs/project-management/pdcar/task-comprehension-single-mainline-s2a-bootstrap.md`
4. `docs/project-management/pdcar/handoff-single-mainline-s2a-bootstrap.md`
5. `contracts/foundation/development-checklists/2026-07-18-single-mainline-s2a-bootstrap*.json`
6. `contracts/foundation/governance-exams/2026-07-18-single-mainline-s2a-bootstrap*.json`
7. `contracts/foundation/implementation-records/2026-07-18-single-mainline-s2a-bootstrap*.json`

## 执行门

1. 新 worktree 必须 clean、branch 与 HEAD 精确。
2. registry schema 与 active overlap validator 必须 0 error。
3. preflight 必须 `ready`；current checklist 必须逐文件全文读取并绑定当时 SHA。
4. 随机 8 题必须一次 100 分；失败试卷不可改写。
5. JSON/schema、UTF-8、allowed-path、`git diff --check` 和全部治理 validator 必须通过。
6. 只允许一个本地治理候选提交；随后停止并等待独立 Acceptance。

## 明确禁止

不修改业务代码、schema、scripts、workflow、AGENTS、README、CONSTRAINTS 或旧证据；不接管、清理或删除旧 worktree；不 push、merge、integrate、deploy；不触碰生产、真实数据、支付或外部系统。S2A Acceptance Go 不自动授权 S2B。

## 停止条件

authority 漂移、workspace 不 clean、active overlap、preflight 非 ready、checklist 不完整、Exam 非 100、越界路径、同一门禁第二次失败或授权过期，立即停止并可见报告，禁止静默重试。
