# 俱乐部联盟 CA-F0/H0 顶层需求基线

基线 ID：`CA-F0-H0-REQ-v1`
项目：`club-alliance`
阶段：`CA-F0-M0 + CA-H0`
状态：H0 base standardized；完整 H0 Go 待平台验收与 `D-CA-003` 关闭
父项目：服务广场
上游正式 Handoff：`SP-H025`

## 1. 目标

俱乐部联盟先成为一个具有独立治理、单一入口标准、版本化机器契约和一致性门禁的长期项目，再递归建设四个子项目：

1. `CA-PC`：公益俱乐部；
2. `CA-SC`：自建俱乐部；
3. `CA-FC`：家庭俱乐部；
4. `CA-UF`：俱乐部友联体。

父项目阶段固定为：

`CA-F0 → CA-H0 → CA-H1 → CA-PC/CA-SC/CA-FC/CA-UF → CA-X → CA-R → CA-O`

展示顺序不等于开发顺序。每个子项目在正式启动后递归执行 `P0-P7` 与 `G0-G6`。

## 2. 本轮范围

### 2.1 CA-F0

- 需求、术语、能力边界和决策记录；
- 两层依赖与阶段门禁；
- 四子项目递归模板；
- 可证伪前提、复审条件、兼容与迁移规则；
- Handoff、实现记录和一致性证据。

### 2.2 CA-H0

- 首页信息架构和路由解析标准；
- `category-registry`、`capability-catalog`、`homepage`、`relationship` 四组 JSON 与 Schema；
- 版本化错误目录；
- H0-C01～C12 与 H0-B001～B033；
- Python 标准库 conformance、fixtures 和报告。

## 3. 明确非目标

- 不实现 CA-H1 页面壳；
- 不修改 frontend、backend、deploy 或上游服务广场合同；
- 不实现创建、加入、审核、成员、关系写入、支付、提现、退款或订阅；
- 不访问测试环境、生产、真实资金或不可逆数据；
- 不把旧 `standard-club-join-review` Go 推导为父项目或其他子项目 Go。

## 4. 上游单一真相源

首页展示事实只来自：

- `contracts/service-plaza/service-plaza-actions.v1.json`
- `contracts/service-plaza/service-plaza-action.schema.json`

H0 只保存 action ID、子项目 ID、实体类型、语义选择器状态、能力 profile 和治理引用。模块禁止复制上游的 `label`、`sort_order`、`target`、`access`、`lifecycle_status`、`return_target` 或 `telemetry_event`。

四入口集合固定为：

`public-benefit-club`、`self-created-club`、`family-club`、`club-federation`

运行时顺序必须从上游记录派生，当前事实为 50/60/70/80，但模块不保存该数值。`club-manage` 单独解析为附属操作，不得成为第五类。

## 5. 首页路由标准

- 根路由：`/services/club-alliance`；返回：`/services`。
- 无 query 表示 home。
- 兼容 query 只允许把现有中文 `category` 值解析为唯一 `selected_action_id` 和焦点状态。
- 兼容解析不得调用任何俱乐部业务 API。
- 空白、未知或多义参数失败关闭并返回稳定错误 ID。
- 直达、刷新、浏览器后退和返回 `/services` 必须确定、可重复。
- CA-H1 前不得修改上游 target。

## 6. 四类语义边界

| 子项目 | 实体类型 | H0 语义 | 状态 |
| --- | --- | --- | --- |
| CA-PC | `club` | `type=standard + category=charity` | Accepted |
| CA-SC | `club` | 推荐 `type=standard + category=general` | `D-CA-003 Pending`，只能保存 proposed metadata，不可执行 |
| CA-FC | `club` | 现有 `type=family` 只登记为 code-present-unverified 事实，完整产品语义在 CA-FC/P0 冻结 | 非 H0 业务 Go |
| CA-UF | `club_relationship` | `relationship_kind=club-federation` | Accepted |

公益不得创建新的 charity ClubType，也不得伪装为 direct。友联体不是 ClubType，不得复用仅限 family 的 `FamilyAlliance`。

## 7. 能力目录标准

能力状态只允许：

`planned | code-present-unverified | standardized | implemented | test-verified | release-go | operations-go | forbidden`

每条能力必须声明：profile、required/optional/forbidden、owner、contract refs、dependency refs、evidence refs，以及 governance/development/acceptance/release/operations 五维 readiness。代码存在不能自动提升为 test-verified、release-go 或 operations-go。

CA-H0 只消费 `ENTRY`、`CATALOG`、`ACCESS`、`LIFECYCLE`、`TELEMETRY`。商业、支付、提现、退款、订阅在所有 profile 中必须为 forbidden。

## 8. 首页职责边界

首页负责：

- 上游入口派生；
- 生命周期和权限展示；
- 路由、返回和焦点状态；
- loading/empty/error/unauthorized/maintenance/offline 等统一状态契约；
- 响应式行为声明；
- 使用上游 telemetry event 的事件转交。

首页不负责任何业务写入、成员或关系生命周期，也不成为第二展示真相源。

## 9. 关系标准

`club-federation` 使用独立关系实体。关系政策必须版本化引用、默认失败关闭、禁止未配置默认值，并保留未来兼容迁移边界。CA-H0 只定义结构和禁止边界，不授权关系 API。

## 10. 递归子项目标准

每个 `CA-PC/SC/FC/UF` 子项目执行：

| 阶段 | 交付 |
| --- | --- |
| P0 | 需求、非目标、术语、负责人、决策事项 |
| P1 | 上下游接口、数据责任、权限和隐私 |
| P2 | 机器契约、Schema、错误目录和 fixtures |
| P3 | 实现与单元/契约测试 |
| P4 | 集成、安全、幂等、事务和串类负例 |
| P5 | 测试环境 API 与真实页面 UAT |
| P6 | 发布、配置双审、备份和回滚演练 |
| P7 | 运营 SLI、告警、runbook、复盘和迭代 |

统一门禁：`G0 准入`、`G1 需求`、`G2 契约`、`G3 实现`、`G4 集成`、`G5 发布`、`G6 运营`。父门禁 No-Go 只阻塞依赖下游，不阻塞无依赖的安全准备。

## 11. 后半程证据

- `CA-X`：真实 API、权限、幂等、事务、串类负例和真实页面 UAT；
- `CA-R`：exact release、配置双审、安全、备份、部署后 smoke 和回滚演练；
- `CA-O`：SLI owner/query/threshold、告警、runbook、升级、留存和决策复审。

没有 exact commit、真实认证、环境入口、测试报告和 Handoff，不得宣称 ready、release-go 或 operations-go。

## 12. 当前门禁

- G0 / CA-F0-M0：Go，平台验收提交 `8f1cad9`，权威集成 `59b8a47`。
- H0 base：允许实施并提交验收。
- 完整 H0 Go：等待所有 H0 合同证据和 `D-CA-003`。
- CA-H1、四类业务、CA-X、CA-R、CA-O：未授权。
