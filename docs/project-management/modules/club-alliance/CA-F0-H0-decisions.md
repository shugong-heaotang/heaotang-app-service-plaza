# 俱乐部联盟 CA-F0/H0 决策记录

所有日期均为 2026-07-11。Accepted 决策者为项目负责人；Pending 决策只能保存建议和局部阻塞范围，不得转化为可执行语义。

## D-CA-001 公益俱乐部实体映射

- status：Accepted
- decision maker：项目负责人
- background：公益与自建当前都需要 Club 组织、成员和生命周期能力，但公益又必须能从普通 standard 数据中正向区分。
- decision：公益俱乐部是 Club 实体，使用 `type=standard + category=charity`。
- alternatives：新增 charity ClubType（边界重复）；复用 direct（语义错误）；只用前端标签筛选（非权威）。
- consequences：复用 standard 能力降低重复实现；代价是 category 必须由服务端权威维护并完成历史数据分类。
- premises：公益与自建共享 standard 组织、成员和生命周期底座，但需要正向 category 区分。
- falsification evidence：若公益被证明具有不兼容的独立 Club 生命周期、权限或数据责任，则该前提失效。
- review trigger/date：出现上述证据或每次 CA-PC 主版本升级时复审；最迟 CA-PC/P0。
- compatibility/migration：保持现有 standard 兼容；历史 charity 数据必须通过服务端权威分类验证。
- forbidden alternatives：新增 charity ClubType；复用 direct；前端全量 standard 后本地筛选。

## D-CA-002 友联体关系实体

- status：Accepted
- decision maker：项目负责人
- background：友联体表达多个既有俱乐部之间的联合关系，不应复制一个新的组织和成员生命周期。
- decision：友联体使用独立关系 `relationship_kind=club-federation`。
- alternatives：新建 ClubType（把关系错误实体化）；复用 FamilyAlliance（把 family 专属关系扩散为通用关系）；自由字符串关系（不可版本化）。
- consequences：Club 和 federation 生命周期解耦；代价是后续 CA-UF 需要独立关系存储、权限和迁移标准。
- premises：友联体连接既有 Club，不拥有独立 Club 成员和组织生命周期。
- falsification evidence：若真实需求证明友联体必须作为独立 Club 完成创建、成员、审核和解散生命周期，则触发复审。
- review trigger/date：首次 CA-UF/P0 或关系模型出现破坏性变化时复审。
- compatibility/migration：关系版本单独演进；不改变 ClubType；破坏性变化升关系主版本。
- forbidden alternatives：伪装为 ClubType；复用 FamilyAlliance；缺少版本政策时失败开放。

## D-CA-003 自建俱乐部精确分类

- status：Accepted
- decision maker：项目负责人
- decision date：2026-07-11
- background：旧 `type=standard` 同时可能承载普通和公益数据，无法在新增公益入口后继续作为自建的精确集合。
- decision：自建俱乐部精确映射为 `type=standard + category=general`；公益继续使用 `type=standard + category=charity`。`GET /api/v1/clubs/search` 的服务端 `type+category` 组合筛选是分页、计数和结果集合的唯一权威，禁止前端全量拉取 `standard` 后本地伪筛选。
- alternatives：standard 且 category 为空（未来需要脆弱的负向排除）；新增 self-created ClubType（破坏旧契约）；推荐的正向 general 分类。
- consequences：正向 general 分类能防止 charity、family、其他 ClubType 和 `club-federation` 串类；代价是历史 standard 数据必须审计迁移，不能自动猜测。
- premises：general 能正向标识普通自建 standard Club，并与 charity 及未来 category 隔离。
- falsification evidence：若 general 无法兼容历史 standard 数据、category 变为多值或层级分类、服务端组合筛选无法与分页/索引保持一致，或公益不再共享 standard 生命周期，则本决策失效。
- review trigger/date：出现任一 falsification evidence、首次 CA-SC/P0 数据迁移评审或 category 合同主版本变化时复审。
- compatibility/migration：旧 `type=standard` 可保留宽查询兼容；精确入口使用 type+category；缺 category 历史数据不得自动猜测，默认排除并进入待分类清单。
- forbidden alternatives：仅按 `type=standard`；用“排除 charity”伪造自建集合；前端本地筛选；新增 self-created ClubType；让 family 或 `club-federation` 进入 general/charity Club 分类。
- authority/evidence：ADR `0019-club-category-authoritative-filter`、合同 `club-category-filter.v1`、后端根因修复 `47ef91bb` 和 `SP-H028`。
- authorization boundary：本决策只关闭 D-CA-003 语义与 H0 Full 前置，不授权 CA-H1、前端消费或四类业务编码；category registry 的 selector 继续 `executable=false`。

## D-CA-004 先建设独立标准首页

- status：Accepted
- decision maker：项目负责人
- background：若从自建业务页直接起步，其列表、加入和状态逻辑会反向定义父入口，使其他三类只能被迫适配自建特例。
- decision：先完成独立标准首页/页面壳标准，再接入四个业务子项目；不得从自建业务页直接起步。
- alternatives：沿用自建页作为父页（最快但接口偏置）；四类各自独立入口（重复壳能力）；先标准首页再递归子项目（采用）。
- consequences：共同状态、权限和导航可复用；代价是业务页面实现前增加 H0/H1 两个门禁。
- premises：四子项目需要共同入口、状态、权限、导航和观测标准。
- falsification evidence：若上游不再存在统一俱乐部入口或四子项目完全独立发布，则复审父页面边界。
- review trigger/date：上游服务广场 IA 主版本变化时复审。
- compatibility/migration：H0 只定义合同；H1 另行授权实现；旧临时业务页通过适配迁移。
- forbidden alternatives：H0 修改前端；把某一业务页当作父首页；首页直接调用业务写 API。

## D-CA-005 单一展示真相源与顺序

- status：Accepted
- decision maker：项目负责人
- background：服务广场已拥有版本化 action 合同；模块若再次保存展示和顺序，会形成两份可能漂移的 IA。
- decision：四入口展示字段和顺序全部派生自 `service-plaza-actions.v1.json`；当前顺序为公益、自建、家庭、友联体。
- alternatives：模块复制完整 action（短期简单但漂移）；只复制 sort（仍是第二顺序源）；只保存 action ID 并运行时派生（采用）。
- consequences：上游兼容变更可自动传播；代价是上游合同失效时首页必须整体失败关闭，不能用本地默认值兜底。
- premises：上游动作合同稳定表达 action ID、展示、排序、target、权限、生命周期和 telemetry。
- falsification evidence：上游不再包含完整四入口、出现重复 ID/排序或合同失效。
- review trigger/date：上游 action 合同主版本变化或 service-plaza IA 决策变更时复审。
- compatibility/migration：模块只保存 action ID 和语义元数据；上游兼容变更自动派生；破坏性变化失败关闭。
- forbidden alternatives：复制 label/sort/target/access/lifecycle/telemetry；模块另建排序源；用口头列举覆盖上游。

## D-CA-006 管理中心不是第五类

- status：Accepted
- decision maker：项目负责人
- background：管理中心与四类入口共处同一区域，但它是具有 `club:manage` 权限的横切操作，不是业务分类。
- decision：`club-manage` 是附属操作入口，保持 preview + `club:manage`，显式排除于四分类。
- alternatives：作为第五类（污染分类）；并入每个子项目（重复操作入口）；独立附属操作（采用）。
- consequences：分类集合稳定为四个；代价是首页派生逻辑必须显式维护“分类集合”和“管理入口”两条选择规则。
- premises：管理能力横跨俱乐部实体，不代表新的业务类别。
- falsification evidence：若未来管理中心被定义为独立服务而非操作，则复审 service_id 和入口归属。
- review trigger/date：管理中心生命周期转 active 或路由主版本变化时复审。
- compatibility/migration：单独解析 management action；不改变四入口集合。
- forbidden alternatives：把管理中心计为第五类；去掉真实 scope；复用分类 selector。

## D-CA-007 能力状态与商业默认禁止

- status：Accepted
- decision maker：项目负责人
- background：boolean implemented 无法区分代码存在、测试验证、发布和运营；商业能力又会引入资金与合规风险。
- decision：能力使用八级状态；required/optional/forbidden 互斥；商业、支付、提现、退款、订阅首期一律 forbidden。
- alternatives：boolean 状态（证据层级丢失）；商业能力 planned（容易被误启用）；八级状态加默认 forbidden（采用）。
- consequences：每次状态提升可审计；代价是能力目录需要持续维护 owner、合同、依赖、证据和五维 readiness。
- premises：代码存在、测试、发布和运营是不同证据层级；商业能力需要独立资金与合规门禁。
- falsification evidence：只有独立正式任务、资金安全验收和发布证据才能改变 forbidden。
- review trigger/date：任何子项目提出商业化范围时立即复审。
- compatibility/migration：新增能力向后兼容；状态提升必须附证据；forbidden 改变须新决策。
- forbidden alternatives：boolean implemented；从 code-present 推导 Go；H0 暗中启用商业能力。
