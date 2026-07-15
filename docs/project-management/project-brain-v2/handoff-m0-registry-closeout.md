# Project Brain v2 M0 registry 收口 Handoff

- 提交角色：Project Brain v2 M0 registry closeout platform governance owner
- 接收角色：independent platform reviewer
- work item：`AIW-20260715-PROJECT-BRAIN-V2-M0-REGISTRY-CLOSEOUT`
- current record：`IR-20260715-PROJECT-BRAIN-V2-M0-REGISTRY-CLOSEOUT-R2`
- exact base：`9b221a8a2a4de7c70ef9d1f86a55656b2c0d2757`
- 当前结论：registry closeout candidate；不是 authority，不是生产授权

## 1. 候选状态语义

候选 registry 中 `operations=integrated`、`closeout=integrated`、`M1=planned` 仅在本 exact candidate 经独立 reviewer 判定 Go，并由平台集成负责人以普通 fast-forward 纳入 authority 后生效。候选分支、提交、自测、检查单、考试或本 Handoff 均不得冒充权威集成。

## 2. 本次仅完成

- 将 `AIW-20260714-PROJECT-BRAIN-V2-OPERATIONS` 候选状态从 `active` 收口为 `integrated`；
- 登记本 registry closeout 工作项的 7 类 allowed paths；候选实际 10 个文件；
- 新增 `AIW-20260716-PROJECT-BRAIN-V2-M1-FACT-CONTRACTS` 为 `planned`；
- 保留 Project Brain v1、M0 内容文件和所有非 PB work item 不变；
- 形成 current R2 checklist、R2 exam 100、R2 IR 与独立验收输入；首次 checklist/exam/IR 原样保留为历史证据。

## 3. 明确未完成与未授权

M1 没有激活、没有创建或确认运行工作树、没有写 contracts、没有实现 source map、scheduler、snapshot、dashboard 或任何业务代码。M2-M5、真实数据、行级会员/健康/交易/客服数据、凭据、环境、部署、导出与 production 全部继续 No-Go。

M1 registry 中的 branch、workspace 和 base 只用于 planned 预留；激活时必须从当时 authority 重新核对 exact base、路径冲突、唯一 owner、clean worktree、current checklist、exam 100 和独立准入，不得复用本候选自动开工。

## 4. 独立 reviewer 验收

必须复验：

1. candidate 直接基于 `9b221a8a2a4de7c70ef9d1f86a55656b2c0d2757`；
2. diff 只有 7 类 allowed paths、实际 10 个文件，且没有第八类路径；
3. operations 仅状态、收口说明和 Handoff 引用按本任务变化；
4. closeout 只有一个 integrated 候选条目；
5. M1 只有一个 planned 条目，未出现 active、运行实现或生产授权；
6. 其余 137 个基线 work items 逐项序列化语义不变；
7. R2 checklist 26/26 current、R2 exam 100、R2 IR verified；首次三份证据保持不可修改；
8. collaboration、total contracts、UTF-8、secret、diff-check、scope 与 freshness 全部通过。

任一 Unknown、漂移、越界或门禁失败均为 `No-Go`。

## 5. blocks / does_not_block

- `blocks`：M1 另行激活与实施准入；
- `does_not_block`：Project Brain v1、R4、Mall、NOVA、Club、Activity、Health、SC remediation 和其他隔离工作项。

## 6. 下一授权

只有本 exact candidate 独立 Go 并普通 fast-forward 进入 authority 后，M0 registry 收口才生效。此后也只能另建 M1 activation 工作项；不得直接把 planned 改 active，不得跳过准入，不得启用 production。
