# CA-H1-M4-B002 管理入口权限失败关闭根因修复

日期：2026-07-11
状态：已完成实现、受控集成、测试环境部署与 B002 环境复验

## 现象与根因

测试环境中，合成普通会员点击管理中心后，动作事件正确记录
`club-manage / blocked / scope_required`，但浏览器仍进入 `?view=manage`，页面显示普通首页。

根因由两部分组成：

1. `ActionControl` 对内部 `Link/NavLink` 在权限拒绝后仍允许默认导航。
2. `ClubAllianceRoute` 只解析 category，未解析上游 `club-manage` 的 view target。

## 修复边界

- 只有 `scope_required` 阻止内部链接默认导航；`authentication_required` 继续进入既有承接页。
- 管理 view 从上游动作 target 解析，不新增本地展示真相源。
- direct view 按共享 evaluator 产生 authentication/scope/focused 状态。
- 不修改后端、业务 API、Schema、部署或四类业务逻辑。

## 自动化证据

- 定向：3 files / 61 tests passed。
- 前端全量：18 files / 155 tests passed。
- production build：passed。
- test-server build：passed。
- 首次全量回归发现“阻止所有未授权导航”破坏生命导航承接页，已按
  authentication 与 scope 两类原因分层修正后全量通过。

测试在系统临时隔离仓库镜像执行，使用主仓锁文件对应的现有 `node_modules`；
未修改依赖、锁文件或正式工作树。独立工作树依赖自举缺口另列平台工具后续项，
不在本缺陷范围内临时扩写脚本。

## 集成、部署与环境关闭证据

- 根因修复提交：`004800f6fec01c3a31a769dbf3d9d12830683a3f`，已进入服务广场权威集成基线。
- 测试环境前端资产：`assets/index-CPIj0Kh9.js`；部署前备份、资产哈希、`/health?json=1` 与 `/ready` 已在 M4 验收证据中记录。
- 使用一次性授权的合成普通会员登录，权威关系证明其不具备 `club:manage`；仓库证据仅记录 `authenticated=true`、`scope_present=false`，不保存手机号、OTP、JWT、cookie 或完整用户标识。
- 首页单击管理入口一次后 URL 保持 `/app/service-plaza/services/club-alliance/`，没有默认进入管理 view。
- 同一时窗 Nginx 记录 `POST /api/v1/service-plaza/action-events` HTTP 200；只读事件记录为 `club-manage / blocked / scope_required / user_id=non-null`，未保存 IP 或完整 `user_id`。
- 同一合法会话直达 `?view=manage`，页面稳定为 `data-page-state=unauthorized`、`reason=scope_required`，并明确缺少 `club:manage`；直达本身不额外伪造动作事件。
- B002 的“事件正确但页面仍导航/仍显示首页”因果链已关闭，页面、Nginx 和权威事件三方一致。

## B002 结论与 M4 剩余门禁

`CA-H1-M4-B002` 结论为 **Verified / Closed**。本结论只关闭管理入口权限失败关闭缺陷；M4 仍需独立完成当前检查单、100 分考试、真实键盘 UAT 结论和最终 Handoff，不能由 B002 关闭结论自动推导 H1 Full Go。
