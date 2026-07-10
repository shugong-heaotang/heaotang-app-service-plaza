# 服务广场前端原子部署与自动回滚

- 日期：2026-07-11
- 工作项：`AIW-20260711-FRONTEND-DEPLOY-ATOMIC`
- 实现记录：`IR-20260711-FRONTEND-DEPLOY-ATOMIC`
- 当前结论：本地脚本与静态安全门禁 Go；测试服务器真实失败演练待生命导航二 M4 后执行

## 根因

原脚本会把当前前端目录移动到 rollback 路径，再激活 staging，但后续 chown/chmod 或其他命令失败时只抛错，不自动恢复旧目录；同时没有校验构建入口资产是否真实出现在 staging 和公共 URL。脚本“生成了备份目录”不等于具备可验证回滚。

## 修复

- 本地构建完成并识别版本化 JS entry asset 后才执行服务器备份；
- 任何上传前强制运行 `Backup-TestServerState.ps1`；
- 上传到 timestamp archive，解压到唯一 staging；
- staging 必须包含根 index、services index 和预期 entry asset；
- 激活后使用 Bash `trap rollback_deployment ERR`，任何远程失败自动移动失败制品并恢复 rollback；
- 提供 `-SimulatePostDeployFailure`，用于真实验证远程失败回滚；
- 公共 URL 使用 timestamp query 和 `Cache-Control: no-cache` 验证预期 asset；
- 公共验证或 post-ready 失败时从本机触发第二层回滚，并再次验证 `/ready` 与 services 页面；
- 部署前后均要求 `/ready` 为 ready 且 db=true；
- 不读取、轮换或输出服务器秘密。

## 本地证据

- `Test-ServicePlazaFrontendDeploymentSafety.ps1` 校验关键安全不变量和 backup-before-upload 顺序；
- PowerShell AST 解析通过；
- 服务广场契约与 UTF-8 门禁通过；
- `git diff --check` 通过。

## 未关闭

- 生命导航二 M4 前禁止改变当前测试环境制品；
- M4 后先以 `-SimulatePostDeployFailure` 部署候选制品，必须证明旧 asset 恢复；
- 随后执行正常部署并记录 target、rollback、expected asset、公共验证及 `/ready` 结果。
