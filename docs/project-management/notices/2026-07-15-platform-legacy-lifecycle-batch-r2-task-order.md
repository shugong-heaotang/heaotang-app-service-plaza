# 平台 Legacy Lifecycle Batch R2 Receipt Task Order

Platform identity: `platform scope; module_id=null`.

- work id: `AIW-20260715-PLATFORM-LEGACY-LIFECYCLE-BATCH-R2`
- record id: `IR-20260715-PLATFORM-LEGACY-LIFECYCLE-BATCH-R2`
- registered base: `d7d57bdb2f9b7fc90038d92a522e56393de1f22a`
- current authority: `05bbf6465edecaa97af5d82792db868ece4f42e8`
- branch: `codex/platform-legacy-lifecycle-batch-r2`
- worktree: `C:/Users/shugo/Documents/worktrees/heaotang-platform-legacy-lifecycle-batch-r2`
- developer: 平台Legacy批次R2实施负责人
- reviewer: 平台治理独立测试负责人
- approver: 项目最高负责人

## Authorized implementation-base chain

Row135 注册基线是 `d7d57bdb2f9b7fc90038d92a522e56393de1f22a`。R12-L candidate `8f8f2f6e90ec11610ff73562979c64c3acbaabfe` 经受控集成为 `05bbf6465edecaa97af5d82792db868ece4f42e8` 后，项目最高负责人明确授权本工作树执行 `ff-only` 到 `05bbf646...`，以读取包含 row135 自身激活信息的 authority。实施基线因此是 `05bbf646...`；fast-forward 后分支仍为 `codex/platform-legacy-lifecycle-batch-r2` 且工作树 clean。该链路不得被解释为擅自 re-anchor。

## Task comprehension receipt

- goal: 在发现现有 schema 不能覆盖本批次后，仅准备一个 `draft-not-registered` 的固定事务设计候选，供后续获权通用化 schema/validator 时复核；设计保留证据齐全的 legacy 技术行投影，并绑定 Social index90 `active -> cancelled` 与 child132 `planned -> active` 的同一未来事务。
- non-goals: 不执行任何 registry 状态变化；不预填 review/integration/post registry；不修改 registry、validator、scripts、旧 receipt、J2 或 Activity/Mall 五行事务；不访问生产、真实数据或资金。
- allowed paths: 本 task-order、全新 checklist/exam/IR/Handoff 与唯一新 receipt JSON。
- dependencies: APP authority `05bbf64...`、registered base `d7d57bd...`、现有 evidence Git objects；`legacy-lifecycle-migration.v1.schema.json` 仅作为结构参考，因为其 receipt id、五行集合、hash 与最大 index 均固定为 Activity/Mall R1，不能合法校验本 Batch R2，也不得在本工作项内修改。
- risks: 把 No-Go 当 Go、猜测旧行 exact、拆分 Social 原子切换、把未注册 JSON 冒充 receipt 或授权、引用可变 current 文件而未绑定 SHA。
- stop conditions: 任一旧行证据链不完整；source/current row hash 不可复算；同一门失败两次；范围扩大；任何实际状态变化或自验集成。
- acceptance evidence: current checklist 26/26、exam100、receipt 自身哈希/证据路径验证、focused/total/encoding/scope/secret/diff 全绿、独立 reviewer 绑定 exact candidate；不得把 Activity/Mall 专用 schema 的预期拒绝误报为本 receipt 的失败或通过。

## Receipt rule

逐行审计 legacy indices 47/88/89/92。只有 source exact、current row hash、投影依据与 evidence path/SHA 全部可证明的行才可纳入设计；证据不足即剔除并在 Handoff 报告。Social indices 90/132 必须成对出现，设计始终 `state=draft-not-registered`、`executable=false`、`applied=false`、`post_registry_sha256=null`、`review=null`、`integration=null`，不得称为 `authorized-not-applied` receipt。

本候选只固定未来事务，不把新 receipt 注册到当前 delivery policy。未来执行前必须由新的独立工作项获权扩展 schema/validator/policy 并重新核验当时 registry；本工作项不得绕过该前置条件。
