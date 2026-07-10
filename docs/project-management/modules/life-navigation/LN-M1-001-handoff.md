# 生命导航阶段 Handoff：LN-M1-001

- 验收单号：`LN-M1-001`
- 通知编号：`LN-TASK-20260710-001`
- 提交负责人：生命导航二负责人
- 提交时间：`2026-07-11T00:36:42+08:00`
- 当前分支与提交：`codex/life-navigation-application-history` / `0bbcc2a5b5f15c4b535f1d5d85ba95e492f89e38`
- 检查点：M1

## 本阶段交付

- 目标：只读核验 POST/GET 运行事实、本人归属、幂等和 limit 规则，形成复用共享 adapter 的前端适配设计；不进入 M2。
- 修改路径：
  - `docs/project-management/modules/life-navigation/LN-M1-001-interface-facts-and-adapter-design.md`
  - `docs/project-management/modules/life-navigation/LN-ICR-20260711-001.md`
  - `docs/project-management/modules/life-navigation/LN-M1-001-handoff.md`
- 未修改的受保护路径：未修改 `app/src/`、`backend-go/`、`contracts/`、`scripts/`、共享样式或公共 API；未修改已提交 M0 证据。
- 接口或契约差异：有。GET limit 固定 1..30、运行实现接受 1..100；后端重放响应头在共享前端 adapter 边界不可达。已提交 `LN-ICR-20260711-001`，未自行修改公共实现。
- 自动化命令与结果：
  - `python -X utf8 scripts/validate_development_checklists.py contracts/foundation/development-checklist.v1.schema.json docs/project-management/modules/life-navigation/certification/checklists --project-root . --require-current`：通过，M0 补正检查单 current。
  - `python -X utf8 scripts/validate_governance_exams.py contracts/foundation/governance-exam.v1.schema.json contracts/foundation/governance-exam-bank.v1.schema.json contracts/foundation/governance-exam-bank.v1.json docs/project-management/modules/life-navigation/certification/exams --project-root .`：通过，M0 考试 passed。
  - `npm test -- --run src/infrastructure/businessApiAdapter.test.ts src/infrastructure/submissionRepository.test.ts src/modules/life-navigation/LifeNavigationModule.test.tsx`：3 个测试文件、13 项测试通过。
  - `go test ./plugins/life-navigation-plugin`：通过。
  - `go test -count=1 -v ./plugins/life-navigation-plugin -run 'Test(AssessmentAndRecordPersistence|CreateRecordIdempotencyIsAtomicUnderConcurrentReplay|CreateRecordHandlerUsesStandardIdempotencyHeaderSemantics|ConcurrentDistinctKeysCannotExceedDailyRecordLimit)$'`：4 项目标测试无缓存通过。
- 环境问题与闭环：首次前端测试因专用工作树无 `node_modules`，`vitest` 无法识别；使用仓库现有锁文件执行 `npm ci`，119 个锁定包安装、0 漏洞，随后原测试通过。该问题属于本地测试依赖缺件，不是产品失败，未修改受控源文件。
- 测试环境证据：M1 未部署、未访问远端测试环境；运行事实来自本地当前源代码与既有自动化测试。
- 发现的问题与根因状态：
  - GET limit 契约漂移：根因是后端历史通用记录列表保留 100 上限，而首切片固定契约收紧为 30 后未同步运行边界。未修复，已申请平台裁决。
  - 重放元数据不可达：根因是统一前端 SDK 抽象只返回业务 data，未建模 HTTP 响应元数据。未修复，模块不能绕过共享 adapter，已申请兼容扩展。
  - 本人归属：后端从会话取用户 ID 并在 SQL 使用 `WHERE user_id=?`；现有持久化测试通过，但当前 life-navigation 包缺少显式“用户 A 不可见用户 B”负向 handler 测试，列为后续平台/模块验收证据缺口。
- 未完成和风险：`LN-ICR-20260711-001` 未裁决；M1 尚待平台 Go/No-Go。未获 Go 前不进入 M2。
- 下一阶段拟做内容：仅在平台裁决 ICR 并签发 `LN-M1-001 Go` 后，进入 M2 的历史数据适配最小实现；本次不提前编码。

## 平台抽查

- 复跑命令：已复核 M0 current/passed 门禁、前端 13 项测试、Go life-navigation 包测试、4 项无缓存目标测试、`Test-TextEncoding` 与 `git diff --check` 记录。
- 代码/接口抽查：接口事实复核一致；未修改业务代码、后端、公共契约、共享 adapter 或 M0 证据。
- 证据完整性：POST/GET、本人过滤、幂等、并发、限额和当前前端 adapter 边界均有源代码与现有测试依据；已接受 `LN-ICR-20260711-001`。
- 结论：No-Go
- No-Go 必须修复项：
  - 平台保留 `execute(): Promise<T>` 并新增可选 `{ data, meta }` 响应能力，`meta` 至少包含 `status`、`requestId`、`idempotencyReplayed`。
  - GET records 的 `limit` 固定为 1..30，越界安全默认 30；平台扫描未发现登记的 >30 消费者。
  - 补充用户 A 不可见用户 B 的跨用户负向测试。
- 是否授权进入下一阶段：否
- 平台复核人及时间：服务广场平台集成负责人，`2026-07-11T00:40:00+08:00`
