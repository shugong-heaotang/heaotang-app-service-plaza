# 新模块治理冷启动历史影响审计（2026-07-13）

## 审计结论

全量只读扫描 `contracts/modules/*/development-checklists/*.json` 后，发现且仅发现四份完成态模块检查单使用 `module_id=null`。四份均只有 26 项 core 输入，没有模块 overlay。历史文件保持原字节，不在本工作项中改写。

这四份证据能够证明当时完成了 core 治理阅读和考试，但不能证明执行者读取了所属模块 overlay。因此原有业务或合同结论不自动撤销，也不能继续把它们当作“模块治理输入完整”的证据；对应模块下一次实质切片必须使用已注册的非空 `module_id` 重新认证，必要时由独立验收人决定是否补做原切片复验。

## 已确认影响

| 模块 | 工作记录 | 检查单路径 | 状态 | module_id | items | 影响与建议 |
| --- | --- | --- | --- | --- | ---: | --- |
| network | `IR-20260712-NETWORK-CANONICAL-OWNER-DECISION-R1` | `contracts/modules/network/development-checklists/2026-07-12-network-canonical-owner-r1.json` | completed | null | 26 | canonical owner 决策保留；后续人脉实质切片必须在注册 network overlay 后重新认证，独立评估是否补验原裁决。 |
| protection-mall | `IR-20260712-PROTECTION-MALL-M0-R3-CORRECTION` | `contracts/modules/protection-mall/development-checklists/2026-07-12-protection-mall-m0-r3-correction.json` | completed | null | 26 | M0 R3 历史结论保留但模块治理证据不完整；后续商城切片不得复用。 |
| protection-mall | `IR-20260712-PROTECTION-MALL-M1-CONTRACTS` | `contracts/modules/protection-mall/development-checklists/2026-07-12-protection-mall-m1-contracts.json` | completed | null | 26 | M1 合同结论不自动撤销；需要在下一次合同变更前建立 protection-mall overlay 并重新认证。 |
| protection-mall | `IR-20260712-PROTECTION-MALL-M1-DOMAIN-EVIDENCE` | `contracts/modules/protection-mall/development-checklists/2026-07-12-protection-mall-m1-domain-evidence.json` | completed | null | 26 | 跨仓领域证据保留；不再作为未来模块起飞依据。 |

## 其他扫描结果

- 非空 `module_id` 的完成态模块检查单均能在当前 `governance-reading-list.v1.json` 找到注册项。
- 已注册模块的完成态检查单均包含其对应 overlay，没有发现未知 module_id 或缺失 overlay 输入。
- 平台级检查单位于 `contracts/foundation/development-checklists/`，允许 `module_id=null`；其平台范围仍由 registry/task order 和受保护路径共同证明。
- 未发现除上表四份之外的模块目录 core-only 完成态检查单。

## 预防门禁

`scripts/tests/test_new_agent_development_checklist.py` 现在执行以下共享规则：

1. 新增模块从 reading list 动态注册，不再维护第二份硬编码名单。
2. 模块目录下完成态检查单必须设置非空、已注册的 `module_id`。
3. 其 items 必须包含对应 overlay。
4. 上表四份历史例外同时固定精确路径、SHA-256、`completed/null` 身份和 26 项 core-only 顺序；例外集合或字节被静默改写都会使测试失败。
5. R2 全依赖审计发现旧 R1 基线 `03ab808f4a21f8a9585ed8aeefeb55e98c5434af` 会把后来形成但早于本修复授权基线的不可变历史证据按新短语回扫为30条 finding。ADR 0019 将本项 implementation base `fb29b857a5476a62cc882bf6bf407e67febcacf9` 固定为一次性 migration cutoff；此后新增到 foundation 的完成态 checklist 必须能关联 registry 中的平台工作项、被 allowed paths 授权，并由 `module_id=platform`、`# 平台`任务单和匹配 work_id证明结构化平台身份；旧英文固定标记仅兼容。cutoff 不得再向后推；模块工作项把 null checklist 放入 foundation 仍失败关闭。

## 后续责任

- 平台集成负责人维护动态 reading list 与共享门禁。
- Network 负责人在下一实质切片前补建模块 bootstrap overlay；Protection Mall 的最小 overlay 已由 R2 平台治理项基于现存三份只读权威输入注册，不修改商城业务或历史证据。
- 独立验收负责人根据原切片风险决定是否追加复验，不允许改写历史 checklist 制造合规。

## R2 第三次复发全依赖审计（2026-07-14）

### exact symptom / exact stop

`AIW-20260712-NOVA-PHASE5-M1-RUNTIME` 已在本地权威 registry 中为 `active` 且 `module_id=nova`，但 reading list 无 `nova`，因此 `New-AgentDevelopmentChecklist.ps1 -ModuleId nova` 在创建 current checklist 前失败。扫描同一生命周期集合又发现 `AIW-20260713-PROTECTION-MALL-M2-CATALOG-SOLUTION` 为 `active/module_id=protection-mall`，reading list 同样无 overlay。只补 NOVA 会让共享全量门禁在商城处立即失败，属于局部假绿。

### causal chain

1. 因为 R1 只在 generator 收到显式 `ModuleId` 时查 reading list，所以 registry 激活交易不依赖 overlay 完整性。
2. 因为 registry 可以先进入 `active/handoff-ready`，所以执行者直到生成 checklist 才发现课程缺失。
3. 因为共享总合同不扫描 lifecycle 模块，所以另一个 active 模块缺 overlay 没有阻止激活。
4. 最早可控原因是“激活前缺少 registry → reading-list 的机器门禁”；R2 在这里修复，而不是只加 NOVA key。

### 全量事实

- reading list：6个 overlay，分别为 life-navigation(5)、club-alliance(2)、health-manager(2)、activity(2)、nova(2)、protection-mall(3)。
- 显式非平台 active/handoff-ready 工作项：activity 1、Protection Mall 1、NOVA 2；正式 reading list 均已有非空 overlay。
- `contracts/modules/*/development-checklists/*.json`：67份，66份 completed；completed/null 仍恰好为上表4份，未增加 legacy exception。
- Foundation migration inventory：从旧 `03ab808f` 到 `fb29b857` 有32份 completed foundation checklist；其中29份旧文件产生30条新规则 finding（一份 NOVA API evidence 同时缺 allowed-path 与固定 task-order短语）。这些字节不在本项授权范围且属于历史快照，保留 finding、不追认新规则、不回写；cutoff 后合成负例继续证明新违规会失败。
- Central authority 首次临时集成：`ea3c70c8...` 无合并冲突，reading-list registry gate通过；cutoff 后 R7 暴露“结构化平台身份齐全但固定英文短语缺失”的单一测试问题。修复验证结构化 registry/task-order事实且未移动cutoff，模块伪装负例继续失败。

### Overlay 只读审计

| 模块 | 路径 | SHA-256 | 语义结论 |
| --- | --- | --- | --- |
| nova | `docs/project-management/notices/2026-07-12-nova-m1-task-order.md` | `ae285cbebc0ecc0c1750e2b70e95db83f1e1d693c57f56260daaa1003320885e` | 正式Phase 5 M1目标、责任、M0认证、M1–M4门禁和生产禁止边界。 |
| nova | `docs/project-management/notices/2026-07-13-nova-phase5-m1-bootstrap-readme.md` | `1ee4d35ca2b22fa09ce42a2c4cf225a9f5dcbf8a2087d235d6cd23f23bdd86e2` | 平台稳定bootstrap；明确APP基线缺少模块正式依赖产物，不能伪写development Go。 |
| protection-mall | `docs/project-management/modules/protection-mall/README.md` | `b6b3e72f5731c7e30bdca13d2b784ae43c5f1a11349a0509f0e8f12c33ada7a4` | 模块身份、接口、非目标和上线/支付边界存在；“当前M0”状态已过时，不能单独作为当前状态证据。 |
| protection-mall | `docs/project-management/notices/2026-07-13-protection-mall-m2-offline-task-order.md` | `407911df84b91c00fabf1e7dd2b9fe6f47de4280b8704fbeabd69f74dc01fd62` | 当前M2目录切片、路径、离线范围与统一No-Go。 |
| protection-mall | `contracts/modules/protection-mall/internal-dependencies.v2.json` | `f8f329a71968efce7a118341088027edc886067ee420c1432c38a7fb4f881a01` | governance=go、development=partial-go、acceptance/release/operations=no-go；支付和上线继续阻塞。 |

Protection Mall 三项来源取自未集成候选 `e1c4020fc3757700818ea15882a286d1ca5e7018` 的只读线索，但逐文件以当前 `fb29b857` 工作树重新核对；未合并其 registry、证据或状态提交。

### blocks / does_not_block / rollback

- blocks：NOVA 新 current checklist、考试、IR/Handoff 与 synthetic E2E 后续治理闭环。
- does_not_block：NOVA 既有28项离线回归、商城既有候选保存、Activity 与其他无重叠切片。
- rollback：回退 R2 reading-list/schema/validator/generator/总合同和治理记录；保持 NOVA No-Go。不得删除 Mall 负例、推迟 cutoff、改写历史 checklist 或关闭总门禁换绿色。
