# 保障商城子项目

## 目标

提前启动保障商城持续开发，但不提前承诺上线。M0 只完成正式治理准入、来源审计、服务广场接入卡和 `mall.api.v1` 契约冻结。

## 当前检查点

`M0-CP1`：来源只读盘点、受控迁移矩阵、接入卡、契约冻结提案和平台会签。

## 范围

- 审阅 `C:/Users/shugo/Documents/商城` 中的既有需求、契约、原型和验收材料。
- 只按文件白名单、来源哈希和独立复核迁移。
- 冻结服务入口、API 信封、请求关联、权限、幂等、审计、配置失败关闭和兼容性原则。

## 非目标

- 不编辑交易业务代码。
- 不部署，不接真实支付，不处理真实会员数据。
- 不修改服务广场受保护协议或入口生命周期。
- 不整体迁移本地 Git 历史、脏工作树、构建物、依赖目录或证据制品。

## 必读顺序

1. 根 `AGENTS.md`、`README.md` 和 `CONSTRAINTS.md`。
2. `docs/project-management/notices/2026-07-12-protection-mall-m0-task-order.md`。
3. 本 README、官方方案、来源迁移矩阵、接入卡和契约冻结提案。
4. `contracts/modules/protection-mall/internal-dependencies.v2.json` 与 `mall-api.v1.json`。
5. `docs/project-management/modules/protection-mall/handoff-m0.md`。

## 冻结边界

- `service_id/action_id=protection-mall`
- `route=/services/protection-mall`
- `return_target=/services`
- `session=shared_session`
- `telemetry=service_plaza.protection_mall.open`
- `lifecycle_status=planned`

## 下一授权

M0-CP1 独立验收和平台会签 Go 后，由项目最高负责人另立 M1 精确代码工作项。
