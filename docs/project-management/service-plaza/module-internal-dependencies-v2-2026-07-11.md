# 模块内部依赖 v2 五维门禁

日期：2026-07-11

## 根因与结论

旧 `module-internal-dependencies.v1` 只能表达 development/acceptance 两维 readiness，节点又禁止 owner、blocks 和 does_not_block，无法无损表达 CA-F0/H0 已批准的治理、决策、合同、Handoff 和局部阻塞语义。平台发布并行 `module-internal-dependencies.v2`，不修改历史 v1。

Validator 保持原 CLI：调用方仍传 v1 Schema 路径；工具读取每个实例的 `contract_version`，自动选择同目录 v1 或 v2 Schema。未知版本失败关闭。总合同门禁同时验证三个旧 v1 模块和一个 v2 fixture。

## v2 规则

- `readiness` 必须分别包含 governance、development、acceptance、release、operations。
- 节点必须包含 owner、blocks 和 does_not_block。
- kind 增加 governance、decision、contract、handoff。
- status 支持 planned、pending、accepted、blocked-local 及分阶段证据状态。
- development/acceptance/release/operations 声称 Go 时，validator 检查相应 required 节点状态；证据不足不得提升。

模块采用的正式版本为 `module-internal-dependencies.v2`。旧 v1 文件继续由 v1 Schema 验证，无需迁移。

## 验证

- `python -X utf8 -m unittest scripts.tests.test_validate_module_internal_dependencies -v`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/Test-ServicePlazaContracts.ps1`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/Test-TextEncoding.ps1`

