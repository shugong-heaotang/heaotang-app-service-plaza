# CA-UF M0 验收矩阵

| ID | 验收点 | 权威证据 | 结论 |
|---|---|---|---|
| UF-A01 | 六类编号分域、服务端分配、不复用 | 合同 identity + 测试 02-04 | Pass |
| UF-A02 | 四维审批、申请复核分离、重复确认拒绝 | 合同 approval + 测试 05-06 + fixtures | Pass |
| UF-A03 | 代表权有来源、范围、期限、撤销和回避 | 合同 representation + 测试 07-08 | Pass |
| UF-A04 | 章程版本化、生效不可变、无章程失败关闭 | 合同 charter + 测试 09 + fixtures | Pass |
| UF-A05 | 分空间交流、群编号、私信同意、隐私最小化 | 合同 communication + 测试 10-11 | Pass |
| UF-A06 | 处分具备理由、证据、审计、申诉和举报 | 合同 moderation + 测试 12 | Pass |
| UF-A07 | 商业能力全部禁止 | 合同 commercial + 测试 13 | Pass |
| UF-A08 | 正反向合成场景覆盖五领域 | fixtures + 测试 14-15 | Pass |

总体结论：合同层 Go；实现层 No-Go，等待平台独立验收与后续 P2 授权。
