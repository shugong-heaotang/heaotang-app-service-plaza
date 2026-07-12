# 健康大管家 MVP-90 M1 P2 Conformance Report

## P2-C1 结论

当前结论：`Exact revision corrected / ready for independent review`。

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

## 后续检查点

P2-C2 才允许实现纯 Python reference runner、稳定错误、幂等、版本冲突和 audit 原子回滚；必须先取得 P2-C1 平台 Go。
