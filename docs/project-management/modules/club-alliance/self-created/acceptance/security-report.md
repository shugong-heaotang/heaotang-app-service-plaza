# CA-SC T0 安全验收报告

- 环境：测试环境 `https://heaotang.cn`
- APP / backend：`2c4b295e6fd625a2df24957f7b8becbc28ad1dcf` / `a998812cf44dc449d85b726706d4ae2573179860`
- 结论：安全边界通过；固定 seed fixture 已清理，测试数据库保持 ready。

## 已验证

1. 未登录访问 search 返回 401；浏览器进入自建页面显示 `authentication-required`，未调用 SC 业务 API。
2. 列表由服务端同时应用 `type=standard AND category=general`，混合 fixture 零串类。
3. 非自建详情返回 404；详情只返回安全 DTO。
4. 加入申请验证首次、同载荷重放、异载荷冲突和并发单 pending。
5. 本人申请使用当前登录身份，不接受客户端 `user_id`；两个合成用户记录隔离。
6. Nginx 时间窗内业务请求仅命中允许的 search/detail/join/my-applications；创建、审核、成员、角色、支付、公益写入和友联体写入请求为 0。
7. 报告不记录手机号、OTP、JWT、cookie 或完整用户标识；浏览器一次性秘密文件已删除。
8. 所有 mutation 仅指向固定 seed 测试 fixture；生产和真实资金操作为 0。

## 残余边界

- 外部 `ab.chatgpt.com` Statsig 超时属于浏览器控制层，不计入 APP 请求或产品故障。
- cleanup 后固定前缀俱乐部、关联申请和成员均为 0；两个批准的合成账号属于共享测试账号池，不在本切片删除范围。
- 创建、审核、成员管理、资金、生产仍为 No-Go。
