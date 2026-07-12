# 健康大管家 MVP-90 M1 C4-S04 安全冻结回执

- work_id：`AIW-20260712-HEALTH-M1-SECURITY-FREEZE`
- branch：`codex/health-m1-security-freeze`
- activation HEAD：`704bc82355b757e9a8d55ad97b736c729f233f9e`
- registration base：`d2608781af981d19021c36dd706f99ee041634b9`
- 执行角色：平台安全负责人
- 日期：2026-07-12
- 状态：`Handoff ready for independent platform review`

## 已完成

- C4-S04 技术安全范围裁决为 `Accepted`，但合同保持 `executable=false`。
- 冻结 7 类主体、12 类资源、11 组精确动作和 15 类服务端拒绝。
- 冻结最小审计字段、禁止日志字段、10 项威胁及验证方向、6 项可证伪前提和复审触发。
- 专业与隐私外部依赖分别记录为 `Pending with owner`，未代签。
- 只修改 registry 允许路径；未编写业务代码、未访问真实健康数据、未部署环境。

## 治理证据

- checklist：`contracts/modules/health-manager/development-checklists/2026-07-12-health-m1-security-freeze.json`
- exam：`contracts/modules/health-manager/governance-exams/2026-07-12-health-m1-security-freeze-attempt-1.json`，score 100
- implementation record：`contracts/modules/health-manager/implementation-records/2026-07-12-health-m1-security-freeze.json`

## Exact revision 负向变异证据

命令：以 Python 3 `jsonschema.Draft202012Validator` 读取 `security-authorization.v1.json` 和 `security-authorization.v1.schema.json`，对深拷贝合同依次执行下列六项变异并调用 `iter_errors`；任一负例无错误或 valid 有错误即非零退出。

结果：

- `valid`：ACCEPT
- `remove_ai_action`：REJECT
- `remove AuditEvent + duplicate resource`：REJECT
- `replace professional dependency`：REJECT
- `unknown subject reference`：REJECT
- `unknown resource reference`：REJECT
- `remove cross_member denial`：REJECT

Schema 现对 subjects 7、resources 12、actions 11、denials 15、threats 10、premises 6 使用精确数量、稳定 ID 白名单和逐 ID 唯一性约束；action subject/resource 引用与三项稳定 external dependency ID 同样失败关闭。decision 记录具体 decision maker，并以 work item、thread 和 owner role 三个引用追溯授权来源。

## 未完成和阻塞

- C4-H01 与 M1 窄模板专业会签仍由专业负责人完成。
- 隐私用途、保留、导出删除、AI 数据使用仍由隐私/法律负责人裁决。
- API、数据库、前后端、环境、部署、真实会员试运行均未授权、未验证。
- 模块目录中历史 M0 checklist 存在 current SHA 漂移；本工作项未修改历史不可变快照，平台应独立处理其“当前快照”口径。本任务自己的 checklist 与 exam 使用当前哈希。

## 请求平台独立复核

请平台复核：主体/资源/动作是否闭合、拒绝是否不枚举且失败关闭、审计失败是否阻止提交、AI 是否没有最终状态权、Schema 是否拒绝删减关键类别、外部依赖是否保持非可执行，以及所有变更是否严格位于 allowed paths。复核通过前不得激活 M1 业务实现。
