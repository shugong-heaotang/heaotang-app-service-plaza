# Project Brain v1 正式任务通知书

- work_id：`AIW-20260712-PROJECT-BRAIN-V1`
- owner：Project Brain 项目负责人 Agent
- governance owner_role：`平台集成负责人`（仅用于本工作项受保护治理路径；产品与交付职责仍由 Project Brain 项目负责人承担）
- base：`f31f67f1613b7c97c9f46969d7c3eb59cdc0e46c`
- branch：`codex/project-brain-v1`
- worktree：`C:/Users/shugo/Documents/worktrees/heaotang-project-brain-v1`
- 风险等级：高
- 当前 record_id：`IR-20260712-PROJECT-BRAIN-V1-M1-R3`

## 目标

建立全 APP 统一知识入口、权威事实模型、自动治理检查和项目负责人只读驾驶舱。现有预集成成果是迁入基础，不得无理由重写。

## 当前授权：M1-CP1

只迁入：

- 根入口 `PROJECT-BRAIN.md`；
- `docs/project-management/project-brain/` 下的需求、架构、计划、验收和 Handoff；
- `contracts/project-brain/` 下四类事实合约、Schema 与示例。

完成定义：入口不复制动态任务状态；四类 JSON 通过 Draft 2020-12 Schema；引用路径真实且位于仓库内；未知和缺证据信息失败关闭；不修改现有业务路由。

## 明确禁止

- 不修改任何 SC remediation 文件；
- 不把 SC T0 的 `integrated` 解释为 T0 Go；
- 不读取、复制或展示秘密、账号、手机号、健康明细或支付明细；
- 不建立第二套任务状态台账；
- 当前检查点不修改 `scripts/`、`app/`、现有路由或生产配置；
- 不自行合并受保护路径。

## 阻塞边界

M1 未 Go 时阻塞 M2/M3/M4；不阻塞 SC remediation、俱乐部、健康、生命导航及其他非重叠工作。M1 完成后由平台集成负责人复核并授权扩展下一段 allowed_paths。

## 状态期限与下一检查点

激活后应在本检查点内形成 checklist、100 分考试、迁入验证、implementation record 和 Handoff。下一检查点为 M2 只读聚合器与治理审计，需另行授权。
