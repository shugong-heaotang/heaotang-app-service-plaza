# 生命导航阶段 Handoff：LN-M1-001

- 验收单号：`LN-M1-001`
- 通知编号：`LN-TASK-20260710-001`
- 提交负责人：生命导航二负责人
- 提交时间：`2026-07-11T00:36:42+08:00`
- 当前分支与提交：`codex/life-navigation-application-history` / `22be354`
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
  - `npm test -- --run src/infrastructure/apiClient.test.ts src/infrastructure/businessApiAdapter.test.ts src/infrastructure/submissionRepository.test.ts src/modules/life-navigation/LifeNavigationModule.test.tsx`：平台修复后 4 个测试文件、30 项测试通过；覆盖新 meta 能力与旧 API 兼容。
  - 在后端提交 `70fa12276e6eac17369c0d1d3c1d23a8e757fcc0` 的隔离临时 worktree 执行 `go test -count=1 ./plugins/life-navigation-plugin`：通过；临时 worktree 已移除。
  - 同一提交执行 `go test -count=1 -v ./plugins/life-navigation-plugin -run 'Test(ListRecordsEnforcesFirstSliceLimitAndUserOwnership|CreateRecordIdempotencyIsAtomicUnderConcurrentReplay|CreateRecordHandlerUsesStandardIdempotencyHeaderSemantics|ConcurrentDistinctKeysCannotExceedDailyRecordLimit)$'`：4 项无缓存目标测试通过。
- 环境问题与闭环：首次前端测试因专用工作树无 `node_modules`，`vitest` 无法识别；使用仓库现有锁文件执行 `npm ci`，119 个锁定包安装、0 漏洞，随后原测试通过。该问题属于本地测试依赖缺件，不是产品失败，未修改受控源文件。
- 测试环境证据：平台修复已通过本地 APP/Go 验证；远端测试环境验证留待 M4，不在 M1 扩大范围。
- 发现的问题与根因状态：
  - GET limit 契约漂移：根因已关闭；后端提交新增 30 上限常量和完整边界测试。
  - 重放元数据不可达：根因已关闭；APP 兼容扩展新增 meta 路径并保留旧 API。
  - 本人归属负向证据：缺口已关闭；新测试覆盖服务层与 handler 层用户 A/B 隔离。
- 未完成和风险：测试环境验证留待 M4；M2 尚未开始，必须使用新的当前检查单和 100 分考试，不能复用 M0 证书。
- 下一阶段拟做内容：仅按平台授权进入 M2 历史数据适配最小实现；开工前先完成新 checklist 与考试。本次复验收口不提前编码。

## 平台抽查

- 复跑命令：平台已复跑 APP 契约/UTF-8、13 个测试文件 62 项测试、正式 build，以及后端包 test/vet；模块负责人复跑 APP 4 个定向测试文件 30 项测试、后端包全量测试和 4 项无缓存目标测试。
- 代码/接口抽查：旧 `apiRequest/execute` API 保持；新 meta 字段完整；后端 limit 与跨用户边界符合裁决；本次复验收口只修改三份 M1 文档，未修改代码或 M0 证据。
- 证据完整性：APP 当前 HEAD 含 `22be354`；后端固定提交为 `70fa12276e6eac17369c0d1d3c1d23a8e757fcc0`；本地复验全部通过，测试环境验证明确留 M4。
- 结论：Go
- No-Go 必须修复项：已完成。共享响应元数据兼容扩展、GET limit 1..30/越界默认 30、跨用户不可见负向测试均已实现并验证。
- 是否授权进入下一阶段：是，仅授权 M2 历史数据适配；M2 开工前必须新建当前 checklist 并通过 100 分随机治理考试。
- 平台复核人及时间：服务广场平台集成负责人，`2026-07-11T00:51:31+08:00`
