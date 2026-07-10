# 服务广场板块接入标准 v1

协议标识：`service-plaza.v1`

## 1. 适用范围

本标准适用于所有希望出现在和奥堂 APP 服务广场中的内部板块和外部合作服务。服务广场只承担服务发现、权限预检、导航交接和返回路径治理，不代替接入方处理具体业务。

机器可读结构见 `contracts/service-plaza/service-manifest.schema.json`。

## 2. 标准目录接口

### 获取服务目录

```http
GET /api/v1/service-plaza/catalog
```

成功响应：

```json
{
  "success": true,
  "data": {
    "contract_version": "service-plaza.v1",
    "items": []
  }
}
```

### 获取单个服务

```http
GET /api/v1/service-plaza/services/{service_id}
```

不存在时返回 HTTP 404：

```json
{
  "success": false,
  "code": "SERVICE_NOT_FOUND",
  "error": "service not found"
}
```

## 3. 清单必填规则

| 字段 | 规则 |
| --- | --- |
| `contract_version` | 固定为 `service-plaza.v1` |
| `service_id` | 小写字母、数字和连字符；发布后不可复用给其他服务 |
| `display_name` | 服务广场展示名称 |
| `category` | `core` 或 `common` |
| `sort_order` | 同一类别内的稳定排序数字 |
| `lifecycle_status` | `active`、`preview`、`planned`、`maintenance`、`offline` |
| `entry.type` | `internal_route`、`external_https` 或 `mini_program` |
| `access.auth_mode` | `shared_session`、`oidc_pkce` 或 `anonymous` |
| `provider.provider_id` | 平台分配的稳定提供方标识 |
| `capabilities` | 该服务可承接的能力标识数组 |

## 4. 导航与认证

- 内部路由必须以 `/services/` 开头，并提供 `/services` 返回路径。
- 外部 Web 入口必须使用 HTTPS，并经过域名白名单审核。
- URL 中禁止携带 JWT、验证码、手机号、健康信息或其他个人数据。
- 内部板块使用 `shared_session`；外部需要登录时使用 `oidc_pkce`。
- `planned`、`maintenance`、`offline` 服务不得执行正式跳转，前端展示标准状态说明。

## 5. 业务 API 最低标准

接入方业务 API 可以保留自己的资源模型，但必须满足：

- 路径带版本号；
- JSON 字段使用 `snake_case`；
- 成功响应使用 `{ "success": true, "data": ... }`；
- 失败响应至少包含 `success=false`、稳定机器码 `code` 和用户可读 `error`；
- 创建成功使用 HTTP 201，查询成功使用 200，校验失败使用 400，未登录使用 401，无权限使用 403，不存在使用 404，频率限制使用 429；
- 用户数据必须从认证会话取得归属，不接受请求体覆盖 `user_id`；
- 重复提交必须声明是幂等返回还是冲突拒绝，并用契约测试固定。

## 6. 接入流程

1. 合作方取得 `provider_id` 和清单模板。
2. 提交清单、图标资产、隐私说明、测试入口和业务 API 文档。
3. 平台执行 Schema、域名、权限、状态、返回路径和安全检查。
4. 在测试环境注册为 `preview` 并完成 UAT。
5. Handoff 通过后更新为 `active`。
6. 变更入口、认证模式、隐私等级或提供方必须重新审核。

## 7. 第一批接入实例

- `life-navigation`：生命导航，核心服务，内部共享会话。
- `club-alliance`：俱乐部联盟，核心服务，内部共享会话。
- `health-manager`：健康大管家，核心服务，内部共享会话，敏感数据等级。
- 活动广场、人脉中心、保障商城、二手集市、AI、学习广场先以 `planned` 状态注册。
