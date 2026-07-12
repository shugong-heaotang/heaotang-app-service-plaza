# H2-M3 最小合成测试资料设计

- checkpoint：`H2-M3-SYNTHETIC-DATA-DESIGN`
- record：`IR-20260712-CLUB-MEMBER-HOME-M3-SYNTHETIC-DATA-DESIGN`
- verdict：`Design Go / environment execution pending`
- 原则：只使用测试环境、合成身份、RunId 归属记录和可恢复清理；不使用真实会员资料，不读取或保存 OTP、JWT、Cookie、完整手机号或完整用户标识。

## 1. 本轮只做四件事

1. 用一个合成新会员建立 `pending` 加入申请，但不建立 `club_members`；预期会员首页仍为 `empty`、当前俱乐部数为 0。
2. 用另一个合成新会员建立 `rejected` 加入申请，但不建立 `club_members`；预期会员首页仍为 `empty`、当前俱乐部数为 0。
3. 用一个合成会员关联一个 `status=dissolved` 的 run-owned 俱乐部；预期响应明确返回 `club_status=dissolved`，不得把它写入 `membership_status`。
4. 每个场景使用独立 RunId，执行前 Plan，执行后 Inspect、Cleanup、Inspect=0、RestoreVerify；不同状态不在同一不透明窗口叠加。

## 2. 最小资料矩阵

| 场景 | 合成资料 | 权威表 | 预期 API/页面事实 | 清理边界 |
| --- | --- | --- | --- | --- |
| `ApplicationPending` | run-owned active standard/general club；合成用户；一条 status=pending 的加入申请；无 membership | `clubs`、`club_join_applications` | 申请存在，但 `joined_club_count=0`、`clubs=[]`、页面仍为 empty | 只删本 RunId 对应申请和俱乐部；不删共享合成用户 |
| `ApplicationRejected` | run-owned active standard/general club；合成用户；一条 status=rejected 的加入申请；无 membership | `clubs`、`club_join_applications` | rejected 只属于申请历史，不得成为当前 membership | 同上 |
| `DissolvedClub` | run-owned dissolved standard/general club；合成用户；一条当前关系 | `clubs`、`club_members` | 返回 `club_status=dissolved`；`membership_status` 仍按当前实现为 active；页面不得把 dissolved 解释成 membership 状态 | 先删 membership，再删 run-owned club |

所有名称和正文使用固定的 `synthetic-only` 文案；RunId 进入俱乐部 code 或可审计引用，不写入真实姓名、家庭情况、健康信息或业务正文。

## 3. 当前不能靠测试资料解决的状态

| 状态 | 当前事实 | 判定 |
| --- | --- | --- |
| `left` | 当前 `club_members` 没有关系状态或历史表；删除关系后没有权威历史实体 | `Unsupported/Unverified`，需要独立后端合同和数据模型工作项 |
| `suspended` | 当前 `club_members` 没有 suspension 字段；会员首页后端把 `membership_status` 固定投影为 `active` | `Unsupported/Unverified`，禁止用 role、club status 或临时字段冒充 |

这两个缺口不阻塞 pending/rejected 与 dissolved 的合成验收，但继续阻止 H2-M3 Full Go。

## 4. 执行门禁

本设计不授权立即修改现有 fixture 脚本或远端数据。下一检查点必须创建独立 fixture-extension 工作项，仅允许：

- 扩展 `Manage-ClubMemberHomeM3Fixture.ps1` 的显式 Scenario 枚举；
- 扩展安全测试，证明 Plan 零远端变更、Apply 幂等失败关闭、Cleanup 只清本 RunId；
- 在隔离测试数据库先验证 SQL、计数和恢复，再申请测试环境窗口；
- 现有部署 hash 未漂移时禁止重复部署。

若浏览器控制通道仍不可用，API/只读数据库证据可以先完成，但浏览器项继续标记 `Unverified`，不得冒充 Full Go。
