# Project Brain 分叉集成与 R5 治理证据收口

## Identity

- pattern_id：`PROJECT-BRAIN-AUTHORITY-LINEAGE-SPLIT`
- owner：平台集成负责人
- affected checkpoint：Project Brain M1-R4 / 最终受控集成
- authoritative base：`806252f33d7ef283ab44ef63c2a9569057589cd7`
- Project Brain source：`815383e4189a12045db11c4c3f10a0859ba07b2e`

## Evidence

- 远端权威 integration 已包含治理考试 retry R5 与健康 HM-R0 激活；本地 `7a3f254b` 是从旧 `8110af6` 演进的未推送集成链。
- `7a3f254b` 同时混有 Project Brain 与商城提交，且 retry registry 状态来自已 No-Go 的旧 R3，禁止整链推送。
- Project Brain 正式分支 `815383e` 已包含 M1-M4、自动化、浏览器验收和 handoff-ready 证据，可作为单独 source 受控合并。
- 模块工作树与旧 integration 工作树存在两组不同 SHA 的未跟踪 R4 文件；项目负责人、实施 Agent 和独立验收线程均否认创建，真实 owner 为 Unknown，因此两组只保全、不采用、不提交。
- 旧 M1-R3 attempt 2 在新 retry R5 Schema 下缺少 previous path/SHA、presentation 和 confirmation 证据；其原始字节及对应 IR 移入 invalidated snapshot，不回写为通过。

## Causal chain

1. Project Brain 在旧 integration 基线上继续完成 M2-M4，而平台同时在另一条远端权威线修复共享治理 retry，因此形成两个合法但分叉的后继。
2. 后续本地集成把 Project Brain 与商城一起合并，并错误继承旧 retry integrated 状态，因此该本地 HEAD 不能作为远端权威直接推送。
3. R4 执行令基于过期 HEAD/clean 假设，两个无登记 owner 的执行通道又分别生成 R4 中间文件，因此 preflight 正确停止。
4. 最早可控根因是平台没有在每次受控集成前重新核验 remote HEAD、registry owner 和 dirty worktree，并缺少单模块 source 合并与共享治理演进的串行协调。

## Resolution

- 不触碰两处原脏工作树，不删除未知 R4。
- 从远端权威 `806252f` 建立专用 reconciliation 工作树。
- 只合并 Project Brain source `815383e`，不合并本地 `7a3f254` 整链，不夹带商城。
- registry 冲突以远端权威 R5/健康状态为基础，Project Brain 最终状态在验收后单独写入。
- 旧 R3 retry attempt 2 与关联 IR 以原字节迁入 invalidated snapshots。
- 在合并后当前治理输入上新建 `IR-20260712-PROJECT-BRAIN-V1-M1-R4-CONTROLLED`，首试 100，不制造 retry。

## Prevention

- 受控集成前必须同时记录 remote HEAD、source HEAD、merge-base、dirty 状态、registry owner 和 allowed paths。
- 不允许从混合多个模块的未推送本地 integration HEAD 直接更新远端。
- 未跟踪治理证据只有 owner/work item/allowed path 三者一致才可采用。
- 共享 Schema 升级后，旧证据失败时保持原字节并显式 invalidated；不得修改旧试卷以适配新 Schema。

## Verdict

- 当前：Pass。freshness 修订 `df67d2a` 已获独立 Go 并进入远端权威 integration；registry 已按真实证据收口。
- does_not_block：健康 HM-R0 F0 只读复核；不冲突模块继续工作。
- No-Go：生产发布、未知 R4 候选采用、商城提交夹带。
