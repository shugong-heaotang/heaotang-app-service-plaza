# H2-M3 fixture 安全能力 Handoff

- checkpoint：`H2-M3-FIXTURE-M0`
- work item：`AIW-20260712-CLUB-MEMBER-HOME-M3-FIXTURE`
- owner：H2 fixture platform agent
- branch：`codex/club-member-home-m3-fixture`
- base / merge-base：`bd1100f740567c67a7fb37d69c16ad1605fc469a`
- status：`Implementation ready / environment execution not authorized`
- verdict：`Fixture capability Go; M3 Entry remains No-Go`

## 1. 本检查点成果

新增 `Manage-ClubMemberHomeM3Fixture.ps1`，只允许批准测试服务器和测试数据库，并提供五个显式操作：

1. `Plan`：只输出脱敏计划，不连接服务器、不修改数据；
2. `Apply`：以唯一 RunId 创建本轮拥有的四身份、俱乐部、关系、待办、活动、动态和通知；
3. `Inspect`：核对本 RunId 的记录数量、场景和故障绑定；
4. `Cleanup`：只删除本 RunId 所拥有的下游记录和俱乐部，不删除四个共享合成用户；
5. `RestoreVerify`：在线备份后只在 `/tmp` 隔离文件恢复，校验 integrity 和 dump SHA，不替换 live DB。

RunId 必须匹配 `club-member-home-m3-YYYYMMDD-HHmmss-8hex`。相同 RunId 已存在时 `Apply` 失败关闭；四个批准合成账号存在任何非本轮 membership、owned club 或未读通知时也失败关闭，不会先清理他人数据换取通过。输出只包含别名、脱敏号码、计数和布尔事实。

## 2. 四身份和三个可重复场景

四身份固定为：

- `new-member`：基线预期 `empty`；
- `family-member`：基线预期 `ready`；
- `multi-club-member`：同时拥有 `standard/general` 与 `standard/charity`，预期 `ready`；
- `manager`：在 run-owned `standard/general` 俱乐部为 `director`，预期 `can_manage=true`。

每个场景必须使用新的 RunId，禁止在同一不透明窗口叠加：

| Scenario | 数据机制 | 预期 |
| --- | --- | --- |
| `Baseline` | 四身份正常关系；critical club 存在但未挂载 | empty/ready 基线 |
| `PartialError` | family club 下增加 run-owned `title=''` 的 `family_tasks` | `family-member` 得到 `CMH_TASKS_UNAVAILABLE`，关键 club 数据保留 |
| `CriticalError` | manager 额外挂载 run-owned `type=standard/category=health` club | 聚合失败关闭，当前后端稳定码为 `CMH_CLUB_CLASSIFICATION_INVALID` |

这里的 Scenario 只选择可清理的数据库 fixture，不是前端 query switch、运行时 fault-control 或共享服务破坏。每轮执行后必须先 Cleanup 并 Inspect 为零，再进入下一 RunId。

## 3. 明确边界

- unauthorized 只使用自然失效或无会话，不由本脚本伪造；
- offline 只使用浏览器离线能力，不由服务端数据模拟；
- maintenance 保持 `Unverified`，本检查点不新增生命周期开关；
- 不修改 `TestAccountOtp.psm1`、CA-SC 脚本、应用代码、后端、Schema、共享配置或部署；
- 不发送 OTP、不读取 JWT/Cookie、不记录完整手机号或完整 user id；
- 不访问生产、不处理真实会员、资金或不可逆数据。

## 4. 自动化证明

`Test-ClubMemberHomeM3FixtureSafety.ps1` 已验证：

- 两份 PowerShell 均可由 Windows PowerShell 5.1 解析，UTF-8 BOM + CRLF；
- Plan 对 Baseline/PartialError/CriticalError 三种场景均可离线重放；
- 四身份只以脱敏标识输出；
- partial/critical 使用指定 run-owned 数据机制；
- Cleanup 覆盖所有本轮下游表且不删除 users；
- 无 OTP、生产、资金、query switch、runtime fault-control 或共享 SC 脚本引用；
- 静态测试执行时 server mutations=0、otp requests=0、secrets persisted=false。

## 5. 未执行和下一门禁

本检查点只证明 fixture 管理能力和静态安全，未执行 `Apply`、远端 `Inspect`、`Cleanup` 或 `RestoreVerify`，未部署任何制品，也未进行四身份浏览器 UAT。因此：

- H2-M3 Entry/Full Go 仍保持 No-Go；
- maintenance 仍为 Unverified；
- 首次测试环境执行前仍需独立批准联合窗口、备份/回滚、OTP 容量和证据责任人；
- 平台集成负责人独立复核本提交后，才可受控集成并另行授权环境运行。
