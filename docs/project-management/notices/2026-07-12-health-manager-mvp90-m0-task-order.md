# 健康大管家 MVP-90 M0 合同与合成一致性任务通知书

- notice_id：`HM-MVP90-M0-TASK-20260712-001`
- platform_work_id：`AIW-20260711-HEALTH-MVP90-M0-DISPATCH`
- module_work_id：`AIW-20260711-HEALTH-MVP90-M0-CONTRACTS`
- Handoff：`SP-H032`
- 下达日期：2026-07-12
- 下达方：平台集成负责人
- 接收方：健康大管家负责人
- 状态：正式下达；模块工作项在平台派发受控集成并同步干净工作树后激活

## 1. 目标

把 MVP-90 PRD C5 中已经形成的 16 个产品语义对象、6 组状态机、6 类角色动作和 `MVP-A001` 至 `MVP-A015` 转换为版本化机器合同、JSON Schema、合成 fixtures 与 Python 标准库 conformance。

M0 只证明合同结构与合成一致性，不证明专业会签、真实业务实现、测试环境或发布可用。

## 2. 权威输入

- PRD 分支：`codex/health-manager-mvp90-prd`
- PRD exact commit：`fdf080f7ab03b2bdba87b77a7b3fd33dbcc8f73c`
- PRD SHA-256：`701ee042f88a156a2c393e7b64bbbea7a4b54c0e94a81be8ea83d8cb05c1e147`
- PRD Handoff SHA-256：`5e9cb98be773c79390136ae80fb60d8617f4a12fefaafdb8dca8ab3f936771f5`
- 平台依赖：`contracts/foundation/module-dependencies/health-manager.v1.json`
- 内部依赖：`contracts/modules/health-manager/internal-dependencies.v1.json`，本轮在原权威路径升级为 `module-internal-dependencies.v2`

PRD C5 状态是 `Document Handoff Ready`，不是 `HM-R0 Professional Freeze`。27 项专业、隐私、容量、时限、商业及试运行决定继续为 `Pending with owner`。

## 3. 唯一工作区与允许路径

- repository：`C:/Users/shugo/Documents/APP系统`
- branch：`codex/health-manager-mvp90-m0`
- worktree：`C:/Users/shugo/Documents/worktrees/heaotang-health-mvp90-m0`
- 最终 base：包含本通知、平台 R2 检查单、100 分考试、IR 和 SP-H032 的权威 integration HEAD
- owner：健康大管家负责人

允许修改路径以 `contracts/foundation/agent-collaboration.v1.json` 中 `AIW-20260711-HEALTH-MVP90-M0-CONTRACTS` 为唯一机器真相源，范围仅包括：M0 requirements、receipt、Handoff、conformance report；内部依赖 v2；object model、state machines、role actions、synthetic scenarios 的 JSON/Schema；fixtures 窄目录、Python conformance；2026-07-12 当前 checklist、考试与 IR。

禁止前端、后端、API、数据库、环境、部署、生产及真实健康数据路径。

## 4. 合同边界

1. 16 个对象必须有稳定 ID、最低语义、owner、version 和 forbidden fields。
2. 6 组状态机必须声明允许与禁止迁移、稳定错误 ID，并拒绝未登记迁移。
3. 6 类角色动作只描述产品责任和服务端授权前置，不提前发明最终 scope 名称。
4. 27 项 Pending 只允许进入不可执行 metadata；不得生成 executable policy。
5. 所有可变价格、容量、比例、有效期、时限只引用版本化策略或配置，不写死数值。
6. 医疗 AI 不得诊断、处方、替代急救或形成疗效承诺。

## 5. 合成数据标准

- 精确 15 个场景，覆盖 `MVP-A001` 至 `MVP-A015`，不得缺失、重复或新增冒充已确认场景。
- 每个 fixture 必须显式 `synthetic=true`、固定 seed/version、生成器版本、销毁策略和非生产标识。
- 可以使用 Faker 或仓库批准的确定性生成工具，但必须固定 seed；工具不可用时使用同等确定性的标准库生成器。
- 禁止复制、改写或推断真实会员、真实病历、手机号、身份证、OTP、JWT、cookie 或其他凭据。
- 生成后必须通过敏感模式扫描、重复运行哈希一致性和 Schema 正反例。
- 仓库外草稿只作审查输入，必须 `review-transform`，不得整目录盲拷贝为权威合同。

## 6. 递归门禁

1. 模块工作树同步最终 base，HEAD/merge-base 一致且 clean。
2. `Test-AgentDevelopmentPreflight.ps1` 为 ready。
3. 新建 `FC-20260712-HEALTH-MVP90-M0`，逐项全文读取并完成当前 SHA。
4. 随机治理考试 8/8，score=100；失败试卷保持不可变。
5. 先提交 requirements 与机器合同，再完成 Schema/fixtures/conformance。
6. 每个短检查点更新 receipt、IR 和 Handoff，提交、推送后由平台独立复核。

## 7. 首检查点验收

- object model：16/16；state machines：6/6；roles：6/6；synthetic scenarios：15/15。
- required 字段、唯一 ID、引用完整性和 forbidden fields 全部通过。
- Pending 不可执行、未知状态迁移失败关闭、角色禁止动作和敏感字段负例通过。
- 同一固定 seed 重放内容与 SHA 一致。
- v2 内部依赖、JSON Schema、conformance、UTF-8、Git diff、范围和敏感扫描通过。

## 8. 明确禁止

- 不授权 M1 业务纵切、前端、后端、接口、Schema 以外的数据库结构、测试环境、部署或生产。
- 不授权真实健康数据、真实会员、收费、资金、AI 诊断、处方或专业政策。
- 不得把 C5、技术评审或本通知误写为专业会签完成。
- 不得以模拟状态、跳过测试、放宽 Schema、复制旧咨询切片 Go 或本地筛选换取表面通过。

## 9. Handoff 条件

模块提交 exact commit、changed paths、current checklist、exam100、IR、合同/Schema/conformance 命令与结果、合成数据 seed/hash、未决风险和下一授权。平台只在独立复核后裁定 M0 Go；M0 Go 也不自动授权 M1。
