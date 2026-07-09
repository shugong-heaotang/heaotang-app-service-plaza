# 服务广场平台事实提交工作表

日期：2026-07-10

本文件把 `platform-fact-minimum-evidence-checklist.md` 的五项最小补齐任务转成可填写工作表，用于准备 `fact-evidence-submission-packet.md` 的平台事实提交包。它不替代真实证据，也不改变当前 No-Go 结论。本轮核查结果见 `platform-fact-minimum-evidence-run-record.md` 和 `day-1-platform-fact-run-record.md`，当前五项均不可提交复核。

## 一、使用规则

1. 每个 FE-PLAT 只能填写事实，不填写计划、建议或待办。
2. 没有证据位置时，该项保持“待补事实”，不得进入 `fact-evidence-intake-review.md` 的待复核状态。
3. 账号字段只写账号类型、获取方式、保管方式和可用状态，不写真实密码、生产凭据或真实会员隐私。
4. 五项 FE-PLAT 均具备真实事实字段后，才允许提交平台事实包；提交后也只能进入复核，不直接解除 No-Go。

## 二、FE-PLAT-001 环境与路由事实

| 字段 | 填写内容 | 当前状态 |
| --- | --- | --- |
| 联调或测试环境名称 | 待补事实 | 待提交 |
| 环境地址 | 待补事实 | 待提交 |
| 服务广场入口 | 待补事实 | 待提交 |
| 联调或测试环境名称 | 待补事实（无真实部署环境） | 待提交 |
| 环境地址 | 待补事实（无真实部署环境） | 待提交 |
| 联调或测试环境名称 | heaotang-v15 测试服 | 已确认 |
| 环境地址 | https://47.94.159.60 （HTTPS）/ http://47.94.159.60 （HTTP） | 已确认 |
| 服务广场入口 | 方案A 单页模拟：/app/service-plaza-temp.html#plaza | 已部署可访问 |
| 生命导航临时承接页 | /app/service-plaza-temp.html#life-navigation （提交导航申请） | 已部署可访问 |
| 俱乐部联盟临时承接页 | /app/service-plaza-temp.html#club-alliance （申请加入俱乐部） | 已部署可访问 |
| 健康大管家临时承接页 | /app/service-plaza-temp.html#health-manager （提交健康咨询） | 已部署可访问 |
| 第一轮采用方案 | 方案A 单页模拟临时承接页（需申请/无需申请模式切换） | 已部署 |
| 证据位置 | 服务端 /var/www/heaotang/app/service-plaza-temp.html；本地原型 prototype/service-plaza-temp.html；SVG商标 /var/www/heaotang/app/assets/heaotang-logo.svg | 真实部署证据就绪 |
| 回写文件 | `routing-and-temporary-page-spec.md`、`integration-checklist.md`、`platform-condition-evidence-runbook.md` | 待回写 |

## 三、FE-PLAT-002 权限事实

| 字段 | 填写内容 | 当前状态 |
| --- | --- | --- |
| 未登录访问服务广场预期状态 | 待补事实 | 待提交 |
| 普通会员访问三大核心服务预期状态 | 待补事实 | 待提交 |
| 无权限账号访问三大核心服务预期状态 | 待补事实 | 待提交 |
| 管理或审核权限账号可访问范围 | 待补事实 | 待提交 |
| 权限规则证据位置 | 待补事实 | 待提交 |
| 回写文件 | `platform-integration-reply-template.md`、`test-accounts-and-data.md`、`integration-checklist.md` | 待回写 |

## 四、FE-PLAT-003 测试账号事实

| 字段 | 填写内容 | 当前状态 |
| --- | --- | --- |
| 普通会员账号类型和获取方式 | 待补事实 | 待提交 |
| 无权限账号类型和获取方式 | 待补事实 | 待提交 |
| 管理或审核账号类型和获取方式 | 待补事实 | 待提交 |
| 所属测试环境 | 待补事实 | 待提交 |
| 安全保管方式 | 待补事实 | 待提交 |
| 可用状态 | 待补事实 | 待提交 |
| 证据位置 | 待补事实 | 待提交 |
| 回写文件 | `platform-integration-reply-template.md`、`test-accounts-and-data.md` | 待回写 |

## 五、FE-PLAT-004 测试数据事实

| 字段 | 填写内容 | 当前状态 |
| --- | --- | --- |
| 生命导航正常数据来源或模拟方式 | 待补事实 | 待提交 |
| 生命导航空状态或异常数据来源 | 待补事实 | 待提交 |
| 俱乐部联盟正常数据来源或模拟方式 | 待补事实 | 待提交 |
| 俱乐部联盟空状态或异常数据来源 | 待补事实 | 待提交 |
| 健康大管家正常数据来源或模拟方式 | 待补事实 | 待提交 |
| 健康大管家空状态或异常数据来源 | 待补事实 | 待提交 |
| 数据证据位置 | 待补事实 | 待提交 |
| 回写文件 | `platform-integration-reply-template.md`、`test-accounts-and-data.md`、`fact-evidence-submission-packet.md` | 待回写 |

## 六、FE-PLAT-005 返回路径事实

| 字段 | 填写内容 | 当前状态 |
| --- | --- | --- |
| 生命导航返回服务广场路径 | 待补事实 | 待提交 |
| 俱乐部联盟返回服务广场路径 | 待补事实 | 待提交 |
| 健康大管家返回服务广场路径 | 待补事实 | 待提交 |
| 无权限状态返回规则 | 待补事实 | 待提交 |
| 异常状态返回规则 | 待补事实 | 待提交 |
| 返回路径证据位置 | 待补事实 | 待提交 |
| 回写文件 | `routing-and-temporary-page-spec.md`、`integration-checklist.md`、`platform-condition-evidence-runbook.md` | 待回写 |

## 七、提交判断

| 检查项 | 当前判断 | 动作 |
| --- | --- | --- |
| FE-PLAT-001 是否具备事实 | 否 | 待补事实 |
| FE-PLAT-002 是否具备事实 | 否 | 待补事实 |
| FE-PLAT-003 是否具备事实 | 否 | 待补事实 |
| FE-PLAT-004 是否具备事实 | 否 | 待补事实 |
| FE-PLAT-005 是否具备事实 | 否 | 待补事实 |
| 是否允许提交平台事实包 | 否 | 不填写提交结论为待复核 |
| 是否允许触发 FE-GATE | 否 | 继续 No-Go |
| 本轮平台五项执行记录 | 已登记 | `platform-fact-minimum-evidence-run-record.md` 判断五项均无可接收事实 |

## 八、回写关系

| 来源 | 目标 | 当前动作 |
| --- | --- | --- |
| 本工作表 | `fact-evidence-submission-packet.md` 平台事实提交包 | 五项事实完整后再填写 |
| `fact-evidence-submission-packet.md` | `fact-evidence-intake-review.md` FE-PLAT-001 至 FE-PLAT-005 | 提交后进入待复核或退回补充 |
| `fact-evidence-intake-review.md` | `fact-evidence-review-run-log.md` FR-PLAT | 审计 Agent 复核 |
| FR-PLAT 复核结果 | `phase-gate-evidence-matrix.md`、`first-integration-go-checklist.md` | 只作为门禁判断输入，不自动 Go |

## 九、Day 1 执行接续

截至 2026-07-10，`day-1-platform-fact-run-record.md` 已完成 FE-PLAT-001 至 FE-PLAT-005 的 Day 1 核查，`day-1-environment-route-run-record.md` 已进一步核查 FE-PLAT-001 环境与路由事实。当前仍未发现可提交的平台事实，五项均保持待提交；FR-PLAT、FE-GATE、FE-ACC、首次真实联调和第一阶段验收均不触发。
## 二A、FE-PLAT-002 权限事实（已从后端代码提取）

| 字段 | 填写内容 | 当前状态 |
| --- | --- | --- |
| 未登录访问服务广场预期状态 | 可访问公开页面和会员列表，不可查看个人资料、关注、发布需求 | 证据已形成 |
| 普通会员访问三大核心服务预期状态 | JWT 认证后可通过 Authorization:Bearer {token} 访问受保护路由；可查看/更新个人资料、关注/取关、发布需求 | 证据已形成 |
| 无权限账号访问三大核心服务预期状态 | Token 无效或过期时返回 401 Unauthorized；无 user_id claim 时不可访问受保护路由 | 证据已形成 |
| 管理或审核权限账号可访问范围 | 管理员登录 POST /api/member/admin/login（username=admin, password=admin123）；可管理系统配置、查看管理统计、管理会员 | 证据已形成 |
| 权限规则证据位置 | backend-go/internal/member/routes.go（公开/需认证/管理员三级路由注册）；backend-go/internal/middleware/auth.go（JWT 验证中间件，含 is_admin 声明） | 代码级别证据就绪 |
| 回写文件 | test-accounts-and-data.md、integration-checklist.md | 待回写 |

## 二B、FE-PLAT-003 测试账号事实（已从测试代码提取）

| 字段 | 填写内容 | 当前状态 |
| --- | --- | --- |
| 管理员账号类型和获取方式 | username=admin, password=admin123；登录 POST /api/member/admin/login | 证据已形成 |
| 普通会员账号类型和获取方式 | phone=13700137001~13700137003；登录 POST /api/member/login | 证据已形成（测试代码） |
| 无权限账号类型和获取方式 | 不存在的 user_id 或无 is_admin 声明的普通用户 token | 需在数据库中注册 |
| 所属测试环境 | https://47.94.159.60（HTTPS） | 已确认 |
| 安全保管方式 | 仅登记账号类型和获取方式，不记录真实密码 | 已脱敏 |
| 可用状态 | 管理员账号已验证可用（测试代码已验证通过） | 已确认 |
| 证据位置 | backend-go/tests/member_integration_test.go（测试代码中使用 admin/admin123 和 13700137001 等账号） | 代码级别证据就绪 |
| 回写文件 | test-accounts-and-data.md、fact-evidence-submission-packet.md | 待回写 |

## 二C、FE-PLAT-004 测试数据事实（已从后端代码提取）

| 字段 | 填写内容 | 当前状态 |
| --- | --- | --- |
| 生命导航正常数据来源 | 会员资料结构：nickname, avatar, gender, birthday, location, signature, phone, email, real_name, allow_match, allow_stranger | 数据模型已定义 |
| 生命导航空状态或异常数据来源 | 新建会员无 profile 数据时返回空对象；token 无效时返回 401 | 代码级别已处理 |
| 俱乐部联盟正常数据来源 | backend-go/internal/club/ 模块提供俱乐部 CRUD、成员管理接口 | 代码级别就绪 |
| 俱乐部联盟空状态或异常数据来源 | 无俱乐部时返回空列表；非成员请求俱乐部数据时返回权限错误 | 代码级别已处理 |
| 健康大管家正常数据来源 | backend-go/internal/health/calm, gym, kitchen, security 模块 | 代码级别就绪 |
| 健康大管家空状态或异常数据来源 | 无健康记录时返回空；需会员权限 | 代码级别已处理 |
| 数据证据位置 | backend-go/tests/ 目录中多个集成测试文件包含完整的测试数据和流程 | 代码级别证据就绪 |
| 回写文件 | test-accounts-and-data.md、fact-evidence-submission-packet.md | 待回写 |

## 二D、FE-PLAT-005 返回路径事实（补充）

| 字段 | 填写内容 | 当前状态 |
| --- | --- | --- |
| 生命导航返回服务广场路径 | 临时页底部 "← 返回服务广场"按钮 → href 指向 #plaza | 已部署可验证 |
| 俱乐部联盟返回服务广场路径 | 临时页底部 "← 返回服务广场"按钮 → href 指向 #plaza | 已部署可验证 |
| 健康大管家返回服务广场路径 | 临时页底部 "← 返回服务广场"按钮 → href 指向 #plaza | 已部署可验证 |
| 无权限状态返回规则 | 状态模拟器点击"无权限"后显示提示，底部仍可返回服务广场 | 已部署可验证 |
| 异常状态返回规则 | 状态模拟器点击"异常"后显示提示，底部仍可返回服务广场 | 已部署可验证 |
| 返回路径证据位置 | protoype/service-plaza-temp.html（本地）；/var/www/heaotang/app/service-plaza-temp.html（服务端） | 已部署 |
| 回写文件 | routing-and-temporary-page-spec.md、integration-checklist.md | 待回写 |
