# 健康大管家 R1-C1 任务理解回执

- work_id：`AIW-20260713-HEALTH-R1-CROSS-MODULE-FREEZE`
- record_id：`IR-20260713-HEALTH-R1-CROSS-MODULE-FREEZE-C1`
- developer：Health Manager continuous development agent
- reviewer：平台独立验收负责人
- approver：项目最高负责人/平台集成负责人（仅在各自权限内）

## 目标

把需求补充的首页 IA、模块权威边界、责任边界、跨模块协议、AI 边界和验收负例冻结为版本化、可机器验证但不可执行的 R1-C1 证据包。

## 非目标与禁止动作

不实现前后端、路由、API、数据库或真实工作流；不使用真实身份或健康数据；不提供互联网诊疗，不诊断、开药、改药、承诺疗效，不收费、支付、部署或进入生产。

## 允许路径

仅限任务书登记的 R1 文档、合同、Schema、conformance、current checklist、考试、实现记录和 Handoff 文件。

## 依赖

平台 preflight ready；健康模块平台依赖与内部依赖 development Go；R0/F2 历史证据只读；最新需求补充按精确 SHA-256 绑定。

## 主要风险与停止条件

- 权威来源哈希漂移、registry/branch/base 不匹配或出现未归属修改时停止。
- 任何方案要求跨模块直写、自动回传、真实数据、医疗执行、收费或部署时停止。
- 会签证据不存在时保持 Pending，不代签、不擅自提升为 Accepted。

## 验收证据

Schema 正例、语义基线、来源哈希、七入口、两路径、五权威边界、三步协议、AI 禁止动作、四类 Pending、12 场景及对应负例测试；另需治理、UTF-8、范围、安全、commit/push 和独立验收证据。
