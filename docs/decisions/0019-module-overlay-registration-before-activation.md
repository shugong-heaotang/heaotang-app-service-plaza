# ADR 0019：模块 overlay 必须在生命周期激活前注册

- 状态：Accepted
- 日期：2026-07-14
- 决策者：项目最高负责人、平台集成负责人
- 问题模式：`RI-NEW-MODULE-CHECKLIST-BOOTSTRAP` 第三次复发

## 背景

第二次复发修复了 checklist generator 的硬编码模块枚举，并为 activity 增加 bootstrap overlay；但校验只在执行者主动传入 `-ModuleId` 时发生。协作 registry 仍能先把没有 overlay 的模块标记为 `active` 或 `handoff-ready`。NOVA 因此在已激活后才发现无法生成 current checklist；同一权威扫描又发现 active Protection Mall 也没有 overlay。局部补 NOVA 会让共享门禁立即因商城变红，不能构成系统修复。

## 决策

1. `contracts/foundation/governance-reading-list.v1.json` 是唯一模块治理课程注册表；不得维护第二份硬编码模块列表。
2. reading list 使用 JSON Schema，并由独立 Python validator 校验结构、非空、唯一、安全相对路径和文件存在性。
3. generator 在生成任何 checklist 前调用同一 schema/file validator；未知、空、缺失或不安全 overlay 失败关闭。
4. Service Plaza 总合同读取协作 registry。任何状态为 `active` 或 `handoff-ready`、且显式 `module_id` 不是 `platform` 的工作项，都必须已有有效 overlay；否则整个门禁失败。
5. 新工作项必须在激活交易前显式填写正确 `module_id` 并注册 overlay。历史无 `module_id` 项不在本修复中猜测归类或改写，但不得继续扩大。
6. NOVA overlay 使用正式 M1 task order 与平台 bootstrap README；Protection Mall 使用只读审计确认的模块 README、当前 M2 offline task order 和 internal dependencies v2。增加商城 overlay 不修改其业务、历史证据、状态或授权。
7. 永久负例从正式 reading list 临时删除 NOVA 或 Protection Mall overlay，并证明当前 active registry 失败关闭；正向必须验证所有注册 overlay 的 pending checklist 路径顺序和 SHA-256。

## Foundation checklist 迁移 cutoff

旧 `test_new_agent_development_checklist.py` 从 `03ab808f` 回扫时，对 implementation base `fb29b857a5476a62cc882bf6bf407e67febcacf9` 之前的完成态 foundation checklists 得到 **30 条 finding、涉及 29 个不可变历史文件**：一份 NOVA API evidence 有两条 finding，22 份 delivery-flow R2–R19/R21–R24 与 6 份 registry-dispatch 证据使用了后来才固定的 task-order短语或旧 record-id 映射。

这些历史文件已经通过各自当时的 checklist/exam/IR 生命周期且不在本项 allowed paths；回写会破坏不可变证据，不能作为本项修复。故 `fb29b857...` 是一次性 migration cutoff：保留旧字节与审计 finding，不追认其满足新短语，也不把 cutoff 推到更晚提交。cutoff 后新增或修改的 foundation completed checklist 必须由 registry allowed path、平台 owner role 和明确写有 `platform scope`、`module_id=null` 的 task order 同时证明；合成永久负例保证缺任一证据仍失败。

## 全依赖审计结论

- reading list 当前共有6个 overlay：life-navigation、club-alliance、health-manager、activity、nova、protection-mall。
- 当前显式模块 lifecycle 中 activity、NOVA、Protection Mall 均为 active；补齐后共享 validator 正向通过。
- 模块 checklist 共67份，66份 completed；仍只有既有4份 completed/null/core-only 历史例外（network 1、Protection Mall 3），SHA 与集合由既有永久门禁锁定。
- 未显式 `module_id` 的历史 active/handoff-ready 项保持可见风险；后续派发必须补字段，但本项不拥有 registry，不能替其改写。

## 后果与回滚

正面结果是错误生命周期状态在模块实现开始前被机器拒绝，并且新增模块只需注册一个 overlay。代价是 registry 与 reading list 必须在受控激活交易中保持原子顺序。

若 validator 或总合同出现错误，回退本候选 schema、validator、reading-list、generator 和总合同变更；NOVA 与受影响新模块保持 No-Go。禁止通过移除总合同调用、把状态改回 planned 以外的伪装、推迟 cutoff 或删除负例换取绿色。

## 可证伪前提

- 所有新模块派发都会提供显式非平台 `module_id`；若 registry 允许持续省略，该门禁无法识别模块，必须升级 registry schema/dispatcher，而不是在 validator 猜工作项名称。
- overlay 输入在切片入口期间是稳定课程；若输出本身必须修改 overlay，执行 ADR 0014/既有 R2 current snapshot 流程。
- reading list 和 registry 继续由受控平台工作项维护；若迁移到外部服务，需要保留等价的原子激活与审计证据。
