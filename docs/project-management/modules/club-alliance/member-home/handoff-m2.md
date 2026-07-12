# H2-M2 真实数据前端挂载 Handoff

- 提交人：Club Alliance frontend agent
- 接收人：平台集成负责人
- 提交时间：2026-07-12
- Gate：当前 checklist completed；治理考试 100 分；前端定向测试与生产构建通过；平台兼容测试 Pending。

## 已完成

- 无 query 的 `/services/club-alliance` 使用共享会话加载 `GET /api/v1/clubs/member-home`。
- guest 直接进入 unauthorized，禁止发会员业务请求；已认证用户只调用严格聚合 adapter。
- `category`、`view=manage` 与非法 query 全部保留 H1 原解析、lifecycle 和 access evaluator。
- 探索入口严格从 action catalog 派生；管理入口只由后端 `can_manage` 决定。
- 覆盖 loading/ready/empty/partial-error/error/unauthorized/maintenance/offline；未知 section key、非字符串错误、畸形 DTO 全部失败关闭。
- `section_errors` 只接收后端稳定字符串码作为发生标志，不向用户透传其内容；前端映射固定安全消息，避免内部错误内容泄露。

## 独立门禁结果

- 定向 Vitest：3 files / 62 tests，全部通过。
- 全量 Vitest：22 files / 215 tests，214 通过、1 失败；唯一失败为未授权 `App.test.tsx:113` 仍断言无 query 展示旧 H1 标题，与批准的 H2 会员首页变更冲突。
- 生产构建：`tsc + vite` 通过，65 modules。
- `git diff --check`：通过。
- 当前结论：**Pending platform compatibility test**；不得标为 verified。

## 未完成

- 由平台主管在授权范围内更新平台兼容测试，前端负责人不修改 `App.test.tsx`。
- 后端 endpoint 的真实提交、测试环境部署和四身份 M3 UAT 不在本前端提交中。

## 变更范围

- `app/src/modules/club-alliance/member-home/`
- `app/src/modules/club-alliance/ClubAlliancePage.tsx`
- `app/src/modules/club-alliance/ClubAllianceRoute.tsx`
- `app/src/modules/club-alliance/ClubAlliancePage.test.tsx`
- 本 Handoff 与同 record_id 治理/实施记录。

## 回滚

- 回滚本前端提交即可恢复 H1 分类导航首页；不涉及后端、数据迁移、部署或生产写入。
