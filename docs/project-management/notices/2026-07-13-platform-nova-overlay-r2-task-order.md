# 平台 NOVA 模块 overlay 激活前完整性门禁 R2 任务单

签发时间：2026-07-14（Asia/Shanghai）
签发角色：项目最高负责人
执行角色：Platform governance bootstrap agent
独立验收角色：平台治理独立测试负责人
工作项：`AIW-20260713-PLATFORM-NOVA-OVERLAY-R2`
实现记录：`IR-20260713-PLATFORM-NOVA-OVERLAY-R2`

## 一、范围裁定

本工作项是 **platform scope** 治理修复，起飞检查单必须使用 `module_id=null`。它修复的是新模块 overlay 注册与激活顺序，不实施 NOVA、Protection Mall 或其他模块业务，不修改 registry，不部署，不访问生产、真实用户、真实数据、消息、验证码或资金。

本项处理 `RI-NEW-MODULE-CHECKLIST-BOOTSTRAP` 第三次复发。必须修复最早可控原因：模块在进入 `active` 或 `handoff-ready` 前，平台缺少一个从协作 registry 到 governance reading-list overlay 的共享、失败关闭、机器可执行的完整性门禁。不得只给 NOVA 增加一条 overlay 后制造局部绿色。

## 二、权威与隔离

- central authority：`ea3c70c8bea4904b455455ffc7c6e29821de2705`
- implementation base / initial HEAD：`fb29b857a5476a62cc882bf6bf407e67febcacf9`
- branch：`codex/platform-nova-overlay-r2`
- worktree：`C:\Users\shugo\Documents\worktrees\heaotang-platform-nova-overlay-r2`
- registry 中的历史激活来源 base 保留原记录，不把它冒充实现 HEAD 或 central authority。
- 实施前必须证明本地 registry 中本项为 `active`、工作树干净、无 active/handoff-ready 共享路径冲突，并完成全新 26/26 current checklist 与随机治理考试 100 分。

## 三、允许路径

仅允许修改以下 17 条 registry 已登记路径：

1. `contracts/foundation/governance-reading-list.v1.json`
2. `contracts/foundation/governance-reading-list.v1.schema.json`
3. `scripts/validate_governance_reading_list.py`
4. `scripts/New-AgentDevelopmentChecklist.ps1`
5. `scripts/Test-ServicePlazaContracts.ps1`
6. `scripts/tests/test_new_agent_development_checklist.py`
7. `scripts/tests/test_validate_governance_reading_list.py`
8. `docs/project-management/notices/2026-07-13-nova-phase5-m1-bootstrap-readme.md`
9. `docs/project-management/service-plaza/new-module-governance-bootstrap-audit-2026-07-13.md`
10. `contracts/foundation/recurring-issues.v1.json`
11. `CONSTRAINTS.md`
12. `docs/decisions/0019-module-overlay-registration-before-activation.md`
13. `contracts/foundation/development-checklists/2026-07-13-platform-nova-overlay-r2*.json`
14. `contracts/foundation/governance-exams/2026-07-13-platform-nova-overlay-r2*.json`
15. `contracts/foundation/implementation-records/2026-07-13-platform-nova-overlay-r2*.json`
16. `docs/project-management/notices/2026-07-13-platform-nova-overlay-r2-task-order.md`
17. `docs/project-management/service-plaza/platform-nova-overlay-r2-handoff.md`

禁止修改 `contracts/foundation/agent-collaboration.v1.json`、任何模块业务代码、部署配置、既有历史 checklist/exam/implementation record，以及任何未登记路径。

## 四、系统修复要求

1. 为 NOVA 建立完整、非空、文件存在且可审计的 governance reading-list overlay，使 `-ModuleId nova` 能生成 pending current checklist。
2. reading-list 建立 schema 和独立 validator；overlay key、路径、非空、唯一性与文件存在性必须失败关闭。
3. 激活前共享门禁必须动态读取 registry，拒绝任意 `active` 或 `handoff-ready` 模块缺少有效 overlay；模块集合不得硬编码为 NOVA 特例。
4. 永久负例必须同时覆盖 NOVA 与 Protection Mall，证明当前 Protection Mall 缺 overlay 会被机器拒绝；本项不得补写其业务证据、修改其历史证据或激活新商城项。
5. generator 与独立 validator 使用同一个 reading-list 契约；未知模块、空 overlay、缺失文件继续失败关闭。
6. `Test-ServicePlazaContracts.ps1` 接入 reading-list schema/validator 与相关全量测试，避免定向测试假绿。
7. 对第三次复发更新 recurring issue、`CONSTRAINTS.md`、ADR 0019，并对所有当前和历史模块依赖/overlay/checklist 做只读全量影响审计。
8. task order、implementation record 与 Handoff 必须包含 root-cause record、`blocks`、`does_not_block`、回滚和精确证据。

## 五、验收

- NOVA 正向：`-ModuleId nova` 生成的输入精确等于 core 与 NOVA overlay 的有序去重集合，全部初始 `checked=false`、哈希正确。
- 负向：unknown、empty、missing file、无 overlay 的 active/handoff-ready NOVA 与 Protection Mall 均失败关闭。
- 回归：activity、life-navigation、club-alliance、health-manager 生成行为保持；历史例外字节不可改写。
- 定向测试、完整 Python 测试、Service Plaza 总合同、development checklist/exam/IR validators、UTF-8、scope、`git diff --check` 和 secret scan 全部通过。
- 形成 candidate commit 并推送；独立验收前不得声称 integrated 或关闭工作项。

## 六、根因边界与回滚

- `blocks`：NOVA Phase 5 M1 新 current checklist、考试、实施记录与后续 synthetic E2E 治理闭环。
- `does_not_block`：NOVA 既有 28 项离线回归、其他无重叠模块、公共契约只读复核。
- 拒绝的绕过：删除 `ModuleId`、手工伪造 checked checklist、只添加 NOVA overlay、不扫描 registry、硬编码模块名单、篡改 Protection Mall 历史证据、跳过总合同。
- 回滚：回退本候选全部 17 条范围内变更，保留根因/测试证据；NOVA 后续门禁继续 No-Go，不削弱共享校验。
