# 健康大管家 MVP-90 M1 P2 确定性合成重放任务通知书

- notice_id：`HM-MVP90-M1-P2-TASK-20260712-001`
- platform_work_id：`AIW-20260712-HEALTH-MVP90-M1-P2-DISPATCH`
- module_work_id：`AIW-20260712-HEALTH-MVP90-M1-P2-SYNTHETIC-REPLAY`
- 下达日期：2026-07-12
- 下达方：平台集成负责人
- 接收方：健康大管家负责人
- 状态：平台正式派发；模块工作项须在本通知受控集成、专用工作树实际创建且 clean 后转 `active`

## 1. 唯一目标

把已经 integrated 的 M0/M1 合同从“结构一致”推进到“可确定性执行”：使用纯 Python、内存内、零网络、零数据库的 reference runner，对 10 步 PDCAR、6 组状态机和 15 个固定 seed 合成场景执行逐事件重放，输出稳定状态轨迹、拒绝结果和 canonical trace hash。

P2 是开发验证内核，不是生产业务实现。所有源合同继续 `executable=false`；运行结果必须同时标记 `synthetic_only=true`、`executable=false`。

## 2. 选择本切片的事实依据

- M0/M1、三项专业签署、C4-S04 和 P1 11 项 conformance 已 integrated。
- P1 已证明 Schema、exact set、source pointer 和 fixture 唯一性，但尚未执行逐事件 actor/action/from/to、resource version、idempotency 和 audit 轨迹。
- 权威后端 integration `e41265905815082433e040412f3dd6b6b33dfede` 尚无 M1 的 16 个对象和 6 组状态机；本轮提前修改 API/DB 会扩大范围。
- 现有 `/api/v1/health/analyze` 在权威后端已失败关闭为 `503 HEALTH_AI_CONSENT_REQUIRED`；P2 禁止调用或绕过它。
- 现有健康前端仍是旧咨询承接页；P2 禁止把旧 `/api/v1/health/consultations` 冒充 PDCAR 实现。

## 3. 两层依赖

平台依赖：`contracts/foundation/module-dependencies/health-manager.v1.json` 中 L0-L5 能力保持 Go。P2 只使用批准的 Python 3/JSON Schema 验证工具链。

模块依赖：

1. `m0.handoff=verified`；
2. `m1.p1-handoff=verified`，integration `8d6fe1d5fd45a005abf950651b8ddfb23dfbc306`；
3. `C4-H01`、M1 窄模板和 MVP-A001-A015 已在 development-only 范围 Accepted；
4. `C4-S04` Accepted；
5. `C4-L02-L04`、全量 `C4-H06`、production identity 继续 No-Go，但不阻塞零真实数据、零持久化的本地合成重放。

任一已接受签署被撤回、版本不兼容或源指针失效，P2 必须失败关闭。

## 4. 精确成果与允许路径

模块 repository：`C:/Users/shugo/Documents/APP系统`

模块 branch：`codex/health-manager-mvp90-m1-p2-synthetic-replay`

模块 worktree：`C:/Users/shugo/Documents/worktrees/heaotang-health-mvp90-m1-p2-synthetic-replay`

模块 owner：`Health Manager module agent` / 健康大管家负责人

精确允许路径：

- `contracts/modules/health-manager/internal-dependencies.v1.json`
- `contracts/modules/health-manager/mvp90-m1/synthetic-replay-plan.v1.json`
- `contracts/modules/health-manager/mvp90-m1/synthetic-replay-plan.v1.schema.json`
- `contracts/modules/health-manager/mvp90-m1/conformance/synthetic_pdcar_reference.py`
- `contracts/modules/health-manager/mvp90-m1/conformance/test_health_mvp90_m1_p2_replay.py`
- `contracts/modules/health-manager/mvp90-m1/conformance/fixtures/synthetic-replay-negative-cases.v1.json`
- `contracts/modules/health-manager/mvp90-m1/conformance/fixtures/synthetic-replay-negative-cases.v1.schema.json`
- `docs/project-management/modules/health-manager/health-manager-mvp90-m1-p2-requirements.md`
- `docs/project-management/modules/health-manager/health-manager-mvp90-m1-p2-receipt.md`
- `docs/project-management/modules/health-manager/health-manager-mvp90-m1-p2-conformance-report.md`
- `docs/project-management/modules/health-manager/health-manager-mvp90-m1-p2-handoff.md`
- `contracts/modules/health-manager/development-checklists/2026-07-12-health-mvp90-m1-p2*.json`
- `contracts/modules/health-manager/governance-exams/2026-07-12-health-mvp90-m1-p2*.json`
- `contracts/modules/health-manager/implementation-records/2026-07-12-health-mvp90-m1-p2*.json`

不得扩大为目录级健康模块授权。`App.tsx`、`HealthManagerRoute.tsx`、`CoreServicePage.tsx`、`submissionRepository.ts`、任何 Go、API、DB、部署和环境路径均不在范围内。

## 5. 最小执行模型

`synthetic-replay-plan.v1` 必须为 15/15 场景声明稳定事件序列。每个事件至少包含 scenario/step、actor、action/transition、resource ref、expected from/to、expected version、idempotency request、denial expectation 和 audit expectation；全部动作、状态和角色必须解析到 M0/M1 权威源，不得复制第二套业务语义。

reference runner 只能接收注入的合同与合成 fixture，不得访问网络、文件持久化、数据库、系统时间、随机数或外部模型。允许读取仓库内已授权的版本化 JSON 输入，输出仅为测试进程内机器结果。

## 6. P2 验收矩阵

1. 15/15 fixture 均进入重放；MVP-A001 完成完整 10 步，其余场景在声明步骤或拒绝点确定性关闭。
2. 所有 from/to/event/actor 均来自 M0 状态机、角色合同和 P1 source pointer；未知或禁止迁移稳定拒绝。
3. 同一输入重复运行得到同一 canonical trace hash；不得依赖当前时间或随机数。
4. 同一 Idempotency-Key + 同载荷返回同一结果；同键异载荷稳定冲突且状态不变。
5. resource version 冲突、跨会员资源、撤回授权、模板过期、服务关系缺失和 C4-S04 拒绝均失败关闭。
6. AI 激活计划、作出专业结论或关闭风险必须拒绝；会员确认前计划不得 active。
7. audit 写入失败时状态、版本和事件均不提交；原始反馈不可被摘要覆盖。
8. 15 场景结果逐项绑定已签署 safe/forbidden/stop 语义，不得改写专业结论。
9. 网络、API、数据库、浏览器、local/session storage、真实身份和真实健康数据调用计数均为零。
10. 所有输出 `synthetic_only=true`、`executable=false`；任何提升均由负例拒绝。
11. 运行 P1 原 11 项 conformance 与 P2 新测试；两组均通过。
12. current checklist 28/28、治理考试 100、IR、内部依赖、UTF-8、diff、scope 和敏感模式门禁通过。

## 7. 短检查点

- P2-C0：签收、两层依赖、current checklist、100 分考试。
- P2-C1：replay plan + Schema，15/15 事件计划及 source closure。
- P2-C2：reference runner、稳定错误、幂等/版本/audit 原子语义。
- P2-C3：15 正例与负例、确定性 hash、零网络/零DB/零真实数据证据。
- P2-C4：模块 Handoff，平台独立复核 P2 Go/No-Go。

每个检查点通过后才进入下一段；发现根因缺陷先关闭并回归，不允许降低断言或跳过失败场景。

## 8. 明确 No-Go

- 共享前端、页面、路由、后端、API、数据库、测试环境、部署、生产。
- 真实会员、真实健康数据、真实身份、收费、资金和外部供应商。
- 全量 C4-H06、C4-L02-L04 和 production identity 的提前 Accepted。
- 把 reference runner、旧咨询接口或旧健康页面描述为可上线的 PDCAR 产品。

P2 Go 后，平台再决定是否分别派发 TypeScript 模块内运行内核、前端页面或后端/API/DB；跨责任域必须使用互不重叠的独立工作项。
