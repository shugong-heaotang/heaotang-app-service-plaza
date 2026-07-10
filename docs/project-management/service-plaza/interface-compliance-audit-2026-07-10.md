# 服务广场三大核心板块接口标准符合性审计

- 审计日期：2026-07-10
- 适用标准：`service-plaza.v1`
- 审计范围：统一目录、认证依赖、生命导航、俱乐部联盟、健康大管家及服务广场前端适配层
- 后端证据基线：`C:\Users\shugo\Documents\heaotang-main\backend-go`
- 前端证据基线：`C:\Users\shugo\Documents\APP系统\app`
- 审计方式：源码静态审计，并交叉核对 `api-acceptance-2026-07-10.json` 的测试环境实测结果
- 变更边界：本轮只生成审计报告，未修改前端或后端源码

## 1. 结论

本报告初次审计结论为 **Partial Go**。2026-07-10 基础设施 A 批次复核后，报告列出的四项 P0 均已关闭，内部三大主动作接口结论更新为 **Go**；外部 OIDC/PKCE 和后续业务功能不在本次内部接口 Go 范围内。

统一目录接口已经具备版本化路径、标准信封、稳定错误码和契约测试，可以作为后续板块接入的基线。三项主动作也已经做到 JWT 保护、`snake_case` 字段、会话归属和基本成功信封；测试环境实测证明生命导航与健康咨询创建返回 201，俱乐部重复申请返回同一申请，健康数据未发生跨用户泄漏。

关闭证据：认证 v1 信封与机器码已统一；俱乐部首次 201、重放 200 且前端读取 `application.id`；三项 POST 强制原子 `Idempotency-Key`；API SDK 保留机器码并启用严格 v1 信封。远程运行 `service-plaza-uat-20260710-220412` 已覆盖首次、重放、异载荷冲突、缺失/非法键、跨用户隔离和关联 ID。

## 2. 审计口径

`service-plaza.v1` 的业务 API 最低要求来自 `service-integration-contract-v1.md` 第 5 节：

1. 路径带版本号；
2. JSON 字段使用 `snake_case`；
3. 成功响应为 `{ "success": true, "data": ... }`；
4. 失败响应至少包含 `success=false`、稳定机器码 `code` 和用户可读 `error`；
5. 创建 201、查询 200、校验失败 400、未登录 401、无权限 403、不存在 404、限流 429；
6. 用户归属来自认证会话，不接受请求体覆盖 `user_id`；
7. 重复提交必须声明幂等返回或冲突拒绝，并用契约测试固定。

严重度定义：

| 等级 | 定义 |
| --- | --- |
| P0 | 会破坏统一接入语义、身份边界、客户端正确性或重复提交安全；正式接入前必须关闭 |
| P1 | 不阻止单次主链路，但会造成规模化接入、错误处理或查询一致性问题 |
| P2 | 一致性、可观测性或数据精度改进；应在后续版本治理中关闭 |

## 3. 逐接口审计

### 3.1 服务目录

| 接口 | 认证 | 信封与错误码 | HTTP 状态 | 分页/幂等/归属 | 结论 |
| --- | --- | --- | --- | --- | --- |
| `GET /api/v1/service-plaza/catalog` | 公开，符合导航目录定位 | `response.OK` 返回 `success/data`，包含 `contract_version` | 200 | 当前基线仅 9 项，无分页要求；不涉及幂等和用户归属 | 通过 |
| `GET /api/v1/service-plaza/services/{service_id}` | 公开 | 成功为标准信封；不存在返回 `SERVICE_NOT_FOUND` | 200/404 | 不涉及 | 通过 |

证据：`plugins/service-plaza-plugin/plugin.go:20,86-106`；`plugin_test.go:28-69` 已固定版本化信封和 404 机器码；前端 `serviceCatalogRepository.ts` 校验 `contract_version`，对应测试见 `serviceCatalogRepository.test.ts:9-43`。

### 3.2 认证依赖

| 接口 | 认证 | 信封与错误码 | HTTP 状态 | 字段/前端 | 结论 |
| --- | --- | --- | --- | --- | --- |
| `POST /api/auth/send-code` 及 `/api/v1/auth/send-code` | 公开 | 成功含 `success=true`，但 `message` 位于顶层且没有 `data`；失败只有 `error`，缺 `success=false` 和 `code` | 校验 400、限流 429 正确 | 请求字段 `phone`；前端仍调用无版本路径 | P0/P1 |
| `POST /api/auth/login` 及 `/api/v1/auth/login` | 公开 | 成功为 `success/data`；失败只有 `error`，缺标准失败信封 | 校验 400、认证失败 401 正确 | `phone`、`code` 为小写字段；前端仍调用无版本路径 | P0/P1 |
| `GET /api/auth/me` 及 `/api/v1/auth/me` | JWT | 成功为 `success/data`；处理器内的 401/404 只有 `error`，缺机器码 | 401/404/200 语义正确 | 用户从令牌解析 | P0/P1 |

证据：`plugins/auth-plugin/plugin.go:24-35,45-119,159-215`；前端路径见 `app/src/auth/AuthContext.tsx:50,57`。

根因：认证插件形成早于统一 `response` 包，仍直接使用 `c.Status(...).JSON(...)`；同时为兼容旧客户端保留了无版本路径，服务广场前端尚未切换到已有的 `/api/v1/auth/*` 别名。

修复：所有认证成功与失败统一走 `response.OK`、`response.ErrCode`；定义 `AUTH_PHONE_INVALID`、`AUTH_CODE_INVALID`、`AUTH_RATE_LIMITED`、`AUTH_TOKEN_INVALID`、`AUTH_USER_NOT_FOUND` 等稳定码；前端切换 `/api/v1/auth/*`，旧路径仅作为有弃用期限的兼容入口。

### 3.3 生命导航

| 接口 | 认证/归属 | 信封与错误码 | HTTP 状态 | 分页/幂等 | 结论 |
| --- | --- | --- | --- | --- | --- |
| `POST /api/v1/life-nav/records` | `Auth:true`；`user_id` 由 `MustGetUserID` 注入，请求体无 `user_id` | 成功标准信封；错误由统一 helper 返回机器码，但业务校验都归为通用 `INVALID_REQUEST` | 创建 201、校验 400、限流 429 | 未声明幂等键或冲突策略，重复请求会再次插入 | P0 |
| `GET /api/v1/life-nav/records?limit=` | 同一会话用户，只查询自己的 `user_id` | 成功 `success/data/items` | 200 | 只有 `limit`，没有 `page/size/total` | P1 |

证据：路由和处理器见 `life-navigation-plugin/plugin.go:46-59,147-172`；字段、会话归属及插入见 `service.go:154-169,539-571`；查询强制 `WHERE user_id = ?` 见 `service.go:605-632`。测试环境证据显示创建为 201，记录 ID 为 116。

根因：当前写入模型是普通自增记录，没有接收 `Idempotency-Key`、业务请求号或唯一约束；列表接口是在早期“最近 N 条”场景形成，未使用平台统一分页 helper。

修复：为创建接口选定一种明确策略。推荐接收 `Idempotency-Key`，按 `user_id + endpoint + key` 建唯一约束并返回首次创建结果；同键同载荷重放返回 200，同键不同载荷返回 409 和 `IDEMPOTENCY_KEY_REUSED`。列表改为 `page/size` 并使用 `response.List`；为关键校验增加 `LIFE_DIMENSION_REQUIRED`、`LIFE_TITLE_REQUIRED` 等码。

### 3.4 俱乐部联盟

| 接口 | 认证/归属 | 信封与错误码 | HTTP 状态 | 分页/幂等 | 结论 |
| --- | --- | --- | --- | --- | --- |
| `GET /api/v1/clubs` | JWT；不接受用户归属覆盖 | 成功为 `success/data/items`；服务异常被映射为 400 | 200 | 无 `page/size/total` | P1 |
| `POST /api/v1/clubs/{id}/join` | `Auth:true`；申请人来自 `MustGetUserID`；请求体只有 `message` | 成功为 `success/data/status/application`；错误虽然有机器码，但不存在、已是成员、待审核等均被压成 400/`INVALID_REQUEST` | 首次创建也返回 200，不符合创建 201；不存在俱乐部未返回 404，已是成员未返回 409 | 已存在 pending 申请时返回同一记录，实测幂等；但响应未声明 `created/replayed`，处理器无法选择 201/200 | P0 |

证据：路由和处理器见 `club-plugin/plugin.go:28-43,213-228,342-356`；会话归属、业务检查及重复 pending 返回见 `service.go:707-750`；数据库存在 `UNIQUE(club_id,user_id,status)`，见 `service.go:65-76`。测试环境证据显示首次和重复请求均为 200，重复请求返回同一申请 ID 12。

根因：`ApplyJoinClub` 只返回申请对象，不返回“本次是否新建”，因此处理器无法按首次创建 201、幂等重放 200 分流；同时处理器把 service 层所有领域错误统一映射为 400。

修复：service 层返回 `(application, created, domainError)`；首次创建用 `response.Created`，pending 重放用 200 并返回 `replayed=true`；将 `club not found` 映射为 404/`CLUB_NOT_FOUND`，`already a member` 映射为 409/`CLUB_ALREADY_MEMBER`，非 active 状态映射为 409/`CLUB_NOT_ACTIVE`。为首次与重放两种状态补 handler 契约测试。

前端存在独立 P0 解析缺陷：后端 `data` 是 `{status, application}`，但 `submissionRepository.ts:43,89` 只读取顶层 `result.id`，所以真实俱乐部申请会生成客户端临时 ID，而不是使用 `application.id`。现有测试只检查请求映射，没有断言返回 ID。修复时应为三类返回分别建立明确 DTO，俱乐部读取 `result.application.id`，并增加真实响应形态测试。

### 3.5 健康大管家

| 接口 | 认证/归属 | 信封与错误码 | HTTP 状态 | 分页/幂等 | 结论 |
| --- | --- | --- | --- | --- | --- |
| `POST /api/v1/health/consultations` | `Auth:true`；`user_id` 来自会话，请求体仅含 `patient_name/symptoms` | 标准成功信封；缺姓名使用稳定码 `HEALTH_PATIENT_REQUIRED`；服务器错误为统一码 | 201/400/500 正确 | 未声明幂等或冲突策略，重复请求会再次插入 | P0 |
| `GET /api/v1/health/consultations?page=&size=` | 强制按会话 `user_id` 查询 | 使用 `response.List`，返回 `items/total/page/size` | 200 | 分页完整；不涉及写入幂等 | 通过 |

证据：路由和处理器见 `health-plugin/plugin.go:27-74`；创建和分页查询均以 `userID` 过滤，见 `service.go:157-199`。测试环境证据显示创建为 201；所有者可查询新记录；隔离账号未读取到该记录。

根因：健康咨询创建仍为普通自增写入，没有请求唯一标识；网络重试可能产生重复咨询，并可能重复触发 AI 分析成本。

修复：采用与生命导航相同的通用幂等中间件和存储规则；幂等判定应在调用 AI 服务和数据库写入之前完成。同键同载荷重放返回原咨询，同键不同载荷返回 409。

## 4. 前端通用解析审计

| 项目 | 当前行为 | 风险 | 等级 | 修复 |
| --- | --- | --- | --- | --- |
| 机器错误码 | `ApiEnvelope` 没有 `code`，`ApiError` 只保留 message/status | 页面无法按稳定码处理登录过期、冲突、限流和字段错误，只能解析文案 | P0 | `ApiEnvelope` 增加 `code`；`ApiError` 保存 `code`；UI 按 code 做稳定分支 |
| 成功信封严格度 | `success`、`data` 都是可选，缺 `data` 时直接返回整个 payload | 非标准接口会被静默接受，契约漂移无法尽早暴露 | P1 | 对 `/api/v1` 默认要求 `success===true` 且存在 `data`；允许例外必须显式配置 |
| 非 JSON 响应 | JSON 解析失败被折叠为空对象 | 可能只显示通用状态码，缺少可追踪信息 | P2 | 保存请求 ID/状态/内容类型，生成标准客户端错误 |
| 俱乐部响应 DTO | 把 `{status,application}` 当成 `{id,status}` | 返回错误的申请 ID | P0 | 建立 `ClubJoinResponse` 并读取 `application.id`，新增返回值断言 |
| 创建时间 | 三类提交都使用客户端当前时间 | 与服务器记录时间可能不一致 | P2 | 优先读取服务端 `created_at`，无值时才使用客户端时间 |

证据：`app/src/infrastructure/apiClient.ts:1-15,45-57`；`submissionRepository.ts:43-92`；现有 `submissionRepository.test.ts` 只覆盖请求路径和请求体，未验证三种真实响应 DTO。

## 5. 优先级整改队列

### P0：正式接入前必须关闭

1. **统一认证信封和机器码**：认证插件全部使用统一响应 helper，并增加 `/api/v1/auth/*` 契约测试。
2. **修复俱乐部创建/重放语义**：首次 201、pending 重放 200、领域错误按 404/409 分类；修复前端 `application.id` 解析。
3. **建立通用幂等机制**：生命导航和健康咨询接入统一 `Idempotency-Key` 处理，在副作用发生前判重，并补同键同载荷、同键异载荷、不同键三组测试。
4. **让前端保留机器码**：`ApiError` 暴露 `code`，401 清会话逻辑继续保留；页面禁止依赖错误文案做业务分支。

### P1：规模化接入前关闭

1. 前端认证路径切换到 `/api/v1/auth/*`，为旧路径规定弃用期限。
2. 生命导航记录和俱乐部列表统一 `page/size/total/items`。
3. 俱乐部领域错误建立类型化映射，禁止 service 文案直接决定 HTTP 语义。
4. `/api/v1` 客户端启用严格成功信封校验，并为允许的非标准接口建立显式兼容清单。

### P2：后续治理

1. 创建结果统一读取服务器 `created_at`。
2. API 错误增加请求追踪 ID，客户端记录内容类型与请求 ID，不记录令牌和敏感健康数据。
3. 将接口 DTO 与 OpenAPI/JSON Schema 生成流程连接，减少手写类型漂移。

## 6. 建议的责任分配与验收证据

平台集成负责人负责标准、共享响应 helper、认证/幂等/分页基建和跨板块契约门禁；各板块负责人负责本板块领域错误码、字段语义和数据归属；前端负责人负责严格解析和 UI 错误分支。标准变更由 APP 总架构负责人裁决并通过 ADR 留痕。

每个 P0 关闭时必须同时提交：

1. 后端 handler 契约测试，断言 HTTP 状态、`success/data` 或 `success/code/error`；
2. 前端适配器测试，使用真实响应形态并断言业务 ID 和机器码；
3. 测试环境实测报告，至少覆盖未登录、字段错误、首次创建、重复提交、跨用户隔离；
4. 更新 Handoff 和门禁结论；不得仅凭编译通过关闭问题。

## 7. 已确认的正向证据

- 三项主动作均使用版本化 `/api/v1` 路径和 `snake_case` 请求字段。
- 三项主动作均由 JWT 路由保护，用户归属取自会话，不接受请求体覆盖 `user_id`。
- 生命导航和健康咨询在测试环境创建返回 201。
- 俱乐部重复 pending 申请返回同一记录，没有创建第二条申请。
- 健康咨询列表使用标准分页信封，且测试环境跨用户隔离验证通过。
- 统一目录和单服务查询已经通过后端契约测试。

因此本报告要求的是关闭明确的契约缺口，而不是推翻现有接口或让服务广场代理各板块业务 API。
