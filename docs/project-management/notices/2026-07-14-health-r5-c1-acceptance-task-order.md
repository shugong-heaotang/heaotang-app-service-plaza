# 健康大管家 R5-C1 独立验收与受控集成任务书

- work_id: `AIW-20260714-HEALTH-R5-C1-ACCEPTANCE`
- record_id: `IR-20260714-HEALTH-R5-C1-ACCEPTANCE`
- owner: Codex platform integration agent
- branch: `codex/health-r5-c1-acceptance`
- worktree: `C:/Users/shugo/Documents/worktrees/heaotang-health-r5-c1-acceptance`
- authority base: `f03aa13dc32111ad3b880a7971ac782f4acb556b`
- candidate source: `eebc197837d85d68c471299eb94bc80778697949`
- module work item: `AIW-20260714-HEALTH-R5-CONSULTATION-SECOND-OPINION-MDT-CONTRACTS`

## Objective

独立复核 R5-C1 结构化转介、人工初审、紧急线下分流、定向专家征集、主责医生/MDT、合规医疗机构承接、第二意见独立性和全过程审计合同；若全部门禁为 Go，只纳入 exact candidate source 的十个模块路径，保留权威 registry 全量状态并将平台验收项与模块项受控收口，再用 expected-remote lease 推送权威集成分支。

## Required gates

1. ownership/preflight、当期 checklist、随机治理考试 100。
2. candidate exact commit、本地/远端一致、clean、十个变更路径均在模块 allowed paths 内。
3. 权威需求补充 SHA-256、Schema、23 项正负 conformance、模块 checklist/exam/IR/Handoff 独立复核。
4. 申请人或核验合法代理、授权、来源、版本、缺失资料和责任人必须可追溯；AI 只整理摘要和缺失清单，不形成诊断。
5. 医生集团医疗质量人员人工初审、资料不足 hold、急症或不适宜线上处理的失败关闭线下分流不得被 AI 或自动流程绕过。
6. 仅允许从已核验专家池定向征集；利益冲突、主责医生/MDT、合规医疗机构承接、第二意见独立版本、原意见和分歧必须保留。
7. 禁止公开身份或完整病历、抢单、竞价治疗、治愈悬赏、疗效承诺、结果付费；费用只记录状态，不配置真实金额或授权收费。
8. collaboration、两层依赖、总合同、UTF-8、diff、范围、秘密与医疗安全模式门禁全部通过。
9. 平台 IR/Handoff、commit、expected-remote lease push；最终将平台和 R5 模块工作项收口为 `integrated`，并在 Handoff 中形成 R1-R5 最终证据索引。

## Prohibited

- 禁止修改 R5 候选模块产物来让验收通过，禁止自降测试、Schema、安全、权限或验收口径。
- 禁止整文件覆盖 authority registry、普通强推、无 lease 覆盖或猜测漂移基线。
- 禁止前后端、共享运行时、API、数据库、真实医生/身份/会员/健康数据、互联网诊疗、诊断/处方/改药、收费/支付、测试服、生产和不可逆操作。
- AI 不得冒充医生、承诺疗效、公开病历、组织抢单/竞价/悬赏、独立关闭专业或紧急风险。

## Verdict boundary

R5-C1 Go 仅确认合成、离线、`synthetic_only=true`、`executable=false` 的咨询、第二意见、专家征集与 MDT 合同可作为后续实现边界。医疗质量、合规医疗机构、隐私法律、平台安全和健康馆运营会签可保持 `pending-with-owner`；这些 Pending 不阻止本合同独立验收，但阻止真实咨询/第二意见/MDT、真实身份和健康数据、互联网诊疗、真实费用、收费、部署与生产。
