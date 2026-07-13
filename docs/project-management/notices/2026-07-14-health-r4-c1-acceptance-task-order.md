# 健康大管家 R4-C1 独立验收与受控集成任务书

- work_id: `AIW-20260714-HEALTH-R4-C1-ACCEPTANCE`
- record_id: `IR-20260714-HEALTH-R4-C1-ACCEPTANCE`
- owner: Codex platform integration agent
- branch: `codex/health-r4-c1-acceptance`
- worktree: `C:/Users/shugo/Documents/worktrees/heaotang-health-r4-c1-acceptance`
- authority base: `9c3bfdb93fb4dd37c2759c64e29a0490eeff7109`
- candidate source: `da66c7db451ae786268d743e0a1ff267fbc4a460`
- module work item: `AIW-20260714-HEALTH-R4-DOCTOR-DIRECTORY-RECOMMENDATION-CONTRACTS`

## Objective

独立复核 R4-C1 医生目录、资质和执业硬门禁、受约束推荐、商业中立、解释、人工复核与退出合同；若全部门禁为 Go，只纳入 exact candidate source 的九个模块路径，保留权威 registry 全量状态并将平台验收项与模块项受控收口，再用 expected-remote lease 推送权威集成分支。

## Required gates

1. ownership/preflight、当期 checklist、随机治理考试 100。
2. candidate exact commit、本地/远端一致、clean、九个变更路径均在模块 allowed paths 内。
3. 权威需求补充 SHA-256、Schema、19 项正负 conformance、模块 checklist/exam/IR/Handoff 独立复核。
4. 法定资质和执业关系、专业匹配、线上/线下安全分流、质量治理、推荐解释、人工复核、退出与重新进入均须失败关闭。
5. 付费、竞价、佣金、广告或机构商业关系不得改变医疗安全与专业匹配排序；AI 不得创建资质/标签、诊断、接诊或关闭专业/紧急风险。
6. collaboration、两层依赖、总合同、UTF-8、diff、范围、秘密与医疗安全模式门禁全部通过。
7. 平台 IR/Handoff、commit、expected-remote lease push；最终将平台和 R4 模块工作项收口为 `integrated`。

## Prohibited

- 禁止修改 R4 候选模块产物来让验收通过，禁止自降测试、Schema、安全、权限或验收口径。
- 禁止整文件覆盖 authority registry、普通强推、无 lease 覆盖或猜测漂移基线。
- 禁止前后端、共享运行时、API、数据库、真实医生/身份/会员/健康数据、互联网诊疗、诊断/处方/改药、公开排名、收费/支付、测试服、生产和不可逆操作。
- AI 不得冒充医生、承诺疗效、绕过资质/执业/安全/质量门禁或独立关闭专业/紧急风险。

## Verdict boundary

R4-C1 Go 仅确认合成、离线、`synthetic_only=true`、`executable=false` 的医生目录与受约束推荐合同可作为后续实现边界。医疗质量、隐私法律、平台安全和健康馆运营会签可保持 `pending-with-owner`；这些 Pending 不阻止本合同独立验收，但阻止 R4 runtime、真实医生和健康数据、互联网诊疗、公开排名、收费、部署与生产。R5 仅可在 R4 受控集成收口后另立工作项。
