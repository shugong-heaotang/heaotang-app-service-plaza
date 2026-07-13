# 平台新模块治理冷启动 R1 正式修复任务单

签发时间：2026-07-13 07:42（Asia/Shanghai）
激活截止：2026-07-13 08:30（Asia/Shanghai）
签发角色：项目最高负责人
问题模式：`GOV-NEW-MODULE-BOOTSTRAP-001`
复发级别：第二次复发，必须执行全模块影响扫描、系统性修复与共享 CI 预防门禁

## 一、裁定

批准建立独立平台治理修复项。禁止活动负责人使用 `ModuleId=null`、手工伪造 checklist 或修改 foundation 路径绕过门禁。

本修复只处理新模块治理冷启动机制，不实施活动 M0 内容，不修改业务代码，不部署，不触达真实用户、支付、消息或生产数据。

## 二、工作身份与角色分离

- `work_id`: `AIW-20260713-PLATFORM-NEW-MODULE-BOOTSTRAP-R1`
- `record_id`: `IR-20260713-PLATFORM-NEW-MODULE-BOOTSTRAP-R1`
- owner: `Platform governance bootstrap agent`
- owner_role: `平台治理负责人`
- reviewer: `平台治理独立测试负责人`
- approver: `项目最高负责人`
- 建议分支：`codex/platform-new-module-bootstrap-r1`
- 建议 worktree：`C:\Users\shugo\Documents\worktrees\heaotang-platform-new-module-bootstrap-r1`
- base：激活时最新、已拉取且干净的 `origin/codex/service-plaza-phase1-integration` HEAD
- 初始状态：`planned`

平台治理负责人、活动 M0 实施负责人和独立测试负责人必须为不同执行主体。

### RACI（责任锁定）

- A 最终负责/批准：项目最高负责人。
- R 系统修复实施：`Platform governance bootstrap agent`，绑定 `AIW-20260713-PLATFORM-NEW-MODULE-BOOTSTRAP-R1`。
- R 共享 registry 释放与受控集成：`Codex platform integration agent`，即当前 freshness gate R2 owner。
- V 独立验证：平台治理独立测试负责人，不得参与实现。
- C/复验：活动 V3 持续负责人；仅在修复合入且 activity worktree 更新后重跑原 checklist 命令，不参与平台修复或自验。

## 三、激活条件

当前 `AIW-20260713-PLATFORM-INTEGRATION-FRESHNESS-GATE-R2` 独占 `contracts/foundation/agent-collaboration.v1.json`。本修复项先由该平台集成负责人登记为 `planned`；其释放 registry 路径后，立即建立独立 worktree 并切换为 `active`。

截至 2026-07-13 08:30 未完成释放和激活，必须登记精确 blocker、阻塞 owner 和下一次处置时间，并升级最高负责人；不得继续无期限等待，也不得让两个 active 工作项同时拥有 registry。

2026-07-13 现状证据：freshness R2 专用 worktree `C:\Users\shugo\Documents\APP系统\.codex-worktrees\platform-integration-freshness-gate-r2` 在核验时存在 7 个未提交治理变更（3 删除、1 修改、3 新增），HEAD=`535b906f330414c14296b5d339ef9509e7c9a4e8`。当前 registry owner 必须先保全并提交/交接这些在途变更，给出释放提交，再登记本项；禁止另一执行主体在脏 worktree 混入提交。

08:30 逾期自动处置：项目最高负责人撤销当前 owner 对本次新修复项的登记职责，指定临时 registry 激活代理；代理仍须从已保全的释放提交创建干净 worktree，不得覆盖或删除原 owner 的在途变更。

## 四、allowed paths

仅允许：

- `scripts/New-AgentDevelopmentChecklist.ps1`
- `contracts/foundation/governance-reading-list.v1.json`
- `docs/project-management/notices/2026-07-13-activity-v3-m0-bootstrap-readme.md`
- `scripts/tests/test_new_agent_development_checklist.py`
- `docs/project-management/service-plaza/new-module-governance-bootstrap-audit-2026-07-13.md`
- `contracts/foundation/recurring-issues.v1.json`
- `contracts/foundation/development-checklists/2026-07-13-platform-new-module-bootstrap-r1*.json`
- `contracts/foundation/governance-exams/2026-07-13-platform-new-module-bootstrap-r1*.json`
- `contracts/foundation/implementation-records/2026-07-13-platform-new-module-bootstrap-r1*.json`
- `docs/project-management/notices/2026-07-13-platform-new-module-bootstrap-r1-task-order.md`
- `docs/project-management/service-plaza/platform-new-module-bootstrap-r1-handoff.md`

Registry 的登记/状态变更仍仅由平台集成负责人执行；不把 registry 授权给修复实现 Agent。

## 五、protected paths

- `contracts/modules/activity/**`
- `docs/project-management/modules/activity/**`
- `app/src/**`
- 后端、部署、服务器、生产配置及密钥
- 既有 checklist/exam/implementation record 内容
- 其他模块实现和其他活动工作项路径

## 六、最小修复范围

1. 移除 `New-AgentDevelopmentChecklist.ps1` 中硬编码模块 `ValidateSet`。
2. 非空 `ModuleId` 必须从 `governance-reading-list.v1.json` 的 `module_overlays` 动态验证；未知 key、空 overlay、缺失文件继续失败关闭。
3. 平台创建 activity bootstrap README，至少固定：模块责任、owner、allowed/protected paths、V3.0 需求 SHA-256 `838C54AE895D223E66FCA8BE8BB54D588DC3F83234B430B91073B8454E2975E6`、M0 非目标、真实触达/验证码/支付/消息/部署/生产禁止边界。
4. reading list 增加 `activity` bootstrap overlay，只引用权威活动任务单与上述平台 bootstrap README。不得要求尚未通过考试才能创建的 M0 正式产物。
5. 增加 activity 正向、unknown-module 负向、overlay 文件缺失负向，以及 life-navigation、club-alliance、health-manager 三旧模块回归测试。
6. 全量只读扫描所有模块历史 checklist 的 `module_id=null`、未知 module_id、缺失 overlay 和 core-only 完成态情况，记录工作项、record_id、路径、状态、items 数量、影响和修复建议；不得在本项中改写历史证据。
7. 已确认的第二次复发证据必须纳入审计报告：
   - network：`2026-07-12-network-canonical-owner-r1.json`，`module_id=null`、`items=26`、`completed`；
   - protection-mall：m0-r3、m1-contracts、m1-domain-evidence 三份 checklist，均为 `module_id=null`、`items=26`、`completed`。
8. 建立共享 CI gate：模块归属工作项的完成态 checklist 必须具有非空、已注册的 `module_id`，其快照必须包含对应 overlay；平台级任务只有在 registry/task order 明确标注 platform scope 时才允许 `module_id=null`。门禁必须对未来新增模块自动生效，不得再次维护模块硬编码列表。
9. 在 `recurring-issues.v1.json` 将本模式登记为第二次复发，记录系统性修复、影响扫描、预防门禁、owner 和证据路径。

## 七、验收标准

- 动态模块来源只有 reading list，不再存在第二份硬编码枚举。
- `activity` 原失败命令可以生成 pending checklist，且 `module_id=activity`。
- checklist 输入精确等于 core 加 activity overlay 去重集合，路径存在、哈希正确、初始 `checked=false`。
- `unknown-module`、缺失文件、空 overlay 明确失败。
- 三个旧模块生成行为及考试/检查单验证器回归通过。
- 全模块历史审计报告完成，明确列出 network/protection-mall 已确认的四份 core-only 完成态 checklist；发现 null 不得静默改写，应登记后续证据补强项并说明其原结论是否需要重新验收。
- 共享 CI gate 对“模块工作项 + module_id=null”失败关闭，对已注册动态 overlay 通过，对明确平台级任务保持兼容。
- `recurring-issues.v1.json` 已按第二次复发登记，系统性修复和预防证据可追溯。
- registry、合同、治理考试、实现记录、UTF-8 和 `git diff --check` 门禁通过。
- 独立测试负责人给出 Go，提交并推送；随后由平台集成负责人受控更新 activity worktree。
- 在 activity worktree 重跑原命令成功后，只允许活动负责人继续完成 current checklist，不自动授权 M0 内容或考试通过。

### 唯一关闭条件

下列十项必须同时有可追溯证据，任一缺失都不得关闭：

1. 动态模块注册，不再硬编码模块名单。
2. activity bootstrap overlay。
3. unknown、empty、missing overlay 负向测试。
4. life-navigation、club-alliance、health-manager 三旧模块回归。
5. network/protection-mall 历史影响审计。
6. 共享 CI gate 阻止模块工作项 `module_id=null`。
7. recurring issue 第二次复发登记。
8. 独立测试负责人 Go。
9. 集成提交与远端推送成功。
10. activity worktree 受控更新后，原失败命令成功生成 `module_id=activity` 的 pending checklist。

## 八、blocks / does_not_block

- `blocks`: activity current checklist、活动治理考试、活动 M0 正式内容。
- `does_not_block`: 仓库外需求整理、平台根因分析、其他不重叠模块工作；不授权业务代码或部署。

## 九、失败与回滚

不得以删除 `ModuleId`、放宽未知模块检查、预先生成 checked checklist、复制旧模块 overlay，或只修 activity 特例作为修复。不得篡改 network/protection-mall 历史完成态快照以制造合规。修复失败时保持 activity 下一门禁为 blocked，回滚平台修复提交并保留根因与测试证据。
