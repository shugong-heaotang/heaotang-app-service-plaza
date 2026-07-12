# NOVA M2 人脉工具契约会签

- work_id：`AIW-20260712-NOVA-M2-PEOPLE-TOOLS-CONTRACT`
- notice：`NOVA-M2-PEOPLE-TOOLS-TASK-20260712-001`
- 日期：2026-07-12
- 会签范围：四项 NOVA 工具与服务端结果 callback 的版本化合同
- 契约包结论：`Contract Package Go`
- M2 总结论：`No-Go`
- executable：`false`

## 1. 精确工具集合

本检查点只标准化以下四项模型可调用工具：

1. `member_search`：按服务端可信身份、tenant、资源权限和字段可见性查找候选人；
2. `connection_draft`：形成无外部发送效果的披露预览和 manifest；
3. `connection_send`：只接受已确认 draft，强制确认票据和 `Idempotency-Key`；
4. `connection_status`：参与者或授权操作员按资源权限查询状态。

`connection_result_callback` 是服务端到服务端回调，不是第五项模型工具。它只允许由 `people_connection_outbox` 身份调用，采用 trusted server tenant、`event_id` 幂等、至少一次投递、重试后 DLQ 和 `connection_status` 对账。NOVA 消费侧只能追加任务事件，不得反写人脉 canonical 状态。

## 2. 安全与治理结论

- actor、tenant 和服务身份只能来自 trusted server context，模型正文、query 或请求体不得覆盖；
- `member_search` 采用字段白名单，手机号、邮箱、证件、原始健康文本、私密备注、精确地址和未批准自由文本一律禁止暴露；
- `connection_draft` 无外部消息效果，输出固定披露清单、披露哈希、有效期和确认要求；
- `connection_send` 的确认票据绑定 actor、tenant、action、target、draft、版本、披露哈希、影响、trace 和有效期；同幂等键同载荷安全重放、异载荷冲突；
- 所有工具均定义 trace/audit 最小字段、敏感值脱敏、稳定错误目录和兼容策略；
- callback 生产、传输与消费责任已分离：人脉 Owner 负责 canonical 状态和 outbox，平台负责传输/Schema/服务身份，NOVA 只负责 append-only 消费和对账；
- 现有 `network` 不安全写路由不得直接包装为 NOVA 工具，三个 legacy 路由已列入禁止清单。

## 3. Canonical 实现依赖

人脉 canonical 实现、唯一 Owner、`network/social` 双事实源迁移和 legacy 禁用方案由独立工作项 `AIW-20260712-NETWORK-CANONICAL-OWNER-DECISION` 裁决。当前状态仍为 `pending`。

因此本契约包只证明接口、安全边界、失败关闭、合成 fixtures 和 conformance 已标准化，不证明 provider 已实现，也不授权：

- 调用 `network` 或 `social` 现有写路径；
- 修改后端、数据库或迁移真实记录；
- 搜索真实会员或发送真实引荐消息；
- 将任何 contract 的 `executable` 改为 `true`；
- 宣称 NOVA M2 Go。

## 4. 机器合同与验证证据

- `contracts/service-plaza/nova/nova-people-tools.v1.json`
- `contracts/service-plaza/nova/nova-people-tools.v1.schema.json`
- `contracts/service-plaza/nova/nova-people-tool-errors.v1.json`
- `contracts/service-plaza/nova/nova-people-tool-errors.v1.schema.json`
- `contracts/service-plaza/nova/nova-connection-callback.v1.json`
- `contracts/service-plaza/nova/nova-connection-callback.v1.schema.json`
- `contracts/service-plaza/nova/fixtures/m2/positive-invocations.v1.json`
- `contracts/service-plaza/nova/fixtures/m2/negative-cases.v1.json`
- `contracts/service-plaza/nova/test_nova_people_tools.py`

合成一致性覆盖：

- 四工具与 callback 正例 5/5；
- 身份伪造、tenant 串流、字段越权、确认票据、幂等、资源权限、callback 身份/冲突、legacy route 和安全重放负例 19/19；
- Python conformance 11/11；
- error catalog 稳定错误 26/26；
- current checklist 26/26，随机治理考试 100 分。

## 5. 可证伪前提与复审触发

前提：

1. 人脉模块最终能提供 trusted server identity、tenant 隔离、资源级权限、确认票据、幂等存储、outbox 和审计能力；
2. canonical 状态只存在一个权威 Owner，NOVA 不直接拥有或改写人脉状态；
3. legacy 数据能够通过显式迁移、隔离或 Sunset 处理，不自动归属未知 tenant；
4. 合成 fixtures 只验证合同语义，不冒充后端、环境或真实用户验收。

出现以下任一事实必须复审并保持失败关闭：

- canonical Owner 选择的实现无法满足本合同，或仍存在 `network/social` 双写；
- actor/tenant 可被请求正文覆盖，或资源权限只能由前端执行；
- send 无法提供一次性确认票据或持久幂等冲突检测；
- callback 不能提供可信服务身份、outbox 重放与状态对账；
- 新增可见字段、事件类型、必填字段或改变既有语义；
- 发现真实数据、凭据或真实消息进入本合同测试。

## 6. 下一门禁

平台只有在独立人脉 Owner 裁决 Accepted、迁移/禁用方案可验证，并由 provider 实现通过后端、测试环境和安全验收后，才可评估 M2 的下一阶段。聊天确认、代码存在或本次 Contract Package Go 均不能替代上述证据。
