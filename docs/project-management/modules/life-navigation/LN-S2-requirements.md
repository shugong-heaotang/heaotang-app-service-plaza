# 生命导航 LN-S2 P0/P1 需求事实与 Base Contract

## 目标与角色

本检查点把“申请时如何选择维度”从前端固定值升级为可审计的版本化依赖结构。项目负责人负责稳定维度语义与旧 `yun` 的最终裁决；生命导航二负责人负责板块标准；平台集成负责人负责接口、门禁与最终验收。

主动作仍是登录用户提交本人导航申请并查看本人历史。本轮不改变既有身份、幂等、本人归属和跨用户隔离标准。

## 已核验事实

- 现有前端申请固定使用 `dimension_id=yun`。
- 现有后端只校验维度非空和长度，不提供权威注册表选择。
- 现有 `GET /api/v1/life-nav/dimensions` 为 `code-present-unverified`；它包含 `BaseScore`、questions、actions、routes 等窄目录禁止字段，并在配置缺失、空或非法时回退代码默认值。
- 旧 application-history M0–M4 只证明身份、幂等、本人历史、跨用户隔离和浏览器主链，不证明 LN-S2 Go。

## P0 待裁决事项

1. 稳定维度 ID、label、sort order、active、version 和 authority。
2. 旧 `yun` 是迁移、兼容只读、独立历史值还是废弃值。
3. 配置缺失、读取失败、空目录和非法目录必须失败关闭，不得回退默认目录。
4. 历史记录遇到未知维度时只显示稳定 ID 和“未解析”，不得伪造 label。
5. 可证伪前提、复审触发条件和兼容迁移责任。

在项目负责人书面裁决前，机器真相源必须保持：`decision_status=pending`、`registry_frozen=false`、`executable=false`、旧 `yun mapping_target=null`。

## P1 Base Contract

- `dimension-registry.v1`：仅保存待裁决候选元数据和旧值事实；不是权威业务注册表。
- `dimension-directory.v1`：只允许 `dimension_id`、`dimension_version`、`label`、`sort_order`；当前返回 unavailable/empty 和稳定错误。
- `application-dimension-selector.v1`：定义服务端权威、验证顺序和失败关闭，但 selector 当前不可执行。
- `error-catalog.v1`：缺失、读取失败、空/非法、重复 ID/order、未知、停用、版本不兼容和 Pending 均有稳定 error ID。
- fixtures：仅固定 seed 合成数据；不含真实姓名、手机号、身份证、申请正文、OTP、JWT、cookie 或真实历史。

## 非目标

本轮禁止前端、后端、API、数据库、测试环境、部署和生产修改；禁止评分、预测、八字、AI 建议、专业结论、价格、交易和下游服务。P0/P1 Base Contract Go 不自动授权 executable selector 或 M2。

## 验收

1. 四组 JSON 实例均通过 Draft 2020-12 Schema。
2. 维度 ID/order 唯一，引用完整；目录无禁止字段。
3. 12 个合成正反例全部得到稳定 fail-closed error ID。
4. 固定 seed、输入 SHA、无 BOM/LF、敏感模式扫描和 canonical hash 可重放。
5. v2 内部依赖明确 Pending 只阻塞 executable、前后端和环境，不阻塞 Base Contract/Handoff。
