# 健康大管家 MVP-90 M1 合成 PDCAR 纵切要求

- work_id：`AIW-20260712-HEALTH-MVP90-M1-SYNTHETIC-PDCAR`
- 当前检查点：`M1-P0`
- 激活范围：`development-only`
- 适用对象：成年合成会员
- 当前状态：P0 实施完成，等待平台独立复核

## 1. 本检查点目标

P0 只证明 M1 已具备进入合同设计的准入条件：

1. 平台级依赖继续满足 development Go；
2. M0 合同与合成一致性成果已 integrated；
3. `C4-H01`、`M1-LIFESTYLE-TEMPLATE v1-proposed`、`MVP-A001`—`MVP-A015` 已在成年合成会员范围 Accepted；
4. `C4-S04` 技术安全合同已 Accepted / integrated；
5. 上述 Accepted 只允许后续合同、Schema、固定 seed 合成 fixtures 与本地 conformance，全部保持 `executable=false`。

## 2. P0 必须同步的证据

| 门禁 | P0 状态 | 权威证据 |
| --- | --- | --- |
| M1 development activation | Accepted | `agent-collaboration.v1`；activation HEAD `cb3fd5548ab578327a81e70e06237f2daa1ffea3` |
| C4-H01 | Accepted / non-executable | `c4-h01-action-boundary-decision.v1.json`；签署 `item-637` |
| M1 窄模板 | Accepted / non-executable | `m1-lifestyle-template-signoff.v1.json`；签署 `item-645`；有效期至 2026-10-10 |
| 15 个专业场景 | 15/15 Accepted / non-executable | `m1-professional-scenario-review.v1.json`；签署 `item-656` |
| C4-S04 | Accepted / non-executable | `security-authorization.v1.json`；source `e68b1a0f...`，integration `e547190...` |
| C4-L02-L04 | Pending with owner | 继续阻止真实身份、真实健康数据、环境、部署、收费和生产 |

## 3. P0 输出

- 将安全合同中 C4-H01 与 M1 窄模板的陈旧 `Pending with owner` 更新为带证据引用的 `Accepted`；
- Schema 精确要求这两项为 Accepted，同时精确要求 `C4-L02-L04` 保持 Pending；
- 将模块内部依赖图切换到 `health-mvp90-m1`，新增 M1 激活、专业、安全、隐私法律和 P0 Handoff 节点；
- 形成当前 checklist、100 分考试、implementation record、receipt 和 Handoff。

## 4. 明确非目标

P0 不创建 `vertical-slice`、`professional-boundaries`、`synthetic-pdcar-scenarios`、fixtures 或业务实现；这些属于平台通过 P0 后的 P1/P2。P0 也不授权共享前端、后端、API、数据库、测试环境、部署、真实会员、真实健康数据、收费、资金或生产。

## 5. 失败关闭

- 若两项 Accepted 证据缺失、被撤回或版本不符，Schema 和内部依赖必须失败；
- 若 C4-L02-L04 被误写为 Accepted，Schema 必须失败；
- 安全合同继续 `executable=false`；
- 任何范围扩大、安全事件、规则/专业前提变化或模板到期，必须重新审核。
