# 测试账号验证码容量门禁实施记录

- 工作项：`AIW-20260711-TEST-OTP-CAPACITY-GATE`
- 实现记录：`IR-20260711-TEST-OTP-CAPACITY-GATE-R5`
- 环境：批准的测试服务器
- 当前状态：实现完成；成功路径等待 UTC 日自然重置后验证

## 根因

生命导航二 M4 的 API UAT 与真实浏览器 UAT 需要彼此隔离的短会话。原计划只统计本轮预期发送次数，没有在开始前读取测试身份已有的 UTC 日累计消耗，导致 API 证据完成后浏览器账号已无剩余额度。受控浏览器不能安全注入 shell 中的 JWT，因此不能把复用会话作为修复。

## 系统性修复

`scripts/Test-TestAccountOtpCapacity.ps1` 在任何 send-code 前只读查询批准测试服务器的 `verification_codes` 当日计数，并以与后端 `date(created_at) = date('now')` 相同的 SQLite UTC 日期口径计算容量。脚本：

- 只接受格式合法的中国大陆手机号和 1 至 5 次需求量；
- 通过标准输入把 SQL 交给固定测试服务器，不把完整手机号写进命令行或报告；
- 不查询 `code`、JWT 或其他秘密；
- 只输出脱敏号码、UTC 日期、已用/剩余/所需次数和布尔结论；
- 容量不足以退出码 2 失败关闭，不自动换号、清理计数或改变后端限流。

当前后端事实为每个手机号、每个 SQLite UTC 日最多 5 次；脚本不允许调用者扩大限额。后端限额变更时脚本必须在同一平台工作项更新并重新验证。

## 当前验证

- 后端源码事实：`backend-go/internal/core/auth/auth.go` 使用 `date('now')` 统计当日次数，达到 5 次返回限流错误。
- 失败路径已于 `2026-07-11T02:42:51+08:00` 从批准测试账号执行：只输出 `199****9992`，SQLite UTC 日期 `2026-07-10`，`used=5`、`remaining=0`、`capacity_ready=false`、`secrets_read=false`，进程稳定返回退出码 2。
- 实现回归：首次执行发现 PowerShell 5.1 把 `$maskedPhone:` 解析为非法变量作用域，已改为 `${maskedPhone}`；第二次发现 `ErrorActionPreference=Stop` 使 `Write-Error` 抢先返回 1，已改为标准错误流直写并复测退出码 2。两个问题均先关闭根因再继续。
- PowerShell AST、UTF-8 BOM 和 CRLF 专项检查通过。
- 总门禁同时发现并关闭历史考试快照字节漂移；当前任务已用规范 LF 检查单完成最终 R5 重新认证，详见 `governance-snapshot-repair-2026-07-11.md`。
- 当前总门禁通过：协作范围无重叠、重复问题登记有效、R5 试卷与检查单哈希一致、实现记录有效、服务广场契约通过、文本编码、全部 PowerShell AST 与 `git diff --check` 通过。
- 成功路径：北京时间 08:00 后、实际浏览器 UAT 前执行；必须先得到 `capacity_ready=true`，再允许一次 send-code。

在成功路径、PowerShell AST、UTF-8、重复问题、契约与实现记录门禁全部通过前，本门禁状态不得升级为 `verified`。
