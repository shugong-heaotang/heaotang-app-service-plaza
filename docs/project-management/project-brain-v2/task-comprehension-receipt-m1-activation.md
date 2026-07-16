# Project Brain v2 M1 激活治理任务理解回执

- work item：`AIW-20260717-PROJECT-BRAIN-V2-M1-ACTIVATION`
- target item：`AIW-20260716-PROJECT-BRAIN-V2-M1-FACT-CONTRACTS`
- exact base：`86ab20f8928a6d70195edb3879fbe7083c20a0f9`
- developer：Project Brain v2 M1 activation governance owner
- reviewer：independent Project Brain v2 M1 activation reviewer
- approver：项目最高负责人
- integration owner：平台集成负责人

## 我的目标

我只建立 M1 的合法进入条件：登记 PB-only activation，刷新 M1 exact base，验证唯一 owner、路径隔离和干净工作树，完成当前治理证据，并把 `planned -> active` 写成仅在独立 Go 和普通 fast-forward 进入 authority 后才生效的条件事实。

## 非目标

我不编写 M1 事实合同或来源映射，不修改 Project Brain v1，不实现 scheduler、snapshot、dashboard、通知或导出，不接触真实数据、凭据、环境、部署或 production，也不推进 M2-M5。

## 允许路径与禁止动作

只允许任务令列出的 exact 7 类路径；任何第八类路径均为 No-Go。禁止 force push、业务代码、运行 scripts、生产启用、真实数据访问、替其他项目改状态、复用 M0 清单/考试、把工作树存在或自测描述为已激活。

## 依赖与证据

- M0 内容和 registry closeout 必须已在当前 authority；
- 当前 authority 必须从远端刷新并在集成前保持 fresh；
- activation 与 M1 工作树必须都从 exact authority 创建并保持 clean；
- activation 只有一个 writer，独立 reviewer 不写候选；
- 首次 checklist/exam/IR 是 registry 编辑前历史证据，R2 是 registry 最终化后的 current 证据；
- 除 activation 和 M1 外，其余 140 个基线 work items 必须逐项序列化语义不变。

## 风险与停止条件

主要风险是 authority 漂移、注册表误改其他项目、路径冲突、M1 实施提前开始、敏感数据范围膨胀或候选冒充权威。任一证据未知、门禁失败、工作树变脏、reviewer 非独立或 scope 越界时立即停止并标记 No-Go。

## blocks / does_not_block

- blocks：M1 第一个去标识事实合同与来源映射检查点；
- does_not_block：Project Brain v1、R4、Mall、NOVA、Club、Activity、Health、SC remediation 与其他隔离工作项。
