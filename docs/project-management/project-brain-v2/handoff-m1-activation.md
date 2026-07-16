# Project Brain v2 M1 激活治理 Handoff

- 提交角色：Project Brain v2 M1 activation governance owner
- 接收角色：independent Project Brain v2 M1 activation reviewer
- work item：`AIW-20260717-PROJECT-BRAIN-V2-M1-ACTIVATION`
- target item：`AIW-20260716-PROJECT-BRAIN-V2-M1-FACT-CONTRACTS`
- current record：`IR-20260717-PROJECT-BRAIN-V2-M1-ACTIVATION-R2`
- exact base：`86ab20f8928a6d70195edb3879fbe7083c20a0f9`
- 当前结论：M1 activation candidate；不是 authority，不是 M1 合同完成，不是生产授权

## 1. 候选状态语义

候选 registry 中 `activation=integrated` 与 `M1=active` 仅在本 exact candidate 经独立 reviewer 判定 Go，并由平台集成负责人普通 fast-forward 纳入 authority 后生效。候选分支、提交、自测、工作树、清单、考试或本 Handoff 均不得冒充权威激活。

## 2. 本次仅完成

- 从远端确认 authority exact HEAD 为 `86ab20f8928a6d70195edb3879fbe7083c20a0f9`；
- 从该 HEAD 创建并核验干净的 activation 工作树和 M1 合同预置工作树；
- 新增一个 PB-only activation 候选工作项；
- 把既有 M1 的 stale reserved base 刷新到 exact authority，并写入条件性 `active`；
- 形成任务令、理解回执、首次 checklist/exam/IR 历史证据以及 current R2 证据链；
- 保持 Project Brain v1 和所有非目标 work item 不变。

## 3. 明确未完成与未授权

本任务没有修改 `contracts/project-brain/v2/**`、`source-map-v2.md`、App 或运行 scripts，没有编写任何 M1 事实合同，没有读取或连接真实数据。M2-M5、scheduler、snapshot、dashboard、通知、导出、行级或可重识别数据、凭据、环境、部署与 production 全部继续 No-Go。

M1 激活后也不能直接进入运行实现。其第一个合法检查点仍需 M1 owner 在 M1 工作树内重新完成自身任务令、current checklist 和 exam 100，然后只交付去标识经营事实合同与来源映射，交独立 reviewer 验收。

## 4. 独立 reviewer 必须复验

1. candidate 直接基于 exact base `86ab20f8928a6d70195edb3879fbe7083c20a0f9`；
2. activation 与 M1 worktree 的 branch、HEAD、clean 状态匹配任务令；
3. diff 只有 7 类 allowed paths、实际 10 个文件，无第八类路径；
4. registry 基线 141 项、候选 142 项；除新增 activation 和目标 M1 外，其余 140 项逐项序列化语义不变；
5. M1 只刷新 `status`、`base_commit`、`migration_note` 和 `handoff_record`，allowed paths、owner、branch 与 workspace 不变；
6. 首次 checklist/exam/IR 原样保留；R2 checklist 26/26 current、R2 exam 100、R2 IR verified；
7. collaboration、checklist、exam、IR、总合同、UTF-8、secret、diff-check、scope 与 authority freshness 全部通过；
8. 候选不包含 M1 合同、真实数据、runtime、部署或 production 授权。

任一 Unknown、漂移、越界、非 PB 变更或 reviewer 不独立均为 `No-Go`。

## 5. blocks / does_not_block

- `blocks`：M1 首个去标识事实合同与来源映射检查点；
- `does_not_block`：Project Brain v1、R4、Mall、NOVA、Club、Activity、Health、SC remediation 和其他隔离工作项。

## 6. 下一授权

独立 Go 后只允许平台集成负责人将本 exact candidate 普通 fast-forward 纳入 authority。权威激活完成后，M1 owner 可以开始 M1 自己的准入证据；本次授权不包含 M1 合同实施、M2-M5 或生产启用。
