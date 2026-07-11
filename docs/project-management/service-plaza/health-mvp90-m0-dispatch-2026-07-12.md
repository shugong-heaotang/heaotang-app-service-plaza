# 健康大管家 MVP-90 M0 正式派发报告

## 结论

- 平台工作项：`AIW-20260711-HEALTH-MVP90-M0-DISPATCH`
- 模块工作项：`AIW-20260711-HEALTH-MVP90-M0-CONTRACTS`
- 通知：`HM-MVP90-M0-TASK-20260712-001`
- Handoff：`SP-H032`
- 平台基线：`d67b0a9df0dc9b9132ee960704d2170b0d63b1e8` 已包含俱乐部 CA-H1 M4 Go；activation integration 为 `b45bed7e5db5b29436745344a3023a49c612db00`
- 状态：平台正式派发文件已形成，待本提交受控集成及模块工作树最终同步；模块仍未签收

## 根因与 R2 治理

首次 current checklist 与考试均完成且考试 100，但派发前审查发现预登记遗漏平台依赖文件、内部依赖 v2 和 R2 证据路径。继续使用首次考试会让治理 SHA 与最终授权范围不一致，因此保留首次快照作为历史证据，不用于最终派发。

平台补齐精确 allowed paths 后重新全文确认当前治理，形成：

- checklist：`FC-20260712-HEALTH-MVP90-M0-DISPATCH-R2`，26/26，SHA mismatch 0；
- exam：`EX-20260712-HEALTH-MVP90-M0-DISPATCH-R2-1`，score 100；
- implementation record：`IR-20260712-HEALTH-MVP90-M0-DISPATCH-R2`。

该问题是派发范围完整性缺口，不是健康产品缺陷；在业务编辑前已根因关闭，没有通过复制草稿或跳过依赖验证绕行。

## 依赖结论

- 平台 L0-L5 依赖保持 Go。
- 旧 `personal-consultation-inbox` 作为历史接口/安全证据保留，但不证明 MVP-90 M0 Go。
- `contracts/modules/health-manager/internal-dependencies.v1.json` 在原权威路径升级为 v2，分别记录 governance/development/acceptance/release/operations。
- 当前 readiness：governance=pending（等待模块激活与签收）、development=partial-go、acceptance/release/operations=pending。
- 27 项专业等决定继续 `blocked-local`，只阻塞可执行专业策略、真实业务、环境和发布，不阻塞 M0 合同结构与合成一致性。

## 范围与安全

本轮只正式派发 16 对象、6 状态机、6 角色动作、15 个合成场景及其 Schema/conformance。合成数据必须固定 seed、显式 synthetic、可重放、可销毁、无真实健康数据和凭据；允许 Faker 等批准工具，但工具和版本必须固定并记录。

禁止前端、后端、API、数据库、环境、部署、生产、真实健康数据、收费及任何专业 Pending 提前 Accepted。

## 下一步

1. 本派发提交受控集成。
2. 模块专用工作树快进至包含通知与 SP-H032 的 final integration HEAD，核验 clean。
3. 单独 activation commit 将模块工作项 `planned -> active` 并记录 exact base。
4. 健康大管家负责人执行模块 preflight、当前 checklist、考试 100、receipt 后进入 M0 首检查点。
