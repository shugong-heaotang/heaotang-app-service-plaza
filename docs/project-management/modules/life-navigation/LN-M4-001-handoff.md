# 生命导航阶段 Handoff：LN-M4-001 No-Go

- 验收单号：`LN-M4-001`
- 通知编号：`LN-TASK-20260710-001`
- 负责人：生命导航二负责人
- 记录时间：`2026-07-11T01:57:34+08:00`
- 实现记录：`IR-20260711-LIFE-APPLICATION-HISTORY-M4`
- 最终结论：No-Go
- 当前工作项：保持 active

## 已通过范围

### 后端部署

- 后端从固定干净工作树和提交 `70fa12276e6eac17369c0d1d3c1d23a8e757fcc0` 部署成功。
- 远端备份：`/root/heaotang-backups/20260711-014016.tar.gz`。
- 本地备份：`D:\Backup\heaotang-test-server\20260711-014016\test-server-state.tar.gz`。
- 部署二进制 SHA-256：`75a9de31b2094c4be6d14c26e9bed96c62a6b6ea7f5876d22ea6f3383a2723b7`。
- `/ready` 为 ready、`db=true`、plugins=24；目录为 9 services / 20 actions。

### 前端部署

- 前端部署成功，目标：`/var/www/heaotang/app/service-plaza`。
- 远端备份：`/root/heaotang-backups/20260711-014107.tar.gz`。
- 本地备份：`D:\Backup\heaotang-test-server\20260711-014107\test-server-state.tar.gz`。
- 回滚目录：`/var/www/heaotang/app/service-plaza.rollback-20260711-014107`。
- 页面资源：`index-BzyZrLZ3.js`。

### Life API UAT

- run：`life-m4-20260711-015041`。
- 账号只记录脱敏标识：用户 A `199****9992`、隔离用户 B `199****9994`。
- ready 200；未登录写入 401；A/B 登录均 200。
- 首次创建 201，record id=118；同键重放 200、仍为 id=118、`Idempotency-Replayed=true`。
- 同键异载荷 409，机器码 `IDEMPOTENCY_KEY_REUSED`。
- 用户 A 历史 GET 200 且包含 id=118；用户 B 历史 GET 200 且不包含该记录。
- request-id 往返通过；token 已清空；`secrets_persisted=false`。

### 浏览器未登录和响应式

- 生命导航路由、一级标题、真实 `AuthPanel`、返回路径和底部导航通过。
- `390x844` 与 `1366x768` 均无横向溢出。

## No-Go 阻塞

- 登录后浏览器 UAT 未取得成功请求证据。
- 随后的只读数据库核查：`today_count=5`、`active_unused=0`。
- 根因：测试身份计划只统计本轮调用，没有在分配正式浏览器账号前读取该 test-only 身份已有的 UTC 日消耗；shell API 会话不能安全注入受控浏览器，浏览器需要的独立短会话没有剩余额度。
- 受影响范围：浏览器登录、提交、成功后刷新历史、刷新页面后持久记录和返回的认证后链路仍未验证。
- 未受影响范围：部署状态和 life API 首次/重放/冲突/本人历史/跨用户隔离已经通过。
- 合规处理：没有换号、清计数、改限流、恢复公开验证码或持久化 OTP/JWT。

## 重测条件

1. 等待 UTC 日 send-code 计数自然重置。
2. 开始前只读确认指定 test-only 身份有可用配额。
3. 仅执行一次 `AuthPanel` send-code，经安全渠道临时取得和输入 OTP；不写入报告、截图、仓库或聊天记录。
4. 完成浏览器登录、提交、成功后历史刷新、页面刷新后记录仍在和返回 `/services`。
5. 完成后清空浏览器会话。
6. 不重新部署，除非二进制哈希、前端资源、路由或 `/ready` 与本 Handoff 记录发生漂移。

## 回滚与证据

- 部署检查均成功，未触发回滚；后端备份和前端 rollback 目录可用。
- 证据：
  - `acceptance/LN-M4-001-local-gates.json`
  - `acceptance/LN-M4-001-deployment-evidence.json`
  - `acceptance/LN-M4-001-api-acceptance.json`
  - `acceptance/LN-M4-001-frontend-uat.md`
  - `acceptance/LN-M4-001-rollback-evidence.json`
- 在认证后浏览器主链路通过前，不得把实现记录升级为 verified/deployed，不得签 M4 Go，不得把 `acceptance_readiness` 推断为 Go。
