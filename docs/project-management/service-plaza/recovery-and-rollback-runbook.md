# 测试环境恢复与回滚操作手册

## 目标

证明备份不是“存在一个压缩包”，而是能在目标 Linux 环境完整解包、通过 SQLite 完整性检查并包含恢复服务所需的二进制、启动脚本和服务广场契约；同时证明部署后门禁失败会恢复原二进制并重新达到 ready。

## 1. 备份恢复演练

```powershell
.\scripts\Test-TestServerBackupRestore.ps1 `
  -ArchivePath D:\Backup\heaotang-test-server\<timestamp>\test-server-state.tar.gz `
  -ReportPath .\docs\project-management\service-plaza\backup-restore-drill-<date>.json
```

工具会将本地备份副本上传到服务器隔离目录，完整解包并检查：

- SQLite `PRAGMA integrity_check` 必须为 `ok`；
- 用户、生命导航、俱乐部申请、健康咨询、幂等键表必须存在；
- 服务端二进制与启动脚本非空；
- 服务广场动作基线为 `service-plaza.action.v1` 且正好 20 项；
- 演练目录最终自动清理。

不能在 Windows 直接把 Linux 系统备份当作正式恢复验收，因为其中可能包含符号链接和 Windows 不允许的文件名。

## 2. 部署失败自动回滚演练

```powershell
.\scripts\Test-ServicePlazaDeploymentRollback.ps1 `
  -ReportPath .\docs\project-management\service-plaza\deployment-rollback-drill-<date>.json
```

工具记录演练前服务端二进制 SHA-256，执行一次真实测试环境部署，在全部远程健康/契约检查后主动触发模拟门禁失败。部署脚本必须执行异常回滚，演练工具随后验证：

- 子部署按预期失败而不是报告成功；
- 当前二进制 SHA-256 恢复为演练前值；
- `/ready` 返回 ready 且数据库可用；
- 演练不启用密钥轮换。

## 3. 失败处理

- 备份无法解包、SQLite 不完整或缺少必需文件：该备份不可用于恢复，立即停止后续发布并重新生成备份。
- 自动回滚后哈希不一致或服务未 ready：不得继续发布，按部署时间戳使用服务器上的 `server.rollback-*` 和启动脚本回滚副本人工恢复。
- 演练文件不得记录令牌、验证码、密码、启动脚本内容或健康数据。
