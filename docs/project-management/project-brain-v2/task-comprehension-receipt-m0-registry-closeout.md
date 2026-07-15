# Project Brain v2 M0 registry 收口任务理解回执

- work item：`AIW-20260715-PROJECT-BRAIN-V2-M0-REGISTRY-CLOSEOUT`
- exact base：`9b221a8a2a4de7c70ef9d1f86a55656b2c0d2757`
- developer：Project Brain v2 M0 registry closeout platform governance owner
- reviewer：independent platform reviewer
- approver：项目最高负责人
- integration owner：平台集成负责人

## 我的目标

我只收口 Project Brain v2 M0 的 registry 事实：operations 从 active 到 integrated；本 closeout 记录为 integrated；M1 仅新增 planned。三项状态都只在 exact candidate 独立 Go 且普通 fast-forward 进入 authority 后生效。

## 非目标

我不激活 M1，不创建 M1 运行工作树，不写 M1 contracts，不实现 scheduler、snapshot 或驾驶舱，不修改 Project Brain v1，也不触碰 R4、Mall、NOVA、Club、Activity、Health 或 SC remediation。

## 允许路径

仅任务令列出的 exact 7 paths。任何第八个路径都是 No-Go。

## 禁止动作

禁止 force push、生产启用、部署、读取真实数据或凭据、改业务代码、改 scripts、替其他项目改 registry 状态、把候选或自测描述为权威完成。

## 依赖与证据

- authority base 必须保持 `9b221a8a2a4de7c70ef9d1f86a55656b2c0d2757`；
- M0 内容候选必须已在该 exact authority 中；
- current checklist 必须逐项读取并完成；
- exam 必须 100；
- operations 的集成事实以 authority 中 M0 exact commit 和既有独立 Go 为依据；
- registry 除 PB 三个目标条目外不得改变任何其他 work item；
- IR、Handoff、合同、UTF-8、secret、scope 和 freshness 均须形成可复验结果。

## 风险与停止条件

主要风险是 registry 误改其他项目、把 planned 写成 active、把候选冒充权威、或基线在提交前漂移。出现任一风险、证据未知、门禁失败或 allowed paths 越界时立即停止并标记 No-Go。

## blocks / does_not_block

- blocks：M1 的另行激活和实施准入；
- does_not_block：Project Brain v1、R4、Mall、NOVA、Club、Activity、Health、SC remediation 与其他隔离工作项。
