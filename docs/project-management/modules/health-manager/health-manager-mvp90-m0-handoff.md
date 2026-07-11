# 健康大管家 MVP-90 M0 Handoff

- work_id：`AIW-20260711-HEALTH-MVP90-M0-CONTRACTS`
- notice：`HM-MVP90-M0-TASK-20260712-001`
- upstream：`SP-H032`
- branch：`codex/health-manager-mvp90-m0`
- current status：`M0 checkpoint handoff-ready`
- acceptance：`Partial Go; platform independent review pending`

## 最终 R2 治理证据

- current checklist：`FC-20260712-HEALTH-MVP90-M0-R2`，28/28，current SHA mismatch=0；
- exam：`EX-20260712-HEALTH-MVP90-M0-R2-1`，score=100，passed；
- implementation record：`IR-20260712-HEALTH-MVP90-M0-R2`，status=`verified`；
- 原检查单、考试和实施记录作为首检查点历史快照保留，不冒充最终 current 证据。

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

## 检查点 2：合成场景与完整 conformance

已完成：

- `MVP-A001`—`MVP-A015` 精确 15 个场景合同与 Schema；
- 固定 seed `HEAOTANG-HM-MVP90-M0-20260712-V1` 的确定性生成器和 15 个独立 fixture；
- fixture file SHA-256 `acb8609734f51d0e729f4e07b8f01d08931c7b4513183f5e501423429f74b177`；
- canonical replay SHA-256 `5b4d28b987a213432764ef0af8bc3ff51ee25fa2037e2ead25adf9eba142e95a`；
- 5 组 Draft 2020-12 Schema、12 项 conformance/负例、敏感模式、固定 seed 重放通过；
- 内部依赖 readiness：governance=go、development=go、acceptance=partial-go、release/operations=pending。

## 当前未完成

- 平台独立复核、M0 Go/No-Go 与受控集成；
- HM-R0 专业会签和 27 项 Pending 决策；
- M1 及以后任何业务实现、环境与发布。

## 保持 No-Go

M1、前后端、API、数据库、环境、部署、生产、真实健康数据、收费、真实会员试运行、专业规则和 27 项 Pending 均未授权。平台即使判定 M0 Go，也只允许另行派发下一切片。
