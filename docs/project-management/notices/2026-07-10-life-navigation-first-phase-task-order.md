# 生命导航第一阶段开发任务通知书

通知编号：`LN-TASK-20260710-001`
下达人：服务广场平台集成负责人
承接人：生命导航负责人
父项目：和奥堂 APP 服务广场
子项目：生命导航 `application-history`
预计有效工程时间：5–7 小时，按检查点推进
当前状态：待项目负责人审阅，尚未正式下达

## 一、任务目标

独立完成生命导航首切片：登录用户从 `/services/life-navigation` 提交导航申请，查看且只能查看本人申请历史，获得加载、空、成功、错误、限额和重放反馈，并可返回 `/services`。

平台集成负责人不代做板块业务，只负责公共接口、阶段抽查、门禁和最终验收。

## 二、固定接口

| 项目 | 标准 |
|---|---|
| 服务 ID | `life-navigation` |
| 页面入口 | `/services/life-navigation` |
| 返回路径 | `/services` |
| 新建记录 | `POST /api/v1/life-nav/records` |
| 本人历史 | `GET /api/v1/life-nav/records?limit=<1..30>` |
| 认证 | 平台共享 JWT；接口从会话取用户 ID |
| 写入可靠性 | 必须提供 `Idempotency-Key` |
| 记录类型 | `application` |
| 请求字段 | `dimension_id`、`record_type`、`title`、`note` |
| 成功语义 | 首次创建 201；同键同载荷重放 200 并带 `Idempotency-Replayed: true` |
| 关键错误 | `INVALID_IDEMPOTENCY_KEY`、`IDEMPOTENCY_KEY_REUSED`、`IDEMPOTENCY_IN_PROGRESS`、`LIFE_RECORD_DAILY_LIMIT` |
| 权限 | 只读本人数据；前端判断不能替代后端归属过滤 |

上述公共接口不得由板块 Agent 私自改变；发现不满足需求时提交接口变更请求。

## 三、技术与治理标准

- 前端：TypeScript strict、React、Vite、Vitest/Testing Library，调用共享 API adapter。
- 后端：Go、Fiber、database/sql，写入授权且幂等；已有接口满足契约时不得重复实现。
- 验证：Python 3、JSON Schema；Windows 自动化为 PowerShell 5.1 UTF-8。
- 依赖精确锁定，禁止 `latest`；不得复制认证、重试、错误解析或公共接口实现。
- 执行 `$heaotang-project-preflight`，完成模块检查单和 100 分随机考试。
- 遇到问题先关闭根因和回归，禁止降低门禁换取表面成功。

## 四、前置条件

1. 平台依赖：`contracts/foundation/module-dependencies/life-navigation.v1.json` 全部 ready。
2. 内部依赖：`contracts/modules/life-navigation/internal-dependencies.v1.json` 为 `development_readiness=go`。
3. 独立工作项、`codex/life-navigation-application-history` 分支和独立工作树已登记。
4. 起飞检查单覆盖平台 core 与 life-navigation overlay。
5. 随机治理考试 8/8、100 分通过。

任一条件不满足，不得开始业务代码。

## 五、允许与禁止修改范围

允许：

- `app/src/modules/life-navigation/`
- 经平台批准的生命导航页面测试与模块样式
- `backend-go/plugins/life-navigation-plugin/`（仅当 M1 证明真实缺口）
- 生命导航项目 README、实施记录和 Handoff

禁止直接修改：

- `contracts/foundation/`、`contracts/service-plaza/`
- 共享认证、API SDK、幂等、响应信封和部署基础设施
- 俱乐部、健康和其他业务模块
- 生产环境、真实资金和不可逆数据

## 六、M0–M4 小阶段门禁

### M0：起飞认证（约 30–45 分钟）

交付：工作项/工作树证据、模块检查单、100 分考试、两层依赖验证。
平台检查：身份、分支、范围、哈希和成绩。
通过前不得编辑业务代码。

### M1：接口事实与适配设计（约 45–60 分钟）

交付：现有 GET/POST 请求响应夹具、错误码、所有权与幂等测试证据、前端适配器设计。
平台检查：是否复用公共 adapter，是否出现契约漂移或重复实现。
这一阶段不做大面积 UI 修改。

### M2：历史数据适配（约 60–90 分钟）

交付：类型化列表 API、加载/空/错状态模型、适配器单元测试；若后端有真实缺口，提交最小根因修复和 Go 回归。
平台抽查：本人归属、错误信封、取消/超时和无重复认证逻辑。

### M3：页面闭环（约 90–120 分钟）

交付：申请表单、本人历史列表、状态反馈、返回路径和组件测试。
平台抽查：未登录、空、成功、重放、限额、错误恢复及文案合规。

### M4：集成与验收（约 60–90 分钟）

交付：全量测试、构建、UTF-8/契约门禁、测试环境部署、真实登录 UAT、实施记录和 Handoff。
平台验收：接口无破坏性变化、跨用户隔离、远端主链路、回滚路径和证据完整。

每个阶段通过后才能进入下一阶段；不得把 M0–M3 全部做完后一次性交验。

## 七、签收回执

正式下达后，生命导航负责人必须先填写：

- 通知编号与工作项 ID
- 负责人和接收时间
- 专用分支、工作树和基线提交
- 是否已理解目标、非目标、允许范围和禁止范围
- 是否发现接口或依赖冲突
- M0 预计提交时间

回执文件：`docs/project-management/modules/life-navigation/task-receipt.md`。未签收不得生成 M0 成绩。

## 八、阶段验收与抽查机制

每一阶段使用唯一验收单号：`LN-M0-001` 至 `LN-M4-001`。板块负责人提交阶段 Handoff 后停止进入下一阶段的业务修改；平台集成负责人复跑关键测试并给出 `Go` 或 `No-Go`。

平台目标在收到完整证据后 30 个有效工作分钟内完成抽查。等待期间板块负责人可以整理文档和测试证据，但不得提前实施下一阶段。

统一表单：`docs/project-management/modules/life-navigation/checkpoint-handoff-template.md`。

## 九、接口变更申请

如果固定接口不能满足需求，生命导航负责人不得直接修改公共契约。必须提交：

- 当前契约和具体缺口
- 为什么模块内适配不能解决
- 影响的消费者和兼容性风险
- 建议方案、迁移、测试与回滚范围
- 是否阻塞当前检查点

统一表单：`docs/project-management/modules/life-navigation/interface-change-request-template.md`。平台集成负责人决定拒绝、模块内解决、兼容扩展或新主版本。

## 十、问题即时上报

发现以下问题立即停止受影响工作并上报，不得积累到 M4：

- 身份、越权、跨用户数据或敏感信息问题
- 契约与运行时不一致
- 同类问题第二次出现
- 数据迁移、幂等、并发或不可恢复风险
- 需要修改受保护平台路径
- 生产、真实资金、不可逆数据或关键业务范围变化

上报必须写明事实、复现、影响范围、已排除原因和建议下一步；不得只写“有问题”。

## 十一、完成标准

- 用户可完成入口—申请—本人历史—返回的完整主链路。
- 其他用户记录不可见；重复提交、限额和网络错误有确定反馈。
- 自动化测试、构建、契约、编码和测试环境 UAT 全部通过。
- 不包含本切片非目标，不产生价格、AI 或专业结论硬编码。
- M0–M4 Handoff、实现记录、检查单和考试记录完整。
