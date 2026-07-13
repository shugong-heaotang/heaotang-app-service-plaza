# 俱乐部联盟 CA-H1 标准首页与页面壳正式任务书

- 通知编号：`CA-H1-TASK-20260711-001`
- 上游 Handoff：`SP-H025`（H0 Full Go）、`SP-H029`（本通知）
- 工作项：`AIW-20260711-CLUB-ALLIANCE-H1-HOMEPAGE`
- 负责人：俱乐部联盟负责人
- 阶段：CA-H1；不包含 CA-SC/FC/PC/UF 业务实现

## 目标与固定边界

建立 `/services/club-alliance` 独立标准首页/页面壳，返回 `/services`。页面从 `service-plaza.action.v1` 的唯一版本化动作目录派生四入口，严格继承上游 `sort_order`：公益俱乐部、自建俱乐部、家庭俱乐部、俱乐部友联体。`club-manage` 仅为附属管理入口，不是第五类。

CA-H1 只消费 ENTRY/CATALOG/ACCESS/LIFECYCLE/TELEMETRY。可以读取 H0 已接受 selector 语义，但所有 selector 继续 `executable=false`；不得调用俱乐部搜索、创建、加入、审核、成员、支付、公益资格或友联关系 API，不得修改后端、部署或生产。

## 必须实现

1. 在精确路由优先级中挂载独立 Club Alliance 模块，避免落入 `CoreServicePage`。
2. 建立共享 action adapter，供 `ServicePlazaPage` 与 Club Alliance 首页共同使用；禁止第二套 action_id、label、target、sort_order、access、lifecycle、telemetry 真相源。
3. 只选择 `region=club_alliance AND service_id=club-alliance AND action_type=service_variant` 的精确四入口，并显式排除 `club-manage`；缺失、重复、错误作用域一律失败关闭。
4. 无 query 为 home；现有中文 `category` query 只确定性解析为唯一 `selected_action_id`，不发业务请求。空白、未知、多义参数显示稳定失败关闭状态。直达、刷新、后退和返回 `/services` 可重复。
5. 复用平台 ActionControl/evaluator 的权限、生命周期和遥测，不在模块内放宽 scopes 或提升 active/preview/planned/maintenance/offline。
6. 页面状态冻结为 H0 `homepage.v1` 的精确八态：`home`、`focused`、`loading`、`empty`、`error`、`unauthorized`、`maintenance`、`offline`。error 提供 retry；不得新增同义状态或用人工联调状态切换器作为验收实现。
7. 320/360/768/桌面响应式无横向滚动，键盘可达、焦点清晰、状态有 aria 语义。

## 开发门禁

- 先完成模块 current checklist、逐项读取、随机考试 100 分和任务签收。
- 定向 Vitest 后运行前端全量测试、TypeScript/生产构建、测试服构建、服务广场总合同、UTF-8 与 `git diff --check`。
- 自动化必须证明：打乱上游输入仍按 50/60/70/80；管理中心排除；query 重放；精确八态；权限/生命周期/遥测复用。网络 allowlist 只允许读取 catalog/actions；测试必须显式拒绝 club search/create/join/review/member/payment/charity/federation 请求。
- 每个检查点提交 exact commit、changed paths、命令结果、未决风险和 `CA-H1-handoff.md`，然后停止等待平台验收。

## 测试环境 UAT 门禁

模块实现 Go 不等于环境 Go。部署必须由独立平台部署授权执行。UAT 需要 exact commit/base URL/environment，验证 `/health?json=1`、`/ready`、真实 catalog/actions，guest/已登录/缺 scope，合法与非法 query，直达/刷新/后退/返回，activated/blocked 遥测无敏感载荷，320/360/768/桌面布局、键盘/焦点/aria，以及浏览器网络证据证明只读取 catalog/actions，未请求 club search/create/join/review/member/payment/charity/federation。未完成真实环境 UAT 不得签 CA-H1 Full Go。

## 禁止范围

禁止 CA-SC/FC/PC/UF 业务流程、后端新增、Schema 修改、deploy/production、真实资金、不可逆数据和擅自修改服务广场 IA。任何公共接口不足必须单独提交平台变更请求，不得扩写本工作项。
