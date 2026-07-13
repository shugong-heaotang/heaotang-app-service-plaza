# 健康大管家精确模块路由平台挂载

- 日期：2026-07-11
- 工作项：`AIW-20260711-HEALTH-ROUTE-MOUNT`
- 实现记录：`IR-20260711-HEALTH-ROUTE-MOUNT`
- 当前结论：本地实现与自动化验证 Go；测试环境尚未部署，健康 M2 仍 No-Go

## 关闭的问题

`/services/health-manager` 原先仅由 `/services/:serviceKey` 通配路由承接，仓库中不存在 `app/src/modules/health-manager` 的稳定挂载边界。健康负责人后续若直接实现模块页面，仍需修改平台 `App.tsx`，会造成板块范围侵入平台受保护路由。

本切片新增精确路由和模块入口：

- `App.tsx` 在通配路由之前显式挂载 `/services/health-manager`；
- `HealthManagerRoute` 固定向通用页面传入 `health-manager` 服务 ID；
- `CoreServicePage` 新增向后兼容的可选 `serviceKeyOverride`，动态俱乐部路由保持原行为；
- 独立模块负责人将来只需替换 `app/src/modules/health-manager` 内部实现，无需改服务广场总路由。

## 范围边界

本切片不实现健康咨询历史、表单字段契约、医疗免责声明或健康业务流程，不修改共享认证、API 适配器、后端和测试服务器。现有通用健康页面行为保持不变；健康 M2 其余前置和测试环境部署证据未完成前继续 No-Go。

## 验证证据

- 定向测试：`2` 个文件、`8` 项测试通过；
- 全量前端：`15` 个文件、`92` 项测试通过；
- `npm run build` 通过；
- `Test-ServicePlazaContracts.ps1` 通过；
- `Test-TextEncoding.ps1` 通过，扫描 `513` 个文件；
- `git diff --check` 通过。

初次测试未执行的根因是新工作树尚无 `node_modules`；按锁文件执行 `npm ci` 后恢复。第二次过滤路径错误是从 `app/` 目录仍使用 `app/src/...`；改用 `src/...` 后通过。两次失败均未计为测试成功。

