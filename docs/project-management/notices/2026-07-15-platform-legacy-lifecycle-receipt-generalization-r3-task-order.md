# 平台 Legacy 生命周期收据通用化 R3 任务单

平台身份：`platform scope; module_id=null`。

- work id：`AIW-20260715-PLATFORM-LEGACY-LIFECYCLE-RECEIPT-GENERALIZATION-R3`
- record id：`IR-20260715-PLATFORM-LEGACY-LIFECYCLE-RECEIPT-GENERALIZATION-R3`
- registered base：`dbfec2713542c9993508be1d69b12208dcf34edd`
- R12-M candidate：`2f4cb9d`
- current authority / implementation baseline：`d079e98ee1a4954bceb6c01eedce71371c187bd8`
- branch：`codex/platform-legacy-lifecycle-receipt-generalization-r3`
- worktree：`C:/Users/shugo/Documents/worktrees/heaotang-platform-legacy-lifecycle-receipt-generalization-r3`
- developer：平台 Legacy 收据通用化 R3 实施负责人
- reviewer：平台治理独立测试负责人
- approver：项目最高负责人

## 授权实施基线链

Row136 注册基线是 `dbfec2713542c9993508be1d69b12208dcf34edd`。R12-M candidate `2f4cb9d` 经受控集成为 `d079e98ee1a4954bceb6c01eedce71371c187bd8` 后，项目最高负责人只授权本工作树执行一次 `ff-only` 到该 authority，以读取 row136 自身激活及 row126/135 释放结果。快进成功且工作树保持 clean；该链路不是自行 re-anchor，也不授予 registry 写入、receipt 执行、push、review 或 integration 权限。

## 任务理解回执

- 目标：新增 delivery-flow policy v3 与通用 legacy receipt v2 schema；使 validator 能同时验证现有 Activity/Mall v1 收据和多个注册收据；把保留的 Batch R2 草案升级为 schema-valid 的 `authorized-not-applied` 收据。
- 非目标：不修改旧 v1 schema、Activity/Mall 收据、旧 Batch Handoff、registry 或 checklist validator；不应用任何收据，不改变 lifecycle 状态，不激活 Social R2，不部署，不访问生产、真实数据或资金。
- 兼容边界：delivery-flow policy v2 与 Activity/Mall v1 字节保持不变；v1 校验行为继续有效。v3 新增多收据注册，但当前 Batch R2 只允许 before-state 验证。
- 完整性边界：每个注册收据必须绑定 path、schema、SHA256；evidence 必须以 `git show <commit>:<path>` 的实际字节复算；blob equivalence 必须比较已注册仓库中的 exact commit/path 对象。
- 原子性边界：indices 90/132 必须作为同一 atomic group 完整出现；`audit_scope` 必须恰好由 transitions 与 omitted rows 分区，index92 只能 omitted，不能产生授权。
- 漂移边界：Batch R2 必须绑定当前 authority 的 registry bytes、逐行哈希、canonical transitions 与 projected state hash；任意当前 registry 漂移、替换收据、交叉收据重叠或部分投影均应 fail closed。
- 停止条件：同一门禁连续失败两次；范围扩大；v1 字节变化；任意 `applied=true`、post/review/integration 预填；registry 写入；部分 Social 切换；自验收或自集成。
- 验收证据：当前清单 26/26、随机治理考试 100、focused tests、总门禁、PowerShell 解析与编码、JSON/Markdown 编码、scope/secret/diff 全绿；随后只提交 exact candidate 给独立 reviewer。

## R3 收据规则

Policy v3 只能信任显式注册的收据。未注册、路径替换、schema/hash 不一致、未知版本、重复注册或跨收据重复 row 均拒绝。Batch R2 固定为 `state=authorized-not-applied`、`execution_enabled=false`、`applied=false`、`post_registry_sha256=null`、`review=null`、`integration=null`；validator 只接受 source/current before-state，不得把其 projected transitions 当作已执行事实。

Activity/Mall v1 继续承担旧 snapshot 与 checklist provenance 兼容职责。Batch R2 v2 仅提供未来事务授权证据，不覆盖或重写 v1；其 indices 47/88/89/90/132 transitions 与 omitted index92 必须共同覆盖声明的 audit scope，且 90/132 不可拆分。
