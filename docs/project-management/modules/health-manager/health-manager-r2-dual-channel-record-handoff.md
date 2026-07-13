# 健康大管家 R2-C1 Handoff

- work_id：`AIW-20260713-HEALTH-R2-DUAL-CHANNEL-RECORD-CONTRACTS`
- record_id：`IR-20260713-HEALTH-R2-DUAL-CHANNEL-RECORD-C1`
- checkpoint：R2-C1 双渠道统一档案合同与负例
- status：`handoff-ready / awaiting independent review`
- executable：`false`

## Completed

1. 冻结同一会员一份主健康档案及会员本人数据权利不变量。
2. 冻结本人自助和健康馆协助两条建档流程及会员专属身份、授权、最终确认动作。
3. 冻结逐项来源、候选确认、追加纠错、授权版本和完整审计链。
4. 明确四类记录不可混称，协助建档不自动建立医生诊疗关系。
5. 增加 Schema、基线与可执行负例；AI、真实数据、代理建档和运行时保持失败关闭。

## Verified

- current checklist 28/28；governance exam attempt 1=100。
- conformance、两层依赖、治理、编码、范围和安全门禁由本提交证据给出，等待独立 reviewer 复跑。

## Pending

- 隐私法律：真实身份、真实健康数据、授权运行时。
- 医疗质量：专业签署记录与医疗服务运行时。
- 平台安全：共享运行时、数据库和环境。
- 健康馆运营：真实工作人员与会员试点。
- does_not_block：合成合同一致性、负例、R2 独立验收。

## No-Go

前后端、API、数据库、真实身份/会员/健康数据、代理建档、互联网诊疗、诊断、处方、改药、收费、支付、测试服、生产和不可逆操作均未授权。

## 门禁根因记录

- issue：`R2-GATE-SENSITIVE-REGEX-FALSE-POSITIVE`
- 症状：第一次 Git grep 因以连字符开头的模式未使用 `-e` 被当作选项；修正后，宽泛 18 位规则又把 current checklist 的 SHA 数字片段误报为身份证样式。
- 影响：最终敏感模式门禁暂时 No-Go；不影响 16 项合同 conformance 和其他治理证据，但在修正并重跑前禁止提交。
- 已尝试：补显式 `-e`；复核全部命中，确认一个是 SHA 片段、一个是专门验证拒绝逻辑的合成手机号标记。
- 根因：扫描器未排除十六进制哈希上下文，且没有把专用负例与数据样本分类。
- owner：健康大管家负责人。
- 下一动作：使用排除十六进制相邻字符的 PCRE 边界扫描；只允许 conformance 中精确的合成手机号负例标记，任何其他命中失败关闭。
- does_not_block：合同、Schema、负例与独立评审；blocks：本提交直到修正扫描通过。

## 下一门禁

独立 reviewer 从 exact commit 复跑 16 项 conformance、current checklist/exam、依赖、IR、UTF-8、diff、范围和秘密扫描；Go 后由平台受控集成并收口 R2，再另立 R3 工作项。
