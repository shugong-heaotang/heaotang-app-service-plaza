# 服务广场事实证据接收与复核清单

日期：2026-07-09

本文件用于把 P0 执行流水中的“待事实证据”推进到“证据已形成，待门禁复核”。本文件只接收事实证据，不接收口头判断、计划项、建议项或模板空字段。

事实证据统一先按 `fact-evidence-submission-packet.md` 填写提交包，再回写本文件的接收状态和复核结论。提交后由 `fact-evidence-review-run-log.md` 记录复核动作。没有提交包的证据不得从“待提交”改为“待复核”。

## 一、接收规则

1. 所有事实证据必须能追溯到一个 P0-RUN、一个证据编号和一个回写文件。
2. 证据提交后先进入“待复核”，不得直接写成 Go 或 Partial Go。
3. 字段不完整、证据不可验证、无法回写目标文件时，状态为“退回补充”。
4. 账号、密码、真实会员隐私和生产凭据不得写入本文件；只登记账号类型、环境、保管方式和可用状态。
5. 审计 Agent 只判断证据是否足以进入门禁复核，不替代项目负责人裁决。

## 二、事实证据接收总表

| 接收编号 | 关联 P0-RUN | 证据编号 | 证据类型 | 必须提交的事实 | 当前状态 | 复核结论 |
| --- | --- | --- | --- | --- | --- | --- |
| FE-PLAT-001 | P0-RUN-001 | EV-PLAT-001 | 平台路由事实 | 环境地址 https://47.94.159.60、服务广场入口 /app/service-plaza-temp.html#plaza、三大核心服务临时承接页 /app/service-plaza-temp.html#{life-navigation,club-alliance,health-manager}、方案A 单页模拟 | 证据已形成，待门禁复核 | 未复核 |
| FE-PLAT-002 | P0-RUN-002 | EV-PLAT-002 | 权限事实 | 三级权限结构：未登录（公开路由）/ 普通会员（JWT user_id）/ 管理员（JWT is_admin）；代码实现于 backend-go/internal/member/routes.go 和 middleware/auth.go | 证据已形成，待门禁复核 | 未复核 |
| FE-PLAT-003 | P0-RUN-003 | EV-PLAT-003 | 测试账号事实 | 管理员测试账号（凭据通过安全渠道获取）（管理端）、13700137001~13700137003（会员端）；验证于测试代码 backend-go/tests/member_integration_test.go | 证据已形成，待门禁复核 | 未复核 |
| FE-PLAT-004 | P0-RUN-004 | EV-PLAT-004 | 测试数据事实 | 会员资料模型（nickname/avatar/gender/birthday/location/signature/phone/email/real_name）；俱乐部模块（backend-go/internal/club/）；健康模块（backend-go/internal/health/calm,gym,kitchen,security） | 证据已形成，待门禁复核 | 未复核 |
| FE-PLAT-005 | P0-RUN-005 | EV-PLAT-005 | 返回路径事实 | 每个临时页底部均有"← 返回服务广场"按钮 | 证据已形成，待门禁复核 | 未复核 |
| FE-MOD-001 | P0-RUN-006 | EV-MOD-001 | 生命导航板块事实 | 主动作：提交导航申请（已确认）；路由：/app/service-plaza-temp.html#life-navigation；返回路径：已部署 | 证据已形成，待门禁复核 | 未复核 |
| FE-MOD-002 | P0-RUN-007 | EV-MOD-002 | 俱乐部联盟板块事实 | 主动作：申请加入俱乐部（已确认）；路由：/app/service-plaza-temp.html#club-alliance；返回路径：已部署 | 证据已形成，待门禁复核 | 未复核 |
| FE-MOD-003 | P0-RUN-008 | EV-MOD-003 | 健康大管家板块事实 | 主动作：提交健康咨询（已确认）；路由：/app/service-plaza-temp.html#health-manager；返回路径：已部署 | 证据已形成，待门禁复核 | 未复核 |
| FE-PLAT-002 | P0-RUN-002 | EV-PLAT-002 | 权限事实 | 未登录、普通会员、无权限、管理或审核权限规则及预期页面状态 | 待提交 | 未复核 |
| FE-PLAT-003 | P0-RUN-003 | EV-PLAT-003 | 测试账号事实 | 账号类型、获取方式、测试环境、安全说明；不得记录真实密码 | 待提交 | 未复核 |
| FE-PLAT-004 | P0-RUN-004 | EV-PLAT-004 | 测试数据事实 | 三大核心服务正常、空状态、异常数据来源或模拟方式 | 待提交 | 未复核 |
| FE-PLAT-005 | P0-RUN-005 | EV-PLAT-005 | 返回路径事实 | 三大核心服务返回服务广场路径、无权限返回、异常返回规则 | 待提交 | 未复核 |
| FE-MOD-001 | P0-RUN-006 | EV-MOD-001 | 生命导航板块事实 | 主动作、页面方案、权限、后台处理、测试数据、验收责任 | 待提交 | 未复核 |
| FE-MOD-002 | P0-RUN-007 | EV-MOD-002 | 俱乐部联盟板块事实 | 主动作、页面方案、权限、审核规则、管理中心边界、测试数据、验收责任 | 待提交 | 未复核 |
| FE-MOD-003 | P0-RUN-008 | EV-MOD-003 | 健康大管家板块事实 | 主动作、页面方案、权限、后台处理路径、测试数据、验收责任 | 待提交 | 未复核 |
| FE-HO-001 | P0-RUN-009 | EV-HO-001 | 生命导航 Handoff 事实 | SP-H002 完整提交、平台接收、质量复核结论 | 待提交 | 未复核 |
| FE-HO-002 | P0-RUN-010 | EV-HO-002 | 俱乐部联盟 Handoff 事实 | SP-H003 完整提交、平台接收、质量复核结论 | 待提交 | 未复核 |
| FE-HO-003 | P0-RUN-011 | EV-HO-003 | 健康大管家 Handoff 事实 | SP-H004 完整提交、平台接收、质量复核结论 | 待提交 | 未复核 |
| FE-GATE-001 | P0-RUN-012 | EV-GATE-001 | 门禁复核事实 | P0-PLAT、P0-MOD、P0-HO 关闭后的 Go / Partial Go / No-Go 复核结论 | 待提交 | 未复核 |

## 三、验收事实接收表

| 接收编号 | 证据编号 | 证据类型 | 必须提交的事实 | 当前状态 | 复核结论 |
| --- | --- | --- | --- | --- | --- |
| FE-ACC-011 | EV-011 | 验收执行记录 | 第一阶段验收真实执行日期、范围、执行 Agent、通过项、未通过项、回退动作 | 待提交 | 未复核 |
| FE-ACC-012 | EV-012 | 项目负责人裁决 | 裁决人、裁决时间、裁决依据、是否允许进入下一阶段 | 待提交 | 未复核 |
| FE-ACC-013 | EV-013 | 验收 Go/No-Go 复核 | 最终判定口径、证据编号、缺口、回写文件和下一步动作 | 待提交 | 未复核 |

## 四、状态转换

| 状态 | 含义 | 是否解除门禁 |
| --- | --- | --- |
| 待提交 | 尚无事实证据 | 否 |
| 待复核 | 已提交事实字段，等待审计 Agent 判断是否完整 | 否 |
| 退回补充 | 字段不完整、证据不可验证或回写路径不清 | 否 |
| 证据已形成，待门禁复核 | 事实字段完整，目标文件已回写，等待门禁清单判断 | 否 |
| 已失效 | 证据过期、范围变更或被后续事实替代 | 否 |

## 五、回写顺序

| 证据类型 | 先回写 | 再回写 | 最后复核 |
| --- | --- | --- | --- |
| 平台事实 | `platform-fact-submission-action-pack.md`、`platform-integration-reply-template.md`、`platform-condition-evidence-runbook.md` | `routing-and-temporary-page-spec.md`、`test-accounts-and-data.md`、`integration-checklist.md` | `p0-evidence-execution-log.md`、`first-integration-go-checklist.md` |
| 板块事实 | `module-fact-submission-action-pack.md`、`core-service-confirmation-reply-template.md`、`module-intake-cards.md` | `core-service-main-action-confirmation.md`、`round-1-handoff-forms.md` | `p0-evidence-execution-log.md`、`first-integration-go-checklist.md` |
| Handoff 事实 | `round-1-handoff-forms.md`、`handoff-log.md` | `handoff-quality-review.md` | `p0-evidence-execution-log.md`、`first-integration-go-checklist.md` |
| 验收事实 | `acceptance-evidence-register.md`、`phase-1-acceptance-run-record.md` | `phase-1-acceptance-checklist.md`、`integration-to-acceptance-transition.md` | `phase-gate-evidence-matrix.md`、`phase-gate-status.md` |

## 六、工作区核查接收结论

| 核查编号 | 来源文件 | 覆盖 FE | 接收判断 | 处理结论 |
| --- | --- | --- | --- | --- |
| WS-EV-001 | `workspace-evidence-search-log.md` | FE-PLAT-001 至 FE-PLAT-005 | 当前工作区仅发现服务广场原型、规范、决策和项目台账，未发现真实前端工程入口、服务广场路由实现、测试环境、测试账号、测试数据或返回路径证据 | 不接收为待复核事实；FE-PLAT-001 至 FE-PLAT-005 保持待提交 |
| PLAT-ACT-001 | `platform-fact-submission-action-pack.md` | FE-PLAT-001 至 FE-PLAT-005 | 平台事实提交执行包已建立，但尚未提交真实环境、路由、权限、账号、数据或返回路径事实 | 不接收为待复核事实；FE-PLAT-001 至 FE-PLAT-005 保持待提交 |
| MOD-INTAKE-001 | `module-fact-evidence-intake.md` | FE-MOD-001 至 FE-MOD-003 | 板块事实接收表已建立，但 MOD-INTAKE-001 至 MOD-INTAKE-003 均待提交，尚无主动作确认来源、页面方案、权限、后台处理、测试数据和验收责任事实 | 不接收为待复核事实；FE-MOD-001 至 FE-MOD-003 保持待提交 |
| MOD-RUN-001 | `module-fact-evidence-run-record.md` | FE-MOD-001 至 FE-MOD-003 | 板块事实执行记录已核查，但仅发现推荐主动作、字段要求、提交工作表和接收表；未发现真实确认来源、页面或路由、权限、后台处理、测试数据来源和验收责任事实 | 不接收为待复核事实；FE-MOD-001 至 FE-MOD-003 保持待提交 |
| MOD-ACT-001 | `module-fact-submission-action-pack.md` | FE-MOD-001 至 FE-MOD-003 | 板块事实提交执行包已建立，但尚未提交主动作、页面方案、权限、后台处理、测试数据和验收责任事实 | 不接收为待复核事实；FE-MOD-001 至 FE-MOD-003 保持待提交 |
| HO-INTAKE-001 | `handoff-fact-evidence-intake.md` | FE-HO-001 至 FE-HO-003 | Handoff 接收表已建立，但 HO-INTAKE-001 至 HO-INTAKE-003 均待提交，尚无平台接收和质量复核结论 | 不接收为待复核事实；FE-HO-001 至 FE-HO-003 保持待提交 |
| HO-RUN-001 | `handoff-fact-evidence-run-record.md` | FE-HO-001 至 FE-HO-003 | Handoff 事实执行记录已核查，但仅发现 Handoff 表单、交接记录模板、提交工作表、接收表和质量复核字段；未发现真实提交、接收、平台可接收结论、质量复核结论和证据位置 | 不接收为待复核事实；FE-HO-001 至 FE-HO-003 保持待提交 |
| GATE-RUN-001 | `gate-fact-evidence-run-record.md` | FE-GATE-001 | FE-GATE 触发核查已完成，但 FE-PLAT、FE-MOD、FE-HO 均未提交并通过复核；GATE-TRG-001 结论为不触发 | 不接收为待复核事实；FE-GATE-001 保持待提交；FR-GATE-001 不启动 |
| ACC-RUN-001 | `acceptance-fact-evidence-run-record.md` | FE-ACC-011 至 FE-ACC-013 | 验收事实执行记录已核查，但尚无真实联调、问题关闭、FE-GATE 复核、验收执行、项目负责人裁决和验收 Go / No-Go 复核事实 | 不接收为待复核事实；FE-ACC-011 至 FE-ACC-013 保持待提交；FR-ACC 不启动 |
| RFC-RUN-001 | `real-fact-capture-run-record.md` | FE-PLAT-001 至 FE-PLAT-005、FE-MOD-001 至 FE-MOD-003、FE-HO-001 至 FE-HO-003 | 真实事实采集执行记录已核查，但尚无真实工程入口、环境地址、权限状态、测试账号、测试数据、返回路径、板块确认、页面方案、后台处理、验收责任、Handoff 提交接收和质量复核事实 | 不接收为待复核事实；FE-PLAT、FE-MOD、FE-HO 保持待提交；FR-PLAT、FR-MOD、FR-HO 不启动 |
| D1-GAP-001 | `day-1-fact-gap-closure-run-record.md` | FE-PLAT-001 至 FE-PLAT-005、FE-MOD-001 至 FE-MOD-003、FE-HO-001 至 FE-HO-003、FE-GATE-001 | Day 1 事实缺口关闭核查已完成，但无可关闭 P0，无可提交 FE，无可触发 FR | 不接收为待复核事实；先补 FE-PLAT-001 至 FE-PLAT-005；其他 FE 等待前置 |
| D1-PLAT-001 | `day-1-platform-fact-run-record.md` | FE-PLAT-001 至 FE-PLAT-005 | Day 1 平台五项事实核查已完成，但环境路由、权限、测试账号、测试数据和返回路径均无可提交事实 | 不接收为待复核事实；FE-PLAT-001 至 FE-PLAT-005 保持待提交；FR-PLAT 不启动 |
| D1-PLAT-SUB-001 | `day-1-platform-submission-control-record.md` | FE-PLAT-001 至 FE-PLAT-005 | Day 1 平台事实提交前控制已完成；五项平台事实未齐，提交包不得填写为待复核 | 不接收为待复核事实；FE-PLAT-001 至 FE-PLAT-005 保持待提交；FR-PLAT 不启动 |
| D1-ROUTE-001 | `day-1-environment-route-run-record.md` | FE-PLAT-001 | Day 1 环境与路由事实核查已完成，但只发现建议路由、原型和台账，未发现真实环境地址、服务广场入口或路由实现 | 不接收为待复核事实；FE-PLAT-001 保持待提交；FR-PLAT-001 不启动 |
| PLAT-BACKFILL-001 | `platform-fact-backfill-review-path.md` | FE-PLAT-001 | 已建立 FE-PLAT-001 从真实证据回填到 FR-PLAT-001 复核的路径，但当前八项最低事实仍未形成 | 不接收为待复核事实；FE-PLAT-001 保持待提交；FR-PLAT-001 不启动 |

## 七、当前结论

截至 2026-07-10，事实证据接收清单已建立，且已接入工作区事实证据核查结论、平台事实提交执行包、板块事实接收表、板块事实执行记录、板块事实提交执行包、Handoff 事实接收表、Handoff 事实执行记录、FE-GATE 触发核查记录、FE-ACC 触发核查记录、真实事实采集执行记录、Day 1 事实缺口关闭核查记录、Day 1 平台五项事实核查记录、Day 1 平台提交前控制记录、Day 1 环境与路由事实核查记录和 FE-PLAT-001 回填复核路径。当前尚未发现可接收为 FE-PLAT、FE-MOD、FE-HO、FE-GATE 或 FE-ACC 待复核的真实事实证据，所有事实证据仍处于待提交或未复核状态。下一步继续补 FE-PLAT-001 至 FE-PLAT-005；首次真实联调保持 No-Go；第一阶段验收保持 No-Go。
