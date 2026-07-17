# Project Brain v2 M2 activation 任务理解回执

我只激活 M2 的独立、离线、只读运行检查点，不实现运行代码。M1 authority 是 `9194d3c52bb1206bedbc6ecd6d5444cb2c6f5df7`。

M2 implementation 只能在其独立工作树、八类路径、current checklist、Exam100 和任务令后开始。允许：只读适配、幂等/互斥、超时/有限重试、不可变快照、失败审计告警与禁用回滚演练。禁止：真实生产源、凭据、App/dashboard、公共 scripts、写操作、部署和 production。

developer、independent reviewer、项目最高负责人 approver、平台 integration owner 保持角色分离。authority 漂移、路径冲突、非 PB registry 变化或证据未知均为 No-Go。
