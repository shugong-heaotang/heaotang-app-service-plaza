# Project Brain v1 M1-CP1 Handoff

日期：2026-07-12  
提交角色：Project Brain 项目负责人 Agent（治理 owner_role：平台集成负责人）  
接收角色：平台集成负责人  
work_id：`AIW-20260712-PROJECT-BRAIN-V1`  
record_id：`IR-20260712-PROJECT-BRAIN-V1-M1-R2`  
结论：M1 首个迁入切片达到项目内 Go，等待平台独立复核；Project Brain v1 整体仍为 No-Go。

## 已完成

- 以权威 integration `f31f67f1613b7c97c9f46969d7c3eb59cdc0e46c` 创建 `codex/project-brain-v1` 专用工作树。
- 登记唯一 Project Brain 工作项及 M1 分段 allowed paths。
- preflight 返回 ready；R2 当前检查单逐项完成；R2 治理考试 attempt 1 为 100 分。
- 首份检查单使用了非规范声明，相关检查单、已通过试卷和预修正实施记录均原样保存在 `contracts/foundation/invalidated-snapshots/project-brain-v1-m1/`；未改写历史证据。
- 迁入唯一入口、产品需求、架构、分阶段计划、验收矩阵及四类事实合约与 Schema。
- 四类合约通过 Draft 2020-12 Schema；全部 JSON 可解析。
- 修正 Nova AI 不存在的候选来源路径，改由当前权威协作登记提供事实来源。
- 所有登记来源路径均在仓库内真实存在；UTF-8 与 `git diff --check` 通过。

## 未完成

- M2 聚合器、治理审计、负向测试及生成快照。
- M3 React 模块、正式内部路由、类型检查、全量测试与构建。
- 手机和桌面浏览器 UAT、键盘与焦点验证。
- 安全审计、独立验收、受控集成和 registry `integrated` 状态。

## 风险

- 当前模块登记是首批静态事实，进入 M2 后必须从权威来源聚合并检查新鲜度，不得变成第二套任务状态。
- Project Brain 将读取共享 registry；只能输出字段白名单，不得向前端复制工作树、账号、令牌或其他敏感字段。
- SC T0 的 `integrated` 仅表示 No-Go/Remediation 证据收口，不代表 T0 Go；本切片未修改任何 SC remediation 文件。

## 下一授权

请平台集成负责人独立复核 M1 的入口唯一性、Schema、来源真实性、路径范围和治理证据。复核 Go 后，授权把 `scripts/build_project_brain.py`、`scripts/validate_project_brain.py`、`scripts/tests/test_project_brain.py` 加入下一段 allowed paths，推进 M2。
