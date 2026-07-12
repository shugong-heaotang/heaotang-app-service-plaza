# NOVA M2 人脉迁移与禁用演练计划

- work_id：`AIW-20260712-NOVA-M2-MIGRATION-DISABLE-DRILL`
- 范围：临时合成 SQLite 数据库
- 状态：已实现，待独立复核
- 生产、真实会员、真实消息：禁止

## 目标

验证 `introductions -> introduction_requests` 单向迁移、未知 tenant 隔离、legacy 写冻结、三条旧写路由 `410 Gone` successor 合同，以及恢复后仍不重新开放不安全写入。

## 阶段

1. `Plan`：只读打开数据库，验证 test marker 并输出计数，数据库 SHA 不变。
2. `Apply`：先创建 SQLite backup，再在单事务中创建迁移证据、写冻结 trigger 和 410 route control；有效记录单向迁移，未知 tenant/非法参与者进入 quarantine。
3. `Inspect`：只读输出 source、migrated、quarantine、410 与 write-block 计数。
4. `Cleanup`：只删除当前 RunId 的迁移/隔离/ledger 记录，保留写冻结和 410，不反向写 legacy。
5. `RestoreVerify`：把 Apply 前 backup 恢复到隔离副本，立即施加相同写冻结与 410，再校验 source 数量、完整性和禁止写入不变量；不覆盖活动数据库。

## 安全边界

- RunId 必须唯一且符合 `nova-m2-*`；
- 数据库必须位于系统临时目录、以 `.drill.db` 结尾，并带 `environment=test`、`allow_destructive_drill=1` marker；
- 必须显式提供 `-ConfirmTestDatabase`；
- 生产样式路径、缺 marker、缺确认、备份覆盖均失败关闭；
- 不修改任何 Go 路由，本轮 410 仅为机器合同和测试数据库控制证据。

## 验收

- Draft 2020-12 合同验证通过；
- Plan 零 mutation；Apply 前 backup；2 条迁移、2 条 quarantine；
- 3 条 legacy route 为 410，3 个 SQLite trigger 阻止 insert/update/delete；
- Cleanup 与 RestoreVerify 均保持 legacy write forbidden；
- 安全脚本完成正反例、UTF-8 BOM/CRLF 和 PowerShell 5.1 解析验证。
