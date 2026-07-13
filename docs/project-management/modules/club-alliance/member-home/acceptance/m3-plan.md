# H2-M3 会员首页分身份 UAT 计划

- checkpoint：`H2-M3`
- owner：Club Alliance acceptance agent
- status：`Planned / No-Go before deployment`
- target route：`/app/service-plaza/services/club-alliance/`
- evidence policy：只使用批准测试环境、合成身份和脱敏证据；不记录 OTP、JWT、Cookie、完整手机号或完整用户标识

## 1. 当前基线与判定

| 范围 | 当前已知事实 | M3 判定 |
| --- | --- | --- |
| 前端 | APP integration `e06d5c6`；全量 `215/215` 与生产构建通过 | 仅证明本地/集成门禁，不证明已部署页面 |
| 后端 | backend integration `97d8bfc5`；定向 `10/10`、Go 全量测试与 vet 通过 | 仅证明本地/集成门禁，不证明测试服真实数据 |
| 联合发布 | SC safe DTO remediation 与部署协调仍 pending | 阻断部署和浏览器 UAT |
| M3 | 尚未冻结 deployed commit、asset hash、四身份会话和环境数据 | `Planned / No-Go before deployment` |

本计划不授权部署、账号创建、数据变更、故障注入或生产访问。进入 M3 前必须由平台/部署负责人提供联合窗口和可恢复方案。

## 2. 四身份与权威数据前置

所有身份必须是测试环境合成身份，登记脱敏标识、取得方式、保管责任、可用状态和允许操作；若需发送验证码，先按全部独立会话数执行 OTP 容量门禁，只有 `capacity_ready=true` 才能继续。

| 身份 | 必备权威数据 | 预期页面事实 | 权限事实 |
| --- | --- | --- | --- |
| 新会员 | 已登录；owned club=0；全部 membership=0；task/activity=0；计数均为 0 | `empty`；显示尚未加入俱乐部；仍显示四个探索入口 | `can_manage=false`；不显示管理入口 |
| 家庭俱乐部普通会员 | 1 个 `type=family/category=family` 的 active membership；`member_role=member`；至少 1 条本人可见、可追溯来源的今日待办；建议至少 1 条本人活动 | `ready`；显示家庭俱乐部、本人角色、状态和唯一进入动作 | `can_manage=false`；不得返回家庭隐私记录 |
| 多俱乐部会员 | 至少 2 个 active membership：`standard/general` 自建和 `standard/charity` 公益；至少 1 条本人活动；服务端排序可核对 | `ready`；摘要计数、两类俱乐部及顺序与权威数据一致 | `can_manage=false`；不得看到其他会员资源 |
| 理事/管理员 | 至少 1 个 active membership；`member_role=director` 或权威 owner/特权关系；scope 必须由服务端关系派生 | `ready`；会员数据正常展示 | `can_manage=true`；仅此身份显示管理附属入口 |

另建独立、可恢复的测试记录按实体覆盖三类状态：加入申请历史 pending/rejected，会员关系历史 left，可选会员停权 suspended，以及俱乐部生命周期 dissolved。其中 pending/rejected 不得计入当前 membership，left 不得出现在当前“我的俱乐部”，suspended 只有在服务端明确支持时才可作为受限当前关系，dissolved 必须作为独立 club_status，不能伪装为会员关系状态。每项都要核对显示文案、可用动作和服务端原始实体；也不得用页面 maintenance/offline 代替。

## 3. 每身份统一证据流程

### 3.1 冻结环境

1. 记录 base URL、环境名、部署时间、前后端 exact commit、JS/CSS asset hash、数据库模式、浏览器版本和 session class。
2. 记录本轮是否允许变更；默认只读。任何会改变账号、关系、生命周期或故障状态的动作必须另获批准。
3. 先验证 `/health?json=1`、`/ready`、登录、聚合 API smoke、前后端门禁和测试环境配置；任一失败即停止浏览器 UAT。
4. 证据时间统一保存本地时间与 UTC，便于浏览器、Nginx、API 和数据库关联。

### 3.2 路由与单动作浏览器步骤

每个导航、刷新、后退、返回、点击或按键单独执行并立即记录，不以 `networkidle` 判断 SPA 完成：

1. 直达无 `category`、无 `view` 的会员首页，等待明确 DOM marker。
2. 真实刷新，确认 URL、身份和页面状态稳定。
3. 从下游页面执行浏览器后退，确认返回同一会员首页且不重复提交。
4. 使用页面返回入口返回服务广场，确认目标路由唯一。
5. 四个探索入口逐项验证 action id、目标 route、权限结果和遥测；不批量点击。
6. 普通身份 direct `?view=manage` 必须失败关闭；理事/管理员才可进入授权管理视图。

每一动作记录：case id、execution id、时间、前置状态、动作、预期、实际 URL、可见标题、DOM marker、active element、网络分类、遥测、服务端关联、结果和下一步。工具超时只记为 automation/control-channel，不能直接判定产品失败。

### 3.3 DOM 与信息架构

无筛选会员首页必须有唯一 `data-member-home-state`。在 `ready/empty/partial-error` 中核对顺序：

1. 会员摘要；
2. 我的俱乐部；
3. 今日待办；
4. 最近活动；
5. 联盟动态（有真实数据或局部错误时）；
6. 探索更多。

四个探索动作必须精确为 `public-benefit-club`、`self-created-club`、`family-club`、`club-federation`；友联体只作为关系探索入口，不得显示为第四种 ClubType。普通会员不得出现管理入口，服务端 `can_manage=true` 的身份才可见。页面和响应均不得出现合同禁止的敏感字段。

### 3.4 网络 allow/deny

模块 allowlist：

- 认证的 `GET /api/v1/clubs/member-home`，严格 v1 信封；
- H1 共享目录所需的 catalog/actions；
- APP 全局 feature-flags；
- 仅在真实动作发生时允许对应 action-events。

每轮记录方法、路径、状态码、次数和时间窗，不记录 Authorization。确认聚合请求不接受或发送 `user_id` 查询参数。

denylist：非当前动作触发的 club search/create/join/review/member/payment/refund/withdraw/subscription API、生产写入、重复提交、runtime mock、catch 后空数组回退，以及任何跨用户资源请求。浏览器控制插件流量必须与 APP 请求分开分类。

### 3.5 权限与服务端关联

每身份至少形成三方证据：

1. 浏览器：URL、状态 marker、标题、可见数据和权限入口；
2. Nginx/API：同一时间窗内的路径、HTTP 状态、次数及既有 request/trace id；
3. 权威查询：只读 DB 或管理查询核对匿名 `user_id=non-null`、owned/membership 数、角色、scope 和返回记录归属。

只保存 null/non-null、计数、合成记录编号或不可逆脱敏标识。任何跨用户俱乐部、待办、活动或私密字段泄露均为安全 Blocker，立即停止该轮。

## 4. 八态的合法证明

| 页面态 | 测试环境证明方法 | 禁止替代 |
| --- | --- | --- |
| loading | 真实聚合请求 pending 时捕获 `loading` marker 和加载文案，随后在同一链路转入最终态；可使用浏览器节流或已批准代理延迟 | 只用组件测试截图 |
| ready | 家庭、多俱乐部、管理员身份取得真实 200，并由 DOM、API 和权威数据三方一致证明；当前俱乐部记录必须分离 club_status 与 membership_status | 静态 fixture |
| empty | 新会员真实 200 合法空集合，权威查询证明 0 关系/任务/活动，DOM 显示 empty | `catch -> []` 或删除真实数据 |
| partial-error | 使用既有、可审计且可恢复的测试环境机制，使非关键 tasks/activities/feed 返回稳定 section error，同时 my-clubs 保持可用 | 新增页面 runtime switcher、伪造空数组 |
| error | 在批准故障窗口让关键聚合或 my-clubs 依赖返回稳定错误，证明页面 alert、API 失败和服务端错误一致，随后恢复 | 把浏览器超时当产品错误 |
| unauthorized | 无会话直达，聚合 API 返回 401 或进入共享登录承接；DOM 不得显示任何“我的”数据 | 注入 JWT 或伪造登录态 |
| maintenance | 通过权威生命周期/配置审批使入口进入维护状态，记录配置版本、审核和恢复 | 前端查询参数或本地开关伪造 |
| offline | 通过权威生命周期/配置审批使入口下线，记录配置版本、审核和恢复 | 组件测试冒充环境证据 |

若测试环境没有合法的 partial-error、error、maintenance 或 offline 触发机制，则这些环境项记为 `Blocked/Unverified`，不得宣称 Full Go。自动化证据可补充但不能替代真实环境要求。

## 5. 响应式、滚动与键盘

每个关键页面态至少验证以下宽度：

| viewport | 重点 |
| --- | --- |
| 320 px | 最窄边界、文字换行、按钮点击面积、无横向溢出 |
| 360 px | 主流小屏、摘要数字和卡片布局 |
| 390 px | 目标手机视口，记录 `body/document scrollWidth` |
| 768 px | 响应式断点、双列区域与阅读顺序 |
| 1280 px | 桌面布局、最大内容宽度和焦点路径 |

每轮保存 viewport、body/document scroll width 和关键元素矩形。页面级横向溢出、内容遮挡、入口不可触达均为 Major；主动作不可用为 Blocker。

键盘逐项验证 Tab、Shift+Tab、Enter：记录 active element、`:focus-visible`、按键和结果。焦点顺序必须符合 DOM 阅读顺序，链接和返回入口可用 Enter 激活，焦点不能落入隐藏管理入口。脚本 `click()`、合成 KeyboardEvent 或单元测试不能替代真实键盘证据。

## 6. 脱敏与证据存储

- 不读取、截图、复制或提交 OTP、JWT、Cookie、完整手机号、完整 user id、证件、健康、家庭隐私、收款信息或真实业务正文。
- 账号只记录角色、环境、脱敏标识和可用状态；用户事实只记录 null/non-null 或匿名合成编号。
- 截图前检查页面、地址栏、开发者工具和通知；发现秘密立即停止，不把瞬时输出写入报告或 Git。
- 网络只保留方法、路径、状态、次数、时间和安全响应摘要；Header 中的 Authorization 必须排除。
- 每条证据的 `secrets` 字段固定为 `none-recorded`；否则该证据无效并进入安全复盘。

## 7. Entry Go / Full Go

### 7.1 Entry Go

只有以下条件全部满足才可部署并启动 M3：

- 前后端目标提交已受控集成，SC safe DTO remediation 已关闭；
- 联合部署窗口、备份、回滚和责任人已确认；
- 部署后 health/ready、asset、登录、聚合 API smoke 全部通过；
- 四个脱敏合成身份与权威数据已准备，OTP 容量满足全部独立会话；
- 三层状态数据和八态触发/恢复方案已批准：申请历史 pending/rejected、会员关系 active/left/suspended、俱乐部生命周期 dissolved；
- 聚合 API、前端 adapter 和页面已停止使用含义不明的单一 status，并通过状态域负向回归；
- Nginx/API/只读 DB 的服务端关联渠道可用；
- exact deployed commits、assets 和允许变更范围已冻结。

当前 Entry verdict：`No-Go`。

### 7.2 Full Go

四身份的 direct、reload、back、return，route/DOM/network allow-deny/permission/server correlation，五个 viewport、真实键盘，以及三层业务状态均通过；八态按本计划取得真实环境证据或任务书明确接受的证据层级；不存在未关闭 Blocker/Major；证据无秘密；测试环境完成恢复并复验 health/ready 和基准 smoke。任一核心接口未调用、状态域串流、单一 status 仍无法判定属于 club 或 membership、异常 401/5xx、跨用户数据、scope 错误、runtime mock/catch-empty、版本不明或缺真实浏览器证据，均为 No-Go。

## 8. 环境恢复与关窗

1. 故障、maintenance/offline、账号关系或测试数据变更前记录原值、审批、操作者和恢复命令；默认不得直接改数据库。
2. 每个状态验证后立即按批准路径恢复，不把多个状态变更叠加到同一不透明窗口。
3. 恢复后复验 `/health?json=1`、`/ready`、聚合 API、四探索入口和基线账号；核对无残留测试任务、生命周期或权限。
4. 保留备份/回滚标识、恢复时间、恢复验证结果和负责人，不保存秘密。
5. 若恢复失败，立即 No-Go，停止后续 UAT，并由部署/平台负责人执行回滚和根因闭环。

## 9. 当前阻塞清单

1. SC safe DTO remediation 尚未关闭；联合部署窗口未批准。
2. 尚无 H2 测试环境 deployed commit、asset hash 和聚合接口现场响应。
3. 四身份账号、OTP 容量和权威数据尚未冻结为本轮证据。
4. 三层状态的测试环境记录尚未提供；现有实现对 club_status / membership_status 的分离也尚未形成环境证据。
5. partial-error、error、maintenance、offline 的安全触发与恢复方案尚未提供。
6. 服务端 correlation 的查询入口、字段和证据责任人尚未冻结。

上述阻塞关闭前，本计划保持 `Planned / No-Go before deployment`。
