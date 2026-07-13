# 健康大管家 R4 医生目录与受约束推荐合同和负例任务书

状态：正式激活；仅执行 `R4-C1` 医生目录硬门禁、受约束推荐、人工复核和退出合同冻结。

## 工作项

- work_id：`AIW-20260714-HEALTH-R4-DOCTOR-DIRECTORY-RECOMMENDATION-CONTRACTS`
- record_id：`IR-20260714-HEALTH-R4-DOCTOR-DIRECTORY-RECOMMENDATION-C1`
- owner：`Health Manager continuous development agent`
- owner_role：健康大管家负责人
- branch：`codex/health-r4-doctor-directory-recommendation-contracts`
- worktree：`C:/Users/shugo/Documents/worktrees/heaotang-health-r4-doctor-directory-recommendation-contracts`
- base：`dfbff8e87792829e3e2dae8010a1ce3cba6b240c`

## 权威需求输入

- `C:/Users/shugo/Documents/项目最高负责人/health-cross-module-requirements/健康大管家-大益健康馆-学习广场-健康俱乐部需求补充-v1.0.md`
- SHA-256：`FC07676F9D0AB0DBAF1A4575457E4D1A67D642D1C483187E28A5B2C64E2A9012`
- R3 受控集成 authority：`dfbff8e87792829e3e2dae8010a1ce3cba6b240c`
- `C:/Users/shugo/Documents/New project` 全部文件只读；不得写入、清理、重置或提交其 staged、modified、untracked 内容。

## R4-C1 最小交付

1. 冻结医生目录最低字段，以及医师资格、执业证书、执业机构、执业范围、诊疗科目、核验时间和当前服务状态的硬门禁；任一必需门禁缺失、过期、冲突或撤销时默认拒绝进入候选池。
2. 冻结推荐顺序：法定资质与执业关系有效 → 专科/病种/执业范围匹配 → 线上或线下安全分流 → 质量治理 → 培训治理 → 可接诊性 → 会员个人偏好。培训认证不得替代法定资质，个人偏好不得越过医疗安全。
3. 冻结推荐解释、不确定性、证据来源、人工复核、投诉/质量暂停和退出机制；AI 只能从已核验候选池匹配并解释，不得自行创建资质、诊断、接诊或关闭专业/紧急风险。
4. 明确禁止付费、竞价、佣金、广告或机构商业关系改变医疗安全门禁和专业匹配排序；当前不授权真实价格、收费、支付或公开医生排名。
5. 形成版本化 JSON 合同、Draft 2020-12 Schema、语义基线和可执行负例 conformance，覆盖未核验/过期/撤销资质、执业范围不匹配、线上不适宜、付费提权、培训替代资质、AI 伪造标签、跳过人工复核、退出后仍推荐、紧急风险被 AI 关闭和 Pending 擅升。

## 精确允许路径

- `docs/project-management/modules/health-manager/health-manager-r4-doctor-directory-recommendation-contracts.md`
- `docs/project-management/modules/health-manager/health-manager-r4-doctor-directory-recommendation-receipt.md`
- `docs/project-management/modules/health-manager/health-manager-r4-doctor-directory-recommendation-handoff.md`
- `contracts/modules/health-manager/r4/doctor-directory-recommendation.v1.json`
- `contracts/modules/health-manager/r4/doctor-directory-recommendation.v1.schema.json`
- `contracts/modules/health-manager/r4/conformance/test_health_r4_doctor_directory_recommendation.py`
- `contracts/modules/health-manager/development-checklists/2026-07-14-health-r4-doctor-directory-recommendation*.json`
- `contracts/modules/health-manager/governance-exams/2026-07-14-health-r4-doctor-directory-recommendation*.json`
- `contracts/modules/health-manager/implementation-records/2026-07-14-health-r4-doctor-directory-recommendation*.json`

## 持续 Pending 与 No-Go

医生集团医疗质量负责人、隐私法律负责人、平台安全负责人和健康馆运营负责人的正式会签继续 `pending-with-owner`。它们阻止真实医生目录、真实身份/健康数据、互联网诊疗、公开排名、收费、支付、测试服、生产和不可逆操作；不阻止 `synthetic_only=true`、`executable=false` 的离线合同、Schema、正负例和独立验收。

禁止前后端业务代码、共享运行时、API、数据库、真实医生或会员数据、诊断、处方、改药、冒充医生、疗效承诺、付费排序、收费、支付、测试服部署、生产和不可逆操作。

## 门禁顺序

ownership/preflight → current checklist 逐项真实阅读 → 随机治理考试 100 → 合同/Schema/文档/负例 → conformance 与两层依赖验证 → implementation record/Handoff → collaboration/总合同/UTF-8/diff/范围/安全 → commit/push → 独立验收或受控集成。
