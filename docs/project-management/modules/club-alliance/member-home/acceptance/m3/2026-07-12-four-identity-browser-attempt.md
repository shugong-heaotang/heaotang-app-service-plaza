# H2-M3 四合成身份浏览器认证尝试

- execution window：2026-07-12 16:20–17:12 +08:00
- environment：approved test server / in-app Browser
- authorization：用户明确允许四个合成账号各发送一次测试验证码
- fixture：Baseline RunId `club-member-home-m3-20260712-170757-9d4d9bd8`
- secrets：`none-recorded`

## 执行边界

每个合成身份最多发送一次验证码。发送前容量已验证；验证码仅经内存通道传入浏览器，不写入项目文件、不输出、不截图。登录结束或失败后不重复发送。

| 身份 | 唯一发送 | 服务端消费事实 | 浏览器页面证据 | 结论 |
| --- | --- | --- | --- | --- |
| new-member | 1 | 未消费；浏览器重连期间自然过期，当日额度随后耗尽 | 无 authenticated DOM | `Blocked/Unverified` |
| family-member | 1 | latest used=true，认证请求成功 | 控制进程在会话状态稳定前跳转，未保留 member-home DOM | `Auth Pass / Page Unverified` |
| multi-club-member | 1 | latest used=true，认证请求成功 | 等待 authenticated DOM 时控制进程超时重置 | `Auth Pass / Page Unverified` |
| manager | 1 | latest used=true，认证请求成功 | 延长控制窗口后仍在 member-home DOM 取证前重置 | `Auth Pass / Page Unverified` |

以上只保存 used true/false、过期状态和匿名角色结论，没有读取或记录验证码、JWT、Cookie、Authorization、完整手机号或完整 user id。

## 控制通道根因

应用内浏览器可完成页面打开、DOM 读取、字段填写、虚拟剪贴板和登录点击；但 Statsig 插件初始化/注册请求持续超时，浏览器控制进程多次在 60–120 秒窗口内重置。三条验证码被服务端消费，说明登录请求已到达并成功；控制进程没有稳定保留登录后的标签和 sessionStorage，因此不能把认证成功推断为会员首页页面通过。

这属于 automation/control-channel，不是已证明的产品失败。也不能用先前 API acceptance、静态组件测试或数据库 fixture 代替真实 DOM、viewport、键盘和网络证据。

## Fixture 恢复

Baseline 场景完成后已执行 Cleanup 和 RestoreVerify：

- run-owned remaining total=0；
- users_deleted=0；
- integrity=ok；
- dump SHA match=true；
- `/ready`=200；
- `/health?json=1` status=ok；
- 系统剪贴板已清空；临时内存传输进程和辅助脚本已删除。

## 当前可审计结论

`Conditional No-Go — synthetic data and authentication evidence passed; authenticated member-home browser DOM remains control-channel Unverified.`

四账号“一次验证码”授权已用完，不得再次发送。下一次浏览器复测必须等待 UTC 日自然重置和新的明确授权，并优先修复或替换同一应用内浏览器控制通道；不得重复部署、不得使用真实资料、不得把 Auth Pass 冒充 Page Pass。
