# CA-SC P0/P1 Handoff

- from：俱乐部联盟自建俱乐部负责人
- to：服务广场平台集成负责人
- date：2026-07-12
- work item：`AIW-20260712-CLUB-SC-P0-P1-CONTRACTS`
- status：handoff-ready
- implementation commit：`8d4d6fe5ece99e411da02f2ccf0b6a0f6902ad87`
- current checklist：`FC-20260712-CLUB-SC-P0-P1-R2`（28/28）
- current exam：`EX-20260712-CLUB-SC-P0-P1-R2-1`（100）
- current IR：`IR-20260712-CLUB-SC-P0-P1-R2`

## 完成

- 冻结 list/detail/join/my、`standard+general` 与详情 active guard。
- 建立合同、Schema、稳定错误、固定 seed 合成 fixtures 和 conformance。
- 建立子项目两层依赖、验收矩阵、回执、R2 current 治理证据与 IR。
- conformance 17/17 通过；`intro` 为权威 Club 文本字段，`description` 负例被拒绝。

## T0 前置勘误（2026-07-12）

- 访问合同统一为 `shared_session`；guest 由父首页承接登录，不调用 SC 业务 API。
- 详情边界资源统一 404 `CLUB_NOT_FOUND`；内部详情/加入失败分别为 500 `CLUB_DETAIL_UNAVAILABLE`/`CLUB_JOIN_UNAVAILABLE`。
- category 输入错误统一使用平台权威 `CLUB_FILTER_CATEGORY_INVALID`。
- 固定 seed 生成器与 committed fixture 已重新统一，conformance 升为 17/17。
- 独立后端复核发现共享 `/clubs/:id` 被 SC 收窄的破坏性回归；合同改用专用 `/clubs/self-created/:id` 并要求通用详情保持兼容。
- 独立前端复核发现 `Number(clubId)` 会把科学计数/十六进制/前导零重解释为其他资源；合同增加 canonical route ID 与零请求失败关闭。
- 测试包显式生成 list/applications 固定深链；动态 `:clubId` 由测试环境 SPA fallback 在 T0 真实验证。

## 未完成/禁止推断

后端与前端检查点已分别提交，等待平台独立复核和受控集成；测试环境和 UAT 未执行。创建、审核、成员管理、资金、生产与真实数据未授权。P0/P1 Go 不代表首闭环完整 Go。

## 请求

平台独立复跑 Schema、合成 conformance、内部依赖、治理、UTF-8、scope 与敏感扫描；通过后激活独立后端切片。
