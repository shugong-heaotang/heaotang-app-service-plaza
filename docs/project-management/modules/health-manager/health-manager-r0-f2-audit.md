# 健康大管家 HM-R0 F2 专业与责任边界审计

- 工作项：`AIW-20260713-HEALTH-R0-F2-AUDIT`
- 检查点：`F2-FRESH-01 closeout`
- 权威激活 HEAD：`e947d70498fbd9e1731d83d71c2aa64645c98a29`
- 审计性质：F1 权威状态新鲜度局部收口
- 当前结论：`F2-FRESH-01 implemented / awaiting independent platform review`
- 可执行：`false`

## 1. 任务理解

F2 只形成专业与责任边界的审计结论和缺口，不实现业务。没有相应 owner 的新书面证据时，任何 `Pending with owner` 不得提升；已 Accepted 的 C4-H01 与 C4-S04 只能维持各自窄范围且继续 `executable=false`；C4-T06 保持 Exact revision，等待 F3 单独处理 PR 处置与最终 Handoff。

## 2. F2-0 入口证据

- 工作项、分支、工作树、远端与 HEAD 已核对一致，工作树在生成本轮治理证据前 clean。
- 平台依赖可用，模块内部依赖 `readiness.development=go`；release/operations 仍 pending。
- current checklist：28/28，哈希与当前治理输入一致。
- 随机治理考试：attempt 1，score 100，status passed。
- F2-0 门禁：checklist/exam/IR/collaboration、总合同、UTF-8 1243、diff、scope、secret 和控制字符扫描全部通过。
- F1 权威事实：source `384436c7`、受控合并 `fb1b8820`、最终验收 `034e46be`。

## 3. 新鲜度发现

### F2-FRESH-01：已关闭本地新鲜度缺陷，等待平台独立复核

`hm-r0-formal-freeze.v1.json`、Schema 和人类可读决定已同步为 `F1-accepted-integrated-for-development-planning`，并精确引用 F1 source `384436c7...`、source merge `fb1b8820...`、acceptance evidence `1af9032e...`、authoritative integration `034e46be...` 以及平台验收报告。该修订没有改变 27 项专业状态、分类、owner 或 `executable=false`，也不授权任何真实活动。

Schema 正例通过；候选状态回退、缺少 F1 证据、Pending 擅升、分类漂移、executable、production identity、auto-merge、P3、F3 提前收口及 C4-T06 重新加入 F1 缺失证据共 10 类负例全部拒绝。

## 4. 27 项现有证据索引

| 决定 | 状态 | 分类 | 主责 | 证据数 | 新鲜度 | 缺失证据 | 下一检查点 |
| --- | --- | --- | --- | ---: | --- | --- | --- |
| C4-P08 | Pending with owner | blocks-real-data-environment | 产品负责人 | 2 | pending-no-new-owner-evidence | 纳排表；能力限制；特殊人群转介方案 | R0-F2 专业与数据边界审计 |
| C4-H01 | Accepted | does-not-block-synthetic | 和奥堂医生集团专业负责人 | 4 | accepted-scope-evidence-present | none | review-trigger driven |
| C4-H02 | Pending with owner | blocks-development | 医疗质量负责人 | 2 | pending-no-new-owner-evidence | 风险规则目录；证据等级；审核版本；复核与关闭方案 | R0-F2 风险规则审计 |
| C4-H03 | Pending with owner | blocks-development | 医生集团医疗质量负责人 | 2 | pending-no-new-owner-evidence | 值班模型；渠道演练；无法联系分支；责任链 | R0-F2 紧急升级责任审计 |
| C4-H04 | Pending with owner | blocks-real-data-environment | 健康管理专业负责人 | 2 | pending-no-new-owner-evidence | 岗位资格；课程与考核；监督抽检；升级清单；容量边界 | R0-F2 管理师准入与监督审计 |
| C4-H05 | Pending with owner | blocks-development | 老年与康复专业负责人 | 2 | pending-no-new-owner-evidence | 筛查规则；环境评估；训练方案；药师与辅具方案；跌倒后处置 | 独立 HM-ELDER-FALL-PREVENTION 专业 PRD |
| C4-H06 | Pending with owner | blocks-development | 对应专业负责人 | 2 | pending-no-new-owner-evidence | 逐类模板；禁忌；适用范围；签署；退出条件 | 每类模板独立专业工作项 |
| C4-H07 | Pending with owner | blocks-real-data-environment | 医生集团专业负责人 | 2 | pending-no-new-owner-evidence | P/D/C/A/R 用语逐项会签；健康概况、计划和复盘用语审查 | R0-F2 专业表述审计 |
| C4-L02 | Pending with owner | blocks-real-data-environment | 隐私与法律负责人 | 2 | pending-no-new-owner-evidence | 数据分类；处理清单；期限；权利响应；保留例外依据 | R0-F2 数据权利审计 |
| C4-L03 | Pending with owner | blocks-real-data-environment | 隐私与法律负责人 | 2 | pending-no-new-owner-evidence | 身份与监护验证；代理范围；撤回和冲突规则 | 独立特殊人群与代理授权工作项 |
| C4-L04 | Pending with owner | blocks-real-data-environment | 隐私与法律负责人 | 2 | pending-no-new-owner-evidence | 供应商与区域；合同；保留策略；训练开关；退出方案 | 独立 AI 数据治理工作项 |
| C4-L05 | Pending with owner | blocks-real-data-environment | 隐私与法律负责人 | 2 | pending-no-new-owner-evidence | DPA；责任边界；最小字段清单；审计；删除与退出证明 | 外部合作独立准入工作项 |
| C4-L06 | Pending with owner | blocks-real-data-environment | 医生集团法务与负责人 | 2 | pending-no-new-owner-evidence | 主体资质；服务条款；责任链；投诉机制；保险方案 | R0-F2 责任主体审计及生产前正式核验 |
| C4-S04 | Accepted | does-not-block-synthetic | 平台安全负责人 | 4 | accepted-scope-evidence-present | none | review-trigger driven |
| C4-S05 | Pending with owner | blocks-development | AI 与平台安全负责人 | 2 | pending-no-new-owner-evidence | 模型选型；拦截目录；测试集；红队结果；供应商评估 | 独立 AI runtime 安全工作项 |
| C4-S07 | Pending with owner | blocks-real-data-environment | 平台安全与运维负责人 | 2 | pending-no-new-owner-evidence | 独立环境方案；访问控制；安全验收；备份回退演练 | 真实数据试运行前独立环境工作项 |
| C4-O01 | Pending with owner | blocks-real-data-environment | 运营负责人 | 2 | pending-no-new-owner-evidence | 任务工时抽样；复杂度权重；安全利用率；主备交接演练 | R0-F2 容量边界审计及运营模型工作项 |
| C4-O02 | Pending with owner | blocks-real-data-environment | 运营负责人 | 2 | pending-no-new-owner-evidence | 服务分层；渠道同意；消息配置；故障演练 | 运营与消息策略独立工作项 |
| C4-O03 | Pending with owner | blocks-real-data-environment | 商业负责人 | 2 | pending-no-new-owner-evidence | 服务包；人工成本；容量；价格试验；消费者条款 | 商业模型与收费独立工作项 |
| C4-O04 | Pending with owner | blocks-development | 运营与商业负责人 | 2 | pending-no-new-owner-evidence | 非医疗价值规则；无歧视评估；反作弊；现金与返佣边界 | 增长与积分独立 PRD |
| C4-O05 | Pending with owner | does-not-block-synthetic | 产品与运营负责人 | 2 | pending-no-new-owner-evidence | 试验设计；统计口径；主观评价；停止条件 | 商业运营指标独立评审 |
| C4-O06 | Pending with owner | blocks-real-data-environment | 运营负责人 | 2 | pending-no-new-owner-evidence | 试运行方案；纳排；容量；值班；同意；投诉；退出；回退演练 | 真实会员试运行前独立 Go/No-Go |
| C4-O07 | Pending with owner | blocks-real-data-environment | 采购与运营负责人 | 2 | pending-no-new-owner-evidence | 需求量；区域模型；主备；资质；质量；退出方案 | 外部能力池独立采购与准入工作项 |
| C4-T03 | Pending with owner | blocks-development | 平台集成负责人 | 2 | pending-no-new-owner-evidence | 共享业务实现精确任务书；前后端/API/DB allowed paths；接口与两层依赖门禁 | 独立共享业务实现工作项 |
| C4-T04 | Pending with owner | blocks-real-data-environment | 平台与运维负责人 | 2 | pending-no-new-owner-evidence | 目标架构；压测；恢复演练；容量模型 | 环境与发布准备独立工作项 |
| C4-T05 | Pending with owner | blocks-real-data-environment | 平台发布负责人 | 2 | pending-no-new-owner-evidence | 环境隔离；备份；回滚；验收；生产授权 | 部署与生产独立工作项 |
| C4-T06 | Exact revision | does-not-block-synthetic | 平台集成负责人 | 7 | exact-revision-open-pr-only | PR #1/#2 的单独处置决定 | R0-F3 PR 处置、变更控制与最终 Handoff |

## 5. F2-0 不作出的结论

- 不把任何 Pending 提升为 Accepted。
- 不扩大 C4-H01、C4-S04 或 M1 窄模板的签署范围。
- 不改变 C4-T06 的 PR 分离要求。
- 不授权 F3/P3、业务代码、共享前后端、API/DB、真实身份、真实会员/健康数据、医疗服务、收费、资金、环境、部署或生产。

## 6. 下一检查点

本短检查点提交后停止编辑，等待平台对 F2-FRESH-01 的独立复核。完整 F2-1 六类矩阵、F3/P3 和任何业务或真实活动仍需另行授权。
