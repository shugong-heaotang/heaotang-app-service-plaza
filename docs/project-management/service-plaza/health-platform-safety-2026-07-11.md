# 健康大管家平台安全前置实施记录

- 平台工作项：`AIW-20260711-HEALTH-PLATFORM-SAFETY-GOVERNANCE`
- 后端工作项：`AIW-20260711-HEALTH-PLATFORM-SAFETY-BACKEND`
- 实现记录：`IR-20260711-HEALTH-PLATFORM-SAFETY-R3`
- 后端分支：`codex/health-manager-platform-safety`
- 后端提交：`e361a8ac3f1b93dced567dbb9a3fb6c98156f555`
- 当前结论：本地实现与全量测试 Go；测试环境部署未执行，状态为 implemented

## 安全发现

### Blocker：健康 AI 未经同意即读取并外发健康数据

原 `POST /api/v1/health/analyze` 会读取登录用户的健康档案和最近指标，拼接提示词并调用 `deepseek-chat`。当前没有健康 AI 同意、供应商边界、医疗安全、危急分流和保留规则契约；这违反“依赖未标准化即关闭能力”的平台规则。虽然首切片的咨询正文没有进入该调用，但不能用较窄结论掩盖同一健康插件中的更大外发风险。

修复后保留兼容路由，但在任何读取和 Provider 调用前固定返回 HTTP 503、机器码 `HEALTH_AI_CONSENT_REQUIRED`；健康插件同时移除对 AI 插件的运行依赖。回归测试证明响应失败关闭且 `success=false`。

### Major：咨询输入和敏感缓存边界不完整

原服务只检查未 trim 的 `patient_name != ""`，未要求症状、未限制长度；空白姓名可通过，超长敏感正文可进入数据库，等价空白输入还会形成不同幂等哈希。GET/POST 咨询响应没有禁止中间缓存。

修复后：

- 姓名和症状先 Unicode trim，再按 80/2000 个 Unicode 字符校验；
- 归一化先于幂等哈希，同键等价空白输入重放同一资源；
- 非法 JSON、缺失和超长字段均返回稳定 400 机器码；
- 咨询 POST/GET 与健康 AI 失败响应均设置 `Cache-Control: private, no-store`。

## 验证证据

- `go test -count=1 ./plugins/health-plugin`：通过。
- `go test -count=1 ./...`：全仓通过。
- `go vet ./...`：通过。
- HTTP 回归覆盖非法 JSON、空白/超长姓名、空白/超长症状、trim 后持久化、no-store、归一化幂等重放和 AI 503 失败关闭。
- 修改行秘密扫描：通过；只使用合成健康文本，未写入真实身份、健康数据、Token、密码或 Provider 凭据。
- 代码扫描确认健康插件不再包含 `AI.Chat`、模型名或健康提示词构造。

## 未关闭项

1. 为避免改变生命导航二 M4 已部署制品，本提交暂不部署；测试环境仍需备份后部署并执行 HTTP 级验证。
2. POST/GET 可展示 DTO 与敏感字段最小化尚未冻结。
3. 结构化日志、遥测、截图和报告的端到端敏感正文排除证据尚未完成。
4. `app/src/modules/health-manager` 平台路由挂载工作项尚未实施。
5. 健康板块通知仍为待启动，本平台修复不构成正式派发或 M2 Go。
