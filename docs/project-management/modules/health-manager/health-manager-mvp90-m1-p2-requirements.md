# 健康大管家 MVP-90 M1 P2 确定性合成重放需求

- work_id：`AIW-20260712-HEALTH-MVP90-M1-P2-SYNTHETIC-REPLAY`
- 当前检查点：`P2-C2 Exact revision`
- 范围：成年合成会员、本地内存、零网络、零数据库
- 输出属性：`synthetic_only=true`、`executable=false`

## C1 目标

建立一份机器可校验的重放计划，而不是复制一套健康业务语义。计划必须：

1. 精确包含 `MVP-A001`—`MVP-A015` 与 `HMM1-F001`—`HMM1-F015`；
2. `MVP-A001` 按顺序覆盖 `M1-S01`—`M1-S10`，全计划覆盖六组 M0 状态机；
3. 每个事件声明 actor、可选的安全授权 action、可选的状态机 transition、资源、期望状态、版本、幂等、拒绝和独立审计结果；action 与 transition 至少存在一个；
4. 场景、fixture、步骤、动作、迁移和拒绝错误必须解析到已集成 M0/M1 源；
5. 允许风险场景使用 M0 已存在但 P1 步骤未列出的安全转移，前提是该事件明确为 `deny`，且状态机、角色和场景拒绝语义均可解析；
6. 不读取系统时间或随机数，不调用网络、API、数据库、浏览器和外部模型；
7. 不把计划或后续 reference runner 描述为可上线业务实现。

## C1 验收

- Draft 2020-12 Schema 正例通过；删场景、提升 executable、取消 synthetic、未知步骤和未知动作负例拒绝；
- 15 个场景和 fixture 一一对应且 source pointer 索引一致；
- 25 个首版事件均能解析到步骤、授权动作、状态机迁移或拒绝规则；授权动作必须逐项匹配 actor、resource、effect 和 prerequisite；
- 事件总数固定为25，event_id、幂等键和 payload_ref 全局唯一；
- scenario/fixture JSON Pointer 必须真正解引用到同一 ID，不接受只比较指针字符串；
- 同一场景、同一资源的后续事件必须满足 `previous.to=current.from` 与 `previous.version.after=current.version.before`；
- `pdcar_loop_recorded` 正常场景不得创建 `RiskEvent` 或 `HumanHandoff`；`emergency_handoff_open` 必须使用权威专业紧急分类迁移；
- fixture `expected_result`、P1 scenario `safe_outcome` 与真人签署的 `proposed_safe_outcome` 必须真实解引用并一致；
- 10 个步骤、6 个状态机均有覆盖；
- P1 原 11 项 conformance 保持通过；
- current checklist、考试、IR、UTF-8、diff/scope 和敏感模式门禁通过。

## 保持 No-Go

`C4-L02-L04`、全量 `C4-H06`、production identity、真实会员/健康数据、共享前后端/API/数据库、测试环境、部署、收费、资金和生产均不在本检查点。

## C2 Reference Runner

P2-C2只实现纯Python、内存内参考运行器：

1. 构造函数只接收已加载的replay plan、state machines和security authorization，不自行读文件；
2. 同资源状态和版本必须连续，非首事件不能凭计划期望值凭空初始化资源；
3. 同一幂等键同一完整事件载荷返回原结果且不重复审计；同键异载荷稳定返回`HM_IDEMPOTENCY_CONFLICT`；
4. 状态冲突、版本冲突、未知/禁止迁移、actor/action/resource不匹配均失败关闭且不修改资源、审计、trace或幂等存储；
5. 审计写失败返回`HM_AUDIT_WRITE_REQUIRED`，本事件的状态、版本、trace、audit和idempotency全部回滚；
6. AI激活计划、作出专业风险分类或直接关闭风险均被权威迁移/授权规则拒绝；
7. canonical trace只由确定性内存状态生成；输出始终`synthetic_only=true`、`executable=false`；
8. 禁止导入或调用网络、数据库、系统时间、随机数、浏览器、文件持久化和外部模型。
9. 运行时必须以 `scenario_id + event_id` 把首次候选事件完整绑定到已验证 replay plan；调用方不得改写 denial、actor、action、resource、transition、version、audit 或其他安全语义。
10. 幂等摘要只排除 Idempotency-Key 本身，`expectation` 及其余完整事件语义必须进入摘要；任何合法字段变化均按同键异载荷处理。

C2不包含负向fixture包和15场景最终矩阵；这些属于获得C2 Go后的P2-C3。

## C3 合成验收矩阵

P2-C3只补齐合成验收证据：

1. 15个权威场景各有一个冻结正例结果，包含 outcome、error、result count 与隔离运行 canonical trace hash；
2. 15个场景各有一个负例，覆盖审计失败、权威拒绝改允许、actor/action/resource/transition/audit漂移、幂等 expectation 变化和资源版本冲突；
3. 每个负例必须返回稳定 error、`committed=false`，并证明 resource、audit、trace、idempotency 四类状态完全不变；
4. 正例与负例 exact set、`synthetic_only=true`、`executable=false` 由 Draft 2020-12 Schema 和测试共同锁定；
5. reference runner 的文件、网络、API、DB、时钟、随机、浏览器、local/session storage、真实身份和真实健康数据运行时入口为零；
6. P2与P1回归、治理、内部依赖、总合同、UTF-8、diff/scope和敏感信息门禁全部通过。

C3仍不产生共享实现、环境、真实数据或可上线能力；通过后只可进入任务书的P2-C4模块Handoff。

## C4 收口要求

P2-C4不修改runner、matrix、Schema或测试，只汇总C1—C3的source/integration、测试、根因关闭、未决风险和No-Go，形成模块Handoff并申请平台最终P2 synthetic Go/No-Go。即使P2最终Go，也只证明合成重放合同与验证内核，不代表业务实现、环境或发布就绪。
