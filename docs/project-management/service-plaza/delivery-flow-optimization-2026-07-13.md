# 平台交付流优化 Handoff

## 当前结论

- 状态：implementation complete / awaiting independent acceptance
- 主因：业务工作被拆成多个长期并行治理项，Handoff 缺少决策时限，范围内下一检查点仍反复等待授权，平台集成负责人形成单点队列。
- 处置：建立 `delivery-flow-policy.v1` 及机器校验。

## 任务理解回执

- goal：减少重复等待和平台单点排队，同时保持根因、权限、安全和独立验收门禁。
- non-goals：不修改业务代码，不直接暂停或覆盖其他负责人正在执行的隔离工作，不授权生产、真实数据或资金操作。
- allowed paths：协作登记及 Schema、delivery flow policy、校验脚本与测试、任务书、状态、检查单、考试、实施记录和本 Handoff。
- risks：错误计算 WIP 会误停工作；自动续跑若跨越风险边界会扩大权限；遗留状态若强行补造会污染历史。
- stop conditions：路径重叠、权限扩大、生产或真实数据、不可逆操作、独立验收失败。
- developer / reviewer / approver：平台治理实施负责人 / APP 总架构独立验收负责人 / 项目最高负责人。
- acceptance evidence：Schema、语义校验、负向单测、总治理门禁、UTF-8、Git diff 和独立验收结论。

## 生效规则

1. 同时最多三个唯一业务主线；每个模块最多一个。当前遗留工作进入 drain mode，不强制中断，但在降到上限前禁止激活新业务主线。
2. 一个业务结果只保留一个总工作项；实现、证据、测试和验收是该工作项的检查点。跨仓库只允许 supporting-checkpoint，不重复计算业务 WIP。
3. 检查点证据通过、范围和风险未扩大、工作树归属清楚且无停止条件时自动续跑。
4. 生产、真实资金、真实健康/会员数据、不可逆变更、权限扩大、安全/法律升级或独立验收失败必须停止并重新授权。
5. `handoff-ready` 必须指定下一责任人；24 小时没有结论自动升级项目最高负责人。
6. 完成必须同时具备业务流恢复和独立验收；提交、文档、测试自述均不能单独关闭工作。

## 迁移

旧工作项不补造历史字段。下一次激活、Handoff 或检查点变化时增加 `flow_policy_version` 和流控制字段。新工作项立即执行本政策。

## 验证

- Policy Schema：通过
- 语义校验：通过
- 单元测试：3/3 通过
- 协作登记：通过，并已自动串联 delivery flow gate
- Service Plaza 总合同：通过
- UTF-8：1277 files 通过
- Git diff：通过
- 独立验收：待执行
