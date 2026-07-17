# APP PDCAR Skill 强制接入激活治理理解确认

- work_id：`AIW-20260717-PLATFORM-PDCAR-SKILL-ENFORCEMENT-ACTIVATION`
- record_id：`IR-20260717-PLATFORM-PDCAR-SKILL-ENFORCEMENT-ACTIVATION-C1`
- actor：`APP PDCAR enforcement activation owner`
- confirmed_at：`2026-07-17T10:20:00+08:00`
- exact authority：`codex/service-plaza-phase1-integration@09cd00a429da37a87d26870310617b928d0894a7`

## 我理解的任务

本切片只证明正式实施在进入 D1/D2 前具备可审核的治理入口。产物是任务书、理解确认、current checklist、随机 Exam100、activation IR 和 Handoff；不是 AGENTS/README/CI/validator/schema 的实现。

## 权限理解

- `B1V Go` 只允许 activation item 七类路径内的 B2 治理证据写入。
- preflight ready、checklist 完成、Exam100、candidate commit 和 Project Brain review 都不能单独授权正式实施。
- 正式实施仍需 activation candidate 独立 Go、受控进入 authority、authority lifecycle 验证，以及另行登记的正式实施 active item。
- 结构验证永远不授予代码、registry、集成、部署或生产权限。

## 边界和角色

唯一 writer 是 `APP PDCAR enforcement activation owner`；独立 reviewer 是 Project Brain，二者不得合并。registry 是 authority，但本检查点不修改其内容。所有既有 non-overlapping work 继续，不因本切片阻塞。

## 验收理解

验收需要 exact authority/candidate、七类 allowed paths、current checklist 的真实读取与哈希、随机 8 题 100 分、同一 record_id 的 IR、Handoff、机器 validator 和 clean diff。任一证据缺失、过期、冲突或越界均为 No-Go。

## 明确禁止

不修改 APP 正式实施入口，不创建 formal worktree，不写业务代码，不 push、不集成、不部署，不接触真实数据、支付或生产，不把活动量或文档存在当成实施完成。
