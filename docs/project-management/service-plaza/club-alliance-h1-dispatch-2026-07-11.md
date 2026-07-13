# 俱乐部联盟 CA-H1 派发与差距复核

日期：2026-07-11  
基线：`e1dc1e28a97a36d1b85cae1aedebaee808d3d0fe`（SP-H025 H0 Full Go）

## 当前差距

- `App.tsx` 没有 Club Alliance 精确路由，当前进入通用 `CoreServicePage`。
- 通用页面会读取俱乐部列表和提交加入理由，违反 H1 零业务 API 边界。
- `category` 只是原始字符串，没有 action_id 唯一解析、失败关闭或重放测试。
- `ServicePlazaPage` 仍维护四 action_id 本地数组；需与新首页共用 adapter。
- 现有管理视图和联调状态切换器不能证明真实目录、权限和生命周期状态。
- 尚无四入口派生、打乱排序、管理排除、query、遥测、320px 和零业务 API 测试。

可复用且本轮不修改：`ServiceCatalogRepository`、`ServiceAction`、`ActionControl`、action evaluator、telemetry。公共基础不足时另建平台工作项。

## 分段验收

- H1-M0：签收、current checklist、考试 100、依赖与允许路径确认。
- H1-M1：共享 adapter 与纯函数契约；打乱输入、缺失/重复/错误作用域和 query 负例通过。
- H1-M2：独立路由和首页壳；状态、权限、生命周期、遥测、响应式和零业务 API 组件测试通过。
- H1-M3：全量前端测试、type/build、总合同、编码与平台独立复核；提交 Handoff。
- H1-M4：另行授权测试环境部署和真实浏览器 UAT；未授权前不得执行。

## 精确实现路径

只允许 registry 中 `AIW-20260711-CLUB-ALLIANCE-H1-HOMEPAGE` 列出的 13 个前端文件、模块 checklist/exam/IR 目录和 `CA-H1-handoff.md`。不允许 `CoreServicePage`、公共 repository/evaluator/telemetry、backend、deploy 或 Schema。

## Go / No-Go

当前结论：平台治理检查单 26/26、随机考试 100 分、正式通知、差距审计和预登记已完成；待派发提交受控集成并创建专用干净工作树后，以独立 activation commit 将模块工作项从 planned 转 active。
