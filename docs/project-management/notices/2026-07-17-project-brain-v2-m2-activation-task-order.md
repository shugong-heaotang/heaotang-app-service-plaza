# Project Brain v2 M2 激活治理任务令

- work item：`AIW-20260717-PROJECT-BRAIN-V2-M2-ACTIVATION`
- exact base：`9194d3c52bb1206bedbc6ecd6d5444cb2c6f5df7`
- activation branch：`codex/project-brain-v2-m2-activation`
- implementation branch：`codex/project-brain-v2-m2-runtime`

## 目标

仅建立 M2 activation 与唯一 M2 runtime 工作项。M1 已 integrated；M2 仅授权只读 job、幂等运行、并发互斥、超时、有限重试、不可变快照、失败记录、审计告警和禁用/回滚演练。

## 激活路径

activation 只允许 registry、任务令、理解回执、Handoff、checklist、exam、IR 七类路径。实施工作另行只允许 registry 所列八类 M2 路径。

## 禁止范围

禁止真实生产源、凭据、环境、App/dashboard、公共 scripts、写接口、源系统修改、部署、通知发送和 production。M3-M5 继续 No-Go。

## 状态语义

候选中的 activation integrated 与 M2 active 只有在 exact candidate 独立 Go 并受控进入 authority 后生效。候选、自测、考试或工作树都不构成运行授权。
