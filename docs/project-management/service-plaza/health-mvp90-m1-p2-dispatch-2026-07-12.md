# 健康大管家 M1 P2 平台派发报告

日期：2026-07-12

平台工作项：`AIW-20260712-HEALTH-MVP90-M1-P2-DISPATCH`

权威起始基线：`de31a235b9679698b9de4e33faa6ab980e0461f6`

## Outcome

P2 采用“确定性合成重放”，不进入共享前端、后端、API 或数据库。P1 已完成合同结构和 11 项 conformance；当前最小真实缺口是逐事件执行轨迹，而不是再增加一层产品文档。

模块工作项：`AIW-20260712-HEALTH-MVP90-M1-P2-SYNTHETIC-REPLAY`。

状态转换：平台派发工作项 `active -> integrated` 后，模块专用 worktree 从最终 integration HEAD 创建并核验 clean，再由独立 activation commit 将模块项 `planned -> active`。旧 M1 P0/P1 工作树保持只读。

## 只读审计证据

- 前端：健康精确路由存在，但仍委托旧 `CoreServicePage` 咨询页；旧写入仅为 `/api/v1/health/consultations`。本轮不得修改或复用这些路径。
- 后端：权威 integration `e41265905815082433e040412f3dd6b6b33dfede` 没有 M1 的 16 对象、6 状态机或 PDCAR API；`/api/v1/health/analyze` 已固定 503 失败关闭。
- 合同：15 个 P1 fixture 当前只有输入标志和期望结果，尚无 actor/action/from/to/version/idempotency/audit 的可执行轨迹。
- 所有权：当前活动工作项未占用本次精确健康 P2 合同、conformance 或文档路径。

## 两层依赖结论

- platform readiness：Go，批准工具链为 Python 3 + JSON Schema。
- module readiness：M0 handoff、M1 P1 handoff、三项专业签署与 C4-S04 均已满足。
- local blockers：C4-L02-L04、全量 C4-H06、production identity 继续阻塞持久化、真实数据、环境和发布；它们不阻塞零网络、零DB、纯合成 P2。

## 责任边界

平台集成负责人负责通知、工作项、精确路径、依赖和最终独立验收；健康大管家负责人负责 P2 replay plan、reference runner、测试、IR 和 Handoff。平台不代做模块实现。

后端/API/数据库工作项本轮不创建。若 P2 Go 后进入真实服务器纵切，必须另建 backend repo 工作项和 APP companion evidence item，不能在一个相对路径范围内跨两个 Git 根。

## 当前治理证据

- checklist：`IR-20260712-HEALTH-MVP90-M1-P2-DISPATCH-R2`，28/28 completed。
- exam：`EX-20260712-HEALTH-MVP90-M1-P2-DISPATCH-R2-1`，100 分 passed。
- R1：错误使用 `FC-` record_id，原始 checklist/exam 已不可变保留在 invalidated-snapshots；未改写为通过。
- preflight：ready。
- 模块激活前仍需完成本派发提交、受控集成、实际 worktree 创建和 registry activation。

## 不能误读的结论

P2 是 development-only reference execution，不是环境验收、生产实现或医疗专业放权。所有合同与结果继续 `executable=false`；P2 的 Python 执行能力只证明合同可被一致重放。
