# 俱乐部联盟 CA-H1 M4 验收执行记录

- work_id：`AIW-20260711-CLUB-ALLIANCE-H1-M4-ACCEPTANCE`
- branch/worktree：`codex/club-alliance-h1-m4-acceptance` / `C:/Users/shugo/Documents/worktrees/heaotang-club-h1-m4-acceptance`
- base：`91547b3db4a8a92537ff19193f2e2a6740318ccd`
- 当前阶段：部署 Pass；`CA-H1-M4-B001` resolved；`CA-H1-M4-B002` 已修复、集成并重新部署，环境复验 Pending；浏览器 UAT In Progress / No-Go。
- 证据：`docs/project-management/modules/club-alliance/acceptance/CA-H1-M4-frontend-uat.md`。

本工作项只验收标准首页/页面壳，不调用 club search/create/join/member 等业务 API。网络证据分别记录模块 catalog/actions、APP 公共 feature-flags 和业务 denylist；部署、备份、回滚、浏览器、权限、遥测和八态未全部闭环前不得判 M4 Go。

`CA-H1-M4-B001` 已由 backend `c4319c206add11f92d763b13b63be8ab2e47679e` 和 APP evidence `ee8dec915ed890ed9fdc732fa6eacb1c3902ed3e` 关闭；测试环境通过不同管理员双审启用。公益、自建、家庭、友联体四分类的 guest blocked 均已取得页面/Nginx/数据库三方证据，稳定为 `blocked / authentication_required / user_id=null`，且未调用俱乐部业务 API。登录 activated 与修复前管理 blocked/scope_required 事件已经完成；完整键盘及 B002 修复后的环境复验仍未完成，因此 M4 尚未 Go。

导航增量：合法 category 刷新重放、浏览器后退、顶部和主体两个返回服务广场入口均已通过；最近俱乐部页面 Nginx 窗口只出现 catalog/actions、APP 全局 feature-flags 与 action-events，业务 denylist=0。Enter 与 Shift+Tab 因当前浏览器控制通道未能稳定触发，保留为未验证而不是产品失败。B002 修复后的登录缺 scope 环境复验仍待关闭，M4 verdict 继续 `In Progress / No-Go`。

登录根因已精确到合法会话前提：受支持浏览器没有已登录标签；candidate A 当日额度已满，candidate B 容量为 `used=0 / remaining=5` 且服务端权威关系证明其没有 `club:manage`。最小解阻是经明确授权后仅对 candidate B 发送一次验证码，在浏览器完成普通会员登录，随即采集四分类 activated 与管理中心 scope_required 三方证据；禁止换号、清计数、调整限流或注入 token。其余不依赖登录的 M4 项不受阻塞且不得重复。

一次性授权已执行：candidate B 登录成功，四分类页面 active/focused 且事件均为 `activated/none/user_id=non-null`；管理中心事件正确为 `blocked/scope_required/user_id=non-null`。但管理 URL `?view=manage` 仍显示标准首页和 active 管理链接，没有呈现 scope_required 页面。根因是 `ClubAllianceRoute` 未解析 management view，现有测试也只覆盖 category 权限。登记 `CA-H1-M4-B002` Blocker，必须用独立前端工作项关闭后再重部署/复测；M4 继续 No-Go。

## 2026-07-11 B002 修复部署增量

- 权威 integration：`004800f6fec01c3a31a769dbf3d9d12830683a3f`，提交内容为 `fix(club-alliance): fail manage view closed`；本地及远端权威 integration/修复分支均指向该提交。
- 修复记录证明定向 3 files / 61 tests、前端全量 18 files / 155 tests、production build 和 test-server build 通过。环境证据与自动化证据分开记录。
- 本轮部署日志记录：remote backup `/root/heaotang-backups/20260711-194454.tar.gz`，local backup `D:/Backup/heaotang-test-server/20260711-194454/test-server-state.tar.gz`，rollback target `/var/www/heaotang/app/service-plaza.rollback-20260711-194451`，deployed asset `assets/index-CPIj0Kh9.js`。
- 本组只读交叉验证：本地备份存在且归档可读；公开页面当前引用 `assets/index-CPIj0Kh9.js`；`/ready` 为 `ready / db=true / plugins=24`，`/health?json=1` 为 `ok / db.connected=true / plugins=24`。
- 当前状态：`CA-H1-M4-B002` 为 `Implemented + Deployed / Environment Retest Pending`。上一合法普通会员浏览器会话已不再可用；本组未申请 OTP、未登录、未读取或注入 token/cookie，也未执行浏览器点击。
- 关闭条件：取得合法已登录且缺 `club:manage` 的普通会员会话后，复验点击管理中心不发生默认导航、动作事件为 `blocked/scope_required/user_id=non-null`，并验证 direct `?view=manage` 显示 `unauthorized/scope_required`；页面、Nginx、只读事件三方一致后才能关闭 B002 并裁定 M4 Go。
- does not block：既有四分类 guest、响应式、query、刷新/后退/双返回、网络 denylist 与自动化八态证据无需重复。Enter 与 Shift+Tab 保持控制通道未验证。
