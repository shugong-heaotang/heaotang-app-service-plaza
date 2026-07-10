# 生命导航 M4 起飞认证与部署前检查：LN-M4-001

- 通知编号：`LN-TASK-20260710-001`
- 执行负责人：生命导航二负责人
- 检查时间：`2026-07-11T01:36:36+08:00`
- 前端工作树：`C:\Users\shugo\Documents\worktrees\heaotang-life-navigation`
- 前端分支与提交：`codex/life-navigation-application-history` / `ef6006608709bc7ba00c48f1c2964805a2528e9e`
- 当前结论：Ready（仅表示 M4 起飞认证和部署前置已就绪；不等于 M4 Go）
- 本轮边界：只执行本地认证、依赖、脚本、制品和证据计划检查；未连接测试服务器、未部署、未读取或写入凭据、未签 M4 Go。

## 1. M4 起飞认证

- checklist：`docs/project-management/modules/life-navigation/certification/checklists/IR-20260711-LIFE-APPLICATION-HISTORY-M4-checklist.json`
  - record：`IR-20260711-LIFE-APPLICATION-HISTORY-M4`
  - 31 项当前治理输入重新全文读取并逐项绑定当前 SHA-256。
  - `created_at=2026-07-10T17:32:19.3491231Z`
  - `checked_at=2026-07-10T17:32:59.7841943Z`
  - `completed_at=2026-07-10T17:33:19.4346338Z`
  - 隔离复制后使用正式 Schema、`--project-root . --require-current` 校验通过，临时目录已安全删除。
- exam：`docs/project-management/modules/life-navigation/certification/exams/IR-20260711-LIFE-APPLICATION-HISTORY-M4-exam-attempt-1.json`
  - attempt：`EX-20260711-LIFE-APPLICATION-HISTORY-M4-1`
  - `generated_at=2026-07-10T17:33:43.9097309Z`
  - `completed_at=2026-07-10T17:33:51.3461434Z`
  - 8/8、score 100、status `passed`；治理考试快照与不可变 checklist 关联校验通过。
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/Test-AgentDevelopmentPreflight.ps1`：`status=ready`。
- 协作登记：`AIW-20260711-LIFE-APPLICATION-HISTORY` 仍为 `active`，工作树、`codex/` 分支和允许路径与当前任务匹配；未修改协作注册表。

## 2. 本地提交和制品依赖

### 前端

- 当前提交包含以下已验收依赖：
  - `9a2717f708a1d6ac5d6e47c26991d219e61e598c`：M2 真实历史与提交 API 适配。
  - `e6243e186b322404e50cf80419ee6c210c335098`：M3 模块页面。
  - `be1b26aab5e85fe63c4494689e1b6551a4417718`：平台精确路由。
  - `ef6006608709bc7ba00c48f1c2964805a2528e9e`：M3 最终 Go。
- `scripts/Build-ServicePlazaTestPackage.ps1` 本地执行通过；`public_base=/app/service-plaza/`，部署 manifest 包含 `services/life-navigation`，且 `app/dist/services/life-navigation/index.html` 存在。

### 后端

- 已批准依赖提交：`70fa12276e6eac17369c0d1d3c1d23a8e757fcc0`，包含生命导航历史 `limit=1..30` 边界和跨用户不可见回归。
- 干净且精确位于该提交的工作树：`C:\Users\shugo\Documents\worktrees\heaotang-life-m1-backend`，分支 `codex/life-m1-backend-contract`。
- 在该工作树 `backend-go` 执行 `go test -count=1 ./...` 与 `go vet ./...` 均通过。
- 阻塞事实：`scripts/Deploy-ServicePlazaBackendTest.ps1` 默认 `BackendRoot` 指向 `C:\Users\shugo\Documents\heaotang-main\backend-go`；该默认仓库当前 HEAD 为 `4cb61a550959e6eaa70dd45bdc8fba73992c86083`，不包含 `70fa122…`，且已有未归属的 `app/dist` 删除/修改。不得从该默认路径构建，不得清理或覆盖其中的现有修改。
- 关闭条件（二选一，须平台负责人明确采用并留下提交证据）：
  1. 将 `70fa122…` 受控集成到权威后端部署分支，并确认部署工作树干净；或
  2. 明确批准本次部署把 `-BackendRoot` 固定为上述干净的 `heaotang-life-m1-backend\backend-go`，部署证据记录完整提交哈希且禁止回落到脚本默认值。

- 解除记录：平台负责人已选择第二种关闭方式。M4 后端部署只允许显式传入 `-BackendRoot C:\Users\shugo\Documents\worktrees\heaotang-life-m1-backend\backend-go`，并在执行前再次断言工作树干净且 HEAD 精确为 `70fa12276e6eac17369c0d1d3c1d23a8e757fcc0`。
- 强制部署约束：禁止省略 `-BackendRoot`，禁止回落脚本默认路径，禁止清理、覆盖或提交 `C:\Users\shugo\Documents\heaotang-main` 中未归属的 `app/dist` 修改；任一断言不满足立即恢复为 No-Go。

## 3. 部署脚本与本地工具检查

- 以下脚本 PowerShell AST 解析均为 0 错误：
  - `scripts/Deploy-ServicePlazaTest.ps1`
  - `scripts/Deploy-ServicePlazaBackendTest.ps1`
  - `scripts/Build-ServicePlazaTestPackage.ps1`
  - `C:\Users\shugo\Documents\heaotang-main\scripts\Backup-TestServerState.ps1`
- 本地 `ssh.exe`、`scp.exe`、`tar.exe`、`npm.cmd`、`go.exe`、`python.exe` 均可用；备份脚本存在。
- 后端部署脚本包含部署前备份、Linux amd64 静态构建、时间戳上传、原二进制备份、PM2 重启、loopback `/ready` 与 `db=true` 检查、失败自动回滚。
- 前端部署脚本包含部署前备份、完整 dist 打包、staging 解包和时间戳 rollback 目录；M4 实际执行时还必须在激活后验证公开 `/app/service-plaza/services/life-navigation/`、资源引用和浏览器主链路，失败时按 rollback 目录恢复，不得只凭上传成功判定通过。
- 本轮没有执行任何 SSH、SCP、HTTP、PM2、远端备份或远端部署命令。

## 4. 测试账号和认证方法

- M4 需要两个相互隔离的非生产测试会员身份：用户 A 用于首次提交、同键重放、冲突和本人历史；用户 B 用于证明不可见用户 A 的记录。
- 账号或短期会话必须由平台负责人通过安全渠道提供；仓库、命令行、报告、截图和 Handoff 均不得保存密码、验证码、JWT 或完整个人标识。
- 浏览器认证必须复用正式共享会话和 `AuthPanel` 语义；页面不得显示后端验证码或 token。同一身份在正式 M4 运行中不得为了 API 与浏览器步骤分别申请验证码。
- 现有 `scripts/Invoke-ServicePlazaApiAcceptance.ps1` 使用专用测试号码并要求测试环境在 send-code 响应中返回测试验证码，可覆盖首次 201、重放 200、冲突 409，但当前账号台账 `test-accounts-and-data.md` 仍将普通会员账号和可用性标为“待补齐”，`security-audit-2026-07-10.md` 也记录“当前没有可安全使用的真实测试验证码或已授权测试会话”。旧远程验收记录不能证明该方法当前仍可用。
- 阻塞根因：测试身份的当前可用状态、验证码取得安全渠道和双用户隔离方法没有一致的权威现状证据。
- 关闭条件：平台负责人只登记账号类型、所属测试环境、获取/保管方式和可用性验证时间；凭据本身通过安全渠道临时交付。随后先执行不持久化凭据的登录探针，失败则停止 M4，不得开启或恢复公开开发验证码作为绕过。

- 解除记录：2026-07-11，两个相互隔离的 test-only 身份 `199****9991` 与 `199****9993` 分别完成 send-code、login、auth-me，三步均为 HTTP 200 且服务端身份存在；验证码和 token 只在内存中短暂使用，验证后已清空，未写入仓库、报告或页面。
- 配额阻塞事实保留：原账号组 `199****9991` / `199****9993` 已被部署前探针和历史验收消耗当日 send-code 配额；正式 API UAT 在创建生命导航记录前即收到 `AUTH_RATE_LIMITED`、HTTP 429，本次失败没有创建 life 记录。不得清除验证码表、修改限流器或继续用该账号组重试来掩盖配额事实。
- 测试身份方法更新：`2026-07-11T01:48:18+08:00`。
- 标准化账号池依据：后端按手机号独立执行每 UTC 日最多 5 次的 send-code 限流，登录使用 `FindOrCreateUser(phone)` 建立隔离身份；`scripts/Deploy-ServicePlazaBackendTest.ps1` 已把 `19900009992` 用作 test phone。平台负责人现将 `19900009992` 与同一非生产测试号段的 `19900009994` 明确登记为本次 M4 另外两名专用 test-only 身份，前者为用户 A、后者为隔离用户 B。
- 安全判断：使用这两个预先登记的合成测试身份不改变每手机号限流、不删除历史计数、不修改服务端时间或数据库，也不扩大到任意号码轮换，因此属于测试账号池容量规划而非绕过安全限流。
- 强制账号方法：
  1. 预检只核对本地配置、账号登记和脚本，不再对正式 UAT 身份调用 send-code。
  2. 正式 UAT 开始时，用户 A 和用户 B 各只调用一次 send-code、login、auth-me；auth-me 是同一会话验证，不得再次申请验证码。
  3. 两个 token 只保存在运行进程内存中，并分别复用于该身份的全部 API 与浏览器 M4 步骤；步骤结束立即清空。
  4. 报告只记录 `199****9992` / `199****9994`、状态码、用户 ID 是否匹配和验证时间，不记录验证码、JWT 或完整手机号。
  5. 任一新身份出现 429、登录失败或身份不一致，立即恢复为 No-Go；不得继续增加临时号码、开启公开开发验证码、修改限流数据或把凭据写入文件作为绕过。

## 5. M4 执行顺序与计划证据

前置 No-Go 关闭后，M4 必须按以下顺序执行，并将每一步的真实结果写入计划路径；文件名不包含账号、token 或验证码：

1. 本地门禁：前端定向/全量测试与 test-server build，后端固定提交的全量 `go test`/`go vet`，契约、UTF-8、秘密扫描和 diff 检查。
2. 部署前证据：远端 `/ready`、PM2 状态、当前前后端制品标识和备份路径。
3. 后端部署（仅当远端不含 `70fa122…` 对应行为）：固定已批准 BackendRoot，备份、上传、原子替换、PM2、`/ready`、失败回滚。
4. 前端部署：备份、构建、staging、激活，验证精确路由和新静态资源；失败立即回滚。
5. API 验收：使用用户 A/B 各自唯一一次取得并持续复用的会话；未登录 401；用户 A 首次 201、同键重放 200 且原 ID/响应头一致、异载荷 409、本人 GET 可见；用户 B GET 不可见用户 A 记录；请求 ID 与错误码可追踪。
6. 浏览器 UAT：复用同一正式 UAT 会话，不再次调用 send-code；验证未登录交接、空/加载、提交、成功后历史刷新、页面刷新后历史仍在、错误恢复、返回 `/services`，覆盖目标移动和桌面视口。
7. 回滚与收口：记录前后制品、备份和精确回滚目标；任何 Blocker/Major 未关闭均为 M4 No-Go。

计划证据文件：

- `docs/project-management/modules/life-navigation/acceptance/LN-M4-001-local-gates.json`
- `docs/project-management/modules/life-navigation/acceptance/LN-M4-001-deployment-evidence.json`
- `docs/project-management/modules/life-navigation/acceptance/LN-M4-001-api-acceptance.json`
- `docs/project-management/modules/life-navigation/acceptance/LN-M4-001-frontend-uat.md`
- `docs/project-management/modules/life-navigation/acceptance/LN-M4-001-rollback-evidence.json`
- `docs/project-management/modules/life-navigation/implementation-records/IR-20260711-LIFE-APPLICATION-HISTORY-M4.json`
- `docs/project-management/modules/life-navigation/LN-M4-001-handoff.md`

这些路径当前只是计划，不得预先创建空报告或写“通过”。当前 Ready 只授权进入 M4 执行；实际证据完成前不得签 M4 Go，`acceptance_readiness` 不得推断为 Go。

## 6. 部署前 No-Go 解除记录

- 原 No-Go 结论保留：默认后端部署源不包含批准修复且有未归属修改；测试身份当时缺少一致的当前可用性证据，因此不得部署。
- 解除依据：平台负责人已把后端源固定为干净的 `70fa122…` 工作树并禁止默认回落；双 test-only 身份现场探针已按不持久化秘密规则通过。
- 解除时间：`2026-07-11T01:38:37+08:00`。
- 当前 Ready 范围：只授权按本文顺序开始 M4 本地门禁、备份、测试环境部署和验收；每个强制断言仍须在执行时重新验证。
- 非授权范围：本记录不构成 M4 Go，不授权生产环境、真实账号、真实资金、秘密持久化或跳过备份/回滚门禁。
