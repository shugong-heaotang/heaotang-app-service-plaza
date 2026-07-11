# 俱乐部联盟 CA-H0 验收矩阵

本文件是 H0-C01～C12 与 H0-B001～B033 的唯一人可读权威定义。`error_id=NONE` 表示正向用例必须通过且不得产生错误。

## 信息架构与合同验收 H0-C01～C12

| ID | 验收内容 | expected | error_id |
| --- | --- | --- | --- |
| H0-C01 | 根路由和返回路径 | `/services/club-alliance`，返回 `/services` | `CAH0_ROUTE_INVALID` / `CAH0_RETURN_TARGET_INVALID` |
| H0-C02 | 四入口精确集合 | PC/SC/FC/UF action ID 各一次 | `CAH0_ACTION_SET_INCOMPLETE` / `CAH0_ACTION_SET_DUPLICATE` |
| H0-C03 | 顺序派生 | 从上游 sort_order 派生，模块不保存数值 | `CAH0_ACTION_ORDER_INVALID` / `CAH0_PRESENTATION_FIELD_COPIED` |
| H0-C04 | 单一展示真相源 | 不复制 label/target/access/lifecycle/telemetry 等字段 | `CAH0_PRESENTATION_FIELD_COPIED` |
| H0-C05 | 管理中心边界 | `club-manage` 单独存在且不进入四分类 | `CAH0_MANAGEMENT_ENTRY_MISSING` / `CAH0_MANAGEMENT_MIXED_WITH_CATEGORIES` |
| H0-C06 | query 兼容解析 | 无 query=home；合法中文 category 唯一映射；异常失败关闭 | `CAH0_QUERY_UNKNOWN` / `CAH0_QUERY_BLANK` / `CAH0_QUERY_AMBIGUOUS` |
| H0-C07 | 导航可重复 | 直达、刷新、后退、返回结果确定，不调用业务 API | `CAH0_ROUTE_INVALID` |
| H0-C08 | 生命周期与权限 | 只消费上游 access/lifecycle，管理保留 `club:manage` | `CAH0_UPSTREAM_CONTRACT_INVALID` |
| H0-C09 | 统一状态与响应式 | 状态集合完整，布局标准为 H1 输入而非 H0 实现 | `CAH0_HOMEPAGE_INVALID` |
| H0-C10 | 遥测 | 使用上游 telemetry 引用，不复制或伪造事件名 | `CAH0_PRESENTATION_FIELD_COPIED` |
| H0-C11 | 能力边界 | required/optional/forbidden 互斥，H0 只消费五项基础能力，商业全 forbidden | `CAH0_CAPABILITY_REQUIRED_FORBIDDEN_CONFLICT` / `CAH0_COMMERCIAL_CAPABILITY_ENABLED` |
| H0-C12 | 关系、决策与递归门禁 | UF 独立关系、决策引用存在、H1/业务严格后置 | `CAH0_RELATIONSHIP_KIND_INVALID` / `CAH0_DECISION_REFERENCE_MISSING` |

## 可执行一致性验收 H0-B001～B033

| ID | 场景 | expected | error_id |
| --- | --- | --- | --- |
| H0-B001 | 基线全部合同 | pass | `NONE` |
| H0-B002 | 上游动作合同不可解析 | fail closed | `CAH0_UPSTREAM_CONTRACT_INVALID` |
| H0-B003 | 缺少一个四入口 | reject | `CAH0_ACTION_SET_INCOMPLETE` |
| H0-B004 | 四入口 action ID 重复 | reject | `CAH0_ACTION_SET_DUPLICATE` |
| H0-B005 | 非 accepted action 混入 | reject | `CAH0_ACTION_NOT_ALLOWED` |
| H0-B006 | 上游排序重复或非递增 | reject | `CAH0_ACTION_ORDER_INVALID` |
| H0-B007 | 缺少 club-manage | reject | `CAH0_MANAGEMENT_ENTRY_MISSING` |
| H0-B008 | club-manage 混入分类 | reject | `CAH0_MANAGEMENT_MIXED_WITH_CATEGORIES` |
| H0-B009 | category registry 复制 label | reject | `CAH0_PRESENTATION_FIELD_COPIED` |
| H0-B010 | category registry 复制 target | reject | `CAH0_PRESENTATION_FIELD_COPIED` |
| H0-B011 | registry 引用未知 action | reject | `CAH0_CATEGORY_UNKNOWN_ACTION` |
| H0-B012 | registry action 重复 | reject | `CAH0_CATEGORY_DUPLICATE_ACTION` |
| H0-B013 | 任一 selector 被构造为 Pending 却标 executable | reject | `CAH0_SELECTOR_PENDING_EXECUTABLE` |
| H0-B014 | capability 缺 owner | reject | `CAH0_CAPABILITY_OWNER_MISSING` |
| H0-B015 | capability 缺 contract refs | reject | `CAH0_CAPABILITY_CONTRACT_MISSING` |
| H0-B016 | capability 缺 dependency refs | reject | `CAH0_CAPABILITY_DEPENDENCY_MISSING` |
| H0-B017 | capability 缺 evidence refs | reject | `CAH0_CAPABILITY_EVIDENCE_MISSING` |
| H0-B018 | capability 缺五维 readiness | reject | `CAH0_CAPABILITY_READINESS_MISSING` |
| H0-B019 | required 与 forbidden 冲突 | reject | `CAH0_CAPABILITY_REQUIRED_FORBIDDEN_CONFLICT` |
| H0-B020 | 支付能力被启用 | reject | `CAH0_COMMERCIAL_CAPABILITY_ENABLED` |
| H0-B021 | 首页保存 sort_order | reject | `CAH0_PRESENTATION_FIELD_COPIED` |
| H0-B022 | 根路由错误 | reject | `CAH0_ROUTE_INVALID` |
| H0-B023 | 返回路径错误 | reject | `CAH0_RETURN_TARGET_INVALID` |
| H0-B024 | 空白 category | fail closed | `CAH0_QUERY_BLANK` |
| H0-B025 | 未知 category | fail closed | `CAH0_QUERY_UNKNOWN` |
| H0-B026 | 同一 category 多义映射 | fail closed | `CAH0_QUERY_AMBIGUOUS` |
| H0-B027 | relationship schema 基线 | pass | `NONE` |
| H0-B028 | 关系 kind 不是 club-federation | reject | `CAH0_RELATIONSHIP_KIND_INVALID` |
| H0-B029 | 复用 FamilyAlliance | reject | `CAH0_FAMILY_ALLIANCE_REUSED` |
| H0-B030 | policy ref 未版本化 | reject | `CAH0_RELATIONSHIP_POLICY_UNVERSIONED` |
| H0-B031 | 关系缺配置时失败开放 | reject | `CAH0_RELATIONSHIP_FAIL_OPEN` |
| H0-B032 | 决策引用不存在 | reject | `CAH0_DECISION_REFERENCE_MISSING` |
| H0-B033 | 未知异常 | 失败关闭且不得掩盖已知错误 | `CAH0_INTERNAL_ERROR` |

## 判定规则

- 每个用例必须输出稳定 `error_id`、fixture ID、contract version 和 pass/fail。
- 已知错误优先于 `CAH0_INTERNAL_ERROR`；可附 `related_errors`，但主错误唯一。
- 删除错误 ID 或改变语义属于 breaking change，必须升级错误目录主版本。
- `D-CA-003` 已 Accepted；SC=`standard+general`、PC=`standard+charity`，服务端组合筛选为唯一权威。CA-H0 只冻结语义，SC selector 继续 `executable=false`；只有 CA-H1 或对应业务切片另行授权后才可启用消费。
- H0-B013 必须由 fixture 显式构造 `status=pending + executable=true`，不能依赖当前基线恰好为 Pending。
- H0 Full 证据必须同时包含模块合同、稳定负例、后端定向/全量回归、测试环境认证 HTTP 零串类与平台最终复核；release/operations 仍不由 H0 提升。
