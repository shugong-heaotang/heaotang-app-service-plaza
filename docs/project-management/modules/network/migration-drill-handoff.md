# NOVA M2 Migration & Disable Drill Handoff

- work_id：`AIW-20260712-NOVA-M2-MIGRATION-DISABLE-DRILL`
- 提交方：NOVA migration and disable drill agent
- 接收方：平台集成负责人
- 日期：2026-07-15
- 状态：`ready for independent review`

## 已完成

1. 完成 current checklist 26/26 和随机治理考试 100 分。
2. 发布版本化 migration JSON/Schema 和 4 条合成 legacy fixture。
3. 实现 `Plan/Apply/Inspect/Cleanup/RestoreVerify`，默认只接受系统临时目录内带 test marker 的 `.drill.db`。
4. 验证 backup、单向迁移、unknown tenant quarantine、禁双写、410 successor、Cleanup/RestoreVerify 不重开 unsafe writes。
5. PowerShell 脚本使用 UTF-8 BOM + CRLF，并通过 Windows PowerShell 5.1 解析。
6. R2 永久执行 insert/update/delete 三类 legacy 写冻结探针，并在 Cleanup 后重复验证三类写入均未重开。
7. R2 新增缺 test marker 与 backup 已存在负例；后者同时验证既有 backup SHA-256 不变。
8. R2 使用全新 current checklist、随机治理考试 100 分和独立 implementation record，不复用 R1 快照。

## 未完成和禁止

- 未修改或部署真实 Go 路由；
- 未运行真实历史数据迁移；
- 未接触生产、真实会员、真实消息、凭据或资金；
- 未将任何 provider 或 NOVA M2 标为 Go。

## 平台复核请求

请复跑安全脚本、JSON Schema、检查单/考试/IR、PowerShell 解析/BOM、总合同、UTF-8、diff 和敏感信息门禁。独立复核前不得集成或进入真实环境。

R2 实施者不承担最终独立验收；平台应以本地 R2 提交 exact SHA 启动新的独立复核，不得仅依据本 Handoff 或自述给 Go。
