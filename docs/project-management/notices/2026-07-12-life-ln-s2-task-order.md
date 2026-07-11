# 生命导航 LN-S2 维度引导申请 P0/P1 任务通知书

- notice_id：`LN-S2-TASK-20260712-001`
- platform_work_id：`AIW-20260712-LIFE-LN-S2-DISPATCH`
- module_work_id：`AIW-20260712-LIFE-LN-S2-P0-P1`
- Handoff：`SP-H033`
- 下达日期：2026-07-12
- 下达方：平台集成负责人
- 接收方：生命导航二负责人
- 状态：正式下达；模块在本派发受控集成并同步 final base 后激活

## 1. 目标

生命导航第二切片 `LN-S2-DIMENSION-GUIDED-APPLICATION` 首轮只完成 P0 需求事实和 P1 机器合同：建立版本化维度注册表、窄目录、申请维度 selector、稳定错误目录、合成 fixtures 与 conformance。

当前申请提交把 `dimension_id` 固定为 `yun`，后端只校验非空和长度。LN-S2 必须把维度选择升级为服务端权威、版本化、失败关闭的标准依赖；前端下拉或本地筛选不能替代服务端权威。

## 2. 现有事实与不可误用证据

- 已完成的 application-history M0-M4 只证明身份、幂等、本人历史和跨用户隔离，不证明 LN-S2 Go。
- 现有 `GET /api/v1/life-nav/dimensions` 记为 `code-present-unverified`：响应包含 BaseScore、questions、actions、routes 等超出窄目录的实现字段，配置缺失/空/非法时会回退代码默认目录。
- P0/P1 不授权修改现有后端，也不得把现有接口或默认目录冒充新标准已完成。

## 3. P0 决策包

必须形成并提交项目负责人裁决：

1. 稳定 dimension ID、label、sort_order、active、version、authority；
2. 旧 `yun` 的兼容、迁移或只读历史策略；
3. 配置缺失、读取错误、空目录和非法数据的失败关闭策略；
4. 旧记录未知维度的显示策略；
5. 角色、主动作、非目标和可证伪前提。

项目负责人裁决前必须保持：`decision_status=pending`、`registry_frozen=false`、`executable=false`、旧 `yun mapping_target=null`。Pending 可以进入决策记录和合同 metadata，但不能进入可执行 selector。

## 4. P1 合同成果

- dimension registry JSON + Schema；
- GET dimensions 窄响应合同 JSON + Schema；
- application dimension selector JSON + Schema；
- 稳定 error catalog JSON + Schema；
- 正常、空白、未知、停用、重复 ID/order、版本不兼容和旧 `yun` 待裁决 fixtures；
- Python 标准库 conformance；
- internal-dependencies v2、requirements、decisions、receipt、report、IR 与 Handoff。

目录只允许批准字段，不得泄漏 BaseScore、questions、actions、routes、评分、预测、八字、AI 建议、专业结论或下游服务实现。

## 5. 工作区与允许路径

- repository：`C:/Users/shugo/Documents/APP系统`
- branch：`codex/life-navigation-ln-s2-p0-p1`
- worktree：`C:/Users/shugo/Documents/worktrees/heaotang-life-ln-s2-p0-p1`
- 最终 base：包含本通知、平台 checklist/exam/IR 和 SP-H033 的权威 integration HEAD
- owner：生命导航二负责人

允许修改路径以 `contracts/foundation/agent-collaboration.v1.json` 中 `AIW-20260712-LIFE-LN-S2-P0-P1` 为唯一机器真相源。平台派发工作项不拥有模块 `internal-dependencies.v1.json`，避免并发双真相源。

禁止 APP 前端代码、后端仓库、API 实现、数据库、测试环境、部署和生产路径。

## 6. 合成数据标准

- 固定 seed：`HEAOTANG-LN-S2-20260712-V1`；正式模块首次读取草稿时重新计算 SHA 并登记。
- 草稿合成包当前 SHA-256：`82dfd8a2c511895eb819a1c7911433c42f237efef1bb218b160fc2eab1d8af08`，仅作输入校验，不自动成为权威证据。
- fixtures 必须显式 synthetic、生成器/version/seed、销毁策略和非生产标识。
- 可以使用 Faker 或批准的确定性工具；必须固定版本与 seed，重复生成哈希一致。
- 禁止真实姓名、手机号、身份证、申请正文、OTP、JWT、cookie 或真实用户历史。

## 7. 递归门禁

1. 模块工作树同步 final integration HEAD，HEAD/merge-base 一致且 clean。
2. preflight ready。
3. 生成并逐项完成 `FC-20260712-LIFE-LN-S2-P0-P1`，模块 overlay 全文读取。
4. 随机治理考试 score=100；失败试卷不可修改。
5. receipt 明确接受 P0/P1、禁止范围和 Pending 边界。
6. 先提交需求事实/决策包，再提交合同/Schema/fixtures/conformance；每个短检查点更新 IR/Handoff。

## 8. P0/P1 验收

- 窄目录无超范围字段；唯一 ID/order 和引用完整性通过。
- 空白、未知、停用、重复、版本不兼容、配置缺失/读取失败全部稳定失败关闭。
- 旧 `yun` 在裁决前没有 executable mapping。
- 申请与历史只保存稳定 ID/version 引用；未知历史维度不伪造 label。
- 权限、幂等、本人归属和跨用户隔离继续继承，不得因 selector 放宽。
- Schema 正反例、conformance、固定 seed 重放、UTF-8、范围和敏感扫描通过。

## 9. 明确禁止

- 不授权 executable selector、前后端编码、API/数据库变更、环境、部署、生产或真实用户数据。
- 不授权评分、预测、八字、AI 建议、专业结论、价格、交易或下游服务。
- 不得通过代码默认目录、前端本地筛选、复制旧 `yun`、跳过 Schema 或降低失败关闭换取表面通过。
- P0/P1 Go 也不自动授权后端、前端或 M2；后续必须独立工作项。

## 10. Handoff

模块提交 exact commit、changed paths、current checklist、exam100、receipt、P0 决策状态、合同/Schema/conformance 命令与结果、合成 seed/hash、未决风险和下一授权。平台独立复核后只裁定 P0/P1；未获得项目负责人 P0 Accepted 时，最终 verdict 只能是 Base Contract Go / Executable No-Go。
