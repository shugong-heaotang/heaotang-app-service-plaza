# H2-M3 申请历史与生命周期 fixture 扩展 Handoff

- checkpoint：`H2-M3-FIXTURE-EXTENSION`
- work item：`AIW-20260712-CLUB-MEMBER-HOME-M3-FIXTURE-EXTENSION`
- owner：H2 fixture extension agent
- branch：`codex/club-member-home-m3-fixture-extension`
- status：`Implementation verified locally / environment execution pending`
- verdict：`Local Fixture Go; test-server execution not yet authorized`

## 已完成

现有 fixture 工具新增三个显式场景：

- `ApplicationPending`：为合成新会员创建一条 pending 加入申请，不创建当前 membership；
- `ApplicationRejected`：为合成新会员创建一条 rejected 加入申请，不创建当前 membership；
- `DissolvedClub`：创建 run-owned dissolved 俱乐部和一条明确的当前关系，用于验证 `club_status=dissolved` 与 `membership_status=active` 分层。

`Get-RunCounts`、Inspect 和 Cleanup 已纳入 `club_join_applications`。Cleanup 先删除 run-owned 申请，再删除关系和俱乐部；始终保留四个共享合成用户。

## 可回滚验证

安全测试在专用临时目录创建隔离 SQLite，三个新场景分别执行：

`Apply → Inspect → Cleanup → remaining=0`

随后执行 `RestoreVerify`，确认隔离备份恢复后的 integrity 为 ok、schema object count 大于 0、dump SHA-256 一致，并删除临时恢复文件。测试结束后整个临时目录删除。

结果：三个场景通过；测试服务器变更 0；OTP 请求 0；秘密持久化 false；真实资料 false。

## 边界与下一步

- `left/suspended` 继续保持 Unsupported/Unverified；当前没有权威会员关系历史/状态模型，禁止 fixture 冒充。
- 本检查点没有连接测试服务器，没有部署，没有调用业务 API，没有读取登录会话。
- 下一步须先由平台独立复核本提交并受控集成；测试环境窗口只运行三个新场景，逐场 Cleanup 和 RestoreVerify，禁止重复部署未漂移制品。
- 浏览器后端恢复后，复用同一部署和对应 RunId 补页面、DOM、网络和键盘证据；控制通道不可用时继续标记 Unverified。
