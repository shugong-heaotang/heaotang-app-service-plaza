# 健康大管家 MVP-90 开发 PRD V1.0 任务通知

通知编号：`HM-MVP90-PRD-TASK-20260711-001`

状态：正式下达；待派发提交受控集成并完成模块工作树最终激活后签收

下达人：服务广场平台集成负责人

承接人：健康大管家负责人

正式 Handoff：`SP-H031`

## 目标与依据

本任务建立独立的 MVP-90 PRD 文档项目，不复用 `AIW-20260711-HEALTH-V1-REQUIREMENTS-DOCS`，也不授权业务实现。上游 HM-R0 母文档状态为 `Technical Review Go / Professional Freeze Pending`；PRD 可以整理已确认的产品结构和显式 Pending 决策，但不得把医疗、隐私、专业责任、价格或运营 Pending 改为 Accepted。

PRD 必须把 90 天最小 PDCAR 闭环变成可评审、可测试、可继续拆分的需求：8 个会员逻辑页面（首页、AI、档案、测评、计划、任务、管理师、我的）和 5 个管理逻辑页面（工作台、会员与风险、沟通记录、计划审核、内容模板），同时覆盖 AI/人工责任、风险/授权/异常、Day 0/1/7/30/90 会员成功及合成数据验收。

## 精确工作项

- work_id：`AIW-20260711-HEALTH-MVP90-PRD-DOCS`
- repository：`C:/Users/shugo/Documents/APP系统`
- branch：`codex/health-manager-mvp90-prd`
- worktree：`C:/Users/shugo/Documents/worktrees/heaotang-health-mvp90-prd`
- base：以最终 activation 提交为准，必须包含本通知和 `SP-H031`

允许路径仅为：

- `docs/project-management/modules/health-manager/health-manager-mvp90-prd-v1.md`
- `docs/project-management/modules/health-manager/health-manager-mvp90-prd-receipt.md`
- `docs/project-management/modules/health-manager/health-manager-mvp90-prd-handoff.md`
- `contracts/modules/health-manager/development-checklists/2026-07-11-health-mvp90-prd.json`
- `contracts/modules/health-manager/governance-exams/2026-07-11-health-mvp90-prd-attempt-1.json`
- `contracts/modules/health-manager/implementation-records/2026-07-11-health-mvp90-prd.json`

## 检查点

- PRD-C0：签收、当前 checklist 逐项读取、随机治理考试 100 分。
- PRD-C1：首批会员、核心问题、承诺/禁止承诺、8+5 页面和母文档追踪矩阵。
- PRD-C2：PDCAR 主流程、核心对象/状态、AI/管理师/医生责任和转人工规则。
- PRD-C3：风险、授权、隐私、异常、15 个场景、合成数据和 Day 0/1/7/30/90 验收。
- PRD-C4：产品、专业、法律、安全、运营、平台联合决策表；每项为 Accepted、exact revision 或 Pending with owner。
- PRD-C5：平台文档验收、Handoff 和后续最小业务切片建议；不自动授权代码。

## 禁止范围

不建设完整 53 页，不包含家庭、俱乐部、加盟、多服务商、分润和真实资金；不得修改业务代码、接口、Schema、环境、部署或生产；不得使用真实健康数据。价格、容量、时限和专业规则只允许使用版本化配置机制和 Pending 元数据，不得写死具体承诺。

在模块工作项仍为 `planned` 时禁止创建 checklist、考试或 PRD。只有平台回传最终 activation commit、权威 base、clean 工作树并把状态改为 `active` 后才可开工。
