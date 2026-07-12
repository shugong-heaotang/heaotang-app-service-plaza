# 活动板块 V3.0 M0 正式任务单

签发日期：2026-07-13（Asia/Shanghai）  
签发角色：项目最高负责人  
来源任务：`019f5872-0f07-7c63-b465-aa05973a5f46`

## 一、授权结论

**批准启动，但本次仅批准 M0 治理与设计检查点。**

本授权允许需求合同化、架构与接口设计、数据模型、确定性 fixtures/mock、自动化合同测试和测试环境准备材料；M0 不得修改业务代码。

本授权不是测试服部署授权，也不是生产上线授权。不得触达真实会员，不得发送真实验证码或外部消息，不得发起真实支付，不得修改生产数据或生产配置。

M1 仅列入计划，必须在 M0 独立验收为 Go 后另行激活。测试服部署和生产上线继续使用各自独立门禁及授权。

## 二、唯一工作身份

- `work_id`: `AIW-20260713-ACTIVITY-V3-M0`
- `record_id`: `IR-20260713-ACTIVITY-V3-M0`
- 模块：`activity`
- 持续负责人：活动板块 V3.0 连续开发任务
- 平台集成负责人：负责登记、路径冲突复核、分支/worktree 建立和合入裁决
- 独立验收负责人：由平台集成负责人指定，且不得与实施负责人为同一主体
- 状态：`approved_pending_activation`

只有平台集成负责人将本工作项登记到权威协作注册表、完成路径冲突复核并创建独立 worktree 后，状态才可改为 `active`。

## 三、权威根、仓库与基线

- 权威治理根：`C:\Users\shugo\Documents\APP系统`
- 目标仓库：`C:\Users\shugo\Documents\APP系统`
- 集成工作树：`C:\Users\shugo\Documents\worktrees\heaotang-app-integration`
- 建议分支：`codex/activity-v3-m0`
- 建议独立 worktree：`C:\Users\shugo\Documents\worktrees\heaotang-activity-v3-m0`
- 核验时基线提交：`485601ce10ad4d3ac7d9db655465754ad5ac0032`

平台集成分支仍在持续变化。创建 worktree 前必须重新读取集成 HEAD；若 HEAD 已变化，以创建时重新核验且记录的提交为正式 `base_commit`，不得静默沿用旧值。

## 四、唯一需求基线

- 来源：`C:\Users\shugo\Documents\活动\和奥堂APP活动板块统一需求说明书-V3.0.md`
- SHA-256：`838C54AE895D223E66FCA8BE8BB54D588DC3F83234B430B91073B8454E2975E6`
- 状态：已确认开发基线

M0 必须在仓库内建立不可变的需求快照或带哈希的需求合同与追踪矩阵。仓库外文件不得作为无法复核、可能漂移的唯一执行依据。来源文件哈希变化时必须停止并重新确认基线。

## 五、M0 路径边界

实施负责人允许新增或修改：

- `contracts/modules/activity/**`（含本模块 dependency、checklist、governance exam、implementation record）
- `docs/project-management/modules/activity/**`

仅平台集成负责人可修改：

- `contracts/foundation/agent-collaboration.v1.json`
- `contracts/foundation/module-dependencies/activity.v1.json`
- `docs/project-management/notices/2026-07-13-activity-v3-m0-task-order.md`

激活校验修订：权威 registry 将整个 `contracts/foundation/**` 定义为平台保护路径，因此模块 dependency、checklist、考试和实施记录采用 `contracts/modules/activity/**`；平台级 dependency 文件由平台集成负责人另行维护。此修订收紧权限，不扩大 M0 范围。

M0 保护路径：

- `app/src/**`
- 所有后端业务实现目录
- 部署脚本、服务器配置、密钥及生产配置
- Club Alliance、Mall/Order/Payment、NOVA、Member/Relationship、Message、Auth/Privacy 既有模块实现
- 其他工作项的 checklist、考试、实施记录和 Handoff

若仓库实际路径结构与本单不一致，平台集成负责人必须在激活前提交精确修订，不得自行扩大 allowed paths。

## 六、依赖与接口所有权

| 依赖域 | 本检查点需要固定的边界 | 接口裁决方 |
|---|---|---|
| Club Alliance | 主办俱乐部、会员身份、角色、提案与审批权限 | Club Alliance 接口所有者 |
| Mall / Order / Payment | 商品引用、订单归因、库存价格、付款确认、退款与分账；M0 不执行交易 | 商城/订单/支付接口所有者 |
| NOVA | 草稿、推荐、解释和审计；禁止 AI 自动发布、邀请、联系或交易 | NOVA 接口所有者 |
| Member / Relationship | 会员等级来源、关系与联系授权、隐私最小化 | 会员/关系接口所有者 |
| Message | 订阅、退订、频率限制和发送审计；M0 不真实发送 | 消息接口所有者 |
| Auth / Privacy | 登录态、scope、资源归属、同意、留存与删除边界 | 鉴权/隐私接口所有者 |

每个接口必须记录 owner、版本、请求/响应 schema、错误语义、权限规则、fixture 来源和 readiness；未经接口所有者确认的内容标记为 `provisional`。

## 七、M0 最小交付物

1. 活动模块 README、版本入口和需求基线哈希。
2. V3.0 需求合同及逐条追踪矩阵，覆盖需求书中的验收条目和负面场景。
3. 模块依赖声明、接口所有者矩阵及 readiness。
4. 领域模型、数据边界、API schema、错误语义和确定性 fixtures。
5. 权限、隐私、AI 行为、消息、交易的禁止边界与安全测试矩阵。
6. 当前任务理解回执、current checklist 和满分 100 分治理考试。
7. M0 实施记录、证据索引和 Handoff。

M0 不得包含业务功能代码，也不得用截图或口头说明替代可执行合同验证。

## 八、M0 Go / No-Go

只有同时满足以下条件，独立验收负责人才能给出 Go：

- 工作项已登记且没有活动路径重叠；分支、worktree、正式 base commit 可追溯。
- 需求快照/合同与上述 SHA-256 一致。
- 所有治理必读项已逐项确认，checklist 当前有效，治理考试 100/100。
- schema、fixtures、合同校验和负面权限用例通过。
- 依赖 owner 已确认，或明确标为 `provisional` 且相应能力不进入 M1 真实闭环。
- 需求书中的待决产品规则已关闭，或被显式隔离为不会影响拟进入 M1 的范围。
- 无业务代码、无部署、无真实外部动作、无生产变更。
- 独立验收人与实施负责人分离，Handoff 证据完整。

任一条件不满足即为 No-Go；不得以“后续补证”标记完成。

## 九、M1 预告（未授权）

建议下一检查点为“俱乐部主办/会员提案 + 活动发现与报名”的最小真实闭环。为降低跨域风险，首个 M1 默认采用免费报名、无真实支付、无主动外部消息版本。

进入 M1 前至少必须固定：会员提案权、俱乐部审批规则、公开可见性/平台审核规则、鉴权和隐私规则、AI 同意及留存规则、各 API 所有者。若交易规则仍未裁决，支付只能保持明确标注的 mock/prototype，不能计入真实闭环验收。

## 十、does_not_block 精确定义

在接口合同稳定前，可以继续进行不越界的需求合同、schema、确定性 fixture、mock adapter、界面原型和自动化合同测试；这些工作不因测试服或生产授权尚未批准而停止。

但 mock 必须版本化并标注 `mock-only` / `non-production`，不得替代真实鉴权、权限、会员来源、支付、消息、隐私和外部系统验收，不得据此宣称 M1 真实闭环完成。

## 十一、激活责任

平台集成负责人应依次完成：

1. 将本单同步到权威仓库并登记唯一工作项。
2. 复核 11 个当前活动/计划工作项的路径，确认无重叠。
3. 重新固定 `base_commit`，创建 `codex/activity-v3-m0` 与独立 worktree。
4. 生成 current checklist，组织随机治理考试；未达到 100 分不得开工。
5. 指定独立验收负责人并记录角色分离。
6. 激活 M0；M0 Go 后再申请 M1，不得自动扩权。

本任务单自签发之日起生效；授权范围以本文为准。
