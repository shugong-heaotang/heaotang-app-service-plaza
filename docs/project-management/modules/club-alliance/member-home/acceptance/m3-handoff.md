# H2-M3 四身份 UAT Handoff

- checkpoint：`H2-M3`
- owner：Club Alliance acceptance agent
- status：`Environment executed / evidence incomplete`
- current verdict：`No-Go — API/recovery passed; browser and lifecycle coverage Unverified`
- plan：`docs/project-management/modules/club-alliance/member-home/acceptance/m3-plan.md`
- implementation record：`IR-20260712-CLUB-MEMBER-HOME-M3-ACCEPTANCE`（implemented）

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
- preservation：两份 R1 原字节仍位于不可变 Git 提交 `ae75d071f9a7c58e9354ad8eb6f41f69d6c09ad9` 的原历史路径；当前树不复制带缺陷字节，只保存 `invalidated-snapshots/member-home-membership-contract/r1/manifest.json`，记录 source commit、original path、Git blob OID、SHA、失效原因和 R2 替代关系。
- blocks：R1 不再作为 current checklist/exam，也不能支撑最终实现记录或 Contract Go。
- does_not_block：已完成的状态分层合同、Schema、fixtures、15 个 conformance 测试及其内容审查；它们由新的 R2 current checklist、随机考试和 IR 重新收口。
- prevention：R2 勾选采用精确 JSON 更新并在考试前运行 diff --check；任何快照格式缺陷都以不可变 Git 对象和规范 manifest 留证，再生成新记录，禁止篡改或复制缺陷字节到当前树。

## 1. 已授权范围

本检查点只授权在批准的联合窗口中执行可回滚测试环境部署和四身份浏览器 UAT。授权对象为新会员、家庭俱乐部普通会员、多俱乐部会员、理事或管理员；证据覆盖 route、DOM、网络 allow/deny、权限、遥测、服务端关联、响应式和键盘。

不授权业务代码、registry、生产、真实会员、真实资金、不可逆数据、未批准账号或绕过共享认证的 Token 注入。本 Handoff 不代表已经部署，也不代表 H2-M3 Full Go。

## 2. 当前输入

| 输入 | 当前事实 | 判断 |
| --- | --- | --- |
| APP integration | `4a9b42ee9be3655deda13603c5a2bf55a8eeb121` | membership R2、fixture capability 与状态分层前端已集成；225/225、双build、总合同通过 |
| H2 frontend | source `bba486a20872908675142fd73d95208861982672` | `club_status` / `membership_status` 严格解析和旧 status 失败关闭已独立复核 Go |
| Backend integration | `e41265905815082433e040412f3dd6b6b33dfede` | 状态分层 DTO 已集成；定向/全量 Go tests 与 vet 通过 |
| SC safe DTO | backend `98426ff8` 与 APP 治理证据均已 integrated，测试环境 ready | 已关闭，不再是 H2 blocker |
| M3 governance | membership R2 checklist completed/exam100；fixture capability 已独立复核并集成 | 允许准备；仍未授权环境执行 |

最终 combined commit、部署资产哈希、后端二进制哈希和数据库模式尚待部署负责人在窗口开始前冻结。

## 3. Entry Go

只有以下条件全部满足才可开始部署：

1. membership 状态字段实现已按 R2 合同独立完成、测试并受控集成。
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

以上为部署前历史判断；本轮环境执行后的 current 结论以下一节为准。

## 9. 2026-07-12 测试环境执行结论

目标 APP `37c6c3aa65b9a1332732d552063d6e06a2d7643a`（含 `4a9b42e`）和 backend `e41265905815082433e040412f3dd6b6b33dfede` 已完成可回滚测试环境部署。部署后 binary SHA-256 为 `f5abea4d24230625c271ac0721ccd2837c291dfe5ad9fcc477465945354c30ec`，入口资产为 `assets/index-DCYGiKy4.js`、SHA-256 `ce2a254c66d46505260ef89f52c9acda0c0707a24a96d0f392cdfe42adaa3de7`；health/ready、备份和回滚目标均已冻结。

三个唯一 RunId 的 Baseline、PartialError、CriticalError 均完成 Plan → Apply → Inspect → Cleanup，Cleanup 内置检查均为 0；真实 API 已证明四身份 empty/ready、普通与管理权限、active club/membership 分层、401 unauthorized、`CMH_TASKS_UNAVAILABLE` 局部错误和权威 422 `CMH_CLUB_CLASSIFICATION_INVALID`。关窗 RestoreVerify integrity/dump SHA 通过，live DB 未替换，最终 fixture 残留为 0。

浏览器运行时无可用实例，故 direct/reload/back/return、DOM、viewport、真实键盘、offline 和浏览器网络证据保持 control-channel Unverified；maintenance 无安全自然条件，按授权保持 Unverified；pending/rejected、left/suspended、dissolved 缺已批准 fixture，禁止直接 DB 捷径，环境状态覆盖亦保持 Unverified。完整证据见 `acceptance/m3/2026-07-12-environment-acceptance.md`。因此本检查点仍为 No-Go，不得宣称 H2-M3 Full Go；若部署 hash 未漂移，下一轮不得重复部署，只补浏览器矩阵和经批准的 lifecycle/history fixture。

## 10. Browser handoff 接续结果

主协调线程提供了精确 handoff URL/title，但 2026-07-12 12:05 Asia/Shanghai 接续时 in-app Browser backend 返回 `Browser is not available: iab`，随后唯一一次可用类型检查返回空列表 `[]`。因此无法调用 `browser.user.openTabs()`、无法 claim 精确标签，也无法读取 URL/title/DOM/page-state。接续全程未重部署、未重跑 fixture、未请求 OTP、未调用业务 API、未读取 token/cookie/完整身份；也没有改用 Chrome、Computer Use、静态 DOM 或既有 API 伪装浏览器证据。

当前 verdict 不变：`No-Go — API/recovery passed; browser and lifecycle coverage Unverified`。这是 automation/control-channel blocker，不是产品失败；Statsig 初始化 timeout 按插件统计控制通道噪声处理。下一轮仅在 in-app Browser backend 恢复后，从 exact URL/title claim 开始补无会话与四合成身份逐动作 UAT，禁止重复任何已完成上游。

### 2026-07-12 15:57 浏览器恢复更新

应用内浏览器已恢复并成功读取目标 URL、title、DOM、viewport 与静态资产，因此原“浏览器 backend 不可用”阻塞关闭。当前无凭据直达显示标准俱乐部首页，heading 为“俱乐部联盟 / 选择俱乐部服务”，`data-member-home-state` 数量为 0；这不足以证明会员首页或 unauthorized 状态通过。

阻塞已转化为部署路由/会话进入条件核对：先确认 `index-DCYGiKy4.js` 是否仍是批准 M3 制品及会员首页的合法进入条件，再决定是否启用合成身份。未核对前不请求 OTP、不读取会话秘密、不执行 fixture、不重复部署。证据见 `acceptance/m3/2026-07-12-browser-resume.md`。

## 11. 最小合成资料接续

已新增 `acceptance/m3/synthetic-data-design.md`，将缺失状态收敛为两个可安全执行的资料组：加入申请 `pending/rejected` 与俱乐部生命周期 `dissolved`。它们只使用 run-owned 合成记录、独立 RunId 和可恢复清理，不需要真实会员资料。

`left/suspended` 当前不能仅靠 fixture 可信构造：数据库没有会员关系状态/历史字段，会员首页后端仍将 `membership_status` 固定投影为 `active`。两项保持 `Unsupported/Unverified`，需要独立后端合同与数据模型工作项；禁止直接改库、复用 role 或用 club status 冒充。该缺口不阻塞先完成 pending/rejected 与 dissolved 的 API/数据库证据，但继续阻止 H2-M3 Full Go。
