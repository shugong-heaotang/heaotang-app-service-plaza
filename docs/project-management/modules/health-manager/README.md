# 健康大管家项目入口

项目 ID：`health-manager`

父项目：和奥堂 APP 服务广场

板块负责人：健康大管家负责人

平台集成负责人：服务广场平台集成负责人

当前产品阶段：R1—R5 离线、合成合同及其独立验收已受控集成

证据模式：`synthetic_only=true`、`executable=false`

健康 active 工作项：以 `contracts/foundation/agent-collaboration.v1.json` 中当前 `status=active` 的健康工作项实时判定；本页不固定数量。

## 当前结论

R1—R5 的实现项和独立验收项共 10 个，已在平台注册表中收口为 `integrated`：

| 阶段 | 已受控集成的离线/合成范围 | 运行时结论 |
|---|---|---|
| R1 | 大益健康馆首页 IA、责任边界、跨模块协议、关键状态与验收负例 | `executable=false` |
| R2 | 本人自助/健康馆协助双渠道统一档案、来源、确认、纠错、授权与审计 | `executable=false` |
| R3 | 学习/俱乐部最小摘要、跳转权威模块、会员确认回传及越权负例 | `executable=false` |
| R4 | 医生资质/执业/专科硬门禁、质量治理、解释、人工复核与退出 | `executable=false` |
| R5 | 咨询、第二意见、专家征集、MDT、合规医疗机构承接与全程留痕 | `executable=false` |

`integrated` 只证明版本化合同、Schema、合成 fixtures、正负测试和平台独立验收已进入权威集成分支；它不等于真实医疗、真实数据、运行时、部署或生产 Go。

## 权威状态与防漂移

- 工作项、owner、base、branch、worktree、allowed paths、状态和 evidence commit 的权威来源：`contracts/foundation/agent-collaboration.v1.json`。
- 本页只陈述 R1—R5 已受控集成的稳定事实，不把任一历史切片继续声明为“唯一 active”。
- 当前入口新鲜度收口工作项为 `AIW-20260717-HEALTH-README-CURRENT-STATE-CLOSEOUT`；其生命周期状态仍以注册表为准。
- 机器断言：`contracts/modules/health-manager/conformance/test_health_manager_readme_current_state.py`，用于拒绝 README/注册表漂移和授权边界升级。

## 启动后的必读输入

除平台 README 第 0 节课程外，还必须完整阅读：

1. 当前注册表中的健康工作项和对应任务书、current checklist、governance exam、implementation record、Handoff；
2. `contracts/foundation/module-dependencies/health-manager.v1.json`；
3. `contracts/modules/health-manager/internal-dependencies.v1.json`；
4. `health-cross-module-requirements/健康大管家-大益健康馆-学习广场-健康俱乐部需求补充-v1.0.md` 的受控只读输入；
5. R1—R5 对应合同、Schema、conformance 与独立验收证据。

新任务必须创建独立工作项、`codex/` 分支和工作树，并以 `ModuleId=health-manager` 完成当期起飞检查单和 100 分随机治理考试。历史 checklist/exam 只证明历史检查点，不能授权新任务。

## 责任边界

- 健康大管家拥有健康档案、授权、健康计划及经确认的健康管理记录。
- 学习广场拥有学习资源、路径与进度；俱乐部联盟拥有俱乐部成员、活动和内容治理。
- 医生集团治理/平台目录拥有医生资质与专业标签；合规医疗机构拥有正式诊疗和电子病历。
- 跨模块首期只允许“展示最小摘要 + 跳转权威模块 + 会员确认回传”，禁止共享数据库表或跨模块直接写库。
- AI 只可整理资料、识别缺失、提示风险、形成候选匹配和解释；不得诊断、开药、改药、冒充医生、承诺疗效或独立关闭专业/紧急风险。

## 当前门禁

- R1—R5 离线/合成合同：`integrated`。
- R1—R5 独立验收：`integrated`。
- 真实身份、真实会员和真实健康数据：No-Go。
- 互联网诊疗、诊断、处方、改药和医疗责任执行：No-Go。
- 真实收费、支付和商业排序：No-Go。
- 前后端、共享运行时、API、数据库、测试服部署和生产：No-Go。
- 不可逆操作：No-Go。

上述 Pending/No-Go 不阻止离线合同、合成 fixtures、负例、文档一致性、防漂移测试和独立验收继续推进；任何运行时、真实数据、医疗、收费、部署或生产工作必须另立工作项并取得明确授权。
