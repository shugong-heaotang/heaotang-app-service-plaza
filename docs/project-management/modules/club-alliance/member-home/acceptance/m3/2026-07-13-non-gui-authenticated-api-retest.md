# H2-M3 非图形化认证 API 接续验收

- work item：`AIW-20260712-CLUB-MEMBER-HOME-M3-ACCEPTANCE`
- 时间：2026-07-13 20:44–20:51 Asia/Shanghai
- 环境：`https://heaotang.cn` 测试环境
- APP 入口资产：`assets/index-gcsUwwTF.js`
- 入口资产 SHA-256：`7e0c59a016ffbc973727459c275df3f92c64e1669e3b4970e47c0e96a98a9da3`
- 验收工作树 HEAD：`f60943a9d7fd97e9dd6507fb7675f83c4934aa11`
- authorization：用户明确允许四个既定合成测试账号各发送一次测试验证码
- secrets：`none-recorded`
- verdict：`Conditional No-Go — authenticated API and permission evidence passed for three roles; new-member member-home assertion and authenticated DOM remain Unverified`

## 1. 执行边界

只使用四个已批准合成身份和测试环境。每个身份在本轮最多新增一次 send-code；不记录或输出 OTP、JWT、Cookie、Authorization、完整手机号或完整用户标识。没有修改生产、真实会员、真实资金、认证限流或服务端数据模型。

浏览器图形控制连续失败后，本轮转为真实认证 API 验收。API 结果只证明认证、聚合数据合同和权限，不替代 direct/reload/back/return、DOM、viewport、键盘、浏览器网络或离线证据。

## 2. 入口与容量门禁

- `/ready`：`status=ready`、`db=true`。
- `/health?json=1`：`status=ok`。
- 执行前 OTP 容量：新会员、家庭会员、多俱乐部会员均 used=0/remaining=5；管理员 used=1/remaining=4；四者 `capacity_ready=true`、`secrets_read=false`。
- 执行后 OTP 容量：新会员、家庭会员、多俱乐部会员均 used=1/remaining=4；管理员 used=2/remaining=3。与执行前相比每个身份恰好新增一次，没有重复发送。
- 未认证 `GET /api/v1/clubs/member-home`：HTTP 401。

## 3. Baseline fixture 生命周期

### Run 1

RunId：`club-member-home-m3-20260713-204816-7ef84f59`。

- Plan/Apply/Inspect：clubs=5、memberships=4、tasks=1、activities=2、registrations=2、announcements=3、notifications=3。
- 新会员 send-code、login 和 `/api/v1/auth/me` 已走通；在赋值 member-home 响应前，验收壳因 PowerShell 大小写不敏感变量 `$home` 与只读 `$HOME` 冲突而停止。
- 没有重发新会员验证码；其 member-home 数据断言保持 `Unverified`。
- finally 清理：所有 run-owned remaining=0、users_deleted=0。
- RestoreVerify：integrity=ok、dump SHA match=true。

### Run 2

RunId：`club-member-home-m3-20260713-204927-8b9e9b8d`。

- Plan/Apply/Inspect：计数与 Baseline 设计完全一致。
- 验收壳改用 `$memberHomeResponse`，只执行尚未发送的家庭会员、多俱乐部会员和管理员三个身份。
- finally 清理：所有 run-owned remaining=0、users_deleted=0。
- RestoreVerify：integrity=ok、dump SHA match=true。
- 关窗 `/ready=ready`、`db=true`，`/health?json=1=ok`。

## 4. 认证 API 与权限矩阵

| 身份 | 本轮新增发送 | 登录 | member-home | joined | tasks | activities | feed | can_manage | club:manage | 状态合同 | 结果 |
| --- | ---: | --- | --- | ---: | ---: | ---: | ---: | --- | --- | --- | --- |
| 新会员 | 1 | Pass | 未保存断言 | Unverified | Unverified | Unverified | Unverified | Unverified | false（`/auth/me`） | Unverified | `Auth Pass / Member-home Unverified` |
| 家庭普通会员 | 1 | Pass | HTTP 200 | 1 | 1 | 1 | 1 | false | false | legacy status=0；非法状态对=0 | Pass |
| 多俱乐部会员 | 1 | Pass | HTTP 200 | 2 | 0 | 1 | 2 | false | false | legacy status=0；非法状态对=0 | Pass |
| 管理员 | 1 | Pass | HTTP 200 | 1 | 0 | 0 | 0 | true | true | legacy status=0；非法状态对=0 | Pass |

三个完整身份均证明 `club_status=active`、`membership_status=active`，且响应不含旧的含义不明 `status` 字段。管理员的 `can_manage` 与 `/auth/me` 权威 `club:manage` scope 一致，两个普通身份均为 false。

## 5. 本地回归

- `npm test -- memberHomeApi.test.ts MemberHomeShell.test.tsx ClubAlliancePage.test.tsx`：3 files、72/72 passed。
- `scripts/Test-ClubMemberHomeM3FixtureSafety.ps1`：passed，静态阶段 OTP requests=0、server mutations=0、secrets persisted=false。
- `python contracts/modules/club-alliance/member-home/test_member_home_contracts.py`：15/15 passed。
- `scripts/Test-ServicePlazaContracts.ps1`：全部服务广场合同、工作项、检查单、考试和实现记录门禁通过。
- `npm run build:test-server`：通过，65 modules transformed。
- `scripts/Test-TextEncoding.ps1`：941 files passed；`git diff --check` 通过。

## 6. 根因记录

### RC-CMH-M3-CONTROL-CHANNEL-002

- symptom：已有测试页面可打开，但自动控制无法稳定获得认证后 DOM；Windows 控制又因不能可信确认当前 URL 被安全终止。
- exact stop：应用内浏览器在登录后页面状态读取时重置；Windows 控制在 `get_window_state` 前终止。
- causal chain：控制后端无法稳定保留标签/会话或可信 URL → 安全策略禁止继续输入敏感认证数据 → authenticated DOM 无法取证。
- product evidence：health/ready、真实登录、三身份 member-home、权限矩阵和本地回归通过，没有产品故障证据。
- tool evidence：两个独立控制入口均在页面证据阶段停止；这是第二次同类 control-channel 复发。
- blocks：认证态 DOM、五档 viewport、真实键盘、浏览器网络、offline 和最终 Full Go。
- does not block：真实认证 API、服务端权限、聚合合同、fixture 清理、恢复和本地回归。
- rejected workaround：禁止用 API Pass、静态组件测试、Token 注入或截图推断 Page Pass。
- prevention gate：控制端不能证明精确 URL 和会话时立即停止浏览器动作；API 与 Page 证据分栏记录，任何一栏缺失都不能升级 Full Go。
- unresolved risk：控制通道属于外部执行基础设施，本工作项没有修改或绕过其安全策略。

### RC-CMH-M3-PS-HOME-COLLISION-001

- symptom：首个身份登录后验收壳报 `Cannot overwrite variable HOME because it is read-only or constant.`。
- root cause：Windows PowerShell 变量名大小写不敏感，局部 `$home` 与内置只读 `$HOME` 冲突。
- action：停止该身份且不重发；finally 清理并恢复；第二次运行改用 `$memberHomeResponse`，其余三个身份全部通过。
- verification：Run 2 三身份完整断言通过，两个 RunId 均 remaining=0、RestoreVerify 通过。
- prevention：后续仓库化验收脚本禁止使用 `$home` 作为变量名，并保留 finally Cleanup/RestoreVerify。

## 7. 当前结论与下一重测条件

本轮将可在无图形控制条件下可信完成的三身份认证 API 和权限矩阵关闭，同时证明每身份只新增一次 OTP 请求、临时数据为零、数据库可恢复。新会员 member-home 断言因本地壳错误发生在记录前，遵守一次授权不重发，保持 Unverified。

最终仍为 `Conditional No-Go`：不能把 API 结果冒充真实 DOM。下一次只在新的 UTC 日容量和新的明确发送授权下补新会员 member-home；authenticated DOM 则必须等待能够可信确认 URL、保留会话并读取页面状态的浏览器控制通道。不得重复部署或复跑已经通过的三身份 API。
