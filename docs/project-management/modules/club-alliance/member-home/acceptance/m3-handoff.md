# H2-M3 四身份 UAT Handoff

- checkpoint：`H2-M3`
- owner：Club Alliance acceptance agent
- status：`Authorized / deployment pending`
- current verdict：`No-Go before deployment`
- plan：`docs/project-management/modules/club-alliance/member-home/acceptance/m3-plan.md`
- implementation record：`IR-20260712-CLUB-MEMBER-HOME-H2-M3`（draft）

## 0. 会员状态合同纠正检查点

本 Handoff 已吸收独立合同工作项 AIW-20260712-CLUB-MEMBER-HOME-MEMBERSHIP-CONTRACT 的语义纠正：

- pending/rejected 是 club-join-application 申请历史，不是 membership；
- left 是 club-membership 历史关系，不进入当前“我的俱乐部”；
- suspended 是可选会员停权，只有服务端正式支持并验收后才可作为当前受限关系；
- dissolved 是 club 生命周期，不是 membership；
- 机器合同要求当前记录分离 club_status 与 membership_status，禁止含义不明的单一 status。

本检查点只纠正文档、合同、Schema、合成 fixture 和 conformance。现有前后端实现与测试环境尚未因此自动满足新合同，故 M3 仍为 No-Go before deployment。

合同检查点证据：

- current checklist：contracts/modules/club-alliance/development-checklists/2026-07-12-club-member-home-membership-contract-r2.json（28/28 completed）；
- current exam：contracts/modules/club-alliance/governance-exams/2026-07-12-club-member-home-membership-contract-r2-attempt-1.json（100 / passed）；
- implementation record：IR-20260712-CLUB-MEMBER-HOME-MEMBERSHIP-CONTRACT-R2；
- conformance：15/15 passed；
- 结论：Contract Go / Implementation and Environment No-Go。

### R1 快照格式根因与隔离

- symptom：R1 checklist 在完成勾选时被 apply_patch 写成两个结尾换行，Git staged diff 报 new blank line at EOF；合同、Schema 与 conformance 内容本身未受影响。
- causal chain：初始 checklist 由官方脚本生成；勾选时采用“删除后完整重建文件”的补丁，补丁生成器在已有 LF 之后又添加空行；attempt-1 随后以该字节快照的 SHA 出题并通过，因而不得原地删空行或改写试卷。
- preserved checklist SHA-256：8cea0d38c65590d54f060bd8b76be80d75a2397ad8f3e924b35000f87d64008b。
- preserved exam SHA-256：e6deb3de77cbfa0413ca6c75d244b0b22315c9baf954e5c7ed774d0b36e9b2db。
- isolation：两份 R1 原字节快照已迁入 contracts/modules/club-alliance/invalidated-snapshots/member-home-membership-contract/r1/；迁移前后 SHA 完全一致。
- blocks：R1 不再作为 current checklist/exam，也不能支撑最终实现记录或 Contract Go。
- does_not_block：已完成的状态分层合同、Schema、fixtures、15 个 conformance 测试及其内容审查；它们由新的 R2 current checklist、随机考试和 IR 重新收口。
- prevention：R2 勾选采用精确 JSON 更新并在考试前运行 diff --check；任何快照格式缺陷都先隔离原字节，再生成新记录，禁止篡改已评分证据。

## 1. 已授权范围

本检查点只授权在批准的联合窗口中执行可回滚测试环境部署和四身份浏览器 UAT。授权对象为新会员、家庭俱乐部普通会员、多俱乐部会员、理事或管理员；证据覆盖 route、DOM、网络 allow/deny、权限、遥测、服务端关联、响应式和键盘。

不授权业务代码、registry、生产、真实会员、真实资金、不可逆数据、未批准账号或绕过共享认证的 Token 注入。本 Handoff 不代表已经部署，也不代表 H2-M3 Full Go。

## 2. 当前输入

| 输入 | 当前事实 | 判断 |
| --- | --- | --- |
| APP integration | `f31f67f` | 候选联合部署基线，部署前必须冻结完整 SHA |
| H2 frontend | `e06d5c6`，全量 `215/215` 与生产构建通过 | 本地/集成门禁已通过，不替代环境证据 |
| Backend integration | `97d8bfc5`，定向 `10/10`、Go 全量 test 与 vet 通过 | 本地/集成门禁已通过，不替代环境证据 |
| SC safe DTO | combined remediation/deployment coordination pending | 当前部署 Blocker |
| M3 governance | checklist completed；exam `100 / passed` | 允许准备，未解除部署 Blocker |

最终 combined commit、部署资产哈希、后端二进制哈希和数据库模式尚待部署负责人在窗口开始前冻结。

## 3. Entry Go

只有以下条件全部满足才可开始部署：

1. SC safe DTO remediation 已独立验证并进入确定的 combined frontend/backend commit。
2. 目标前后端完整 SHA、构建资产、数据库模式、base URL 和允许变更范围已冻结。
3. 部署负责人确认备份、自动回滚、人工回滚、恢复责任人和关窗标准。
4. 四个脱敏合成身份、权威关系数据和 OTP 独立会话容量已准备；`capacity_ready=true`。
5. `/health?json=1`、`/ready`、登录、聚合 API smoke、部署包和静态资产预检通过。
6. `partial-error/error/maintenance/offline` 的安全、可审计、可恢复触发方式获批。
7. Nginx、API request id 与只读 DB/管理查询的服务端关联渠道已就绪。

任一条件缺失，保持 `No-Go before deployment`。

## 4. 部署与回滚门禁

部署前记录备份标识、原前后端版本、原资产哈希、原配置和数据库状态；禁止直接修改生产或用未审计 SQL 构造证据。部署必须复用既有原子发布及自动回滚能力。

部署后先验证 health、ready、入口 HTML、JS/CSS 资产、登录和 `GET /api/v1/clubs/member-home`，再进入浏览器 UAT。任何 ready 失败、核心 API 异常、跨用户数据、scope 错误或资产不一致都立即触发回滚，不继续采集“部分通过”证据。

状态/故障验证后逐项恢复，不能叠加多个不透明变更。关窗前再次验证 health、ready、聚合 API、四探索入口和基线账号，记录恢复时间、结果和责任人；恢复失败即最终 No-Go。

## 5. 四身份与关系状态

- 新会员：0 owned、0 membership、0 task/activity；证明真实 `empty` 与 `can_manage=false`。
- 家庭俱乐部普通会员：active family membership、member role、本人待办/活动；证明家庭数据最小化与普通权限。
- 多俱乐部会员：active `standard/general` 与 `standard/charity`；证明摘要计数、权威排序和本人归属。
- 理事或管理员：scope 由权威 owner/特权关系派生；只有该身份 `can_manage=true`。

另以独立可恢复数据按实体覆盖申请历史 pending/rejected、会员历史 left、可选会员停权 suspended、俱乐部生命周期 dissolved。申请历史不得计入当前 membership；历史关系不得出现在当前列表；解散必须通过独立 club_status 表达。这些业务状态也不等同于页面 maintenance/offline。

## 6. 八态和浏览器证据

`loading/ready/empty/partial-error/error/unauthorized/maintenance/offline` 必须按 `m3-plan.md` 的合法触发方式证明。自动化和组件 fixture 只作补充；没有真实、可恢复环境机制的状态必须标记 `Blocked/Unverified`，不得用 runtime switcher、catch-empty 或截图伪造。

每身份逐动作验证 direct、reload、back、return 和探索入口；在 320、360、390、768、1280 px 记录 scroll width 与关键矩形，并用真实 Tab、Shift+Tab、Enter 记录焦点。网络只允许聚合 API、共享目录/feature flags 和真实动作对应 telemetry；denylist 请求计数必须为 0。

浏览器、Nginx/API 和只读 DB/管理查询形成同时间窗三方关联。浏览器控制超时单列为 control-channel，不直接归为产品失败。

## 7. 脱敏

- 不读取、截图、复制、提交 OTP、JWT、Cookie、完整手机号、完整 user id 或 Authorization。
- 不记录证件、健康、家庭隐私、收款信息或真实业务正文。
- 账号只保存角色、环境、脱敏标识和可用状态；用户事实只保存 null/non-null、计数或合成编号。
- 每条证据的 secrets 字段必须为 `none-recorded`；否则该证据无效并停止验收。

## 8. Full Go 条件

四身份、八态、三层业务状态、五档 viewport、真实键盘、路由/DOM/网络/权限/遥测/服务端关联全部达到计划要求；聚合 API 和页面必须分别证明 club_status、membership_status，且申请历史不串入当前列表；所有 Blocker/Major 关闭；证据无秘密；环境恢复并通过基准 smoke 后，才可把 draft IR 更新为 verified/deployed 并形成 H2-M3 Full Go。

当前尚缺前后端状态字段迁移、combined commit、部署资产、四身份会话、环境状态触发和现场三方证据，因此结论保持 Authorized / deployment pending、No-Go before deployment。
