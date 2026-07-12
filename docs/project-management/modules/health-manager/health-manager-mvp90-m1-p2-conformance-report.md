# 健康大管家 MVP-90 M1 P2 Conformance Report

## P2-C1 结论

当前结论：`P2-C1 Go / P2-C2 Exact revision corrected candidate ready for independent review`。

| 检查项 | 结果 |
| --- | --- |
| replay plan Draft 2020-12 Schema | PASS |
| 场景 exact set | 15/15 PASS |
| fixture 唯一与索引闭包 | 15/15 PASS |
| A001 完整步骤覆盖 | 10/10 PASS |
| 全局状态机覆盖 | 6/6 PASS |
| 事件总数与唯一性 | 25/25；event/key/payload 全局唯一 |
| 授权 action actor/resource/effect/prerequisite | 逐事件 PASS |
| scenario/fixture pointer 真实解引用 | 15/15 PASS |
| 同资源状态与版本连续性 | PASS |
| A001 normal profile | task recorded；RiskEvent/HumanHandoff=0 |
| A003 emergency profile | triage_pending→emergency；professional actor |
| fixture expected_result / signed safe outcome | 15/15 PASS |
| Schema 与闭包负向变异 | extra/duplicate/wrong-pointer/wrong-action-resource 全部 REJECT |
| synthetic/executable | true / false |

## 已验证边界

测试只读取仓库内版本化 JSON，未运行 reference runner，未访问网络、数据库、系统时间、随机数、浏览器、真实身份或真实健康数据。风险场景若使用 P1 步骤未直接列出的 M0 安全迁移，测试要求其为拒绝结果，并继续验证该迁移、actor 和错误来自权威合同。

## 根因闭环：HM-M1-P2-C1-ACTION-SEMANTIC-CONFLATION

- first_seen / recurrence_count：2026-07-12 / 1；affected checkpoint：P2-C1。
- symptom：12/25 事件虽然引用了真实 `action_id`，但 action 的 actor/resource/effect 与事件不匹配；`security.audit_metadata` 被错误用于业务资源。
- exact stop：平台 `P2-C1 Exact revision / No-Go`，source `fedaeab192f198791817367b4f70871ffda43ce3` 未集成。
- reproduction：对每个事件把 `resource_ref` 首段与 C4-S04 action.resources 交叉核对，并检查 subject/effect/prohibitions；错误映射在旧5项测试全绿时仍可通过。
- causal chain：因为旧计划只有一个必填 `action_id`，因此状态迁移命令、授权类别和审计动作被混为同一概念；因为测试只检查 action 全局存在，因此合法但错误的 action 仍被接受；这是最早可控根因。
- impact：仅影响 P2-C1 计划与测试证据；不修改 M0/M1 权威合同、专业签署、共享代码、环境或真实数据。
- rejected workaround：禁止继续用 `security.audit_metadata` 填补缺失业务动作，也不放宽 action enum 或删除源闭包断言。
- systemic fix：状态机 transition 作为权威命令；安全 action 改为可选且存在时必须逐项匹配 actor/resource/effect/prerequisite；审计保持独立 `audit_expectation`，不得代表业务写。
- prevention gate：exactly25、event/key/payload 唯一、真实 JSON Pointer 解引用、action-resource/actor/effect/prerequisite 和 audit-as-write 拒绝。
- positive/regression：P2-C1 5项测试与 P1 11项回归；负例覆盖 extra、duplicate、wrong pointer、upstream reorder、wrong action-resource 和 audit-as-write。
- blocks：P2-C2；does_not_block：其他已授权且不依赖本计划的项目。
- verdict：等待平台独立复核；未获 Go 前保持只读。

## 根因闭环：HM-M1-P2-C1-NORMAL-REPLAY-DISCONTINUITY

- first_seen / recurrence_count：2026-07-12 / 1；affected checkpoint：P2-C1 R3。
- symptom：A001 同一 `HealthTask` 从 `pending→in_progress` 后直接从 `completed` 开始下一事件，缺少 `in_progress→completed`；正常 fixture 同时创建了 `RiskEvent` 与 `HumanHandoff`。
- exact stop：平台 `P2-C1 R3 Exact revision / No-Go`；source `ab74ac84c400f5d02d784fb8317d45a93eb50e58` 未集成。
- expected / actual：正常首轮应形成连续任务链并记录复盘，且已签署语义明确“无专业触发”；实际事件链不可连续执行并漂移到风险/转人工路径。
- causal chain：因为首版门禁只验证单事件 from/to 属于状态机，因此跨事件资源连续性未验证；因为只核对 scenario ID 与步骤，未把 fixture `expected_result` 和签署 safe outcome 转成场景 profile 约束，因此风险占位事件可在正常场景中绿测；最早可控根因为缺失跨事件与结果语义门禁。
- impact：阻塞 P2-C2 runner；不影响 M0/M1 权威合同、专业签署或其他项目。
- rejected workaround：不增加第26事件，不保留风险/转人工占位凑六机覆盖，不降低A001正常语义。
- systemic fix：A001 保持11事件，以 `in_progress→completed→pending_check→recorded` 替换风险/转人工占位；A003 按 `emergency_handoff_open` 与签署结果使用 `triage_pending→emergency:CLASSIFY_EMERGENCY`，A013继续覆盖 human-handoff。
- prevention gate：同资源状态/版本连续；A001拒绝RiskEvent/HumanHandoff且任务终态必须recorded；A003迁移、actor、fixture expected_result和签署safe outcome闭包；不连续状态/版本、normal-with-risk、wrong-emergency-profile负例均拒绝。
- security/data/release impact：零；所有数据仍合成，未进入环境、真实数据或生产。
- verdict：等待平台R4独立复核；未获 Go 前不进入P2-C2。

## 后续检查点

P2-C1已由平台独立验收Go，squash integration=`40a042b`，authoritative evidence HEAD=`5004cdc`。

## P2-C2 Reference Runner

| 检查项 | 结果 |
| --- | --- |
| A001 11事件内存顺序重放 | PASS |
| canonical trace hash跨独立runner一致 | PASS |
| 同键同载荷安全重放 | PASS，无重复state/audit/trace |
| 同键异载荷（含语义变化） | `HM_IDEMPOTENCY_CONFLICT` |
| version conflict | 状态、audit、trace不变 |
| audit failure | state/version/event/audit/idempotency全回滚 |
| AI激活计划/专业分类/直接关闭风险 | REJECT |
| 未完成前序直接激活计划 | `HM_RESOURCE_STATE_CONFLICT` |
| unknown transition | `HM_P2_UNKNOWN_TRANSITION` |
| 网络/DB/clock/random导入 | 0 |
| runner输出边界 | synthetic_only=true / executable=false |

当前runner只接受注入合同和合成事件，不自行读取文件或连接任何外部系统。负向fixture包、15场景最终执行矩阵和完整零调用证据保留给P2-C3。

## 根因闭环：HM-M1-P2-C2-CALLER-CONTROLLED-SAFETY-SEMANTICS

- first_seen / recurrence_count：2026-07-12 / 1；affected checkpoint：P2-C2 R3。
- symptom：调用方把权威计划中的 `denial_expectation` 从 deny 改为 allow 后，运行器仍可提交并写入 allow audit；幂等摘要同时遗漏合法的 `idempotency.expectation`。
- exact stop：平台 `P2-C2 Exact revision / No-Go`；source `d351d35113c977d011d6ce5fe2f4fddfaa8e50a3` 不集成，C3 不授权。
- reproduction：对 A005/A008/A009/A014/A015 分别执行 Schema 合法 deny→allow 变异，旧 runner 返回 committed；同键把 expectation 从 `new_result` 改为 `return_original_result`，旧 runner 返回 replayed。
- expected / actual：权威拒绝边界和完整事件载荷变化必须失败关闭；实际由调用方自报 denial，并从幂等摘要排除了 expectation。
- causal chain：因为 runner 只验证调用方自报的 deny 条件，因此 allow 分支没有权威来源；因为首次执行未绑定 replay plan 事件，因此安全语义可漂移；因为摘要额外排除 expectation，因此合法字段变化不可见。最早可控根因是运行时没有把候选完整绑定到权威事件。
- impact：阻塞 P2-C2 Go 与 C3；不影响已签署专业源、C1集成、其他模块、环境或真实数据。
- rejected workaround：不依赖调用方诚信、不只增加单一 A008 特判、不把 expectation 继续视为非载荷元数据。
- systemic fix：初始化时建立 `(scenario_id,event_id)` 权威事件表；首次执行在任何提交前进行完整事件一致性检查；幂等摘要只排除 key。
- prevention gate：Schema 合法 deny→allow、跨会员、撤权、风险、版本冲突与 expectation 变化全部拒绝；每个失败断言 resource/audit/trace/idempotency 不变。
- positive/regression：修订后 P2 15项与 P1 11项通过；零文件、网络、DB、clock、random、browser、model依赖保持。
- security/data/release impact：关闭本地参考运行器的安全语义绕过；仍仅合成数据且 executable=false，不产生环境或发布影响。
- verdict：corrected candidate 等待平台独立复核；未获 C2 Go 前不进入 C3。

## P2-C3 合成矩阵结论

| 检查项 | 结果 |
| --- | --- |
| 正例 exact set | MVP-A001—A015，15/15 PASS |
| 负例 exact set | NEG-A001—A015，15/15 PASS |
| 正例隔离重放 | outcome/error/result count 15/15 与冻结矩阵一致 |
| canonical trace hash | 15/15 两次隔离运行一致并匹配冻结值 |
| 负例稳定错误 | 15/15 与矩阵 expected_error_id 一致 |
| 负例无副作用 | resource/audit/trace/idempotency 15/15 全部不变 |
| Schema 负例 | 缺项、重复ID、提升executable、取消synthetic全部REJECT |
| 零外部运行时入口 | file/network/API/DB/clock/random/browser/storage/real-data=0 |
| 输出边界 | synthetic_only=true / executable=false |
| 回归 | P2 19/19、P1 11/11 PASS |

C3矩阵只冻结本地合成验证结果，不改变专业源、隐私法律Pending、共享实现和真实活动No-Go。当前结论为ready for independent review；未获C3 Go前不进入P2-C4。
