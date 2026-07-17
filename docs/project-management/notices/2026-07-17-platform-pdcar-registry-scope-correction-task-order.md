# PDCAR formal implementation 共享 registry 范围纠正任务令

- 日期：2026-07-17
- authority/base：`d3b0f69a49b05a9fb463e2575d23e14ac2dd9b6c`
- branch：`codex/platform-pdcar-registry-scope-correction`
- workspace：`C:/Users/shugo/Documents/APP系统/.codex-worktrees/platform-pdcar-registry-scope-correction`
- writer：temporary platform registry correction owner
- reviewer：independent Project Brain reviewer
- approver：项目最高负责人
- integration owner：平台集成负责人

## 明确授权

项目最高负责人于2026-07-17明确授权：只从`AIW-20260717-PLATFORM-PDCAR-SKILL-ENFORCEMENT`的`allowed_paths`移除`contracts/foundation/agent-collaboration.v1.json`，保持其`active`状态及其他范围不变；独立验收、受控集成后继续Project Brain M2 remediation。

本任务使用外部阻滞登记和独立核验作为授权依据。独立核验SHA-256为`2978787a0ec2561a7e8dfb1ca7f619c68139a7dfe2e0fb956e935ead378714e9`。

## 唯一语义变更

1. 目标work item仍为`active`。
2. owner、owner_role、repository_root、workspace_path、branch、base_commit、started_with_clean_worktree、preexisting_changes_acknowledged、migration_note和handoff_record逐字段保持不变。
3. 原15项`allowed_paths`只删除共享registry一项；其余14项顺序和值保持不变。
4. 不新增、暂停、取消或集成任何PDCAR或Project Brain work item。
5. PDCAR后续registry lifecycle必须另立closeout工作项，不由formal implementation项自改registry。

## 本纠正候选的7类证据路径

1. `contracts/foundation/agent-collaboration.v1.json`
2. 本任务令
3. `docs/project-management/pdcar/task-comprehension-platform-pdcar-registry-scope-correction.md`
4. `docs/project-management/pdcar/handoff-platform-pdcar-registry-scope-correction.md`
5. `contracts/foundation/development-checklists/2026-07-17-platform-pdcar-registry-scope-correction*.json`
6. `contracts/foundation/governance-exams/2026-07-17-platform-pdcar-registry-scope-correction*.json`
7. `contracts/foundation/implementation-records/2026-07-17-platform-pdcar-registry-scope-correction*.json`

## 验收与停止条件

- 深比较必须证明全registry只有目标数组的一个元素删除，其他work item和顶层字段完全不变。
- collaboration validator、总合同、checklist、Exam、IR、UTF-8、diff、secret、范围和freshness全部通过。
- exact candidate必须由独立reviewer判定Go；Go前不得push或integration。
- authority漂移、第二项语义变化、第八类路径、PDCAR状态/其他字段变化或任何Project Brain预授权均立即No-Go。
- 本任务不实现PDCAR，不创建其正式workspace，不修改Project Brain runtime，不接触真实数据、凭据、网络、部署、timer或production。
