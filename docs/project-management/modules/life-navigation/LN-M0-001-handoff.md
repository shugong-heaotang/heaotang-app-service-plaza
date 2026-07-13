# 生命导航阶段 Handoff：LN-M0-001

- 验收单号：`LN-M0-001`
- 通知编号：`LN-TASK-20260710-001`
- 提交负责人：生命导航二负责人
- 提交时间：`2026-07-11T00:19:43+08:00`
- 补正提交时间：`2026-07-11T00:24:03+08:00`
- 当前分支与提交：`codex/life-navigation-application-history` / `4876817d8c162ae2e93ef7e5290fee1d0357ada5`
- 登记基线提交：`65ec907c061b743784acc568ec5304581351b6fb`
- 检查点：M0

## 本阶段交付

- 目标：完成任务签收、工作项与工作树核验、core + life-navigation overlay 起飞检查单、随机治理考试和平台/模块两层依赖验证；完成后停止，等待平台 Go/No-Go。
- 修改路径：
  - `docs/project-management/modules/life-navigation/task-receipt.md`
  - `docs/project-management/modules/life-navigation/certification/IR-20260711-LIFE-APPLICATION-HISTORY-checklist.json`
  - `docs/project-management/modules/life-navigation/certification/exams/IR-20260711-LIFE-APPLICATION-HISTORY-exam-attempt-1.json`
  - `docs/project-management/modules/life-navigation/certification/checklists/IR-20260711-LIFE-APPLICATION-HISTORY-M0-R1-checklist.json`
  - `docs/project-management/modules/life-navigation/certification/exams/IR-20260711-LIFE-APPLICATION-HISTORY-M0-R1-exam-attempt-1.json`
  - `docs/project-management/modules/life-navigation/LN-M0-001-handoff.md`
- 未修改的受保护路径：`app/src/`、`contracts/`、`scripts/`、任务通知书及所有其他模块；未修改任何业务代码。
- 工作项与隔离结论：`AIW-20260711-LIFE-APPLICATION-HISTORY` 为生命导航二负责人的唯一活动工作项；分支和工作树与登记一致；编辑前工作树干净；当前 HEAD 是登记基线的后代；M0 修改均位于允许目录。
- 接口或契约差异：无；固定 GET/POST、本人归属和幂等契约未作修改。
- 原异常记录：`IR-20260711-LIFE-APPLICATION-HISTORY` 检查单和 `EX-20260711-LIFE-APPLICATION-HISTORY-1` 试卷原样保留作为历史异常证据。原检查单 `completed_at=2026-07-10T16:22:00Z` 晚于原试卷 `generated_at=2026-07-10T16:18:41.8073233Z`，但原试卷绑定最终检查单 SHA-256，时间证据自相矛盾；二者不得用于 M0 授权。
- 补正起飞检查单：`FC-20260711-LIFE-APPLICATION-HISTORY-M0-R1`，`record_id=IR-20260711-LIFE-APPLICATION-HISTORY-M0-R1`，31 项 core + life-navigation overlay 已重新逐项全文读取并记录当前 SHA-256。真实 UTC 时序为 `created_at=2026-07-10T16:21:47.3598625Z`、全部 `checked_at=2026-07-10T16:22:47.1119493Z`、`completed_at=2026-07-10T16:23:07.6676601Z`；检查单 SHA-256 为 `24193cab8311f590268d02239fe1dbb7bca5c548c0333424036b37042cf7bd73`。
- 补正随机考试：只在新检查单完成并验证后生成 `EX-20260711-LIFE-APPLICATION-HISTORY-M0-R1-1`；`generated_at=2026-07-10T16:23:33.4428012Z`、`completed_at=2026-07-10T16:23:44.4506784Z`，attempt 1，8/8，score 100，status `passed`；绑定的新检查单 SHA-256 与上项一致，未读取题库 `correct_option`，无失败卷或补考。
- 平台依赖结论：development Go。生命导航声明的 10 项 v1 平台能力均存在、版本满足，状态均为 `verified` 或 `deployed`，注册表和证据路径验证通过。
- 内部依赖结论：`development_readiness=go`；`acceptance_readiness=partial-go`。后者反映历史 UI 尚未实现，属于 M1-M4 后续工作，不阻塞 M0，但不得据此宣称验收 Go。
- 自动化命令与结果：
  - `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/Test-AgentDevelopmentPreflight.ps1`：`status=ready`。
  - `python -X utf8 scripts/validate_development_checklists.py contracts/foundation/development-checklist.v1.schema.json docs/project-management/modules/life-navigation/certification/checklists --project-root . --require-current`：通过，补正检查单完整且治理哈希当前一致。
  - `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/New-AgentGovernanceExam.ps1 ...`：生成 attempt 1。
  - `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/Submit-AgentGovernanceExam.ps1 ... -AnswersCsv A,B,B,B,B,C,B,C`：补正试卷通过，score 100。
  - `python -X utf8 scripts/validate_governance_exams.py contracts/foundation/governance-exam.v1.schema.json contracts/foundation/governance-exam-bank.v1.schema.json contracts/foundation/governance-exam-bank.v1.json docs/project-management/modules/life-navigation/certification/exams --project-root .`：通过，试卷评分和不可变检查单关联正确。
  - `python -X utf8 scripts/validate_foundation_dependencies.py contracts/foundation/foundation-capabilities.v1.json --project-root . --module contracts/foundation/module-dependencies/life-navigation.v1.json`：通过。
  - `python -X utf8 scripts/validate_module_internal_dependencies.py contracts/foundation/module-internal-dependencies.v1.schema.json contracts/modules/life-navigation/internal-dependencies.v1.json --project-root .`：通过。
- 测试环境证据：M0 不部署、不访问测试环境；不适用。
- 发现的问题与根因状态：
  - 平台初次复核 No-Go 的根因是首次执行时先生成并提交考试，后以手工预设的未来 `completed_at` 完成检查单，造成“考试早于检查单完成”，同时试卷 SHA-256 又指向最终检查单的自相矛盾证据。该做法违反真实时间与先完成检查单再考试的顺序要求；原证据已明确撤销授权效力但保持不可变。
  - 另一次工具问题是把检查单与考试 JSON 混放同一验证输入目录，验证器把全部 `*.json` 当作试卷而产生 `PermissionError`；根因是输入目录混放，现按 `certification/checklists/` 与 `certification/exams/` 分目录保存。
- 防复发措施：
  - 所有时间只在动作发生时使用 `[DateTime]::UtcNow.ToString('o')` 获取，不预填未来时间，不从预计时间推导证据时间。
  - 检查单分两步完成：全文重读后先写每项 `checked_at`，随后获取更晚 UTC 单独写 `completed_at`；通过 `--project-root . --require-current` 验证后才运行出题脚本。
  - 每次提交前机器比较 `created_at <= checked_at <= completed_at(checklist) < generated_at(exam) <= completed_at(exam)`，并核对试卷 `checklist_sha256` 等于新检查单当前 SHA-256。
  - checklist 与 exams 使用独立目录；验证命令固定使用 `--project-root`，不使用不存在的 `--repo-root`。
- 未完成和风险：M0 尚待平台集成负责人复核并签发 `LN-M0-001 Go/No-Go`；当前不得进入 M1。acceptance 仍为 Partial Go。
- 下一阶段拟做内容：仅在平台签发 `LN-M0-001 Go` 后，按通知进入 M1 接口事实与适配设计；本次提交不提前执行。

## 平台抽查

- 复跑命令：
  - `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/Test-AgentDevelopmentPreflight.ps1`
  - `python -X utf8 scripts/validate_development_checklists.py contracts/foundation/development-checklist.v1.schema.json docs/project-management/modules/life-navigation/certification/checklists --project-root . --require-current`
  - `python -X utf8 scripts/validate_governance_exams.py contracts/foundation/governance-exam.v1.schema.json contracts/foundation/governance-exam-bank.v1.schema.json contracts/foundation/governance-exam-bank.v1.json docs/project-management/modules/life-navigation/certification/exams --project-root .`
  - `python -X utf8 scripts/validate_foundation_dependencies.py contracts/foundation/foundation-capabilities.v1.json --project-root . --module contracts/foundation/module-dependencies/life-navigation.v1.json`
  - `python -X utf8 scripts/validate_module_internal_dependencies.py contracts/foundation/module-internal-dependencies.v1.schema.json contracts/modules/life-navigation/internal-dependencies.v1.json --project-root .`
  - `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/Test-TextEncoding.ps1`
  - `git diff --check`
- 代码/接口抽查：未修改业务代码和公共契约，变更仅模块文档。
- 证据完整性：补正 record 时序与哈希一致，原异常证据保留且不授权。
- 结论：Go
- No-Go 必须修复项：已完成。
- 是否授权进入下一阶段：是，仅授权 M1 接口事实与适配设计。
- 平台复核人及时间：服务广场平台集成负责人，`2026-07-11T00:32:19+08:00`
