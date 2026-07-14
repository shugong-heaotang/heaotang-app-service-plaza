# NOVA M2 人脉迁移与禁用演练报告

## 结论

当前结论：`R2 remediation complete / independent review pending`。

演练仅使用运行时创建并最终删除的临时合成 SQLite 数据库，没有连接测试服务器、生产数据库或真实会员数据，也没有发送消息或修改后端路由。

## 结果矩阵

| 项目 | 结果 |
| --- | --- |
| Contract + Draft 2020-12 Schema | PASS |
| Plan 数据库 SHA 不变 | PASS |
| Apply 前 backup | PASS |
| 单向迁移 | 2/2 |
| unknown tenant / invalid participant quarantine | 2/2 |
| legacy write insert/update/delete probes | REJECT / REJECT / REJECT |
| legacy route 410 + successor | 3/3 |
| Cleanup 不重开 unsafe writes | PASS |
| RestoreVerify 隔离副本完整性 | PASS |
| RestoreVerify 不重开 unsafe writes | PASS |
| 缺显式 test 确认 | REJECT |
| 生产样式路径 | REJECT |
| 缺 test marker | REJECT |
| backup 已存在 | REJECT，原 backup SHA-256 不变 |
| PowerShell 编码 | UTF-8 BOM + CRLF，PowerShell 5.1 解析通过 |

## 说明

本证据证明迁移和禁用机制可在临时合成数据库确定性演练；不证明真实历史数据可迁移，不证明 Go provider、路由 410 或环境部署已完成。NOVA M2 继续 No-Go，等待 provider、后端路由独立工作项和测试环境安全验收。

R2 修复补齐了此前仅执行 insert 探针、未永久覆盖 update/delete、缺 test marker 和 backup 冲突的证据缺口，并统一两份 PowerShell 脚本的 UTF-8 BOM/CRLF。R2 实现者不承担最终独立验收；本报告仍不得作为集成或真实环境授权。
