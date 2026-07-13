# 生命导航阶段 Handoff：LN-M2-001

- 验收单号：`LN-M2-001`
- 通知编号：`LN-TASK-20260710-001`
- 提交负责人：生命导航二负责人
- 提交时间：`2026-07-11T00:59:00+08:00`
- 当前分支与基线提交：`codex/life-navigation-application-history` / `22be354`
- 检查点：M2
- 实现记录：`IR-20260711-LIFE-APPLICATION-HISTORY-M2`

## 本阶段交付

- 目标：完成本人申请历史的类型化数据适配、application 映射、加载/空/成功/错误状态模型和支持重放元数据的 POST 包装；不修改页面 UI，不进入 M3。
- 修改路径：
  - `app/src/modules/life-navigation/lifeNavigationApi.ts`
  - `app/src/modules/life-navigation/lifeNavigationApi.test.ts`
  - `app/src/modules/life-navigation/index.ts`
  - `docs/project-management/modules/life-navigation/certification/checklists/IR-20260711-LIFE-APPLICATION-HISTORY-M2-checklist.json`
  - `docs/project-management/modules/life-navigation/certification/exams/IR-20260711-LIFE-APPLICATION-HISTORY-M2-exam-attempt-1.json`
  - `docs/project-management/modules/life-navigation/implementation-records/IR-20260711-LIFE-APPLICATION-HISTORY-M2.json`
  - `docs/project-management/modules/life-navigation/LN-M2-001-handoff.md`
- 未修改路径：未修改 `LifeNavigationModule.tsx`、共享 `app/src/infrastructure/`、共享样式、后端、contracts、scripts 或 M0/M1 历史证据。
- 接口或契约差异：无。GET 使用 `/api/v1/life-nav/records?limit=<1..30>`；POST 使用 `/api/v1/life-nav/records`，固定 `record_type=application`，只调用共享 `defineBusinessRead/Write`、`createBusinessApiAdapter` 与 `executeWithMeta`。
- 数据与状态：
  - 定义 `LifeNavigationRecordDto`、`LifeNavigationHistoryResponse` 和 `LifeNavigationApplicationRecord`。
  - UI 模型过滤非 `application` 记录并映射 `displayStatus=submitted`，不虚构业务流转状态。
  - 历史状态为 discriminated union：`loading | empty | ready | error`；error 原样持有共享 `ApiError`。
  - limit 默认 30；只发送整数 1..30，0、31 和其他越界值安全回退 30。
  - POST 使用 `executeWithMeta`，按 `idempotencyReplayed` 返回 `created | replayed`，不自行实现 fetch、认证、重试或错误解析。
- 起飞认证：
  - checklist：`IR-20260711-LIFE-APPLICATION-HISTORY-M2`，31 项重新全文读取，`created_at=2026-07-10T16:54:48.2343822Z`、`checked_at=2026-07-10T16:56:02.4690274Z`、`completed_at=2026-07-10T16:56:20.7028818Z`。
  - exam：`EX-20260711-LIFE-APPLICATION-HISTORY-M2-1`，attempt 1，8/8，score 100，status `passed`；`generated_at=2026-07-10T16:57:06.1424949Z`、`completed_at=2026-07-10T16:57:16.0772031Z`。
- 自动化命令与结果：
  - `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/Test-AgentDevelopmentPreflight.ps1`：`status=ready`。
  - M2 checklist 单独复制到受控临时目录后执行 `python -X utf8 scripts/validate_development_checklists.py contracts/foundation/development-checklist.v1.schema.json <temp-dir> --project-root . --require-current`：通过，临时目录已删除。
  - `python -X utf8 scripts/validate_governance_exams.py contracts/foundation/governance-exam.v1.schema.json contracts/foundation/governance-exam-bank.v1.schema.json contracts/foundation/governance-exam-bank.v1.json docs/project-management/modules/life-navigation/certification/exams --project-root .`：通过。
  - `npm test -- --run src/modules/life-navigation/lifeNavigationApi.test.ts src/modules/life-navigation/LifeNavigationModule.test.tsx`：2 个测试文件、17 项测试通过。
  - `npm test`：14 个测试文件、76 项测试通过。
  - `npm run build`：TypeScript build 与 Vite production build 通过。
- 测试覆盖：GET 路径；limit 0/1/30/31；默认 30；application 过滤；empty/ready/submitted 映射；共享 `ApiError` 机器码与 requestId；POST 201 created、200 replay meta、显式幂等键和固定 `record_type=application`。
- 测试环境证据：M2 未部署、未访问远端测试环境；测试环境集成与真实登录 UAT 留待 M4。
- 发现的问题与根因状态：
  - 首次直接对 `certification/checklists/` 执行 `--require-current` 时，历史 M0-R1 快照因平台更新 `agent-collaboration.v1` 被正确判定 stale。根因是验证命令把当前 M2 与不可修改历史快照放在同一目录整体检查，并非 M2 清单内容错误。
  - 处理方式：未修改 M0；把 M2 原件复制到受控 TEMP 目录用正式 Schema、`--project-root . --require-current` 单独验证并删除临时目录。M2 当前哈希验证通过。
  - 未发现新的接口、权限、幂等或错误信封缺口。
- 未完成和风险：本阶段无 UI 渲染；`loading/empty/ready/error` 与 `created/replayed` 尚未接入页面，属于 M3。测试环境行为留 M4。
- 下一阶段拟做内容：仅在平台签发 `LN-M2-001 Go` 后进入 M3 页面闭环；本次完成后停止，不提前修改 UI。

## 平台抽查

- 复跑命令与结果：
  - M2 checklist 时间链与 SHA-256 绑定：通过；`created < checked < checklist completed < exam generated < exam completed`，试卷绑定当前清单哈希。
  - M2 checklist 使用正式 Schema、`--project-root . --require-current` 单独验证：通过。
  - `python -X utf8 scripts/validate_governance_exams.py contracts/foundation/governance-exam.v1.schema.json contracts/foundation/governance-exam-bank.v1.schema.json contracts/foundation/governance-exam-bank.v1.json docs/project-management/modules/life-navigation/certification/exams --project-root .`：通过，M2 attempt 1 为 100 分。
  - `python -X utf8 scripts/validate_implementation_records.py contracts/foundation/implementation-record.v1.schema.json docs/project-management/modules/life-navigation/implementation-records --project-root .`：通过。
  - `npm test -- --run src/modules/life-navigation/lifeNavigationApi.test.ts src/modules/life-navigation/LifeNavigationModule.test.tsx`：2 个文件、17 项通过。
  - `npm test`：14 个文件、76 项通过。
  - `npm run build`：通过。
  - `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/Test-ServicePlazaContracts.ps1`：通过。
  - `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/Test-TextEncoding.ps1`：通过。
  - `git diff --check`：通过。
- 代码/接口抽查：模块只复用共享 `createBusinessApiAdapter`、`defineBusinessRead/Write` 与 `executeWithMeta`；GET limit 始终为 1..30、只保留 `record_type=application`、UI 状态映射为 `submitted`，POST 按 meta 区分 created/replayed，符合固定合同且未虚构审核或完成生命周期。未自行实现 fetch、认证、重试或错误解析。
- 证据完整性：当前 checklist、100 分考试、implementation record、定向/全量测试、build、契约和编码门禁均可复跑；M0/M1 历史证据未修改。
- 结论：Go
- No-Go 必须修复项：无。
- 是否授权进入下一阶段：是，仅授权 M3 页面闭环；M3 开工前必须新建当前 checklist 并通过 100 分随机治理考试。
- 平台复核人及时间：服务广场平台集成负责人，`2026-07-11T01:02:27+08:00`
