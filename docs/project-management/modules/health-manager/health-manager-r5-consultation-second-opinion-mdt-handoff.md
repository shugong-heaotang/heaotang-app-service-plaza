# 健康大管家 R5-C1 Handoff

- work_id：`AIW-20260714-HEALTH-R5-CONSULTATION-SECOND-OPINION-MDT-CONTRACTS`
- record_id：`IR-20260714-HEALTH-R5-CONSULTATION-SECOND-OPINION-MDT-C1`
- checkpoint：R5-C1 咨询、第二意见与疑难病例协同合同和负例
- status：`handoff-ready / awaiting independent review`
- executable：`false`

## Completed

1. 冻结咨询、第二意见、疑难病例专家征集和 MDT 的结构化转介包、申请权限、授权、来源、版本、缺失资料和责任人。
2. 冻结医生集团医疗质量人工初审、资料不足 hold、紧急/专业风险停止线上流程并转线下合规医疗机构。
3. 冻结已核验专家池定向征集、执业范围、服务方式、利益冲突披露/复核、主责医生或 MDT 和医疗机构承接责任。
4. 冻结第二意见独立性、意见原文与分歧不可覆盖、事件级全程留痕和只记录费用状态而不授权真实金额。
5. 禁止公开身份/完整病历、抢单、医生竞价、治愈悬赏、结果付费、疗效承诺、非医疗机构诊疗与 AI 诊断/风险关闭。
6. 增加 Draft 2020-12 Schema、语义基线和 21 个可执行负例，共 23 项 conformance。

## Verified

- current checklist 28/28、当前治理 SHA 匹配；governance exam attempt 2=100，attempt 1=50 保留为不可变失败证据。
- 需求补充 SHA-256：`fc07676f9d0ab0dbaf1a4575457e4d1a67d642d1c483187e28a5b2c64e2a9012`。
- `python -X utf8 -m unittest contracts.modules.health-manager.r5.conformance.test_health_r5_consultation_second_opinion_mdt -v`：23/23 passed。
- foundation dependencies、health internal dependencies、全部 checklist/exam/IR snapshots、collaboration 和 Service Plaza 总合同通过。
- `scripts/Test-TextEncoding.ps1`：1396 files passed。

## Root-cause closeout

- `R5-GATE-CHECKLIST-VALIDATION-CONTEXT`：首次校验遗漏 `--project-root`，随后发现 attestation 必须使用固定字面量；按原校验器修正并从同一门禁重跑，不弱化规则。
- `R5-GATE-EXAM-RANDOM-ANSWER-SEQUENCE`：attempt 1 错误复用另一张随机试卷答案导致 50 分；失败快照不变，完整重读 remediation 并以 attempt 2=100 关闭。
- retry 控制通道首次无法驱动 `Read-Host`，未生成试卷；改为同一 PowerShell 作用域回传脚本展示后的精确 path+nonce，生成的 remediation_rereads 保留展示哈希、nonce 与确认时间。
- 聚合 Python 门禁包装器首次未传递参数而进入解释器，输出未计作通过；随后逐条调用原始 CLI。平台依赖首轮又因把 `--module` 误作模块 ID 失败，读取 CLI 后改传模块依赖 JSON 路径，原门禁与后续全套验证均通过。
- 提交前暂存命令首轮误用 Bash `\` 续行符，在 PowerShell 解析阶段失败且未改动状态；改用 PowerShell 路径数组后，10/10 staged 路径全部位于登记范围。

## Pending

- 医生集团医疗质量：真实人工初审、专家池、主责医生/MDT 和质量政策。
- 合规医疗机构：正式诊疗、电子病历和服务承接。
- 隐私法律：真实身份、代理、授权、真实健康数据和互联网诊疗。
- 平台安全：共享运行时、API、数据库和环境。
- 健康馆运营：真实会员试点、线下承接和真实费用流程。
- does_not_block：R5 合成合同一致性、负例、独立验收和受控集成。

## No-Go

前后端、共享运行时、API、数据库、真实医生/身份/会员/健康数据、互联网诊疗、诊断、处方、改药、冒充医生、疗效承诺、公开病历、抢单、医生竞价、治愈悬赏、结果付费、真实收费、支付、测试服、生产和不可逆操作均未授权。

## 下一门禁

独立 reviewer 从 exact commit 复跑 23 项 conformance、current checklist/exam/IR、两层依赖、UTF-8、diff、范围、秘密与敏感模式门禁；Go 后由平台受控集成并收口 R5。
