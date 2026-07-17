# Project Brain v2 M1 来源映射

## 1. 结论

M1 只冻结事实定义、来源责任和失败关闭契约，不运行任何读取任务。所有 source mapping 的 `runtime_enabled=false`，整个 package 的 `runtime_enabled=false`、`production_enabled=false`。

首批事实共 3 项：2 项 G0 治理事实映射真实权威制品；1 项 G1 仅为 synthetic contract fixture，用于证明阈值、小样本抑制、权限、freshness 和重识别边界。当前没有任何真实经营数据源获准。

## 2. 权威映射

| fact_id | classification | 唯一 authority | source owner | 运行状态 | permitted use |
| --- | --- | --- | --- | --- | --- |
| `governance.work_items.status_counts` | G0 | `contracts/foundation/agent-collaboration.v1.json` | 平台集成负责人 | mapping verified；runtime off | portfolio status、ownership audit |
| `governance.implementation_records.verification_counts` | G0 | `contracts/foundation/implementation-records/` 与其 Schema/validator | 平台质量负责人 | mapping verified；runtime off | delivery quality、evidence completeness |
| `synthetic.operations.completed_services.count` | G1 | `fixture://contracts/project-brain/v2/examples/trusted-g1-synthetic.json` | M1 synthetic fixture owner | synthetic only；runtime off | contract validation only |

任何未来真实 G1 指标都必须另行获得业务定义、唯一 source owner、真实只读 authority、分类、阈值、重识别审查和独立 Go，不能把 synthetic fact 改名后直接使用。

## 3. G1 隐私阈值 v1

- 标准最小群体：20；
- 高重识别风险最小群体：50；
- 最多组合维度：2；
- 低于阈值必须抑制；
- 禁止行级下钻；
- 禁止未授权拼接；
- 计数按 5 取整；
- P1/H1/F1/C1/S1 全部禁止；
- `member_id`、姓名、联系方式、健康、订单/支付、客服正文、人脉身份和精确地址等维度全部禁止。

该策略只用于 M1 合同验证，`production_enabled=false`。后续阈值变更必须新版本，不得在运行中静默改值。

## 4. 状态与失败关闭

- `Trusted`：authority 唯一、来源可达、freshness/quality/authorization 均通过且无冲突；G1 还必须通过阈值。synthetic `Trusted` 仅表示合同测试通过，`decision_usable=false`。
- `Unknown`：来源缺失、不可达、过期或证据不足；`value=null`、`decision_usable=false`。
- `No-Go`：分类、质量、权限、authority 冲突、阈值或发布边界明确失败；`value=null`、`decision_usable=false`。

禁止用零值、猜测值或未标记旧值代替 `Unknown/No-Go`。

## 5. 合法与负向证据

合法样例全部明确 `synthetic=true`：

- G0 Trusted synthetic；
- G1 Trusted synthetic（sample size 125、value 120、threshold pass、不可用于经营决策）；
- G0 stale Unknown（value null）。

10 个负例必须全部被预期原因码拒绝：行级会员、小样本、stale-as-Trusted、unauthorized-as-Trusted、敏感分类、多个 authority、写能力、未批准 G1 真实源、Unknown 携带值、synthetic provenance 缺失。

## 6. M2 解锁条件

M1 只有在本合同包获得独立数据分级/重识别 `Go`、普通 fast-forward integrated 且 authority fresh 后，才允许另行激活 M2。M2 仍只能实现只读 scheduler、不可变快照、审计、告警和失败演练；不得启用真实生产源、老板驾驶舱或 production。
