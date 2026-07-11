# 生命导航项目入口

项目 ID：`life-navigation`
父项目：和奥堂 APP 服务广场
板块负责人：生命导航二负责人
平台集成负责人：服务广场平台集成负责人
当前切片：`LN-S2-DIMENSION-GUIDED-APPLICATION`（P0/P1 Base Contract）

## 目标

在已完成的申请与本人历史闭环上，建立版本化维度注册表、窄目录和服务端权威 selector 的 P0/P1 依赖标准。项目负责人完成 P0 裁决前，标准只允许不可执行的 Base Contract。

## 权威输入

按平台 README 第 0 节完成核心课程，再读取：

1. `docs/project-management/notices/2026-07-12-life-ln-s2-task-order.md`
2. `docs/project-management/modules/life-navigation/LN-S2-requirements.md`
3. `docs/project-management/modules/life-navigation/LN-S2-decisions.md`
4. `contracts/foundation/module-dependencies/life-navigation.v1.json`
5. `contracts/modules/life-navigation/internal-dependencies.v1.json`

开始编码前必须完成带 `ModuleId=life-navigation` 的起飞检查单和随机治理考试，成绩必须为 100。

## 边界

本切片只做 P0 需求事实、P1 JSON/Schema、固定 seed 合成 fixtures 和 conformance。不得实现前端、后端、API、数据库、环境或部署；不得提供题库、评分、预测、八字、AI 建议、专业结论、价格、交易或下游服务。公共服务广场契约和基础设施路径属于平台受保护范围。

## 当前门禁

- governance：Go（当前检查单 31/31，治理考试 100）
- development：Partial Go（P0/P1 Base Contract；Executable No-Go）
- acceptance / release / operations：Pending
- P0：`decision_status=pending`、`registry_frozen=false`、`executable=false`
- 旧 `yun`：`mapping_target=null`
- 签收回执：`LN-S2-receipt.md`
- 阶段 Handoff：`LN-S2-handoff.md`
- 接口变更申请：`interface-change-request-template.md`
