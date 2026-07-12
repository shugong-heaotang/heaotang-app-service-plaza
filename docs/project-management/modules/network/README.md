# 人脉板块

## 项目定位

人脉板块负责会员发现、引荐请求和连接生命周期。当前工作只冻结唯一 Owner、canonical 读写边界和 legacy 迁移/禁用顺序，不实现接口、不处理真实会员数据、不发送消息。

## 当前结论

- 唯一领域 Owner：`People Network module owner`。
- 搜索读侧：`network-plugin` 只能在 tenant、资源权限和字段可见性加固后作为投影来源。
- 连接写侧：`social-plugin` 的 `introduction_requests` 生命周期是 canonical 目标；当前仅 `code-present-unverified`，未达到 NOVA 可执行条件。
- 统一入口：NOVA 只能调用未来的 People/Connection facade，禁止直连 `network` 或 `social` legacy 写路由。
- `network` 的 introductions/referral/status 写路径立即对 NOVA 标记 `forbidden`，并冻结新增调用方。

## 必读顺序

1. 根 `README.md` 与 `AGENTS.md`。
2. `docs/project-management/notices/2026-07-12-nova-m2-people-tools-task-order.md`。
3. `canonical-implementation-decision.md`。
4. `migration-disable-plan.md`。
5. `contracts/modules/network/internal-dependencies.v1.json`。
6. 当前 checklist、exam、IR 与 `handoff.md`。

## 非目标

- 不修改 `network-plugin`、`social-plugin`、数据库或路由。
- 不迁移或读取真实会员记录。
- 不启用 NOVA M2，不发送真实引荐或连接消息。
- 不把现有 legacy 路径包装成新工具。

## 下一检查点

平台独立复核本决策后，分别派发 facade/tenant/权限实现和 legacy 禁用实现；任何写入实现必须先通过版本化工具契约会签。
