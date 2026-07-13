# 健康大管家 MVP-90 M0 合同需求

## 1. 来源与状态

- 通知：`HM-MVP90-M0-TASK-20260712-001`
- 上游 PRD：`HM-MVP90-PRD-V1`，exact commit `fdf080f7ab03b2bdba87b77a7b3fd33dbcc8f73c`
- PRD SHA-256：`701ee042f88a156a2c393e7b64bbbea7a4b54c0e94a81be8ea83d8cb05c1e147`
- PRD 状态：`Document Handoff Ready`
- 专业状态：`Technical Go / Professional Freeze Pending`

本文件将 PRD 产品语义转换为机器合同，但不是 API、数据库 Schema、页面或专业政策。

## 2. M0 冻结范围

1. 16 个对象：会员服务关系、授权、档案项、测评会话、目标、计划、计划版本、任务、任务反馈、检查记录、风险事件、转人工事件、沟通记录、服务记录、模板版本、审计事件。
2. 6 组状态机：开始健康管理、健康计划及版本、健康任务、风险事件、转人工与沟通、授权。
3. 6 类角色：会员、AI、管理师、医生/专业人员、医生集团、平台。
4. 15 个场景：`MVP-A001`—`MVP-A015`，每个场景使用独立、显式、可重放的合成 fixture。

## 3. 机器合同不变量

- 对象 ID、版本、owner、最低语义字段和 forbidden fields 唯一且完整。
- AI 草案不能冒充生效计划；提醒或消息不能冒充执行、接管或问题解决；订单/核销不能冒充专业结果。
- 未登记状态迁移使用稳定错误 `HMM0_TRANSITION_NOT_REGISTERED` 失败关闭。
- Pending 决策必须 `status=pending-with-owner`、`executable=false`、有 owner；不得生成 executable policy。
- 角色合同只描述产品责任和服务端授权前置；最终 scope 名称保持 Pending。
- 价格、容量、比例、有效期、时限、阈值和频率只允许引用版本化配置，禁止硬编码。
- AI 不得诊断、处方、改药、替代急救、保证疗效，或独立降低/关闭专业和紧急风险。

## 4. 合成数据不变量

- 生成器：`heaotang-deterministic-fixture-v1`，固定 seed `HEAOTANG-HM-MVP90-M0-20260712-V1`。
- 生成方式：Python 标准库 `hashlib` 的确定性派生；本工作树没有批准的固定 Faker 依赖，因此不新增未锁定包。
- 每个 fixture 显式 `synthetic=true`、`environment=non-production`、生成器/seed/version、销毁策略和场景 ID。
- 禁止真实姓名、会员 ID、手机号、身份证、OTP、JWT、cookie、病历、真实机构或外部报告。
- 相同 seed 重放必须产生相同规范 JSON SHA-256；不同场景的主体与对象引用不得重复。

## 5. 失败关闭与负例

- 缺对象、重复 ID、未知引用、缺 owner/version/forbidden fields：合同失败。
- 未登记迁移、从紧急引导直接进入普通计划、AI 关闭专业/紧急风险：失败。
- Pending 被标为 executable、角色禁止动作被允许、最终 scope 被提前发明：失败。
- fixture 缺 synthetic/non-production/seed、含敏感模式、数量不是 15 或 ID 不连续：失败。
- 合成场景不得以自动化代替专业、消费者语言、人工接管、无障碍或环境 UAT。

## 6. 明确非目标

前端、后端、API、数据库、测试环境、部署、生产、真实健康数据、收费、真实会员试运行、专业风险规则、响应 SLA、人员容量值和模型供应商均不在 M0。
