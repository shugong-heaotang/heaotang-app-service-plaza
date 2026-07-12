# CA-SC 自建俱乐部列表安全 DTO 根因修复

日期：2026-07-12  
工作项：`AIW-20260712-CLUB-SC-LIST-SAFE-DTO-BACKEND`、`AIW-20260712-CLUB-SC-LIST-SAFE-DTO-EVIDENCE`  
负责人：Club backend agent

## 结论

本地实现检查点完成，结论为 **Implementation Go / Environment Pending**。

- 后端分支：`codex/club-sc-list-safe-dto-backend`
- 后端基线：`97d8bfc5d1396f7907b1e76dfcb7c333a2913436`
- 后端实现提交：`df0575a05c8f75d927d079dc8c662e2cd25b9e55`
- 证据分支：`codex/club-sc-list-safe-dto-evidence`
- 未执行部署、测试环境变更或生产操作。

## 根因

`GET /api/v1/clubs/search` 的 service 层已经执行权威 `type+category` 组合筛选和过滤后分页，但 handler 将 `[]*Club` 直接放入响应信封。完整领域实体包含 `owner_id`、`code`、父级、品牌、地址、Logo、成员数和时间戳等列表合同禁止字段。根因是 HTTP 出口缺少专用列表 DTO，而不是数据库查询或分页算法错误。

## 修复

1. 在 handler 层新增 `clubSearchItemDTO`，字段严格为：
   - `id`
   - `name`
   - `intro`
   - `city`
   - `type`
   - `category`
   - `status`
2. `searchClubs` 在生成响应信封前逐项投影；不再直接序列化 `Club`。
3. 保持 `SearchClubsByCategory`、`total`、`page`、`size` 和所有稳定错误码不变。
4. HTTP handler 回归测试解析真实响应信封，断言：
   - 七个允许字段全部存在且没有第八个字段；
   - `owner_id`、`code`、`parent_id`、`level`、`brand_id`、`province`、`address`、`logo`、`member_count`、`created_at`、`updated_at` 均不存在；
   - `standard+general`、过滤后 `total/page/size` 与既有错误语义保持不变。

## 修改范围

后端仅修改：

- `backend-go/plugins/club-plugin/plugin.go`
- `backend-go/plugins/club-plugin/service_test.go`

证据仓只新增当前 checklist、考试、implementation record 和本报告。没有修改 T0、APP registry、H2、数据库 Schema 或其他业务文件。

## 验证证据

- current checklist：26/26 completed。
- governance exam：attempt 1，score=100，passed。
- 定向：`go test ./plugins/club-plugin -run 'TestSearchClubs|TestClubSearchHandler' -count=1`，通过。
- 全量：`go test ./...`，通过。
- 静态检查：`go vet ./...`，通过。
- 格式与差异：`gofmt`、`git diff --check`，通过。
- 后端远端分支已确认指向 `df0575a05c8f75d927d079dc8c662e2cd25b9e55`。

## 未完成与下一门禁

本检查点不包含部署和真实测试环境 HTTP 取证。平台集成负责人独立复核并受控集成后，T0 验收才能以新后端提交重新构建、部署并验证真实响应字段；在此之前不得把本地实现 Go 写成 Environment Go 或 Release Go。
