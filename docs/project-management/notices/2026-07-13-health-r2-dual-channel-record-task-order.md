# 健康大管家 R2 双渠道统一档案合同与负例任务书

状态：正式激活；仅执行 `R2-C1` 统一档案、双渠道建档、来源、候选确认、纠错、授权和审计合同冻结。

## 工作项

- work_id：`AIW-20260713-HEALTH-R2-DUAL-CHANNEL-RECORD-CONTRACTS`
- record_id：`IR-20260713-HEALTH-R2-DUAL-CHANNEL-RECORD-C1`
- owner：`Health Manager continuous development agent`
- owner_role：健康大管家负责人
- branch：`codex/health-r2-dual-channel-record-contracts`
- worktree：`C:/Users/shugo/Documents/worktrees/heaotang-health-r2-dual-channel-record-contracts`
- base：`e892e4ea0919f7c762bd35fc1606ceab946acb4b`

## 权威需求输入

- `C:/Users/shugo/Documents/项目最高负责人/health-cross-module-requirements/健康大管家-大益健康馆-学习广场-健康俱乐部需求补充-v1.0.md`
- SHA-256：`FC07676F9D0AB0DBAF1A4575457E4D1A67D642D1C483187E28A5B2C64E2A9012`
- R1 受控集成 authority：`e892e4ea0919f7c762bd35fc1606ceab946acb4b`
- `C:/Users/shugo/Documents/New project` 全部文件只读；不得写入、清理、重置或提交其 staged、modified、untracked 内容。

## R2-C1 最小交付

1. 冻结同一会员仅一份主健康档案、档案主体始终为会员本人的不变量。
2. 冻结本人网上自助与大益健康馆协助建档两条流程；协助方不得代替身份确认、授权或最终确认。
3. 冻结资料来源、逐项候选确认、纠错、授权版本、操作人与时间、完整审计链。
4. 区分会员自述、健康管理记录、专业签署记录和医疗机构电子病历，不把协助录入升级为医疗记录。
5. 形成版本化 JSON 合同、Schema、正例和可执行负例 conformance。

## 精确允许路径

- `docs/project-management/modules/health-manager/health-manager-r2-dual-channel-record-contracts.md`
- `docs/project-management/modules/health-manager/health-manager-r2-dual-channel-record-receipt.md`
- `docs/project-management/modules/health-manager/health-manager-r2-dual-channel-record-handoff.md`
- `contracts/modules/health-manager/r2/dual-channel-record.v1.json`
- `contracts/modules/health-manager/r2/dual-channel-record.v1.schema.json`
- `contracts/modules/health-manager/r2/conformance/test_health_r2_dual_channel_record.py`
- `contracts/modules/health-manager/development-checklists/2026-07-13-health-r2-dual-channel-record*.json`
- `contracts/modules/health-manager/governance-exams/2026-07-13-health-r2-dual-channel-record*.json`
- `contracts/modules/health-manager/implementation-records/2026-07-13-health-r2-dual-channel-record*.json`

## 持续 No-Go

禁止前后端业务代码、共享路由或样式、API、数据库、真实身份、真实会员、真实健康数据、代理人建档、互联网诊疗、诊断、处方、改药、收费、支付、测试服部署、生产和不可逆操作。AI 只能整理合成资料、识别缺失和解释候选；不得自动确认资料、代替会员授权、删除原始资料或独立关闭专业/紧急风险。

## 门禁顺序

ownership/preflight → current checklist 逐项真实阅读 → 随机治理考试 100 → 合同/Schema/文档/负例 → conformance 与两层依赖验证 → implementation record/Handoff → collaboration/总合同/UTF-8/diff/范围/安全 → commit/push → 独立验收或受控集成。
