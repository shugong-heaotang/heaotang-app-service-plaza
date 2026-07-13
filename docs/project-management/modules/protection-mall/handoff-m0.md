# 保障商城 M0 Handoff

状态：Active / M0-CP1 待平台会签与独立验收
work_id：`AIW-20260712-PROTECTION-MALL-M0`  
base：`de31a235b9679698b9de4e33faa6ab980e0461f6`

## 已完成

- 项目最高负责人已决定商城提前启动持续开发，但不提前上线。
- 商城专用分支、独立工作树、负责人、允许路径和独立验收角色已指定。
- 服务广场预留入口五项固定值已写入任务书。
- 本地商城建议稿已纳入 M0 官方留存范围。
- 平台 preflight 通过，当前检查单逐项完成，治理考试 100 分。
- 以零写入方式盘点本地商城来源，形成来源哈希和受控迁移矩阵。
- 形成服务广场接入卡、`mall.api.v1` 契约冻结提案与机器草案。
- 未编辑商城业务代码，未修改服务广场受保护协议，未部署或触碰真实资金/会员数据。

## 当前检查点

等待平台集成负责人会签接入卡和契约提案；等待 APP 总架构独立验收 Agent 复核 M0-CP1。

## 治理证据

- 入口历史快照：`contracts/foundation/development-checklists/2026-07-12-protection-mall-m0-cp1.json` 与对应 attempt 1，均保留不可修改
- 最终 current checklist：`contracts/foundation/development-checklists/2026-07-12-protection-mall-m0-cp1-r2.json`
- 最终 current exam：`contracts/foundation/governance-exams/2026-07-12-protection-mall-m0-cp1-r2-attempt-1.json`，100 分

## 本次变更

- `docs/project-management/modules/protection-mall/README.md`
- `docs/project-management/modules/protection-mall/source-inventory-and-migration-matrix-m0-cp1.md`
- `docs/project-management/modules/protection-mall/service-plaza-access-card-m0-cp1.md`
- `docs/project-management/modules/protection-mall/mall-api-v1-freeze-proposal-m0-cp1.md`
- `contracts/modules/protection-mall/internal-dependencies.v2.json`
- `contracts/modules/protection-mall/mall-api.v1.json`

## 未迁移内容

业务代码、SQL、依赖锁文件、WP3 本地结论、`.git`、`node_modules`、`artifacts`、ZIP、凭据和非商城运维修改全部未迁移。

## 风险

- 商城模块尚未写入平台统一 module overlay；本次使用平台 core checklist，并额外全文读取任务书和商城官方方案。后续由平台受保护路径工作项决定是否登记 overlay。
- `development_readiness=partial-go`：M0 文档与契约工作可继续，但 M1 业务依赖仍为 draft。
- 支付安全、资金状态机、回调验签和对账未 Go，继续阻塞上线。

## 平台会签退回与修复

- 第一次会签结论：暂时 No-Go；v1 草案缺少 v2 依赖合同必需字段，且 `evidence:null` 会导致专用验证器失败。
- 根因：只做了 JSON 语法解析，没有运行 `validate_module_internal_dependencies.py` 专用机器合同门禁。
- 修复：删除无效 v1 草案，建立五维 readiness 的 `internal-dependencies.v2.json`；M0 三项为 required，M1/release 项为非 required 且明确阻塞关系。
- R2 checklist/exam 保持不可修改；修复完成后以 R3 current checklist/exam/IR 重新申请会签。

## 禁止事项

不得整体暂存本地商城工作区，不得覆盖或强推不同历史，不得自行修改服务广场受保护协议，不得部署、接入真实支付或处理真实会员数据。

## 下一授权

M0-CP1 独立验收与平台会签 Go 后，另立 M1 商城业务实现工作项并开放精确代码路径。
