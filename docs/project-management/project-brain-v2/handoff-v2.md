# Project Brain v2 M0 Handoff

- 提交角色：Project Brain v2 project owner
- 接收角色：independent Project Brain v2 reviewer
- work item：`AIW-20260714-PROJECT-BRAIN-V2-OPERATIONS`
- record：`IR-20260714-PROJECT-BRAIN-V2-M0`
- initial base：`36b245871dd95d53964fb20cf4c30a05ceb89a77`
- resumed authority：`a47bbbacae21596be6511b70539d92f0666715a5`
- 当前结论：M0 candidate，等待独立验收；不是 integrated，不是生产授权

## 1. 已完成

已形成：

- 项目章程和角色关系；
- 范围与非范围；
- v1 单一权威、只读和失败关闭继承；
- 来源映射和 `Unknown/No-Go` 原则；
- scheduler/dashboard 只读架构；
- 数据分级与首期准入；
- M1-M5 里程碑和解锁条件；
- M0 独立验收标准；
- ADR0021；
- current checklist 26/26；
- governance exam attempt1 score 100。

首期只允许项目治理事实和经 M1 合同、阈值及重识别审查批准的去标识经营聚合。行级会员、健康、交易资金和客服数据明确禁止。

production route、snapshot、job、dashboard 和 export 默认关闭。代码集成与生产启用分离。

## 2. 未完成

以下均未完成或未授权：

- M0 独立验收；
- 项目最高负责人最终批准；
- 平台受控集成；
- M1 事实合同；
- M2 scheduler 与 snapshot；
- M3 老板驾驶舱；
- M4 权限、审计、发布和回滚演练；
- M5 最终验收；
- 环境、部署、真实数据和生产启用。

## 3. reviewer 检查重点

请逐项核对 `acceptance-v2.md`，重点检查：

- 是否产生第二权威；
- 是否存在隐式回写；
- 是否允许行级敏感数据；
- 去标识聚合是否被误当成自动安全；
- 是否静默展示陈旧值；
- 是否默认启用生产；
- 是否把代码集成当作生产授权；
- M1-M5 是否被越级授权；
- developer/reviewer/approver/integration owner 是否保持分离。

任一问题均应退回 `No-Go`，不得用后续补文档替代当前证据。

## 4. blocks / does_not_block

- `blocks`：M1-M5、Project Brain v2 运行实现、环境、部署和 production。
- `does_not_block`：Project Brain v1、SC remediation、Mall 和其他路径不重叠的独立项目。

## 5. 下一授权

仅当 M0 获得独立 Go、项目最高负责人批准并由平台集成负责人受控 integrated 后，才可新建 M1 经营事实合同工作项。

M2-M5 继续保持 No-Go。Handoff、候选提交或分支推送均不改变 registry，也不授权 production。

## 6. 回退方式

若 reviewer 判定 No-Go：

1. 保留失败结论和证据；
2. 退回具体 M0 文件修订；
3. 不修改验收标准来换取通过；
4. 重跑受影响门禁；
5. 形成新的 Handoff；
6. 不前移 M1-M5。
