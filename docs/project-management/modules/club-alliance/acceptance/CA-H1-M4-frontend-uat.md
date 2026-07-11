# CA-H1 M4 测试环境前端 UAT

## 当前裁定

- 状态：`In Progress / No-Go`。
- 原因：`CA-H1-M4-B001` 已完成根因修复、双人审批、测试环境部署并取得 guest blocked 真实事件；登录允许、登录缺 `club:manage`、其余合法 category、完整键盘与导航证据仍未全部完成。部署成功和单类事件通过不等于 M4 Go。
- 产品 Blocker：未发现页面实现 Blocker。
- 平台 Blocker：`CA-H1-M4-B001` 已 resolved；根因修复和环境启用均使用版本化 business variable 与不同管理员提案/审核，未直接改数据库、未恢复旧单管理员入口。
- 验收通道问题：应用内浏览器控制层向 `ab.chatgpt.com` 发送自身 Statsig 请求时多次 10 秒超时；页面 DOM 与测试服务器访问日志仍正常。该流量不是和奥堂 APP 请求，不计入模块或 APP 网络面。

## 环境与部署

- 日期：2026-07-11（Asia/Shanghai）。
- 测试环境：`https://heaotang.cn`。
- 模块实现提交：`e8c5dd23e7f87ee92f158ba6a719e498ca4eb577`。
- M3 平台集成：`91547b3db4a8a92537ff19193f2e2a6740318ccd`。
- M4 登记提交：`d38e3e796b81fd5aada6b16ca0dec5214bfba446`。
- 前端资产：`assets/index-CfiMm2q0.js`；CSS：`assets/index-CG40mPcg.css`。
- 部署目标：`/var/www/heaotang/app/service-plaza`。
- 服务器备份：`/root/heaotang-backups/20260711-102730.tar.gz`。
- 本地备份：`D:/Backup/heaotang-test-server/20260711-102730/test-server-state.tar.gz`。
- 前端回滚目录：`/var/www/heaotang/app/service-plaza.rollback-20260711-102726`。
- 部署前后 `/ready`：`ready`、`db=true`；`/health?json=1`：`status=ok`、`db.connected=true`、`plugins=24`。
- 公开资产校验：通过；部署脚本确认公开页面引用 `assets/index-CfiMm2q0.js`。
- 运行时目录：9 个服务、20 个动作；`club-alliance` 为 core sort 20。

## 自动化与本地入口

- 前端全量：18 files / 143 tests，通过。
- test-server build：通过。
- 服务广场合同、协作、检查单、考试、IR、工具链门禁：通过。
- UTF-8：666 files，通过。
- M4 平台 checklist：26/26；考试 `EX-20260711-CLUB-H1-M4-ACCEPTANCE-1` score 100。

## 浏览器页面与响应式

首页直达：`/app/service-plaza/services/club-alliance/`，真实 DOM 显示 heading“俱乐部联盟”、状态 `home`、四入口顺序为公益/自建/家庭/友联体；`club-manage` 位于独立 complementary“俱乐部联盟管理附属入口”，不是第五类；顶部和主体返回均指向 `/app/service-plaza/services`。

| 视口 | document/body scrollWidth | 布局 | 结论 |
| --- | --- | --- | --- |
| 320×800 | 320/320 | 单列，四卡宽约 277px | 无横向滚动，Pass |
| 360×800 | 360/360 | 单列，四卡宽 317px | 无横向滚动，Pass |
| 768×900 | 768/768 | 2 列，各 340px | 无横向滚动，Pass |
| 1280×900 | 1280/1280 | 有界 2 列，各约 300px | 无横向滚动，Pass |

焦点证据：顶部和主体返回链接均可获得真实 `focus-visible`，computed outline 为 `rgba(15, 118, 110, 0.32) solid 3px`。浏览器控制层对 Shift+Tab 的两种组合键编码均未移动焦点；公益链接 `press('Enter')` 返回后 URL 仍为首页，未取得产品导航结果。两项保持“浏览器控制通道未验证”，不判 Pass，也不判产品 No-Go；当前不得把自动化单测替代为完整环境键盘 UAT。

## Query 与失败关闭

| 输入 | 实际状态 | 稳定错误/结果 | 错误入口链接 |
| --- | --- | --- | --- |
| 无 query | home | 四入口 + 管理附属 | 不适用 |
| 公益俱乐部 | unauthorized（guest） | `authentication_required` | 未执行业务 API |
| 自建俱乐部 | unauthorized（guest） | `authentication_required` | 未执行业务 API |
| 家庭俱乐部 | unauthorized（guest） | `authentication_required` | 未执行业务 API |
| 俱乐部友联体 | unauthorized（guest） | `authentication_required` | 未执行业务 API |
| 空白 | error/alert | `CAH0_QUERY_BLANK` | 0 |
| UNKNOWN | error/alert | `CAH0_QUERY_UNKNOWN` | 0 |
| 同值重复 | error/alert | `CAH0_QUERY_AMBIGUOUS` | 0 |
| 多个不同值 | error/alert | `CAH0_QUERY_AMBIGUOUS` | 0 |
| 畸形编码 `%E0%A4%A` | error/alert | 解码后未知值，`CAH0_QUERY_UNKNOWN` | 0 |

四个合法 category 的独立访客状态均已逐项取得真实页面证据；每项均显示对应入口“当前不可访问”、`unauthorized` 页面和稳定原因 `authentication_required`。

## 网络分类

浏览器侧 `performance` API 在受控 evaluate 环境不可用，因此没有伪造 Resource Timing。改用同时间窗 Nginx access log 与本地 allowlist 自动化交叉验证：

- 10:30～10:54 的 `club-alliance` Referer 请求只出现 `GET /api/v1/service-plaza/catalog`、`GET /api/v1/service-plaza/actions` 和 APP 全局 `GET /api/v1/service-plaza/feature-flags`，均 200。
- `feature-flags` 属于 `ActionRuntimeProvider` 公共层既有请求，单列记录，不算模块新增请求。
- 同一时间窗未出现 club search/create/join/review/member/payment/charity/federation 请求。
- 浏览器控制层 `ab.chatgpt.com` Statsig 请求不是测试应用请求，服务器访问日志中不存在，不纳入 APP 证据。

### 2026-07-11 导航与网络增量证据

- 刷新：直达自建 category 后页面为 `unauthorized / authentication_required`；执行真实 reload 后 URL 完全保持，稳定原因与标题各唯一出现一次，Pass。
- 浏览器后退：从上述 category 状态执行 back，回到无 query `/app/service-plaza/services/club-alliance/`，且“选择俱乐部服务”标题唯一出现，Pass。
- 顶部返回：唯一 `返回服务广场` 链接跳转到 `/app/service-plaza/services`，Pass。
- 主体返回：唯一 `← 返回服务广场` 链接跳转到 `/app/service-plaza/services`，Pass。
- Shift+Tab：底部返回链接已显示 3px focus-visible，但 Playwright `Shift+Tab`、DOM/CUA `SHIFT+TAB` 均未改变 activeElement，记录为控制通道未验证。
- Enter：唯一公益入口 `press('Enter')` 未报产品错误但 URL 保持首页；前一次调用曾遇 webview attach 超时。为避免重复遥测事件，不继续重试，记录为控制通道未验证。
- Nginx 最近俱乐部 Referer 窗口聚合：`catalog GET 200=30`、`actions GET 200=30`、APP 全局 `feature-flags GET 200=38`、`action-events POST 200=6`。
- 同一窗口业务 denylist 计数为 0；未出现 club search/create/join/review/member/payment/charity/federation API。
- Nginx 只记录方法、路径、状态码聚合；数据库事件证据只保存 action_id、telemetry_event、outcome、reason、时间及 user_id 为 null/non-null，不保存 IP、手机号、OTP、JWT、完整 user_id 或敏感业务正文。

### 动作遥测阻断事实

- `GET /api/v1/service-plaza/feature-flags` 实际返回 `action_telemetry=false`。
- 源码事实：开关关闭时 `reportActionEvent` 在客户端返回 `feature_disabled`，不发送 `POST /api/v1/service-plaza/action-events`。
- Nginx 同时间窗印证：真实 guest click 后只有 catalog/actions/feature-flags，没有 action-events POST，也没有俱乐部业务 API。
- 后端旧 `PUT /api/v1/admin/service-plaza/feature-flags/:flagKey` 固定返回 `409 CONFIG_APPROVAL_WORKFLOW_REQUIRED`；这是正确失败关闭，但当前没有后续 maker-checker 提案/独立审核接口可完成开关启用。
- 直接修改 SQLite、复活旧单人入口或伪造 action-events 均违反 ADR 0011，本验收不采用。
- 关闭条件：平台实现并验收功能开关 proposal/review/version/audit 的双人流程；使用两个独立测试管理员在测试环境启用 telemetry；随后复测 guest blocked、登录 activated、缺 `club:manage` blocked，并通过管理 API/只读数据库验证字段白名单与脱敏 user_id。

### 2026-07-11 B001 关闭与 guest blocked 增量证据

- 后端实现及后端集成提交：`c4319c206add11f92d763b13b63be8ab2e47679e`；APP 治理证据提交：`ee8dec915ed890ed9fdc732fa6eacb1c3902ed3e`。
- 测试环境备份：`/root/heaotang-backups/20260711-143203.tar.gz`；部署二进制 SHA-256：`584105eb6846e086ea2a77acc89f207c4a1955e2f30a035273922fdd34ab1889`；部署后 `/ready`、`db=true`、`plugins=24`、actions=20 通过。
- 关键配置使用两个不同合成管理员完成 `true → false → true` 版本化提案/审核；同人审核返回 403；报告未保存手机号、OTP、JWT 或完整 user_id；当前公开 `action_telemetry=true`。
- 页面单步：从无 query 首页点击唯一“公益俱乐部”入口，URL 变为唯一公益 category，页面显示“需要登录或相应权限”，稳定原因 `authentication_required`。
- Nginx：`2026-07-11 16:43:16 +0800` 出现真实浏览器 `POST /api/v1/service-plaza/action-events`，HTTP 200，Referer 为公益 category 页面。
- 数据库只读交叉：最新记录为 `public-benefit-club / service_plaza.public_benefit_club.open / blocked / authentication_required / user_id=null`，UTC 时间 `2026-07-11 08:43:16`。
- 结论：guest blocked 遥测项 Pass；B001 resolved。该证据不替代登录 activated、缺 `club:manage` blocked 或其余 M4 项。

### 2026-07-11 四分类 guest blocked 完整环境证据

- 自建俱乐部：真实点击后 URL 为唯一自建 category，页面为 `unauthorized / authentication_required`；数据库记录 `self-created-club / service_plaza.self_created_club.open / blocked / authentication_required / user_id=null`，UTC `2026-07-11 09:11:10`。
- 家庭俱乐部：真实点击后 URL 为唯一家庭 category，页面为 `unauthorized / authentication_required`；数据库记录 `family-club / service_plaza.family_club.open / blocked / authentication_required / user_id=null`，UTC `2026-07-11 09:08:34`。
- 俱乐部友联体：真实点击后 URL 为唯一友联体 category，页面为 `unauthorized / authentication_required`；数据库记录 `club-federation / service_plaza.club_federation.open / blocked / authentication_required / user_id=null`，UTC `2026-07-11 09:23:50`。
- 连同上节公益记录，四分类均由页面状态、Nginx `POST /api/v1/service-plaza/action-events` HTTP 200 和数据库只读记录交叉证明；数据库输出仅保留 `user_id=null`，未落手机号、OTP、JWT、IP 或完整用户标识。
- 自建页面在浏览器回合清理后仅用同一已返回 URL 直达恢复 DOM，没有重复点击；数据库中 09:11:10 仅有一条本轮自建事件。
- 浏览器控制层 `ab.chatgpt.com` Statsig 超时继续归类为控制层噪声，未进入 APP/Nginx 证据。

## 尚未关闭

1. `CA-H1-M4-B001` 已关闭；保留上述 exact commit、部署、双审与 guest blocked 证据。
2. 刷新、浏览器后退和两个返回入口已 Pass；Enter、Shift+Tab 因浏览器控制通道不能稳定触发而保持未验证，最终门禁前需换稳定真实键盘通道复测。
3. 合成登录、四分类 activated 和管理中心 blocked/scope_required 事件证据已完成；仍需关闭 `CA-H1-M4-B002` 用户可见管理页面权限状态缺口。
4. 四分类 guest blocked 与登录 activated/管理 blocked 遥测均已完成，载荷未保存 OTP/JWT/完整个人标识/敏感业务数据。
5. 八态由 143/143 全量与 56/56 定向自动化证明；环境只记录安全、自然可重复状态，不新增人工状态切换器，不把未构造的 maintenance/offline 冒充截图通过。
6. 完成后才能把 verdict 改为 Pass；任何 Blocker/Major 未关闭维持 No-Go。

## 登录角色证据根因与正式解阻方案

- 浏览器只读枚举：当前受支持通道只有 Codex In-app Browser，且仅存在一个空白 New tab；没有可见合法已登录测试会话。当前运行时未提供可接管的 Chrome 标签。未读取 cookie、localStorage、token、OTP 或手机号。
- 合成账号容量门禁（UTC `2026-07-11`）：candidate A `used=5 / remaining=0 / capacity_ready=false`；candidate B `used=0 / remaining=5 / capacity_ready=true`；两次查询均 `secrets_read=false`。
- candidate B 服务端只读资格核对：账号已存在，owned clubs=0，privileged club memberships=0，预期 `club:manage=false`；未读取或输出完整身份。
- 后端权威机制：每个身份每个 SQLite UTC 日最多5次 send-code，验证码30分钟过期；自然重置为 UTC 00:00（北京时间次日08:00）。登录使用 `FindOrCreateUser`，scope 仅由俱乐部 owner 或特权成员关系派生，禁止管理员直接伪造 scope。
- 根因：M4 缺少一个合法普通会员浏览器会话；不是页面、遥测、权限 evaluator 或后端 scope 逻辑失败。
- Owner：平台集成负责人负责容量门禁、一次合成登录和三方取证；模块负责人继续只读，不接触凭据。
- 最小授权：允许对已批准且容量通过的 candidate B 执行且仅执行一次 send-code；OTP 仅通过一次性非仓库通道进入同一浏览器，登录成功/过期后立即销毁，不在消息、命令、报告或 Git 中出现。不得换号、清计数、改限流、注入 JWT/shell token。
- 登录后的唯一验收动作：四分类各一次，预期 `activated / none / user_id=non-null`；管理中心一次，预期 `blocked / scope_required / user_id=non-null`。每项由页面、Nginx action-events POST 和管理查询/只读数据库三方交叉；不执行业务 API。
- does_not_block：部署、备份、ready/health、四视口、query 正反例、四分类 guest、刷新、后退、双返回、allowlist/denylist、自动化八态和本地总门禁均已完成，不需重复。
- 当前仍禁止申请新 OTP；在最小授权明确前，登录角色两项保持 Pending，M4 继续 No-Go。

## 2026-07-11 合成普通会员登录与权限取证

- 最小授权后仅对 candidate B 执行一次 send-code；登录成功后页面出现“退出登录”和本人功能。系统临时秘密文件已删除，身份/OTP 内存值已清空，未执行第二次发送。
- 四分类页面：公益、自建、家庭、友联体分别进入唯一 category URL，对应标题可见且入口为 active/focused。
- 数据库只读事件：四分类依次为 `activated / none / user_id=non-null`，UTC 时间分别为 `10:08:51`、`10:10:53`、`10:20:46`、`10:22:22`；Nginx action-events POST 均为 HTTP 200。
- 管理中心：candidate B 权威关系继续为 owned clubs=0、privileged memberships=0；动作事件正确记录 `club-manage / blocked / scope_required / user_id=non-null`，UTC `10:23:52`，Nginx POST 200。
- 敏感信息：报告与工具结果未保存完整号码、OTP、JWT、cookie、完整 user_id 或业务正文。

### CA-H1-M4-B002 管理 view 页面权限状态缺口

- 现象：点击管理中心后 URL 进入 `?view=manage`，遥测正确为 `blocked/scope_required`，但页面仍显示标准首页并把管理中心链接标为 active，没有呈现 unauthorized/scope_required。
- 代码根因：`ActionControl` 的内部 Link 会报告拒绝并继续导航；`ClubAllianceRoute` 仅调用 `resolveClubAllianceQuery(location.search, view.categories)` 解析 category，没有解析或验证 `view=manage`，因此该 query 落入 home model。
- 测试缺口：现有 `ActionControl.test.tsx` 只断言 access-required 事件内容；`ClubAlliancePage.test.tsx` 只覆盖 category 的 scope_required，没有覆盖 management view。
- 影响：后端 scope、前端 evaluator 和遥测均正确，但用户可见权限状态错误，属于 M4 Blocker；不得以事件正确替代页面修复。
- 关闭方案：独立前端根因工作项为 `view=manage` 建立确定性解析和失败关闭；无 scope 时渲染 unauthorized/scope_required，有 scope 时才允许管理 focused 状态；补缺失、重复、未知 view 负例及页面/事件回归。
- Owner：平台集成负责人负责权限路由壳修复与独立验收；俱乐部业务 API、后端、数据和生产继续禁止。
