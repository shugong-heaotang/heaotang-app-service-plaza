# 健康大管家 R5 咨询、第二意见与疑难病例协同合同和负例任务书

状态：正式激活；仅执行 `R5-C1` 结构化转介、人工初审、紧急分流、主责医生/MDT、合规医疗机构承接和全程留痕合同冻结。

## 工作项

- work_id：`AIW-20260714-HEALTH-R5-CONSULTATION-SECOND-OPINION-MDT-CONTRACTS`
- record_id：`IR-20260714-HEALTH-R5-CONSULTATION-SECOND-OPINION-MDT-C1`
- owner：`Health Manager continuous development agent`
- owner_role：健康大管家负责人
- branch：`codex/health-r5-consultation-second-opinion-mdt-contracts`
- worktree：`C:/Users/shugo/Documents/worktrees/heaotang-health-r5-consultation-second-opinion-mdt-contracts`
- base：`b6736b6117c05780cd6a8df9f3ca162ea1f3f40b`

## 权威需求输入

- `C:/Users/shugo/Documents/项目最高负责人/health-cross-module-requirements/健康大管家-大益健康馆-学习广场-健康俱乐部需求补充-v1.0.md`
- SHA-256：`FC07676F9D0AB0DBAF1A4575457E4D1A67D642D1C483187E28A5B2C64E2A9012`
- R4 受控集成 authority：`b6736b6117c05780cd6a8df9f3ca162ea1f3f40b`
- `C:/Users/shugo/Documents/New project` 全部文件只读；不得写入、清理、重置或提交其 staged、modified、untracked 内容。

## R5-C1 最小交付

1. 冻结咨询、第二意见和疑难病例专家征集的结构化转介包：申请人/合法代理关系、授权状态、主要诉求、已有资料引用、来源、版本、缺失资料和责任人；AI 只整理摘要与缺失清单，不形成诊断。
2. 冻结医生集团医疗质量人员人工初审与紧急风险失败关闭分流；急症、资料不足或不适宜线上处理时必须转线下合规医疗机构，AI 不得独立关闭专业或紧急风险。
3. 冻结已核验专家池定向征集、利益冲突声明、主责医生或 MDT 组建、第二意见独立性、意见原文和分歧留痕；正式诊疗只能由具备相应资质的医疗机构承接。
4. 冻结全过程审计：事件、责任人、时间、版本、授权、原始意见、后续安排和费用状态只记录结构，不配置真实金额或收费；禁止公开身份/完整病历、抢单、竞价治疗、治愈悬赏、疗效承诺和结果付费。
5. 形成版本化 JSON 合同、Draft 2020-12 Schema、语义基线和可执行负例 conformance，覆盖未授权代理、公开病历、AI 诊断、跳过人工初审、紧急风险被关闭、未核验专家、利益冲突未披露、无主责医生、非医疗机构承接、竞价/悬赏/结果付费、意见原文被覆盖和 Pending 擅升。

## 精确允许路径

- `docs/project-management/modules/health-manager/health-manager-r5-consultation-second-opinion-mdt-contracts.md`
- `docs/project-management/modules/health-manager/health-manager-r5-consultation-second-opinion-mdt-receipt.md`
- `docs/project-management/modules/health-manager/health-manager-r5-consultation-second-opinion-mdt-handoff.md`
- `contracts/modules/health-manager/r5/consultation-second-opinion-mdt.v1.json`
- `contracts/modules/health-manager/r5/consultation-second-opinion-mdt.v1.schema.json`
- `contracts/modules/health-manager/r5/conformance/test_health_r5_consultation_second_opinion_mdt.py`
- `contracts/modules/health-manager/development-checklists/2026-07-14-health-r5-consultation-second-opinion-mdt*.json`
- `contracts/modules/health-manager/governance-exams/2026-07-14-health-r5-consultation-second-opinion-mdt*.json`
- `contracts/modules/health-manager/implementation-records/2026-07-14-health-r5-consultation-second-opinion-mdt*.json`

## 持续 Pending 与 No-Go

医生集团医疗质量负责人、合规医疗机构、隐私法律负责人、平台安全负责人和健康馆运营负责人的正式会签继续 `pending-with-owner`。它们阻止真实咨询/第二意见/MDT、真实身份或健康数据、互联网诊疗、真实费用、收费、支付、测试服、生产和不可逆操作；不阻止 `synthetic_only=true`、`executable=false` 的离线合同、Schema、正负例和独立验收。

禁止前后端业务代码、共享运行时、API、数据库、真实医生或会员数据、诊断、处方、改药、冒充医生、疗效承诺、公开病历、抢单、竞价治疗、治愈悬赏、结果付费、真实收费、支付、测试服部署、生产和不可逆操作。

## 门禁顺序

ownership/preflight → current checklist 逐项真实阅读 → 随机治理考试 100 → 合同/Schema/文档/负例 → conformance 与两层依赖验证 → implementation record/Handoff → collaboration/总合同/UTF-8/diff/范围/安全 → commit/push → 独立验收或受控集成。
