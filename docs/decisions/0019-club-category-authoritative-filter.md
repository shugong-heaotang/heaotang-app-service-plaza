# ADR 0019：俱乐部 type 与 category 使用服务端权威组合筛选

- 状态：Accepted
- 决策者：项目负责人
- 日期：2026-07-11

## 决策

自建俱乐部精确映射为 `type=standard AND category=general`；公益俱乐部保持 `type=standard AND category=charity`。`GET /api/v1/clubs/search` 的服务端 `type+category` 组合筛选是分页、计数和返回集合的唯一权威。禁止前端获取全部 standard 后本地筛选。

家庭俱乐部与 `club-federation` 不得落入 general/charity Club 分类。未知、空白或不支持的 category 失败关闭并返回稳定机器错误。混合 general/charity/family/其他类型数据必须证明零串类。

## 排除方案

- 仅按 `type=standard`：会把公益混入自建。
- 前端本地筛选：绕过服务端权威、分页和计数。
- 新增 SC ClubType：破坏既定 type/category 分层。

## 可证伪前提与复审

前提：现有 Club 模型能稳定表达 `standard+category`，category 为单值平面分类，数据库能保证组合筛选和索引一致性。

以下任一证据触发复审：general 无法兼容历史 standard 数据；category 变为多值或层级；组合筛选无法与分页/索引保持一致；公益不再共享 standard 组织生命周期。复审不允许在前端临时筛选绕行。

本 ADR 只关闭 D-CA-003 语义，不授权 CA-H1 或四类业务编码。
