# 健康咨询敏感数据审计与空症状伪造回退修复

- 日期：2026-07-11
- 工作项：`AIW-20260711-HEALTH-SUBMISSION-NO-FALLBACK`
- 实现记录：`IR-20260711-HEALTH-SUBMISSION-NO-FALLBACK`
- 当前结论：本地代码、测试、构建与静态审计 Go；测试环境运行日志和截图待验证

## Blocker 根因与修复

安全审计发现共享前端把空白 `symptoms` 替换为“希望获得健康咨询”。这不是用户输入，会绕过服务端必填校验并制造虚假健康记录，直接违反冻结合同。

修复后：

- 只执行 trim；空白输入发送空字符串；
- 服务端权威返回 `HEALTH_SYMPTOMS_REQUIRED`；
- 自动化断言请求体不包含旧固定句子；
- 不在前端复制后端长度或错误判断。

## 静态审计范围与结论

| 范围 | 结论 | 证据 |
|---|---|---|
| `health-plugin` 生产代码 | 未发现 slog/log/Printf/console/遥测输出咨询字段 | `rg` 对生产 Go 路径扫描 |
| 健康模块与 submission repository | 未发现 console、analytics、track、telemetry 或固定症状回退 | 目标生产路径 `rg` 扫描退出为无匹配 |
| 动作遥测 | 只提交 service/action/telemetry_event 等动作元数据，不接收 patient_name/symptoms | `app/src/infrastructure/actionTelemetry.ts` 字段审查 |
| 测试与文档 | 仅使用“合成测试用户/合成症状”等明确合成数据；未发现真实健康身份 | 测试源与报告关键词扫描 |
| 密钥与令牌 | 新增文件未包含 Bearer 值、密码、私钥或 Provider 凭据 | 修改路径秘密模式扫描 |

咨询正文仍会按产品合同出现在加密传输的 POST 请求、本人 GET 响应和数据库咨询字段；这属于功能必需数据，不代表可写入日志或遥测。

## 验证

- `npm test -- --run src/infrastructure/submissionRepository.test.ts`：5/5；
- `npm test -- --run`：15 文件、93/93；
- `npm run build`：通过；
- 目标生产路径敏感扫描：无日志、遥测、分析或固定症状回退；
- `scripts/Test-ServicePlazaContracts.ps1`、`scripts/Test-TextEncoding.ps1`、`git diff --check`：通过。

## 残余风险

- 静态扫描不能证明反向代理、运行时异常栈或外部观测平台绝不记录请求体；测试环境部署后必须提交合成 marker，扫描服务器日志、遥测载荷和 UAT 截图。
- 正式生产医疗免责声明和保留周期仍是独立门禁。
