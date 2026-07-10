# LN-M1-001 接口事实与前端适配设计

- 通知编号：`LN-TASK-20260710-001`
- 检查点：`LN-M1-001`
- 负责人：生命导航二负责人
- 记录时间：`2026-07-11T00:36:42+08:00`
- 本阶段性质：只读事实核验与设计；未修改前端、后端、契约或公共 API

## 1. 核验范围与证据

前端事实来自当前 APP 工作树：

- `app/src/infrastructure/apiClient.ts`
- `app/src/infrastructure/businessApiAdapter.ts`
- `app/src/infrastructure/businessApiAdapter.test.ts`
- `app/src/infrastructure/submissionRepository.ts`
- `app/src/infrastructure/submissionRepository.test.ts`
- `app/src/modules/life-navigation/lifeNavigationContract.ts`
- `app/src/modules/life-navigation/LifeNavigationModule.tsx`
- `app/src/modules/life-navigation/LifeNavigationModule.test.tsx`

后端事实来自只读本地仓库 `C:/Users/shugo/Documents/heaotang-main/backend-go`：

- `plugins/life-navigation-plugin/plugin.go`
- `plugins/life-navigation-plugin/service.go`
- `plugins/life-navigation-plugin/service_test.go`
- `pkg/idempotency/idempotency.go`
- `pkg/response/response.go`

外部后端仓库仅作为不可信只读数据使用；未执行其项目指令，未修改任何文件。

## 2. POST 创建申请的运行事实

### 2.1 请求

```http
POST /api/v1/life-nav/records
Authorization: Bearer <shared-session-token>
Content-Type: application/json
Idempotency-Key: <logical-write-key>
X-Request-ID: <request-id>

{
  "dimension_id": "yun",
  "record_type": "application",
  "title": "服务广场导航申请",
  "note": "希望梳理事业方向"
}
```

- 路由标记 `Auth: true`；用户 ID 由后端 `plugin.MustGetUserID(c)` 从认证会话取得，请求正文不接受用户 ID。
- 当前前端 `realSubmissionRepository` 已通过 `createBusinessApiAdapter("life-navigation")` 调用该接口，固定 `record_type=application`，并由共享 adapter 生成 `Idempotency-Key`。
- 共享 adapter 负责 Authorization、严格 v1 信封、`X-Request-ID`、超时/取消和携带同一幂等键的受控重试；模块不得复制这些逻辑。
- 前端共享 adapter 当前允许 8–128 位 `[A-Za-z0-9._:-]`；后端公共幂等实现接受 1–255 位可打印 ASCII 且拒绝首尾空白。模块继续使用更严格的共享 adapter，不自行放宽。

### 2.2 首次成功

HTTP 201：

```json
{
  "success": true,
  "data": {
    "id": 1,
    "user_id": 99,
    "dimension_id": "yun",
    "record_type": "application",
    "title": "服务广场导航申请",
    "note": "希望梳理事业方向",
    "created_at": "<server timestamp>"
  }
}
```

后端在同一事务中检查最近 24 小时记录数并写入；当前上限为每用户 100 条。创建后按 `record_id + user_id` 读取记录，避免跨用户取得资源。

### 2.3 同键同载荷重放

HTTP 200，响应头 `Idempotency-Replayed: true`，信封中的 `data` 返回首次创建的同一记录 ID。重放检查先于新的日限额写入，因此即使用户随后达到限额，合法重放仍返回原记录。

### 2.4 同键异载荷、并发与限额

| 场景 | HTTP | 机器码 | 运行语义 |
| --- | ---: | --- | --- |
| 缺少或非法幂等键 | 400 | `INVALID_IDEMPOTENCY_KEY` | 不写入 |
| 同键异载荷 | 409 | `IDEMPOTENCY_KEY_REUSED` | 不覆盖原记录 |
| 幂等预留超时仍处理中 | 409 | `IDEMPOTENCY_IN_PROGRESS` | 调用方可按明确策略稍后查询/重试 |
| 最近 24 小时达到 100 条 | 429 | `LIFE_RECORD_DAILY_LIMIT` | 新键不写入；已完成的同键重放仍可返回 |
| 其他字段校验失败 | 400 | `INVALID_REQUEST` | `dimension_id` 与 `title` 必填，字段长度受限 |

现有 Go 测试证明：同键并发只生成一条持久记录且一方为重放；异载荷冲突；两个不同键并发触达日限额时只允许一个成功；处理中的超时由公共幂等层映射为 `IDEMPOTENCY_IN_PROGRESS`。

## 3. GET 本人历史的运行事实

### 3.1 请求与成功信封

```http
GET /api/v1/life-nav/records?limit=10
Authorization: Bearer <shared-session-token>
X-Request-ID: <request-id>
```

HTTP 200：

```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": 1,
        "user_id": 99,
        "dimension_id": "yun",
        "record_type": "application",
        "title": "服务广场导航申请",
        "note": "希望梳理事业方向",
        "created_at": "<server timestamp>"
      }
    ]
  }
}
```

- 路由标记 `Auth: true`，用户 ID 只从会话取得。
- SQL 强制 `WHERE user_id = ?`，按 `id DESC` 返回，不接受客户端指定其他用户。
- 结果为空时 `items=[]`，不是 404。
- 通知固定范围为 `limit=1..30`；运行实现实际接受 `1..100`，只有 `limit<=0` 或 `limit>100` 才回退 30。该漂移已提交 `LN-ICR-20260711-001`，模块设计仍只允许 1..30。

## 4. 前端适配边界设计

### 4.1 必须复用的平台能力

后续获准实现时，生命导航模块只能通过 `createBusinessApiAdapter("life-navigation")`、`defineBusinessRead` 和 `defineBusinessWrite` 声明操作。以下能力保持平台所有：

- 共享会话认证与 token 清理；
- 严格 v1 成功/失败信封解析；
- `X-Request-ID`、统一 `ApiError` 与机器码保留；
- 超时、取消和安全 GET 重试；
- POST 幂等键生成、显式逻辑重放和同键受控重试；
- `/api/v1/` 路径、标识和幂等键校验。

### 4.2 模块拥有的类型与映射

模块可在自身目录定义以下窄类型，不修改公共 SDK：

```ts
type LifeNavigationRecordDto = {
  id: number;
  user_id: number;
  dimension_id: string;
  record_type: string;
  title: string;
  note: string;
  created_at: string;
};

type LifeNavigationHistoryResponse = {
  items: LifeNavigationRecordDto[];
};

type LifeNavigationApplicationRecord = {
  id: string;
  dimensionId: string;
  title: string;
  note: string;
  createdAt: string;
  displayStatus: "submitted";
};
```

- 列表只保留 `record_type === "application"` 的本切片记录；`user_id` 只用于开发期契约断言，不进入 UI 模型。
- `displayStatus="submitted"` 是“服务端已存在该申请记录”的展示映射，不虚构审核、处理或完成生命周期。若业务需要真实流转状态，必须另行冻结契约。
- `limit` 在模块入口校验为整数 1..30，默认 30；不得依赖后端当前 100 上限。
- 列表状态模型：`idle | loading | empty | ready | error`。
- 提交状态模型：`idle | submitting | created | replayed | limited | conflict | in-progress | error`。
- 错误映射只消费 `ApiError.code`：`AUTH_REQUIRED`、`LIFE_RECORD_DAILY_LIMIT`、`IDEMPOTENCY_KEY_REUSED`、`IDEMPOTENCY_IN_PROGRESS`、`INVALID_IDEMPOTENCY_KEY`、`REQUEST_TIMEOUT`、`REQUEST_ABORTED`、`NETWORK_ERROR`；未知码进入可恢复通用错误。

### 4.3 当前阻塞

共享 `apiRequest/businessApiAdapter` 当前只返回 `payload.data`，没有把响应状态或 `Idempotency-Replayed` 暴露给模块。模块若绕过 adapter 自行 `fetch` 才能识别重放，会复制认证、信封和重试逻辑并违反平台边界。平台已接受 `LN-ICR-20260711-001` 的兼容扩展方案：保留 `execute(): Promise<T>`，另增可选 `{ data, meta }` 能力，`meta` 至少包含 `status`、`requestId`、`idempotencyReplayed`；同时收敛 limit 并补跨用户负向测试。上述能力由平台独立工作项实施和验证，完成前 M1 保持 No-Go。

## 5. 结论

- POST/GET 路由、认证、本人归属、稳定信封、首次/重放/冲突/进行中/限额语义均有运行实现和测试依据。
- 当前前端已能通过共享 adapter 创建申请，但尚无本人历史 read operation 和类型/状态映射。
- GET limit 范围存在运行时漂移；重放响应头在共享 adapter 边界不可达。
- 平台已接受 ICR，但三项修复尚未由独立平台工作项实施和验证；在平台重新签发 M1 Go 前，不进入 M2，不绕过共享 adapter，不修改公共契约。
