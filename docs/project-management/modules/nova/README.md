# NOVA 第五阶段项目入口

项目 ID：`nova`  
父项目：和奥堂 APP  
承接角色：Codex platform integration agent（平台集成负责人）  
当前工作项：`AIW-20260712-NOVA-M1-RUNTIME`

## 目标

先建立 NOVA 可独立测试和恢复的任务运行底座与版本化公共工具契约，再随人脉、活动等真实业务能力成熟逐项接入闭环；APP 上线前完成综合智能化验收。

## 当前范围

当前仅执行 M0 起飞认证：签收任务、声明真实依赖、完成平台 preflight、逐项读取当前检查单、通过 8/8 随机治理考试并提交 M0 Handoff。

## 非目标

- M0 不实现 `/api/nova/chat`、任务状态机、工具网关或任何业务代码。
- M0 不修改既有公共契约。
- 本项目不代替人脉、活动或消息负责人实现其内部业务。
- mock 证据不代表真实业务闭环或上线验收 Go。
- 不接触生产数据、真实资金、生产凭据或不可逆操作。

## 必读顺序

1. 根目录 `AGENTS.md`。
2. 根目录 `README.md` 第 0 节及其完整权威阅读链。
3. `docs/project-management/notices/2026-07-12-nova-m1-task-order.md`。
4. 本 README。
5. `contracts/modules/nova/platform-dependencies.v1.json`。
6. `contracts/modules/nova/internal-dependencies.v1.json`。
7. 当前任务新生成的起飞检查单、随机治理考试与 M0 Handoff。

## 当前门禁

- 平台依赖 `development_readiness`：`go`。
- NOVA 内部依赖 `development_readiness`：`no-go`；M1 实现仍须项目最高负责人另行签发 Go。
- 当前检查点：M0 起飞认证。
- M0 未经项目最高负责人验收为 Go，禁止进入 M1 业务实现。

## 下一检查点

提交 M0 Handoff，列明精确变更、命令结果、风险、`blocks` 与 `does_not_block`，等待项目最高负责人裁决 `NOVA-M0-001`。
