# 活动板块 V3.0 M1 六依赖 Owner 回执请求

M0 集成提交：`094bafdbba48c84f41611ca541c8225e4de4a8dd`

| 依赖 | Owner | 要求状态 | 当前状态 |
| --- | --- | --- | --- |
| Club Alliance | Club Alliance 接口所有者 | `go` | `requested` |
| Auth / Privacy | 鉴权/隐私接口所有者 | `go` | `requested` |
| Member / Relationship | 会员/关系接口所有者 | `isolated-not-called` 或受限 `go` | `requested` |
| NOVA | NOVA 接口所有者 | `isolated-not-called` | `requested` |
| Message | 消息接口所有者 | `isolated-not-called` | `requested` |
| Mall / Order / Payment | 商城/订单/支付接口所有者 | `isolated-not-called` | `requested` |

每个 Owner 必须核对版本、schema、错误语义、权限、真实调用范围和 readiness，并形成仓库证据。聊天确认不能替代签署。强依赖未 Go 时 backend 保持 planned；frontend 仅允许 mock-only/non-production does_not_block 开发。
