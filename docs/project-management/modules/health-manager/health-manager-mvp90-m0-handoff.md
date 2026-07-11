# 健康大管家 MVP-90 M0 Handoff

- work_id：`AIW-20260711-HEALTH-MVP90-M0-CONTRACTS`
- notice：`HM-MVP90-M0-TASK-20260712-001`
- upstream：`SP-H032`
- branch：`codex/health-manager-mvp90-m0`
- current status：`M0 checkpoint in progress`
- acceptance：`No-Go until synthetic scenarios and full conformance complete`

## 检查点 1：治理与三组核心合同

已完成：

- preflight ready；
- current checklist `FC-20260712-HEALTH-MVP90-M0` 28/28；
- exam `EX-20260712-HEALTH-MVP90-M0-1` score=100；
- receipt、requirements 与模块 README 当前入口；
- 16 个对象和 27 项不可执行 Pending 的 JSON/Schema；
- 6 组状态机及明确允许/禁止迁移的 JSON/Schema；
- 6 类角色动作、服务端授权前置和最终 scope Pending 的 JSON/Schema。

已验证：三组实例通过 Draft 2020-12 Schema；检查单与考试 validator 通过。

## 仍未完成

- `MVP-A001`—`MVP-A015` 合成场景合同与固定 seed fixtures；
- 完整 Python conformance、正反例、重放 SHA、敏感模式扫描；
- conformance report、最终 IR、内部依赖与 M0 平台验收申请。

## 保持 No-Go

M1、前后端、API、数据库、环境、部署、生产、真实健康数据、收费、真实会员试运行、专业规则和 27 项 Pending 均未授权。
