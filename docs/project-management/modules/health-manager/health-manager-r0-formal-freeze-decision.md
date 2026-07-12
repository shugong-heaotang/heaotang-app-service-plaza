# 健康大管家 HM-R0 V1.0 开发规划正式冻结决定

- freeze_id：`HM-R0`
- 产品版本：`V1.0`
- 唯一冻结状态：**Accepted for development planning**
- F1 检查点状态：`candidate / awaiting independent platform review`
- 生效范围：产品宪法、MVP-90需求拆解、独立后续工作项规划
- 可执行：`false`
- 当前不授权：业务代码、共享前后端、API、数据库、环境、真实身份、真实会员/健康数据、医疗服务、收费、资金、部署、生产和 P3
- 原始候选：`codex/health-manager-v1-requirements@ce9a4c75`，HM-R0 / V1.0 Final Candidate
- 决策机器合同：`contracts/modules/health-manager/hm-r0-formal-freeze.v1.json`

## 1. 决定

HM-R0 / V1.0 Final Candidate 可以作为后续需求拆解、合同设计和独立开发任务规划的上位产品宪法。该冻结只说明产品定位、PDCAR 核心、AI+健康管理师+医生三层责任、健康计划核心对象以及安全失败关闭原则可以继续作为开发规划依据。

“Accepted for development planning”不等于专业政策全部完成，不等于真实会员服务可运行，也不等于 PR、业务实现、环境、收费或生产获批。F1 文件由模块提交后仍需平台独立复核；平台 Go 前工作项不得标为 integrated。

## 2. 分类定义与数量

- `blocks-development`：缺失证据阻止对应可执行业务切片、专业政策或共享实现启动，共 **7** 项。
- `blocks-real-data-environment`：可继续规划和合成验证，但真实身份、健康数据、人员服务、环境、发布或生产仍禁止，共 **16** 项。
- `does-not-block-synthetic`：已在窄范围 Accepted、无需成为合成证据前置，或通过 Exact revision 与合成规划分离，共 **4** 项。

状态统计：Accepted 2 项，Pending with owner 24 项，Exact revision 1 项；合计 27 项。

## 3. 27 项证据闭包

| 决定 | 当前状态 | 分类 | 主责 | 缺失证据/当前证据 | 下一检查点 |
| --- | --- | --- | --- | --- | --- |
| C4-P08 | Pending with owner | blocks-real-data-environment | 产品负责人 | 纳排表；能力限制；特殊人群转介方案 | R0-F2 专业与数据边界审计 |
| C4-H01 | Accepted | does-not-block-synthetic | 和奥堂医生集团专业负责人 | 已形成窄范围证据 | 按复审触发重新审核 |
| C4-H02 | Pending with owner | blocks-development | 医疗质量负责人 | 风险规则目录；证据等级；审核版本；复核与关闭方案 | R0-F2 风险规则审计 |
| C4-H03 | Pending with owner | blocks-development | 医生集团医疗质量负责人 | 值班模型；渠道演练；无法联系分支；责任链 | R0-F2 紧急升级责任审计 |
| C4-H04 | Pending with owner | blocks-real-data-environment | 健康管理专业负责人 | 岗位资格；课程与考核；监督抽检；升级清单；容量边界 | R0-F2 管理师准入与监督审计 |
| C4-H05 | Pending with owner | blocks-development | 老年与康复专业负责人 | 筛查规则；环境评估；训练方案；药师与辅具方案；跌倒后处置 | 独立 HM-ELDER-FALL-PREVENTION 专业 PRD |
| C4-H06 | Pending with owner | blocks-development | 对应专业负责人 | 逐类模板；禁忌；适用范围；签署；退出条件 | 每类模板独立专业工作项 |
| C4-H07 | Pending with owner | blocks-real-data-environment | 医生集团专业负责人 | P/D/C/A/R 用语逐项会签；健康概况、计划和复盘用语审查 | R0-F2 专业表述审计 |
| C4-L02 | Pending with owner | blocks-real-data-environment | 隐私与法律负责人 | 数据分类；处理清单；期限；权利响应；保留例外依据 | R0-F2 数据权利审计 |
| C4-L03 | Pending with owner | blocks-real-data-environment | 隐私与法律负责人 | 身份与监护验证；代理范围；撤回和冲突规则 | 独立特殊人群与代理授权工作项 |
| C4-L04 | Pending with owner | blocks-real-data-environment | 隐私与法律负责人 | 供应商与区域；合同；保留策略；训练开关；退出方案 | 独立 AI 数据治理工作项 |
| C4-L05 | Pending with owner | blocks-real-data-environment | 隐私与法律负责人 | DPA；责任边界；最小字段清单；审计；删除与退出证明 | 外部合作独立准入工作项 |
| C4-L06 | Pending with owner | blocks-real-data-environment | 医生集团法务与负责人 | 主体资质；服务条款；责任链；投诉机制；保险方案 | R0-F2 责任主体审计及生产前正式核验 |
| C4-S04 | Accepted | does-not-block-synthetic | 平台安全负责人 | 已形成窄范围证据 | 按复审触发重新审核 |
| C4-S05 | Pending with owner | blocks-development | AI 与平台安全负责人 | 模型选型；拦截目录；测试集；红队结果；供应商评估 | 独立 AI runtime 安全工作项 |
| C4-S07 | Pending with owner | blocks-real-data-environment | 平台安全与运维负责人 | 独立环境方案；访问控制；安全验收；备份回退演练 | 真实数据试运行前独立环境工作项 |
| C4-O01 | Pending with owner | blocks-real-data-environment | 运营负责人 | 任务工时抽样；复杂度权重；安全利用率；主备交接演练 | R0-F2 容量边界审计及运营模型工作项 |
| C4-O02 | Pending with owner | blocks-real-data-environment | 运营负责人 | 服务分层；渠道同意；消息配置；故障演练 | 运营与消息策略独立工作项 |
| C4-O03 | Pending with owner | blocks-real-data-environment | 商业负责人 | 服务包；人工成本；容量；价格试验；消费者条款 | 商业模型与收费独立工作项 |
| C4-O04 | Pending with owner | blocks-development | 运营与商业负责人 | 非医疗价值规则；无歧视评估；反作弊；现金与返佣边界 | 增长与积分独立 PRD |
| C4-O05 | Pending with owner | does-not-block-synthetic | 产品与运营负责人 | 试验设计；统计口径；主观评价；停止条件 | 商业运营指标独立评审 |
| C4-O06 | Pending with owner | blocks-real-data-environment | 运营负责人 | 试运行方案；纳排；容量；值班；同意；投诉；退出；回退演练 | 真实会员试运行前独立 Go/No-Go |
| C4-O07 | Pending with owner | blocks-real-data-environment | 采购与运营负责人 | 需求量；区域模型；主备；资质；质量；退出方案 | 外部能力池独立采购与准入工作项 |
| C4-T03 | Pending with owner | blocks-development | 平台集成负责人 | 共享业务实现精确任务书；前后端/API/DB allowed paths；接口与两层依赖门禁 | 独立共享业务实现工作项 |
| C4-T04 | Pending with owner | blocks-real-data-environment | 平台与运维负责人 | 目标架构；压测；恢复演练；容量模型 | 环境与发布准备独立工作项 |
| C4-T05 | Pending with owner | blocks-real-data-environment | 平台发布负责人 | 环境隔离；备份；回滚；验收；生产授权 | 部署与生产独立工作项 |
| C4-T06 | Exact revision | does-not-block-synthetic | 平台集成负责人 | 平台对本 F1 候选的独立复核与受控集成；PR #1/#2 的单独处置决定 | R0-F3 PR 处置、变更控制与最终 Handoff |

## 4. 已提升为 Accepted 的窄范围决定

### C4-H01

张树功于 2026-07-12 对 17 项职责边界作出 Accepted；范围严格限定为成年合成会员 HM-MVP90-M1 PDCAR 纵切，`executable=false`。不得外推到全量 C4-H06、真实身份、真实健康数据、诊断、处方、治疗、收费、环境或生产。

### C4-S04

平台安全负责人已冻结 M1 成年合成会员范围的主体、资源、动作、拒绝矩阵、审计字段和威胁模型，合同仍为 `executable=false`。C4-L02—L04、真实数据和生产身份继续 Pending。

## 5. C4-T06 Exact revision

原决定把“HM-R0 母文档冻结”和“Draft PR 合并”捆绑在同一项。现拆分为：

> HM-R0 母文档可冻结为 Accepted for development planning；Draft PR #1 与 PR #2 是否更新或合并继续由平台单独裁决，当前均保持 Draft。

原因是产品规划冻结、GitHub 合并和业务授权具有不同责任人、证据和风险，不能由一个布尔状态互相替代。该修订需在 R0-F3 由平台复核 PR 元数据与差异后收口。

## 6. 失效与复审触发

出现下列任一情况，冻结状态暂停并重新评审：产品定位或 PDCAR 核心变化；专业责任、安全底线、数据权利、人群或家庭授权变化；范围跨出开发规划或合成证据；身份、组织、资质或法律授权证据变化；AI 模型、供应商、工具、提示或自主性变化；拟使用真实身份、真实健康数据、环境、医疗服务、收费、部署或生产；任何 Accepted 证据撤回、到期或发生可信矛盾。

## 7. 变更控制

产品定位、PDCAR 核心、专业责任、安全底线、数据权利和生态边界属于母文档重大变更，必须重新建立正式工作项、current checklist、100 分考试、责任域裁决和平台独立复核。页面字段、接口、排期、运营活动、价格试验和执行细节进入 MVP-90 PRD、商业运营文件或独立实现工作项，不反向改写产品宪法。

## 8. 后续边界

F1 通过后只可进入 R0-F2 的专业边界、风险升级、管理师准入/监督/容量、数据权利/特殊人群和 15 风险底线审计。F2、F3 未获正式授权前不得提前执行；任何共享代码、API/DB、环境或真实活动仍必须另立工作项。
