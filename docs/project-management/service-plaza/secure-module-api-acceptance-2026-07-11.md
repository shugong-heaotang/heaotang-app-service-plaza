# 三大核心服务安全 API 验收工具（2026-07-11）

## 结论

部署后 API 验收已从“读取 `send-code` HTTP 响应中的验证码”改为受限测试服务器内存取码，并在任何发送前执行 UTC 日额度预检。静态安全门禁通过；本切片没有发送验证码、没有登录、没有修改测试服务器，也没有把验证码或令牌写入报告。

当前结论为：本地实现 Go；测试环境执行等待生命导航二 M4 单次复测和候选制品部署后进行。

## 安全边界

- 只允许 `https://heaotang.cn`、`root@47.94.159.60` 和批准的测试 SQLite 路径。
- 只允许合成账号池 `19900009991` 至 `19900009994`。
- 两个账号都先运行 `Test-TestAccountOtpCapacity.ps1`，不足即失败关闭。
- HTTP 响应中的 `data.code` 不再读取，并在响应对象中立即删除。
- OTP 只通过 SSH 标准输入执行只读查询，取最新未使用、未过期的 6 位值；函数不记录该值。
- 登录响应中的 token 被捕获后立即从响应对象删除；OTP、主 token 和隔离 token 使用结束后置空。
- JSON 报告只保存脱敏号码、用户 ID 和验收结果，明确 `secrets_persisted=false`。

## 新增覆盖

- `GET /api/v1/clubs/search?type=standard` 只返回 active/standard。
- `GET /api/v1/clubs/join-applications/my` 包含本次申请。
- 健康创建和历史响应包含 `private, no-store`。
- 健康历史 DTO 不包含 `user_id`、`ai_advice`。
- 非法健康分页回退为 `page=1`、`size=20`。
- 保留生命导航、俱乐部申请、健康咨询的首次、重放、冲突和跨用户隔离验证。

俱乐部管理者审核仍需要单独批准的管理账号和测试夹具；当前脚本不伪造管理权限，也不直接改数据库制造审核结果。

## 验证证据

```text
Test-ServicePlazaApiAcceptanceSafety.ps1: passed
OTP requests sent: 0
Server mutations: 0
HTTP code exposure consumed: false
Secrets persisted: false
Invalid target: rejected before SSH
Invalid environment: rejected before capacity query
PowerShell AST parse: passed
Service Plaza contracts: passed after governance snapshot R3
Text encoding: passed
```

## 后续执行顺序

1. 生命导航二在 UTC 日额度恢复后完成一次 M4 浏览器复测。
2. 执行前端模拟失败回滚演练并确认旧资源恢复。
3. 正常部署已构建候选制品。
4. 重新运行 OTP 容量预检；容量充足才执行本验收脚本。
5. 保存脱敏 JSON 报告并完成三板块浏览器 UAT、安全日志扫描和综合验收。
