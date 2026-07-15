# 保障商城 P0/P1 产品化 Handoff

状态：runtime integrated；shared route/CI candidate ready for independent review。

当前只授权模块运行时首检查点。共享路由、CI、后端路由、数据库、写操作、支付、真实数据、部署和上线均未随本文件自动授权。

## Runtime 候选结论

- 严格消费 `mall.catalog.v1`，拒绝版本漂移、额外字段、责任映射错误、不安全金额、重复标识和非法俱乐部保障权益。
- 所有网络访问只经过共享 `businessApiAdapter`；未登录不发请求，卸载或切换场景会取消旧请求。
- 页面覆盖 loading、empty、ready、error，错误不使用示例商品兜底，并保留请求编号和可聚焦重试入口。
- 请求序号隔离迟到响应，加载期间抑制同一场景重复请求。
- 价格使用 BigInt 按币种标准 minor-unit 位数拆分，不先转换为浮点主单位，最大安全整数保持精确。
- 场景按钮具有 `aria-pressed`、键盘激活、可见焦点和至少 44px 触控高度；结果区提供 live/busy 语义。

## 验证证据

- 模块测试：3 files / 18 tests passed。
- APP 全量回归：26 files / 249 tests passed。
- 生产构建：`tsc -b && vite build` passed。
- 当前 implementation record：`IR-20260715-PROTECTION-MALL-P0-P1-RUNTIME-R3`。

## Platform Wiring 候选证据

- 精确路由 `/services/protection-mall` 位于通用 `/services/:serviceKey` 之前。
- 路由测试：`App.test.tsx` 8/8 passed；证明真实目录信封、独立页面和共享 Authorization。
- APP 全量回归：26 files / 250 tests passed。
- 生产构建：`tsc -b && vite build` passed。
- APP quality CI：锁文件安装、全量测试、生产构建、UTF-8；最小权限 `contents: read`。
- 当前 implementation record：`IR-20260715-PROTECTION-MALL-P0-P1-PLATFORM-WIRING`。

## 下一检查点

1. Runtime source `6ea6be4` 已获 Independent Go，并由 `d8c6b9a`、`a1f0763` 受控集成。
2. Platform Wiring 已在通用 `:serviceKey` 之前挂载 `/services/protection-mall`，并以真实 `mall.catalog.v1` 信封验证路由、共享会话和非通用页边界。
3. `.github/workflows/app-quality.yml` 使用 Node 20 和锁文件安装，执行全量测试、生产构建及 UTF-8 门禁。
4. Platform Wiring 仍须 Independent Go 后受控集成；HTTP 目录路由未实现时，真实页面必须保持可恢复错误态，不得伪造成功目录。

## 持续 No-Go

后端路由、数据库、订单、写操作、支付、资金、退款、真实权益发放、真实数据、测试服部署、生产发布与运营仍为 No-Go。
