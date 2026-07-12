# 健康大管家 MVP-90 M1 P2 确定性合成重放需求

- work_id：`AIW-20260712-HEALTH-MVP90-M1-P2-SYNTHETIC-REPLAY`
- 当前检查点：`P2-C1`
- 范围：成年合成会员、本地内存、零网络、零数据库
- 输出属性：`synthetic_only=true`、`executable=false`

## C1 目标

建立一份机器可校验的重放计划，而不是复制一套健康业务语义。计划必须：

1. 精确包含 `MVP-A001`—`MVP-A015` 与 `HMM1-F001`—`HMM1-F015`；
2. `MVP-A001` 按顺序覆盖 `M1-S01`—`M1-S10`，全计划覆盖六组 M0 状态机；
3. 每个事件声明 actor、action、transition（若为无状态写入或拒绝则为 `null`）、资源、期望状态、版本、幂等、拒绝和审计结果；
4. 场景、fixture、步骤、动作、迁移和拒绝错误必须解析到已集成 M0/M1 源；
5. 允许风险场景使用 M0 已存在但 P1 步骤未列出的安全转移，前提是该事件明确为 `deny`，且状态机、角色和场景拒绝语义均可解析；
6. 不读取系统时间或随机数，不调用网络、API、数据库、浏览器和外部模型；
7. 不把计划或后续 reference runner 描述为可上线业务实现。

## C1 验收

- Draft 2020-12 Schema 正例通过；删场景、提升 executable、取消 synthetic、未知步骤和未知动作负例拒绝；
- 15 个场景和 fixture 一一对应且 source pointer 索引一致；
- 25 个首版事件均能解析到步骤、动作、状态机迁移或拒绝规则；
- 10 个步骤、6 个状态机均有覆盖；
- P1 原 11 项 conformance 保持通过；
- current checklist、考试、IR、UTF-8、diff/scope 和敏感模式门禁通过。

## 保持 No-Go

`C4-L02-L04`、全量 `C4-H06`、production identity、真实会员/健康数据、共享前后端/API/数据库、测试环境、部署、收费、资金和生产均不在本检查点。
