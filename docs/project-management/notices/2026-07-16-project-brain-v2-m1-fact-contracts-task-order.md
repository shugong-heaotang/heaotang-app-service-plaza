# Project Brain v2 M1 去标识经营事实合同任务令

- work item：`AIW-20260716-PROJECT-BRAIN-V2-M1-FACT-CONTRACTS`
- record：`IR-20260716-PROJECT-BRAIN-V2-M1-FACT-CONTRACTS`
- registered base：`86ab20f8928a6d70195edb3879fbe7083c20a0f9`
- resumed authority：`8e89ceda79827ee24fa115b2e993ba1c3f529aaa`
- branch：`codex/project-brain-v2-m1-fact-contracts`
- workspace：`C:/Users/shugo/Documents/APP系统/.codex-worktrees/project-brain-v2-m1-fact-contracts`

## 目标

冻结 Project Brain v2 首批可执行的事实合同：为 G0 项目治理事实和 G1 去标识经营聚合定义唯一 authority、source owner、只读来源、口径、统计窗口、freshness、质量、分级、用途、角色、证据和失败状态；提供版本化隐私阈值策略、合法合成样例、禁止行级/小样本/过期/冲突/越权负例以及机器验证。形成来源映射、IR 和 Handoff 后交独立 reviewer。

## 本检查点交付

1. `contracts/project-brain/v2/**`：事实合同 Schema、来源映射 Schema、阈值策略、首批 G0 catalog、G1 synthetic-only catalog、合法样例、负例、验证器与测试；
2. `docs/project-management/project-brain-v2/source-map-v2.md`：人类可读的权威、Owner、用途与失败关闭映射；
3. 本任务令、current checklist、exam100、verified IR 和 `handoff-m1.md`。

## exact allowed paths

仅允许 registry 已登记的 7 类路径：

1. `contracts/project-brain/v2/**`
2. `docs/project-management/notices/2026-07-16-project-brain-v2-m1-fact-contracts-task-order.md`
3. `docs/project-management/project-brain-v2/source-map-v2.md`
4. `docs/project-management/project-brain-v2/handoff-m1.md`
5. `contracts/foundation/development-checklists/2026-07-16-project-brain-v2-m1*.json`
6. `contracts/foundation/governance-exams/2026-07-16-project-brain-v2-m1*.json`
7. `contracts/foundation/implementation-records/2026-07-16-project-brain-v2-m1*.json`

任务理解回执放在 `contracts/project-brain/v2/task-comprehension-receipt-m1.json`，属于第 1 类路径。不得新增第八类路径。

## 合同不变量

- 每个事实恰好一个 authority 和 source owner；冲突不得自动择一；
- `read_mode=read_only`、`write_capability=none`；
- 只允许 G0/G1；P1/H1/F1/C1/S1 必须拒绝；
- G1 必须绑定版本化阈值策略、小样本抑制、禁下钻、禁未授权拼接和重识别复核；
- 任一必填事实缺失、过期、不可达、质量失败、权限不足、样本不足或权威冲突，只能 `Unknown/No-Go`；
- 合法样例均为 synthetic，不得伪装为真实经营数据；
- Project Brain v1 和业务源系统保持唯一权威，v2 不写回。

## 角色

- developer：Project Brain v2 M1 project owner
- reviewer：independent Project Brain v2 M1 reviewer
- approver：项目最高负责人
- integration owner：平台集成负责人

## 完成门禁

current checklist 26/26、exam 100、Schema/semantic validator、合法样例、全部负例 fail closed、总合同、UTF-8、diff-check、secret0、exact scope、authority freshness、verified IR、Handoff 和独立 Go 全部通过。候选只有在独立 Go 后才可普通 fast-forward 集成。

## 持续 No-Go

禁止 App、平台运行 scripts、scheduler、snapshot、dashboard、通知、导出、真实数据、凭据、环境、部署和 production；禁止任何行级会员、健康、订单、支付、客服、人脉数据或可重识别聚合。M2-M5 继续 No-Go。
