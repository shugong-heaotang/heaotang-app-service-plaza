# 平台 R12-L Parallel Child Activation Task Order

Platform identity: `platform scope; module_id=null`.

- work id: `AIW-20260715-PLATFORM-REGISTRY-R12L-PARALLEL-ACTIVATION`
- record id: `IR-20260715-PLATFORM-REGISTRY-R12L-PARALLEL-ACTIVATION`
- authority/base: `d7d57bdb2f9b7fc90038d92a522e56393de1f22a`
- branch: `codex/platform-registry-r12l-parallel-activation`
- worktree: `C:/Users/shugo/Documents/worktrees/heaotang-platform-registry-r12l-parallel-activation`
- developer: 平台注册表R12-L实施负责人
- reviewer: APP总架构独立验收负责人
- approver: 项目最高负责人

## Task comprehension receipt

- goal: 以单一 registry 事务登记两个 planned Social R2 child，并行激活 Legacy V2 Independent Acceptance R1 与 Platform Legacy Lifecycle Batch R2。
- non-goals: 不改变 legacy 90/91/126；不执行 Legacy 五行事务；不修改 J2、旧 Handoff、receipt、validator、业务代码或历史治理证据；不推送、不自验、不集成。
- allowed paths: registry 与本 R12-L task-order/checklist/exam/IR/Handoff 六个路径。
- dependencies: APP authority `d7d57bd...`；backend authority `091c9be...`；Legacy V2 source `d9822e1...` 与 integration `92ce89e...`。
- risks: 新旧 Social 路径重叠、跨 Git 根伪路径、reviewer 修改被验实现、记录身份与 work id 不匹配。
- stop conditions: 同门连续失败两次；任一 active scope 重叠；child worktree/base 不 clean 或不一致；身份/角色不分离；生产、真实数据、资金或五行事务。
- acceptance evidence: checklist 26/26、exam100、collaboration/delivery/total/encoding/scope/secret/diff 全绿，独立 reviewer 绑定 exact candidate。

## Child contracts

1. Social Backend R2：backend repository exact `091c9be...`，精确预留 `nova_connection_provider.go` 与 `_test.go`，状态保持 `planned`，不得写入。
2. Social Evidence R2：APP exact `d7d57bd...`，精确预留全新版本化 task-order/checklist/exam/IR/Handoff，状态保持 `planned`，禁止 registry 自写。
3. Legacy V2 Independent Acceptance R1：APP exact `d7d57bd...`，`active`，只拥有全新 review task-order/checklist/exam/evidence/Handoff；绑定 source `d9822e1...` 与 integration `92ce89e...`，禁止修改 J2、旧 Handoff、receipt 或 registry。
4. Platform Legacy Lifecycle Batch R2：APP exact `d7d57bd...`，`active`，只拥有全新 task-order/checklist/exam/IR/Handoff 与新 receipt JSON；receipt 仅可保持 `authorized-not-applied`，未来只处理证据齐全的 legacy 47/88/89/92 子集以及 Social 90 与 Backend R2 的原子切换，不执行任何事务。
5. R12-L 与两个 active child 均不计原始 23 分母，active window 至少 12 小时，开发、验收、批准角色分离。
