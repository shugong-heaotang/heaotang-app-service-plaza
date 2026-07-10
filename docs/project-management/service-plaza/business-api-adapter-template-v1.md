# 业务 API 适配器模板 v1

## 目的

板块只负责业务请求和响应的映射，不自行实现认证、严格响应信封、错误解析、请求关联 ID、超时、取消、重试或幂等键。公共实现位于 `app/src/infrastructure/businessApiAdapter.ts`，可编译示例位于 `app/src/modules/_template/exampleServiceApi.ts`。

## 责任边界

| 由平台适配器统一负责 | 由板块适配器负责 |
| --- | --- |
| Bearer 会话附加 | `serviceId` 和 `operationId` |
| `/api/v1/` 严格成功/失败信封 | API 路径和 HTTP 写方法 |
| `ApiError`、机器错误码和请求 ID | 业务输入到请求体的映射 |
| 请求超时、取消和关联 ID | 响应业务类型 |
| GET 瞬时故障安全重试 | 页面状态和业务校验 |
| 写入幂等键及同键受控重试 | 是否需要显式复用同一逻辑写入的键 |

板块代码不得直接从 `apiClient.ts` 导入 `apiRequest`，也不得自行设置 `Authorization`、`Idempotency-Key` 或重试策略。外部合作服务不使用本模板；它必须通过后续 OIDC/PKCE 专项适配器接入。

## 新板块接入步骤

1. 在板块目录创建一个 `*Api.ts` 文件。
2. 使用 `createBusinessApiAdapter("板块-service-id")` 建立边界。
3. 使用 `defineBusinessRead` 或 `defineBusinessWrite` 声明每个操作。
4. 只填写 `operationId`、v1 路径、写方法、业务请求体和响应类型。
5. 页面或状态层只调用板块导出的语义方法，例如 `records.list()` 或 `applications.create()`。
6. 用 Mock HTTP 响应覆盖成功、机器错误码、取消、写入重放和业务映射。
7. 运行前端全量测试、构建和 UTF-8 门禁。

最小形状：

```ts
const api = createBusinessApiAdapter("activity-plaza");

const createApplication = defineBusinessWrite<Input, Application>({
  operationId: "create-application",
  method: "POST",
  path: () => "/api/v1/activities/applications",
  body: (input) => ({ activity_id: input.activityId }),
});

export const applications = {
  create: (input: Input, options?: BusinessApiExecutionOptions) =>
    api.execute(createApplication, input, options),
};
```

## 关键语义

- 默认 `authMode` 是 `shared-session`；只有明确公开的内部 v1 读取接口才能在操作声明中指定 `anonymous`。
- 读操作固定使用 GET，并仅对公共 SDK 允许的瞬时故障进行最多两次尝试。
- 写操作自动生成 `{serviceId}-{operationId}-{nonce}` 幂等键，重试期间保持不变。
- 页面因超时后恢复而确认重放同一次逻辑写入时，可以通过 `BusinessApiExecutionOptions.idempotencyKey` 复用原键；新业务意图不得复用旧键。
- 适配器拒绝非 `/api/v1/` 地址、非 kebab-case 标识和非法幂等键，不能借模板调用旧接口或外部域名。
- 底层 `ApiError` 不被包装，页面仍能读取稳定的 `code`、`status` 和 `requestId`。

## 验收命令

```powershell
Set-Location app
npm test
npm run build
Set-Location ..
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/Test-TextEncoding.ps1
```

## 当前迁移证据

`submissionRepository.ts` 的生命导航、俱乐部申请、健康咨询和俱乐部列表均已改用本模板。该文件只保留业务字段映射和前置业务校验，不再复制认证、幂等头、错误解析或重试配置。
