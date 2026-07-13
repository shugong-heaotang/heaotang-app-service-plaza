# 平台交付流优化 Handoff

## 当前结论

- 状态：R4、R6、R8、候选 dadcc42 与候选 71889d4 的 independent review 均为 No-Go 且保持不可覆盖；R15 正在关闭 registry 新鲜度和非 Git repository_root fail-closed 永久回归，完成后进入第三次独立复验
- 主因：业务工作被拆成多个长期并行治理项，Handoff 缺少决策时限，范围内下一检查点仍反复等待授权，平台集成负责人形成单点队列；原 R2 又只优化技术流，没有约束客户价值和商业结果。
- 处置：同步权威 HEAD `094bafdbba48c84f41611ca541c8225e4de4a8dd`，升级 `delivery-flow-policy.v1`、机器校验和商业价值门禁。

## 任务理解回执

- goal：减少重复等待和平台单点排队，同时保持根因、权限、安全和独立验收门禁。
- non-goals：不修改业务代码，不直接暂停或覆盖其他负责人正在执行的隔离工作，不授权生产、真实数据或资金操作。
- allowed paths：协作登记及 Schema、delivery flow policy、校验脚本与测试、任务书、状态、检查单、考试、实施记录和本 Handoff。
- risks：错误计算 WIP 会误停工作；自动续跑若跨越风险边界会扩大权限；遗留状态若强行补造会污染历史。
- stop conditions：路径重叠、权限扩大、生产或真实数据、不可逆操作、独立验收失败。
- developer / reviewer / approver：平台治理实施负责人 / APP 总架构独立验收负责人 / 项目最高负责人。
- acceptance evidence：Schema、语义校验、负向单测、总治理门禁、UTF-8、Git diff 和独立验收结论。

## 生效规则

1. 同时最多三个唯一业务主线；每个模块最多一个。当前遗留工作进入 drain mode，不强制中断，但在降到上限前禁止激活新业务主线。
2. 一个业务结果只保留一个总工作项；实现、证据、测试和验收是该工作项的检查点。跨仓库只允许 supporting-checkpoint，不重复计算业务 WIP。
3. 检查点证据通过、范围和风险未扩大、工作树归属清楚且无停止条件时自动续跑。
4. 生产、真实资金、真实健康/会员数据、不可逆变更、权限扩大、安全/法律升级或独立验收失败必须停止并重新授权。
5. `handoff-ready` 必须指定下一责任人；4 小时没有首次响应即提醒，24 小时没有结论自动升级项目最高负责人。
6. 完成必须同时具备业务流恢复和独立验收；提交、文档、测试自述均不能单独关闭工作。
7. 新业务主线在激活前必须写清客户、问题、价值事件、指标目标、测量窗口、端到端负责人、商业假设、停止条件和端到端旅程。

## 商业与流程审计结论

1. 旧计划把跨模块主链路放在全部板块完成后，反馈过晚，容易形成“大量合同已完成、商业闭环仍未验证”。调整为每个业务主线从首个检查点就带一个合成端到端价值事件。
2. Nova 的后端实现、跨仓证据和迁移演练被登记成多个并行活动项；下个检查点必须迁移为一个业务主线加 supporting checkpoints，不再重复计算业务 WIP。
3. 活动已经具备“需求—匹配—报名—俱乐部承接—交易/履约”的天然价值链，商城正在建设目录与责任主体，因此首个跨板块试点选定为“活动 → 俱乐部 → 商城”的合成无资金闭环。
4. 俱乐部当前验收重点是页面身份与状态，但商业上还缺少“加入后获得什么持续价值”的指标；在下一业务切片激活前必须定义会员价值事件和留存/复访代理指标。
5. 健康和生命导航当前大量工作停留在文档、合同或待裁决状态；后续不得仅以文档数量推进，必须绑定可验证的用户结果，同时继续保持医疗、隐私和真实数据 No-Go。

## 首个跨板块价值流

客户提出活动需求，活动模块完成授权检索和匹配，俱乐部承担主办/审批责任，商城只引用责任主体明确的目录条目并形成无资金履约意向。成功标准为：关键合成旅程全部通过，越权、重复归因、责任主体缺失、快照变异和真实资金调用全部为零。

## R4 独立验收结论（不可覆盖）

- 结论：No-Go；没有 P0，有六类 P1 制度缺口。
- 缺口：新增工作项可不声明政策而绕过；过期只与 `updated_at` 比较而不与验证时钟比较；Handoff 下一责任人与 4/24 小时 SLA 未机器执行；WIP 和重复主线未合并计算 `active` 与 `handoff-ready`；`integrated` 可缺失指标、价值事件、独立验收和集成提交；负向测试缺少角色分离、模块 WIP 与缺失流字段回归。
- 处置：保留原提交及 No-Go 证据，另建 R5 候选；未经新的独立 Go 不集成。

## R6 独立验收结论（不可覆盖）

- 验收对象：`0f339656ba15e861971edaed3a157e461256c3c1`；结论 No-Go，不允许受控集成；P0 为零。
- 已通过：当前时钟失效、next owner 与 4/24 小时核心 SLA、`active + handoff-ready` 合并 WIP、角色分离/模块 WIP/缺字段负向测试。
- P1：候选未包含当时最新权威 `f5546f25…`；遗留状态哈希可在同一政策中重算自证；integrated 的证据路径、Git 提交、验收人和指标达标均可伪造。
- P2：`escalated_at` 已建模但未证明逾期实际升级。
- R7 处置：合并 `f5546f25…`；Schema 常量锚定遗留摘要；校验证据路径存在、提交存在及祖先关系、验收角色匹配、结构化指标达标、升级对象和升级时间。

## R8 独立验收结论（不可覆盖）

- 验收对象：`3f6b1b03eef1e9fb2b010c364d13da4430a2a811`；结论 No-Go，不允许受控集成；P0 为零。
- 已通过：权威新鲜度、工作树、伪造路径与 SHA、假 Git 提交、祖先关系、未登记验收人、指标未达标、Handoff 升级证据、WIP、实时过期、角色分离、R8 current 认证和全仓门禁。
- P1：Schema 常量仍与候选处于同一修改边界；同时修改遗留状态、政策哈希和 Schema const 后验证返回空错误。
- R9 处置：验证器直接从不可变 Git 对象 `33f5e45499fbadaac71f07bbe6de5d72579e39c9` 读取 `contracts/foundation/agent-collaboration.v1.json` 的遗留 `work_id + status` 前缀逐项比较；三联篡改负向测试必须失败。

## 迁移

旧工作项不补造历史字段。以 `AIW-20260713-PROTECTION-MALL-M2-PORTS-SIMULATION` 为遗留切换点，切换点以前的 115 个 work_id 顺序与 `work_id + status` 状态快照分别由 SHA-256 固化；任何插入、删除、重排或未迁移状态变化都会失败。切换点后的全部新工作项必须声明 `flow_policy_version` 并具备完整流字段。

## 验证

- Policy Schema：通过
- 语义校验：通过
- 单元测试：20/20 通过（1 个当前正例、19 个负向/边界回归）
- 协作登记：通过，并已自动串联 delivery flow gate
- Service Plaza 总合同：通过
- UTF-8：待 R5 最终验证
- Git diff：通过
- R2 独立验收：No-Go（落后权威基线且缺少商业价值门禁）
- R3 入口检查单：26/26；治理考试 100
- R4 最终 current 检查单：26/26；治理考试 100
- R4 独立验收：No-Go，结论已保留
- R5 入口检查单：26/26；治理考试 100
- R6 最终 current 检查单：26/26；治理考试 100
- R6 独立复验：No-Go，结论已保留
- R7 入口检查单：26/26；治理考试 100
- R8 最终 current 检查单：26/26；治理考试 100
- R8 独立复验：No-Go，结论已保留
- R9 入口检查单：26/26；治理考试 100
- R10 最终 current 检查单：26/26；治理考试 100
- R10 独立复验：待新候选 exact commit 后执行

## 组织阻滞清障记录

- 阻滞等级：L2 跨单元。
- 被阻滞结果：跨板块开发不能稳定转化为可验证的客户和商业价值。
- 因果链：并行工作项过多 → 证据与实现拆成长期活动项 → 平台 Handoff/授权排队 → 缺少端到端价值指标和唯一决策人。
- 原业务负责人：各业务主线负责人；清障负责人：平台集成负责人；决策负责人：项目最高负责人；独立验收：APP 总架构独立验收负责人。
- 最小恢复动作：集成流政策，活动与商城先迁入商业价值门禁，按合成跨板块价值事件推进。
- 首次响应期限：4 小时；决策期限：24 小时；逾期升级项目最高负责人。
- 验证标准：原来等待授权的范围内下一检查点能自动续跑；活动—俱乐部—商城合成价值流可重放；没有人工特批、真实资金、真实数据或生产绕行。
- 防复发：新业务主线缺少价值字段、WIP 超限、同模块多主线、角色未分离或状态过期时机器门禁失败；2026-07-14 复查迁移和首个价值流证据。

## R11 P0 治理检查点

### 根因与处置

- Activity V3 M0 登记的 base_commit=485601ce10ad4d3ac7d9db655465754ad5ac0032 不存在于 APP repository_root 的 Git 对象库；原始可追溯基线修正为 485601cb4b40025ce5b96fc746b9996bbf80250d。
- Activity 恢复基线没有冒充原始基线，继续以 reactivation_base=5d6d22b51b65abf87a5f7c9b9bdd419ce04dfd40 保存在 migration note。
- validate_agent_collaboration.py 现在对 active 与 handoff-ready 项逐项调用其自身 repository_root 的 Git 对象库；不能再假设 validator 当前仓库就是工作项仓库。
- planned、cancelled 和不可变 legacy 行保留为元数据，不因本地对象库被清理而被误拒绝；激活或进入 Handoff 时自动转入强制对象检查。
- 新增 planned AIW-20260713-PLATFORM-NOVA-OVERLAY-R2，base 为 59263f7e9717907bdc3953e752ad1a8fd3f2789a，完整声明 delivery-flow 字段。实施 Agent 的 allowed paths 明确不包含 agent-collaboration.v1.json，registry 仍由平台集成负责人所有。

### 测试与边界

- 新增 5 项 validator 单测：跨仓正确对象、对象只存在于错误仓库、handoff-ready 缺对象、planned/cancelled legacy 豁免、repository_root 缺失。
- 新增单测：5/5 通过。
- delivery-flow 回归：20/20 通过。
- 协作 registry 与串联 delivery-flow gate：通过。
- Service Plaza 总合同：通过。
- UTF-8：1350 文件通过。
- R11 入口检查单：26/26；治理考试 attempt 1 为 100 分。
- R11 修改治理核心输入后不改写历史清单/试卷；按 RI-CURRENT-CHECKLIST-MUTABLE-OVERLAY 规则另建最终 current 认证。
- 未修改业务代码、生产、真实数据、真实资金、部署或不可逆状态。

### Handoff

- developer：平台治理实施负责人。
- independent reviewer：APP 总架构独立验收负责人。
- verdict：候选测试 Go；集成保持 Pending，必须绑定推送后的 exact commit 独立复验。
- next gate：最终 current checklist/exam 100，IR、diff/secret 复核、commit/push，随后独立验收；实施负责人不得自行集成。

## dadcc42 独立验收 No-Go 与 R13 整改

### 不可覆盖结论

- 验收对象：dadcc42c76e1dbc008d13780a19d248d11c54fb6。
- 结论：No-Go，禁止集成。
- P0-1：新增 scripts/tests/test_validate_agent_collaboration.py 不在父提交既有 allowed paths；同提交向 registry 添加自身路径不能追溯授权该提交。
- P0-2：planned NOVA overlay R2 的 owner、title、business stream、next checkpoint、阻塞范围和 allowed paths 未逐字段采用平台负责人原案。

### R13 根因整改

- 从累计候选差异中删除越权新增测试文件，也删除 delivery-flow 工作项对该文件的同提交自增授权。
- 5 个 base commit 负向/边界测试迁入父提交已经授权的 scripts/tests/test_validate_delivery_flow_policy.py。
- NOVA R2 按平台负责人建议修正 owner、title、business_stream_id、next_checkpoint、blocks、does_not_block 和完整 allowed paths。
- NOVA R2 实施范围不包含 registry；registry 的登记与未来状态切换继续由当前 delivery-flow owner 执行。
- 后续共享 overlay 完整性门禁必须扫描所有 active 模块，并同时发现 active Protection Mall 缺 overlay；只让 NOVA 通过仍属失败。
- R13 入口检查单：26/26；考试 attempt 1：100 分。
- 下一门禁：R13 IR、R14 最终 current 认证、25 项回归、总合同、UTF-8、范围/diff/secret、提交推送及第二次独立验收。

## R14 最终 current 认证与候选交接

- R14 checklist：26/26 current 哈希一致；精确 attestation 已通过总合同校验。
- R14 governance exam：attempt 1，100 分；exam 与修正后的 checklist SHA-256 一致。
- 跨仓 base commit 与 delivery-flow 回归：25/25 通过。
- `validate_agent_collaboration.py`、`validate_delivery_flow_policy.py`、implementation-record validator：全部通过。
- Service Plaza 总合同：通过；UTF-8：1359 个文件通过。
- 累计候选不再包含 `scripts/tests/test_validate_agent_collaboration.py`；5 个 base commit 负例已位于父提交授权的 `scripts/tests/test_validate_delivery_flow_policy.py`。
- NOVA overlay R2：平台建议字段已逐项采用，allowed paths 为 17 项，且实施 Agent 不拥有 registry。
- verdict：候选具备提交与推送条件；`dadcc42` 继续禁止集成，新候选仍为 Pending，必须由 APP 总架构独立验收负责人绑定远端 exact commit 复验。

## 71889d4 第二次独立验收 No-Go 与 R15 整改

- 验收对象：`71889d44b2243b6c715335a47a4c3d0e17a18c3a`。
- 结论：No-Go，禁止集成；R13/R14 已关闭项保持有效且不得回退。
- P1：registry 的 `next_checkpoint` 仍描述已经完成的 R14 和推送动作；现已刷新为“第三次独立复验与受控集成”，并同步 `updated_at`。
- P2：原 25 项回归未永久覆盖“repository_root 路径存在但不是 Git 仓库”；新增 fail-closed 负例，要求 active 工作项产生包含 `not a git repository` 的明确错误。
- R15 入口检查单：26/26；治理考试 attempt 1：100 分。
- 下一门禁：26 项回归、R16 最终 current 认证、IR、validators、总合同、UTF-8、范围/diff/secret、提交推送及第三次独立验收。

### R16 最终 current 认证

- R16 checklist：26/26 current；governance exam attempt 1：100 分。
- 累计回归：26/26；新增非 Git repository_root 负例真实执行并通过。
- registry 只描述剩余的第三次独立复验与受控集成，不再重复已完成的 R14/推送动作。
- verdict：整改候选具备提交推送条件；提交后保持 Pending，实施负责人不自行集成。
