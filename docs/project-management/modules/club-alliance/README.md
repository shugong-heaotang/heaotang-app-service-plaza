# 俱乐部联盟长期项目入口

项目 ID：`club-alliance`
板块负责人：俱乐部联盟负责人
父项目集成负责人：服务广场平台集成负责人
当前阶段：`CA-SC P0/P1`
当前状态：CA-F0/H0 Full 与 CA-H1 M4 已 Go；`D-CA-003` 已 Accepted。自建俱乐部首个会员侧闭环已按 `SP-H034` 正式启动，当前仅建设列表、详情、加入和本人申请状态的合同与合成一致性。

## 目标与阶段

先建立顶层标准和独立标准首页，再接入四个递归子项目：`CA-F0 → CA-H0 → CA-H1 → CA-SC/CA-FC/CA-PC/CA-UF → CA-X → CA-R → CA-O`。旧 `standard-club-join-review` README、通知、依赖 Go、回执和 Handoff 仅代表旧自建切片，已被本入口取代，不能证明新项目 Go。

本轮只授权 CA-F0-M0 与 CA-H0：需求事实、能力矩阵、机器契约、Schema、fixtures、conformance 和决策包；不授权 CA-H1 前端实现或四类业务编码。

## 已接受语义

- 公益：Club 实体，`type=standard + category=charity`。
- 友联体：独立关系实体，`relationship_kind=club-federation`；不是 ClubType，不复用 FamilyAlliance。
- 首页四入口继承上游排序：公益、自建、家庭、友联体；管理中心为附属操作入口。
- 单一展示真相源是 `contracts/service-plaza/service-plaza-actions.v1.json`，模块不得复制 label、sort、target、access、lifecycle 或 telemetry。

## 自建俱乐部当前权威语义

- `D-CA-003` 已 Accepted：自建俱乐部只能是 `type=standard AND category=general`。
- 列表必须使用服务端 `type+category` 权威组合筛选，禁止前端全量拉取后本地筛选。
- 详情必须额外失败关闭非 `active+standard+general`。
- 本轮只允许会员侧 list/detail/join/my；创建、审核、成员管理、资金、生产和真实数据仍禁止。

## 必读与门禁

先完成根 README 第 0 节，再读 `docs/project-management/notices/2026-07-12-club-sc-first-closure-task-order.md`、两层依赖和 `self-created/CA-SC-handoff.md`。每阶段独立工作项、分支/工作树、检查单、考试、实现记录和 Handoff；无证据即未通过。
