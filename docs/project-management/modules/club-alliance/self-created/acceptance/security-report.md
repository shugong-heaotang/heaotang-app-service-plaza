# CA-SC T0 安全验收报告

- 环境：测试环境 `https://heaotang.cn`
- APP / backend：`2c4b295e6fd625a2df24957f7b8becbc28ad1dcf` / `98426ff83a1218080019faa377c152a81ecca437`
- fixture run：`club-sc-t0-20260712-100100`
- 结论：`Pass`（仅限 CA-SC T0 安全边界）

## 已验证

1. 未登录 search 返回 401；guest 页面显示 `authentication_required`，未调用 SC 业务 API。
2. 服务端同时应用 `type=standard AND category=general`；10 条混合 fixture 中仅 5 条有效自建数据进入列表，零串类。
3. 列表和详情均使用字段白名单 DTO。列表精确字段为 `id/name/intro/city/type/category/status`，详情按合同返回；`owner_id/code/parent_id/level/brand_id/province/address/logo/member_count/created_at/updated_at` 等禁止字段计数为 0。
4. 非自建详情 404；加入申请首次、同载荷重放、异载荷冲突及并发单 pending 均通过。
5. 本人申请使用当前登录身份；两个合成用户的申请记录隔离，不接受客户端 user_id 越权。
6. 模块网络仅命中 search/detail/join/my-applications allowlist；创建、审核、成员、角色、支付、公益写入和友联体写入请求为 0。
7. 唯一 RunId 清理后，run-owned clubs、applications、members 和 `api_idempotency_keys` 均为 0，数据库 ready。
8. 报告不记录手机号、OTP、JWT、cookie 或完整用户标识；浏览器秘密文件和恢复临时文件均已删除。
9. SQLite 在线备份在隔离临时数据库完成恢复，`PRAGMA integrity_check=ok`，备份/恢复 dump SHA 匹配，未修改在线数据库。

## 保留边界

- 环境 Enter 仍是控制通道 Unverified，不属于安全放宽，也不作为产品失败。
- 创建、审核、成员管理、资金、生产和真实数据继续 No-Go。
