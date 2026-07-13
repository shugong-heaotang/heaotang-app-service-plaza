# H2-M3 合成申请历史与生命周期测试服执行证据

- execution window：2026-07-12 16:01 +08:00
- environment：approved test server / SQLite
- fixture source：integration `1c8e064`，registry closeout `5abadd7`
- deployment mutation：0
- real data：false
- secrets：`none-recorded`

## 执行顺序

每个场景使用独立 RunId，严格执行：

`Plan → Apply → Inspect → Cleanup → RestoreVerify`

不同状态未在同一窗口叠加；Cleanup 完成后才进入下一场景。

| 场景 | RunId | Inspect 权威事实 | Cleanup | RestoreVerify | 结论 |
| --- | --- | --- | --- | --- | --- |
| ApplicationPending | `club-member-home-m3-20260712-160113-936de170` | applications=1，status=pending；目标合成新会员 current membership=0 | 全部 8 类 run-owned 记录 remaining=0；users_deleted=0 | integrity=ok；schema objects=400；dump SHA match | Pass |
| ApplicationRejected | `club-member-home-m3-20260712-160132-1f48dd47` | applications=1，status=rejected；目标合成新会员 current membership=0 | remaining total=0；users_deleted=0 | integrity=ok；dump SHA match | Pass |
| DissolvedClub | `club-member-home-m3-20260712-160141-69ccb699` | clubs=6，memberships=5；目标 run-owned club status=dissolved | remaining total=0；users_deleted=0 | integrity=ok；dump SHA match | Pass |

## 安全与边界

- 未记录或读取 OTP、JWT、Cookie、Authorization、完整手机号或完整 user id。
- 未修改 Schema、业务代码、共享配置或部署制品。
- 未使用真实会员、家庭、健康、资金或生产资料。
- `left/suspended` 没有权威会员关系历史/状态模型，继续为 Unsupported/Unverified；没有用 role、删除当前关系或 club status 冒充。

## 当前判定

测试资料能力和测试服可逆性达到 Go；申请历史 pending/rejected 与 club lifecycle dissolved 的数据库层证据关闭。浏览器展示仍需合成身份会话，且必须复用现有冻结部署和已验证 RunId 机制逐场重建、逐场清理，不能用本数据库证据冒充页面通过。
