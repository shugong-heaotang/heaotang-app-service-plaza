# 健康大管家 MVP-90 PRD 阶段 Handoff

- Handoff ID：`HM-MVP90-PRD-HANDOFF-20260711-001`
- 上游 Handoff：`SP-H031`
- 工作项：`AIW-20260711-HEALTH-MVP90-PRD-DOCS`
- 提交人：健康大管家负责人
- 接收人：服务广场平台集成负责人、和奥堂医生集团专业负责人及联合评审角色
- 日期：2026-07-11
- 分支：`codex/health-manager-mvp90-prd`
- 当前阶段：PRD-C1 工作稿
- 当前结论：C0 Go；C1 已形成首稿，待平台检查点评审；业务实现 No-Go。

## 已完成

1. 核对正式通知、活动工作项、基线、激活 HEAD、merge-base、工作树和六条允许路径。
2. 运行 preflight，完成平台依赖和健康大管家内部依赖验证。
3. 逐项全文读取28个治理输入，完成 current checklist。
4. 随机治理考试8题全部正确，score=100。
5. 建立 MVP-90 PRD 工作稿，覆盖首批会员、核心问题、承诺/禁止承诺、8+5 页面和 PDCAR。
6. 将用户确认的52项会员需求业务目录、服务标准、外部能力池纳入 PRD，而非保留为仓库外材料。
7. 对养老“抗摔”需求完成差距分析，正式定义为“老年跌倒风险预防与跌倒后处置”，拆分为6个子业务。

## 养老跌倒预防结论

- 当前 MVP 具备承载该需求的测评、风险提示、人工转介、不适暂停和紧急入口框架。
- 当前没有专业跌倒风险规则、家庭环境评估、肌力平衡训练、药师复核、辅具适配、紧急 SLA 和跌倒后随访闭环。
- 不得声称养老抗跌倒业务已经开发完成。
- 建议在基础 MVP 切片通过后，另行派发 `HM-ELDER-FALL-PREVENTION` 专项 PRD 和实现工作项。

## 当前治理证据

- Checklist：`contracts/modules/health-manager/development-checklists/2026-07-11-health-mvp90-prd.json`，28/28，current。
- Exam：`contracts/modules/health-manager/governance-exams/2026-07-11-health-mvp90-prd-attempt-1.json`，100，passed。
- Receipt：`docs/project-management/modules/health-manager/health-manager-mvp90-prd-receipt.md`。
- PRD：`docs/project-management/modules/health-manager/health-manager-mvp90-prd-v1.md`。

## 未完成

- PRD-C2 至 PRD-C5；
- 页面级字段、对象、状态机和角色权限完整矩阵；
- 15个风险/异常验收场景和合成数据矩阵；
- 联合决策表的专业、法律、安全、运营会签；
- 最终 implementation-record、全文验证和平台文档验收。

## Pending

- HM-R0 正式专业冻结；
- AI、管理师和医生允许/禁止动作的专业会签；
- 风险分级、紧急值班和无法联系机制；
- 管理师准入、容量、标准工时和响应承诺；
- 数据保留、导出、删除和特殊人群规则；
- 价格、套餐、积分、供应商数量和服务时限；
- 老年跌倒专项专业规则和合作单位准入。

## 边界

- 本阶段没有修改业务代码、接口、Schema、环境、部署或生产。
- 没有使用真实健康数据、真实会员资料或真实资金。
- C1 推送到 GitHub 只用于阶段评审，不代表合并、正式冻结或业务开发授权。

## 下一检查点

平台确认 C1 方向后进入 PRD-C2；若平台要求精确修订，只在六条允许路径内处理，并保留所有专业与商业 Pending。
