# 健康大管家 R3 健康学习与健康俱乐部入口合同和负例任务书

状态：正式激活；仅执行 `R3-C1` 最小摘要、权威跳转、会员确认回传和模块隔离合同冻结。

## 工作项

- work_id：`AIW-20260714-HEALTH-R3-LEARNING-CLUB-ENTRY-CONTRACTS`
- record_id：`IR-20260714-HEALTH-R3-LEARNING-CLUB-ENTRY-C1`
- owner：`Health Manager continuous development agent`
- owner_role：健康大管家负责人
- branch：`codex/health-r3-learning-club-entry-contracts`
- worktree：`C:/Users/shugo/Documents/worktrees/heaotang-health-r3-learning-club-entry-contracts`
- base：`be4563ae504c32595f05e2908757129068f8f15b`

## 权威需求输入

- `C:/Users/shugo/Documents/项目最高负责人/health-cross-module-requirements/健康大管家-大益健康馆-学习广场-健康俱乐部需求补充-v1.0.md`
- SHA-256：`FC07676F9D0AB0DBAF1A4575457E4D1A67D642D1C483187E28A5B2C64E2A9012`
- R2 受控集成 authority：`be4563ae504c32595f05e2908757129068f8f15b`
- `C:/Users/shugo/Documents/New project` 全部文件只读；不得写入、清理、重置或提交其 staged、modified、untracked 内容。

## R3-C1 最小交付

1. 学习广场只向健康馆提供“正在学、最近完成、推荐学习、资源引用”等最小摘要；资源、路径、笔记和进度仍由学习广场权威拥有。
2. 俱乐部联盟只向健康馆提供可见俱乐部卡片、本人加入状态、加入方式和安全提示等最小摘要；成员关系、活动和反馈仍由俱乐部联盟权威拥有。
3. 健康馆只展示摘要并跳转到权威模块；禁止共享数据库写入、复制权威状态或由健康大管家改变学习进度和俱乐部成员关系。
4. 学习完成、俱乐部活动或反馈只有在会员明确确认、保留来源/版本/责任人并经健康管理复盘后，才能形成健康管理记录候选；不得自动回传或升级为医疗记录。
5. 形成版本化 JSON 合同、Schema、正例和可执行负例 conformance，覆盖未授权摘要、字段超量、伪造来源/路由、自动回传、权威夺取、完整健康档案读取、AI 医疗越界和 Pending 擅升。

## 精确允许路径

- `docs/project-management/modules/health-manager/health-manager-r3-learning-club-entry-contracts.md`
- `docs/project-management/modules/health-manager/health-manager-r3-learning-club-entry-receipt.md`
- `docs/project-management/modules/health-manager/health-manager-r3-learning-club-entry-handoff.md`
- `contracts/modules/health-manager/r3/learning-club-entry.v1.json`
- `contracts/modules/health-manager/r3/learning-club-entry.v1.schema.json`
- `contracts/modules/health-manager/r3/conformance/test_health_r3_learning_club_entry.py`
- `contracts/modules/health-manager/development-checklists/2026-07-14-health-r3-learning-club-entry*.json`
- `contracts/modules/health-manager/governance-exams/2026-07-14-health-r3-learning-club-entry*.json`
- `contracts/modules/health-manager/implementation-records/2026-07-14-health-r3-learning-club-entry*.json`

## 持续 No-Go

禁止前后端业务代码、共享路由或样式、API、数据库、跨模块直接写库、真实身份/会员/健康数据、互联网诊疗、诊断、处方、改药、收费、支付、测试服部署、生产和不可逆操作。AI 只能整理已授权的合成摘要、识别缺失、匹配已审核学习资源或俱乐部候选并解释原因；不得自动确认、自动回传、形成诊断或独立关闭专业/紧急风险。

## 门禁顺序

ownership/preflight → current checklist 逐项真实阅读 → 随机治理考试 100 → 合同/Schema/文档/负例 → conformance 与两层依赖验证 → implementation record/Handoff → collaboration/总合同/UTF-8/diff/范围/安全 → commit/push → 独立验收或受控集成。
