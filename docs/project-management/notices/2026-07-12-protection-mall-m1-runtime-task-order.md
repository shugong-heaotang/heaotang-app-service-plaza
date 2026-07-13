# 保障商城 M1 领域运行内核派发任务书

日期：2026-07-12

本任务书建立两个互不重叠的工作包；二者均须从本任务书受控集成后的权威基线创建干净工作树并完成各自 preflight 后才可 active。

## 工作包 A：后端领域内核

- work_id：`AIW-20260712-PROTECTION-MALL-M1-DOMAIN-CORE-BACKEND`
- owner：Backend platform agent（平台后端负责人）
- repository：`C:/Users/shugo/Documents/heaotang-main`
- branch：`codex/protection-mall-m1-domain-core`
- worktree：`C:/Users/shugo/Documents/worktrees/heaotang-protection-mall-m1-domain-core`
- allowed paths：仅商城 Go 领域核、新建同目录单元测试与同仓 README/治理入口所要求的最小证据路径；精确文件须在激活提交中按实际仓库路径冻结。

范围：只实现内存领域核及单元测试，覆盖责任校验、库存/订单/履约/售后/权益回滚五状态机、scope 与资源归属、幂等判定、稳定错误，以及乱序、并发、补偿回归。

## 工作包 B：APP 跨仓证据伴随项

- work_id：`AIW-20260712-PROTECTION-MALL-M1-DOMAIN-CORE-EVIDENCE`
- owner：Codex platform integration agent（平台集成负责人）
- repository：`C:/Users/shugo/Documents/APP系统`
- branch：`codex/protection-mall-m1-domain-core-evidence`
- worktree：`C:/Users/shugo/Documents/worktrees/heaotang-protection-mall-m1-domain-core-evidence`
- allowed paths：任务 Handoff、模块 checklist/exam/IR、跨仓合同映射及对应协作登记条目；不得修改后端源码。

## 禁止事项

禁止路由、数据库/迁移、支付、真实资金、回调、退款、对账、部署、真实数据、Nova 推荐、跨模块组合订单和 GraphRAG。任何一个工作包的 Go 均不授权上述事项。

## 激活条件

平台派发提交已进入权威集成基线；两个实际工作树存在、干净，且 `HEAD=base=merge-base`；协作登记精确列出每项 allowed paths 后，才可从 planned 变为 active。
