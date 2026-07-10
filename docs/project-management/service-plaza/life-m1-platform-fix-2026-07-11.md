# 生命导航 M1 公共接口根因修复

- 日期：2026-07-11
- ICR：`LN-ICR-20260711-001`
- 实现记录：`IR-20260711-LIFE-M1-PLATFORM-FIX`
- APP 分支：`codex/life-m1-platform-contract`
- 后端分支：`codex/life-m1-backend-contract`
- 当前结论：本地验证 Go；尚未部署测试环境

## 裁决

1. `GET /api/v1/life-nav/records?limit=` 继续以冻结合同 `1..30` 为准。`limit<=0` 或 `limit>30` 使用安全默认 30；扫描当前仓库未发现登记的 `limit>30` 消费者。
2. 共享 API SDK 以向后兼容方式新增 `apiRequestWithMeta<T>()`，返回 `{data, meta}`；原 `apiRequest<T>()` 继续只返回 `T`。
3. `BusinessApiAdapter` 新增可选 `executeWithMeta()`；原 `execute()` 返回形状保持不变。
4. 元数据只暴露稳定且非敏感的 `status`、`requestId`、`idempotencyReplayed`，不向模块暴露 Authorization、原始 Headers 或内部重试状态。
5. 生命导航模块必须继续复用共享 adapter，不得自行调用 `fetch` 读取重放头。

## 根因与修复

| 问题 | 根因 | 修复 |
| --- | --- | --- |
| 固定合同上限 30，后端接受到 100 | 历史通用列表上限未随首切片合同收紧 | 后端统一使用 `maxRecordHistoryLimit=30`，补 0/1/30/31/100/101 边界回归 |
| 模块无法识别 `Idempotency-Replayed` | SDK 只返回信封 `data`，没有建模响应元数据 | 平台新增可选元数据调用，保留旧 API 完全兼容 |
| 缺少显式跨用户历史负向测试 | 既有测试只间接覆盖 SQL 归属 | 新测试同时种入用户 99/88，验证 service 与 handler 只返回会话用户记录 |

## 变更

APP：

- `app/src/infrastructure/apiClient.ts`
- `app/src/infrastructure/apiClient.test.ts`
- `app/src/infrastructure/businessApiAdapter.ts`
- `app/src/infrastructure/businessApiAdapter.test.ts`

后端：

- `backend-go/plugins/life-navigation-plugin/service.go`
- `backend-go/plugins/life-navigation-plugin/service_test.go`
- 提交：`70fa12276e6eac17369c0d1d3c1d23a8e757fcc0`

## 验证

- 前端定向基础设施测试：2 文件、23 项通过。
- 前端全量测试：13 文件、62 项通过。
- `npm run build`：`tsc -b` 与 Vite 构建通过。
- 后端生命导航包 `go test -count=1` 与 `go vet` 通过。
- 后端全量 `go test -count=1 ./...` 与 `go vet ./...` 通过。
- `Test-ServicePlazaContracts.ps1`、`Test-TextEncoding.ps1` 和 `git diff --check` 在交付前复跑。

首次 gofmt 调用因已经位于 `backend-go` 却重复写入 `backend-go/` 路径而未执行；使用正确路径重跑 gofmt、包测试和 vet 后通过。前端工程没有独立 `typecheck` 脚本；按仓库实际 `build=tsc -b && vite build` 完成类型和构建门禁。这两项均为命令口径问题，不是产品缺陷，也未通过跳过检查处理。

## 剩余边界

- 本切片未部署测试环境；M4 集成阶段必须部署 APP 与后端并用真实登录会话验证首次 201、重放 200/元数据、本人历史和跨用户隔离。
- 本次兼容扩展不改变现有消费者；后续生命导航 M2 可使用 `executeWithMeta()`，其他模块按需采用。
