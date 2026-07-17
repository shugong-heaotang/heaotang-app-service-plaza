# Project Brain v2 M2 activation Handoff

- work item：`AIW-20260717-PROJECT-BRAIN-V2-M2-ACTIVATION`
- exact base：`9194d3c52bb1206bedbc6ecd6d5444cb2c6f5df7`
- 当前结论：activation candidate；不是 authority，不是 runtime/production 授权

候选只新增 M2 activation 与一个 M2 runtime 工作项。M2 runtime 只允许离线读取 M1 权威合同与 synthetic fixture，生成不可变派生证据；真实源、生产任务、dashboard、部署与 production 全部关闭。

独立 reviewer 必须验证：M1 integrated；registry 只新增两项；非 PB work items 不变；7 类 activation 路径；implementation 八类路径无 active 冲突；checklist/exam/IR、总合同、UTF-8、diff、secret0、authority freshness 和 clean 全部通过。

只有本 exact candidate 独立 Go 并受控进入 authority 后，才允许创建 M2 runtime 工作树并执行其自身 preflight。
