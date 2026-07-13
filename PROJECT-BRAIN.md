# 和奥堂 Project Brain

Project Brain 是和奥堂 APP 的统一知识与项目事实入口。它聚合现有权威文件，不替代任务登记、实施记录、Handoff、ADR 或验收证据。

## 开始位置

1. 开发治理与必读顺序：`README.md`、`AGENTS.md`、`CONSTRAINTS.md`
2. 当前 Agent 工作项：`contracts/foundation/agent-collaboration.v1.json`
3. Project Brain 产品与架构：`docs/project-management/project-brain/README.md`
4. 模块、知识、决策和风险：`contracts/project-brain/`
5. 自动审计输出：`contracts/project-brain/generated/project-brain.audit.json`
6. 项目负责人驾驶舱：开发/测试环境内部路由 `/internal/project-brain`；普通 production 构建默认关闭且不包含快照资产

## 权威规则

- 一个事实只允许一个权威来源。
- 聊天内容、驾驶舱快照和汇总报告都不是原始权威事实。
- 未验证、缺失或过期的信息显示为 `Unknown`、`Partial Go` 或 `No-Go`。
- Project Brain 第一版只读，不执行审批、部署、支付、退款、健康判断或生产数据修改。
- 高风险事项必须保留开发、复核和批准角色分离。

## 更新流程

修改权威事实 → 运行 Project Brain 构建与审计 → 运行治理和编码门禁 → 独立验收 → 更新 Handoff → 受控集成。
