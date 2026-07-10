# 俱乐部联盟长期项目入口

项目 ID：`club-alliance`
板块负责人：俱乐部联盟负责人
父项目集成负责人：服务广场平台集成负责人
当前阶段：`CA-F0-M0 + CA-H0`
当前状态：模块 G0 已完成：当前检查单 28/28、随机治理考试 100 分、`SP-H025` 回执和 CA-F0-M0 接收检查点已形成；等待平台阶段验收，不据此宣称 CA-H0 Go。

## 目标与阶段

先建立顶层标准和独立标准首页，再接入四个递归子项目：`CA-F0 → CA-H0 → CA-H1 → CA-SC/CA-FC/CA-PC/CA-UF → CA-X → CA-R → CA-O`。旧 `standard-club-join-review` README、通知、依赖 Go、回执和 Handoff 仅代表旧自建切片，已被本入口取代，不能证明新项目 Go。

本轮只授权 CA-F0-M0 与 CA-H0：需求事实、能力矩阵、机器契约、Schema、fixtures、conformance 和决策包；不授权 CA-H1 前端实现或四类业务编码。

## 已接受语义

- 公益：Club 实体，`type=standard + category=charity`。
- 友联体：独立关系实体，`relationship_kind=club-federation`；不是 ClubType，不复用 FamilyAlliance。
- 首页四入口继承上游排序：公益、自建、家庭、友联体；管理中心为附属操作入口。
- 单一展示真相源是 `contracts/service-plaza/service-plaza-actions.v1.json`，模块不得复制 label、sort、target、access、lifecycle 或 telemetry。

## 局部待决策

`D-CA-003`：自建是否精确映射 `type=standard + category=general`。Pending 只阻塞可执行 selector、category API 和 SC/PC 分类编码；不阻塞 H0 基础结构与 base conformance，也不得在决定前生成业务 selector。

## 必读与门禁

先完成根 README 第 0 节，再读 `docs/project-management/notices/2026-07-11-club-alliance-foundation-task-order.md`、两层依赖和当前 Handoff。每阶段独立工作项、分支/工作树、检查单、考试、实现记录和 Handoff；无证据即未通过。
