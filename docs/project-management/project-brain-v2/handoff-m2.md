# Project Brain v2 M2 Handoff

- work item：`AIW-20260717-PROJECT-BRAIN-V2-M2-READONLY-REFRESH`
- exact base：`701519ea1130b6620607de753aa03a7d93953f0b`
- 当前结论：R1 immutable No-Go；R2 remediation candidate ready for fresh independent review；不是 accepted、integrated 或 production

## R1 独立验收历史

- immutable candidate：`35399d046493da0e14003f218d503f6c9fcd68fb`
- 结论：`Acceptance No-Go / no-integrate`，2 P0、4 P1、0 P2；未推送、未集成。
- 外部报告：`C:\Users\shugo\Documents\项目最高负责人\project-brain-v2\2026-07-17-project-brain-v2-m2-runtime-independent-review.md`
- 报告 SHA-256：`5445d33da285ef3437917db2f9fac6a52befb97165c42ce39ee1410ce0722d7b`

R2 已针对六项发现增加强制隔离和变异回归：state root/repo/source/junction overlap、unknown/extra capability、非目标 M1 runtime flag、有效旧 pointer 替换、run 删除/audit 截断、永久阻塞 timeout、独立 actor+role audit Schema。

## 已交付

- 离线 `OfflineScheduler.tick`：从不可变运行历史计算 due time，不包含生产 timer/worker。
- `RefreshEngine`：只消费 M1 合同和 policy allowlist 的 synthetic fixture。
- 默认策略 `enabled=false`，11 个运行/网络/写入/production 能力开关均为 false；未知字段也拒绝。
- 内容寻址 snapshot、不可变 run record、last-trusted 指针、append-only SHA-256 audit chain 和 evidence-only alert。
- 幂等 run ID、单实例互斥、超时、最多三次重试、1 MiB 输入上限、UTC 时间和原因码。
- Unknown/No-Go 失败关闭、失败不覆盖、snapshot/run/pointer/audit/schedule 防篡改以及只移动派生指针的回滚演练。

## 开发者验证

- M2 runtime contract validator：通过；6 个 Schema，默认禁用，production capability false，network-capable import 0。
- M2 R2 单元、负向和变异测试：34/34 通过，0 skip。
- M1 原合同 validator 与回归/变异测试：20/20 通过。
- current checklist：26/26；随机治理考试：100。
- 总合同、协作、checklist、exam、IR 与 UTF-8（1584 files）门禁：通过。
- R2 exact scope：22 files，八类登记路径内，out-of-scope 0；changed-file secret scan 0。R1 的 21 files 结果未冒充 R2。
- fresh fetch 后 remote authority 与 local exact base 均为 `701519ea1130b6620607de753aa03a7d93953f0b`。
- `git diff --check`：通过。

开发者验证不是独立验收。R2 exact candidate commit、当前远端 authority、diff/secret/UTF-8/总合同/freshness 结果必须在候选提交后重新绑定；R1 reviewer 不自动成为 R2 Go。

## 验收边界

M2 必须证明只读 allowlist、无网络/无凭据/无源写入、幂等与互斥、超时和有限重试、不可变 snapshot、append-only audit、失败 alert、失败不覆盖 last-trusted、禁用与回滚演练。所有证据只能使用治理制品和 synthetic fixture。

M3 dashboard、真实数据、环境、部署、生产 job、通知发送、export 和 production route 全部 No-Go。独立 reviewer 必须执行负向/变异测试，不能只复跑开发者测试。

独立 reviewer 还必须重点攻击：运行记录与 audit 不一致、last-trusted 指针篡改、同 run ID 输入变化、并发锁、超时、重试耗尽、M1 runtime 标志被擅自打开、任一 production capability 打开、schedule history 篡改以及回滚到不存在或被修改的 snapshot。
