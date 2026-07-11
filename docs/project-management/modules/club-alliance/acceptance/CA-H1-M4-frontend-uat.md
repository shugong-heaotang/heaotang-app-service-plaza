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

焦点证据：顶部返回链接获得真实 `focus-visible`，computed outline 为 `rgba(15, 118, 110, 0.32) solid 3px`。浏览器控制层没有可靠发送 Enter；唯一 locator 的真实 click 已成功进入公益俱乐部 guest `unauthorized` 状态，URL 带唯一 category，页面显示 `authentication_required`。当前不得把自动化单测替代为完整环境键盘 UAT。

## Query 与失败关闭

| 输入 | 实际状态 | 稳定错误/结果 | 错误入口链接 |
| --- | --- | --- | --- |
| 无 query | home | 四入口 + 管理附属 | 不适用 |
| 公益俱乐部 | unauthorized（guest） | `authentication_required` | 未执行业务 API |
| 空白 | error/alert | `CAH0_QUERY_BLANK` | 0 |
| UNKNOWN | error/alert | `CAH0_QUERY_UNKNOWN` | 0 |
| 同值重复 | error/alert | `CAH0_QUERY_AMBIGUOUS` | 0 |
| 多个不同值 | error/alert | `CAH0_QUERY_AMBIGUOUS` | 0 |
| 畸形编码 `%E0%A4%A` | error/alert | 解码后未知值，`CAH0_QUERY_UNKNOWN` | 0 |

其余三个合法 category 的独立 focused/guest 状态仍需逐项环境记录；本地自动化已经覆盖四项，不作为环境完成证据。

## 网络分类

浏览器侧 `performance` API 在受控 evaluate 环境不可用，因此没有伪造 Resource Timing。改用同时间窗 Nginx access log 与本地 allowlist 自动化交叉验证：

- 10:30～10:54 的 `club-alliance` Referer 请求只出现 `GET /api/v1/service-plaza/catalog`、`GET /api/v1/service-plaza/actions` 和 APP 全局 `GET /api/v1/service-plaza/feature-flags`，均 200。
- `feature-flags` 属于 `ActionRuntimeProvider` 公共层既有请求，单列记录，不算模块新增请求。
- 同一时间窗未出现 club search/create/join/review/member/payment/charity/federation 请求。
- 浏览器控制层 `ab.chatgpt.com` Statsig 请求不是测试应用请求，服务器访问日志中不存在，不纳入 APP 证据。

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

## 尚未关闭

1. `CA-H1-M4-B001` 已关闭；保留上述 exact commit、部署、双审与 guest blocked 证据。
2. 单步完成 Enter、Shift+Tab、刷新、浏览器后退和两个返回入口。
3. 使用批准的合成测试账号验证登录允许和登录但缺 `club:manage`；不得注入 shell token或在报告记录 OTP/JWT。
4. 取得真实环境 activated/blocked 遥测证据，并确认载荷无 OTP/JWT/完整个人标识/敏感业务数据。
5. 八态由 143/143 全量与 56/56 定向自动化证明；环境只记录安全、自然可重复状态，不新增人工状态切换器，不把未构造的 maintenance/offline 冒充截图通过。
6. 完成后才能把 verdict 改为 Pass；任何 Blocker/Major 未关闭维持 No-Go。
