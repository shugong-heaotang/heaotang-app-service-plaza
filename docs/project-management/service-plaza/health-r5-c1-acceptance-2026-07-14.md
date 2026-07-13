# 健康大管家 R5-C1 独立验收与受控集成 Handoff

- 平台工作项：`AIW-20260714-HEALTH-R5-C1-ACCEPTANCE`
- 模块工作项：`AIW-20260714-HEALTH-R5-CONSULTATION-SECOND-OPINION-MDT-CONTRACTS`
- exact source：`eebc197837d85d68c471299eb94bc80778697949`
- authority activation：`cb1cdb91332fc24f5914e4b9eecd4c28e9e897db`
- verdict：`R5-C1 Contract Evidence Go / Controlled Integration Go`

## Completed

1. exact source 本地/远端一致且 clean；单提交十个路径全部位于模块 allowed paths，受控集成后十个 blob 与 source 逐项一致。
2. 结构化转介包保留申请类型、本人或核验合法代理权限、授权、主要诉求、资料引用、来源、版本、缺失资料、责任协调人和时间；AI 只生成非诊断性摘要和缺失清单。
3. 医生集团医疗质量人员人工初审不可绕过；资料不足保持 hold，急症、专业风险或不适宜线上处理必须停止线上流程并转线下合规医疗机构，AI 不得独立关闭风险。
4. 专家征集只面向已核验专家池定向发起，保留资质、执业、范围、服务方式和利益冲突；禁止公开病例板、抢单、竞价和未核验专家。
5. 主责医生或 MDT、成员角色与范围、合规医疗机构承接均可追溯；第二意见保持独立版本，原意见和分歧不可覆盖，AI 不得选择最终医疗结论。
6. 全过程事件级审计保留责任主体、时间、来源、版本、政策与关联引用；纠错追加版本，费用只记录状态，不授权真实金额、收费或支付。
7. 禁止公开身份或完整病历、治愈悬赏、疗效承诺、结果付费、非医疗机构诊疗以及商业因素越过医疗安全顺序。

## Verified

- 需求补充 SHA-256：`fc07676f9d0ab0dbaf1a4575457e4d1a67d642d1c483187e28a5b2c64e2a9012`。
- R5 conformance 在 source 与受控集成工作树均为 23/23 passed。
- 模块 checklist 28/28 current；exam attempt 1=50 保留，完整补课后 attempt 2=100；同 `record_id` IR/Handoff 有效。
- 平台入口 checklist 28/28 current、exam attempt 1=100；registry 收口后平台最终 R2 checklist/exam/IR 使用同一 R2 `record_id`。
- foundation 与 health internal dependencies：development Go。
- collaboration、development checklist、governance exam、implementation record、Service Plaza 总合同、UTF-8、diff、范围、秘密和敏感模式门禁全部通过。
- 唯一电话样式位于 conformance 合成拒绝负例；非测试电话样式 0、身份证样式 0、秘密模式 0。

## R1-R5 最终证据索引

| 阶段 | exact source | 受控集成 commit | 独立验收 Handoff | 结果 |
| --- | --- | --- | --- | --- |
| R1 需求与原型冻结 | `e50d48c4dd28307f9f09170ad1466c3b20064b26` | `e892e4ea0919f7c762bd35fc1606ceab946acb4b` | `docs/project-management/service-plaza/health-r1-c1-acceptance-2026-07-13.md` | 13/13，Go |
| R2 双渠道建档 | `df676a5be4135d6c1e29abc06043b5c1a1cc6842` | `be4563ae504c32595f05e2908757129068f8f15b` | `docs/project-management/service-plaza/health-r2-c1-acceptance-2026-07-13.md` | 16/16，Go |
| R3 学习与俱乐部入口 | `8565f1b43cfa196fdc5546ebf5316da71da8e074` | `dfbff8e87792829e3e2dae8010a1ce3cba6b240c` | `docs/project-management/service-plaza/health-r3-c1-acceptance-2026-07-14.md` | 17/17，Go |
| R4 医生目录与受约束推荐 | `da66c7db451ae786268d743e0a1ff267fbc4a460` | `b6736b6117c05780cd6a8df9f3ca162ea1f3f40b` | `docs/project-management/service-plaza/health-r4-c1-acceptance-2026-07-14.md` | 19/19，Go |
| R5 咨询、第二意见、专家征集与 MDT | `eebc197837d85d68c471299eb94bc80778697949` | 本 Handoff 所在最终 closeout commit | `docs/project-management/service-plaza/health-r5-c1-acceptance-2026-07-14.md` | 23/23，Go |

R1-R5 的 Go 仅表示离线、合成、`synthetic_only=true`、`executable=false` 的需求、合同、Schema、正负测试和治理证据已完成并受控集成；不表示医疗服务、真实数据、收费、部署或生产 Go。

## Root-cause closeout

- current checklist 首次调用漏传必需参数；补齐后又把 `--require-current` 误用于全部历史快照，产生设计内 stale 报告。停止重复后改为受控临时目录只校验本轮 current，并对历史目录单独执行不可变 Schema 校验，两者均通过。
- 安全扫描首次对字符串流执行 `Select-String` 丢失路径，唯一合成电话负例被误分为非测试；改用 `-LiteralPath` 保留路径后，非测试命中为 0。
- registry 通用 status 补丁误触 action-telemetry；提交前的 work_id 语义差异断言捕获并精确恢复，最终仅两个 R5 项的 status 和 migration_note 变化。

## Pending

- 医生集团医疗质量负责人：真实人工初审、专家池、主责医生/MDT 和质量政策。
- 合规医疗机构负责人：正式诊疗、电子病历和服务承接。
- 隐私与法律负责人：真实身份、代理、授权、真实健康数据和互联网诊疗。
- 平台安全负责人：共享运行时、API、数据库和环境。
- 大益健康馆运营负责人：真实会员试点、线下承接和真实费用流程。
- does_not_block：R1-R5 离线合成阶段完成、证据归档和后续经新授权的独立实现规划。
- blocks：真实咨询、第二意见、专家征集、MDT、真实身份/健康数据、互联网诊疗、真实费用、收费、部署和生产。

## No-Go

本次不授权前后端、共享运行时、API、数据库、真实医生/身份/会员/健康数据、互联网诊疗、AI 诊断/处方/改药、冒充医生、疗效承诺、公开病历、抢单、医生竞价、治愈悬赏、结果付费、真实收费/支付、测试服、生产或不可逆操作。
