# 俱乐部联盟 CA-H1 M4 验收执行记录

- work_id：`AIW-20260711-CLUB-ALLIANCE-H1-M4-ACCEPTANCE`
- branch/worktree：`codex/club-alliance-h1-m4-acceptance` / `C:/Users/shugo/Documents/worktrees/heaotang-club-h1-m4-acceptance`
- base：`91547b3db4a8a92537ff19193f2e2a6740318ccd`
- 当前阶段：部署 Pass；`CA-H1-M4-B001` 与 `CA-H1-M4-B002` 均 resolved；浏览器 UAT 仅剩真实 Enter/Shift+Tab 证据，M4 继续 In Progress / No-Go。
- 证据：`docs/project-management/modules/club-alliance/acceptance/CA-H1-M4-frontend-uat.md`。

本工作项只验收标准首页/页面壳，不调用 club search/create/join/member 等业务 API。网络证据分别记录模块 catalog/actions、APP 公共 feature-flags 和业务 denylist；部署、备份、回滚、浏览器、权限、遥测和八态未全部闭环前不得判 M4 Go。

`CA-H1-M4-B001` 已由 backend `c4319c206add11f92d763b13b63be8ab2e47679e` 和 APP evidence `ee8dec915ed890ed9fdc732fa6eacb1c3902ed3e` 关闭；测试环境通过不同管理员双审启用。公益、自建、家庭、友联体四分类的 guest blocked 均已取得页面/Nginx/数据库三方证据，稳定为 `blocked / authentication_required / user_id=null`，且未调用俱乐部业务 API。合法合成普通会员的四分类 activated、管理 blocked/scope_required，以及 B002 修复后的点击不导航和 direct `unauthorized/scope_required` 均已完成。M4 尚未 Go 的唯一原因是真实键盘证据未取得。

导航增量：合法 category 刷新重放、浏览器后退、顶部和主体两个返回服务广场入口均已通过；最近俱乐部页面 Nginx 窗口只出现 catalog/actions、APP 全局 feature-flags 与 action-events，业务 denylist=0。Enter 与 Shift+Tab 因应用内键盘通道未触发默认行为、Windows 通道又被 URL 安全校验停止而保留为未验证，不推断为产品失败。M4 verdict 继续 `In Progress / No-Go`。

登录根因已精确到合法会话前提：受支持浏览器没有已登录标签；candidate A 当日额度已满，candidate B 容量为 `used=0 / remaining=5` 且服务端权威关系证明其没有 `club:manage`。最小解阻是经明确授权后仅对 candidate B 发送一次验证码，在浏览器完成普通会员登录，随即采集四分类 activated 与管理中心 scope_required 三方证据；禁止换号、清计数、调整限流或注入 token。其余不依赖登录的 M4 项不受阻塞且不得重复。

一次性授权已执行：candidate B 登录成功，四分类页面 active/focused 且事件均为 `activated/none/user_id=non-null`；管理中心事件正确为 `blocked/scope_required/user_id=non-null`。但管理 URL `?view=manage` 仍显示标准首页和 active 管理链接，没有呈现 scope_required 页面。根因是 `ClubAllianceRoute` 未解析 management view，现有测试也只覆盖 category 权限。登记 `CA-H1-M4-B002` Blocker，必须用独立前端工作项关闭后再重部署/复测；M4 继续 No-Go。

## 2026-07-11 B002 修复部署增量

- 权威 integration：`004800f6fec01c3a31a769dbf3d9d12830683a3f`，提交内容为 `fix(club-alliance): fail manage view closed`；本地及远端权威 integration/修复分支均指向该提交。
- 修复记录证明定向 3 files / 61 tests、前端全量 18 files / 155 tests、production build 和 test-server build 通过。环境证据与自动化证据分开记录。
- 本轮部署日志记录：remote backup `/root/heaotang-backups/20260711-194454.tar.gz`，local backup `D:/Backup/heaotang-test-server/20260711-194454/test-server-state.tar.gz`，rollback target `/var/www/heaotang/app/service-plaza.rollback-20260711-194451`，deployed asset `assets/index-CPIj0Kh9.js`。
- 本组只读交叉验证：本地备份存在且归档可读；公开页面当前引用 `assets/index-CPIj0Kh9.js`；`/ready` 为 `ready / db=true / plugins=24`，`/health?json=1` 为 `ok / db.connected=true / plugins=24`。
- 平台主线部署后浏览器只读证据：首页仍保持四入口既定顺序、独立管理 complementary 和两个 `/app/service-plaza/services` 返回入口；guest direct `?view=manage` 显示“需要登录或相应权限”“管理中心当前不可访问”及 `authentication_required`，可返回俱乐部联盟首页。该证据证明 guest 登录承接路径未回归，但不替代已登录缺 scope 的 `scope_required` 复验。
- 同一回合仅出现浏览器控制层 `ab.chatgpt.com` Statsig timeout，页面 DOM 正常；该流量不是 APP 网络请求，继续按控制层噪声记录。
- 当前状态：`CA-H1-M4-B002` 为 `Verified / Closed`。一次性授权的合成普通会员会话完成复验：点击管理中心保持原首页，Nginx `POST action-events` HTTP 200，权威事件为 `blocked/scope_required/user_id=non-null`；direct `?view=manage` 为 `unauthorized/scope_required` 并明确缺少 `club:manage`。
- M4 唯一关闭条件：人工在已知测试 URL 完成一次 Shift+Tab 焦点回退和一次 Enter 激活，记录焦点、focus-visible 与 URL 前后；不得用脚本 click 或合成事件替代。

## 2026-07-12 最终证据收口状态

- 最终治理快照：`FC-20260712-CLUB-H1-M4-FINAL` 26/26，考试 `EX-20260712-CLUB-H1-M4-FINAL-1` score 100。
- B002 收口：`IR-20260712-CLUB-H1-M4-MANAGE-GUARD-CLOSEOUT`，实现/部署/页面/Nginx/只读事件均已验证。
- 重复键盘证据问题登记为 `RI-BROWSER-UAT-KEYBOARD-CONTROL`：应用内三类键盘通道未产生默认行为；Windows 原生通道连续两次因无法高置信确认 Chrome URL被安全策略停止。
- 当前没有产品 Blocker；存在一个证据 Blocker。人工键盘 UAT 完成前不得把 M4、SP-H029 或健康 M0 自动激活条件标为通过。
- does not block：既有四分类 guest、响应式、query、刷新/后退/双返回、网络 denylist 与自动化八态证据无需重复。Enter 与 Shift+Tab 保持控制通道未验证。
