# 平台 R12-K Registry Current-Clock and Overlay Unblock Task Order

Platform identity: `platform scope; module_id=null`.

- work id: `AIW-20260715-PLATFORM-REGISTRY-R12K-SOCIAL-OVERLAY-UNBLOCK`
- record id: `IR-20260715-PLATFORM-REGISTRY-R12K-SOCIAL-OVERLAY-UNBLOCK`
- authority/base: `92ce89eab132ef5326f49de3fa3e619f1b949fb2`
- branch: `codex/platform-registry-r12k-social-overlay-unblock`
- worktree: `C:/Users/shugo/Documents/worktrees/heaotang-platform-registry-r12k-social-overlay-unblock`
- developer: 平台注册表R12-K实施负责人
- reviewer: APP 总架构独立验收负责人
- approver: 项目最高负责人

## Task comprehension receipt

- goal: 形成一个最小、原子的 registry 候选，先消除 fresh Overlay No-Go 已取代的共享路径占用，并在当前时钟下保持全部 18:30 非终态行真实有效。
- non-goals: 不执行 Legacy 五行事务；不修改业务、validator、schema、历史 checklist/exam；不伪造独立验收、response、reviewed_at 或集成事实；不部署、不推送、不自验、不自集成。
- allowed paths: `contracts/foundation/agent-collaboration.v1.json` 与本 R12-K 的 task-order、checklist、exam、IR、Handoff 六类文件。
- dependencies: APP authority exact `92ce89e...`、fresh Overlay No-Go exact `d09d5d0...`、Delivery Flow V2 门禁、独立 reviewer 后续复验。
- risks: 错误终态化、共享路径仍重叠、跨过 status expiry、把聊天结论伪装成文件证据。
- stop conditions: 任一同门连续失败两次；证据不足以合法终态化；出现未授权路径；registry 与 Git authority 不一致。
- acceptance evidence: current checklist 26/26、exam 100、collaboration/delivery/aggregate/encoding/diff/scope/secret 全绿、独立 reviewer 对 exact candidate 的结论。

## Atomic transaction

1. `index 119` 与 `index 125`：依据已入 authority 的 fresh Overlay No-Go `d09d5d0...` 真实取消，清空非终态计时/交接字段并释放共享路径；不写独立 Go。
2. `index 109/111/117/123`：保持真实非终态，仅刷新 `updated_at`、`target_date`、`next_checkpoint`、`status_expires_at` 与必要阻塞说明。
3. `index 126`：只有在 authority 内存在 file-backed independent Go path/SHA/reviewed_at 时才可 `integrated`；否则保持 `active` 并 current-clock 刷新，明确证据缺口。
4. Social Backend R2 与 Evidence R2：仅在既有行/路径/工作树证据可合法换绑且无 active/handoff-ready 路径冲突时登记或激活；否则不得扩大事务，先交付 Overlay 解除与 current-clock 最小候选。
5. receipt `LLM-20260715-ACTIVITY-MALL-M2-R1` 保持 `authorized-not-applied`，五个 legacy status 不变。

## Checkpoints

1. Preflight、全新 checklist、exam 100。
2. 精确证据扫描与冲突判定。
3. 单一 registry 原子编辑及永久门禁。
4. IR/Handoff、diff/security/scope、单提交后停止，交独立 reviewer。
