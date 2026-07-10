# 生命导航阶段 Handoff：LN-M3-001

- 验收单号：`LN-M3-001`
- 通知编号：`LN-TASK-20260710-001`
- 提交负责人：生命导航二负责人
- 提交时间：`2026-07-11T01:13:14+08:00`
- 当前分支与基线提交：`codex/life-navigation-application-history` / `9a2717f`
- 检查点：M3
- 实现记录：`IR-20260711-LIFE-APPLICATION-HISTORY-M3`
- 当前结论：M3 最终 Go；平台路由接线与独立复核完成，已授权按治理入口进入 M4，但 M4 尚未开始

## 本阶段交付

- 新增模块本地 `LifeNavigationPage`，复用共享 `AuthProvider/useAuth`、`AuthPanel`、`AppFrame` 和 `Link`；未登录时直接进入真实验证码登录交接，不提供模拟联调状态切换。
- 生产默认 API 直接包装 M2 的 `loadLifeNavigationApplicationHistory` 与 `submitLifeNavigationApplication`；仅为组件测试开放窄 `LifeNavigationPageApi` 注入，不在生产代码中放置假数据。
- 登录后自动加载本人申请历史，覆盖 `loading / empty / ready / error + retry`；列表只展示“已提交”、提交时间和申请说明，不暴露内部 ID、维度或虚构审核状态。
- 申请表单覆盖提交中、created、replayed、每日上限、幂等处理中、幂等冲突、认证失效、网络/超时和未知错误；created/replayed 后刷新历史。
- 认证失效会清理共享会话并回到真实登录入口；历史 GET 使用 `AbortController`，组件卸载时终止读取。
- 返回动作固定到 `/services`；`index.ts` 已导出页面、页面 props 和窄 API 类型，供平台路由层接线。
- 修改路径：
  - `app/src/modules/life-navigation/LifeNavigationPage.tsx`
  - `app/src/modules/life-navigation/LifeNavigationPage.css`
  - `app/src/modules/life-navigation/LifeNavigationPage.test.tsx`
  - `app/src/modules/life-navigation/index.ts`
  - `docs/project-management/modules/life-navigation/certification/checklists/IR-20260711-LIFE-APPLICATION-HISTORY-M3-checklist.json`
  - `docs/project-management/modules/life-navigation/certification/exams/IR-20260711-LIFE-APPLICATION-HISTORY-M3-exam-attempt-1.json`
  - `docs/project-management/modules/life-navigation/implementation-records/IR-20260711-LIFE-APPLICATION-HISTORY-M3.json`
  - `docs/project-management/modules/life-navigation/LN-M3-001-handoff.md`
- 明确未修改：`app/src/App.tsx`、`app/src/pages/CoreServicePage.tsx`、共享 `app/src/auth/`、`app/src/components/`、`app/src/infrastructure/`、共享样式、后端、contracts、scripts 和 M0/M1/M2 历史证据。

## 起飞认证

- checklist：`IR-20260711-LIFE-APPLICATION-HISTORY-M3`，31 项重新全文读取；`created_at=2026-07-10T17:06:14.8274421Z`、统一 `checked_at=2026-07-10T17:07:38.6997392Z`、`completed_at=2026-07-10T17:08:16.0798347Z`。
- exam：`EX-20260711-LIFE-APPLICATION-HISTORY-M3-1`，attempt 1，8/8，score 100，status `passed`；`generated_at=2026-07-10T17:08:47.2017694Z`、`completed_at=2026-07-10T17:08:58.0026676Z`。
- 当前清单单独复制到受控临时目录后使用正式 Schema 与 `--require-current` 校验通过，临时目录已安全删除；历史清单未被改写。
- 治理考试快照校验通过，试卷绑定不可变已完成清单。

## 自动化与测试证据

- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/Test-AgentDevelopmentPreflight.ps1`：`status=ready`。
- `npm test -- --run src/modules/life-navigation/LifeNavigationPage.test.tsx src/modules/life-navigation/lifeNavigationApi.test.ts src/modules/life-navigation/LifeNavigationModule.test.tsx`：3 个测试文件、31 项通过。
- `npm test`：15 个测试文件、90 项通过。
- `npm run build`：TypeScript 与 Vite production build 通过。
- `python -X utf8 scripts/validate_implementation_records.py contracts/foundation/implementation-record.v1.schema.json docs/project-management/modules/life-navigation/implementation-records --project-root .`：通过，引用证据路径存在。
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/Test-ServicePlazaContracts.ps1`：通过，含依赖、协作、清单、考试、实施记录和工具链门禁。
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/Test-TextEncoding.ps1`：通过，446 个文件符合编码规则。
- `git diff --check`：通过。
- `git status --short` 路径审计：仅包含 4 个 `app/src/modules/life-navigation/` 文件和 4 个 `docs/project-management/modules/life-navigation/` M3 证据文件，无越界修改。
- 组件测试覆盖未登录真实交接、loading/abort、empty、历史列表、created、replayed、每日上限、处理中/冲突/网络/未知错误、认证失效、错误恢复和 `/services` 返回路径；M2 API 与模块契约测试继续保留。

## 问题闭环

- 首次生产构建发现三个测试 mock 的 `status` 字面量被 TypeScript 拓宽为 `string`，导致测试文件不能满足 `LifeNavigationHistoryState` 判别联合类型。根因是 mock 未显式携带 `LifeNavigationPageApi["loadHistory"]` 签名；已为相关 mock 增加精确函数类型并重新执行定向测试与构建，两者通过。未弱化产品类型或测试门禁。
- 未发现路由或认证边界阻塞。共享认证失效处理使用 `logout()`，不复制 token 管理；页面路由接线由平台层完成。

## 平台接线与验收边界

- 本分支只导出 `LifeNavigationPage`，**没有修改平台 `App.tsx` 或 `CoreServicePage`**。
- 平台负责人仍须把 `/services/life-navigation` 精确路由到 `LifeNavigationPage`，并复跑路由级测试、构建与真实认证集成检查。
- 在平台完成接线前，`LN-M3-001` 只能视为“模块交付待集成”，不得记录平台最终 Go，也不得声称浏览器入口已切换到新页面。
- 本阶段完成后停止，不进入 M4，不部署测试环境，不执行真实登录 UAT。

## 平台抽查

- 证书复核：M3 当前 checklist 31 项完整、哈希与治理输入一致；随机治理考试 attempt 1 为 8/8、score 100，清单和考试关联校验通过。
- 定向复跑：`npm test -- --run src/modules/life-navigation/LifeNavigationPage.test.tsx src/modules/life-navigation/lifeNavigationApi.test.ts src/modules/life-navigation/LifeNavigationModule.test.tsx`，3 个测试文件、31 项通过。
- 构建复跑：`npm run build` 通过，TypeScript 和 Vite production build 无错误。
- 代码审查：页面生产默认使用 M2 真实 API；测试替身只经窄接口注入；共享认证、应用框架和返回路由契约复用正确；错误映射、成功后历史刷新和卸载读取取消均有组件测试；未修改 `App.tsx`、`CoreServicePage.tsx`、共享基础设施、后端或公共契约。
- 结论：Partial Go（仅模块）。
- No-Go 必须修复项：`/services/life-navigation` 尚未精确路由到 `LifeNavigationPage`；平台接线和路由级验证完成前不得签最终 Go。
- 是否授权进入下一阶段：否，不得进入 M4。
- 平台复核人及时间：服务广场平台集成负责人，`2026-07-11T01:16:33+08:00`。

## 平台路由集成后最终复核

- 平台集成提交：`be1b26aab5e85fe63c4494689e1b6551a4417718`（`fix: route life navigation page`）。
- 平台证据：`IR-20260711-LIFE-M3-ROUTE-INTEGRATION` 和 `SP-H010` 均存在、引用路径完整；平台路由集成清单状态为 `completed`，随机治理考试 attempt 1 为 8/8、score 100、status `passed`。
- 路由与代码审查：
  - `AppRoutes` 将 `/services/life-navigation` 精确映射到导出的 `LifeNavigationPage`，并置于 `/services/:serviceKey` 动态路由之前。
  - 从 `/services` 标准目录点击生命导航进入模块页面，不再落入通用临时承接页，也不展示联调状态切换。
  - 路由测试未注入页面假 API，而是经过页面生产默认值调用 M2 `loadLifeNavigationApplicationHistory` 与 `submitLifeNavigationApplication` 边界。
  - 生命导航请求序列精确为 `GET /api/v1/life-nav/records?limit=30`、`POST /api/v1/life-nav/records`、成功后再次 `GET /api/v1/life-nav/records?limit=30`，证明提交后刷新本人历史。
  - 页面底部返回动作导航到 `/services`，路由级测试确认重新显示服务广场。
- 生命导航二负责人独立复跑证据（基线 `be1b26a`）：
  - `npm test -- --run src/App.test.tsx`：1 个测试文件、4 项通过。
  - `npm test`：15 个测试文件、90 项通过。
  - `npm run build`：TypeScript 与 Vite production build 通过。
  - `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/Test-ServicePlazaContracts.ps1`：通过，含依赖、协作、清单、考试、实施记录和工具链门禁。
  - `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/Test-TextEncoding.ps1`：通过，450 个文件符合编码规则。
  - `git diff --check`：通过。
- 最终结论：Go。M3 的精确入口、真实 M2 API 边界、提交后刷新和返回路径均已形成可复跑的本地路由闭环，先前唯一 No-Go 项已关闭。
- No-Go 必须修复项：无。
- 是否授权进入下一阶段：是；仅授权在新建当前 M4 checklist、重新全文阅读、通过 8/8 及 100 分随机治理考试后进入 M4。
- 阶段边界：本次未进入 M4、未部署测试环境、未执行真实登录或跨用户隔离 UAT；这些证据不得由 M3 本地结果替代。
- 最终复核人及时间：生命导航二负责人，`2026-07-11T01:29:27+08:00`。
