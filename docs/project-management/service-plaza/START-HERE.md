# 服务广场项目推进从这里开始

本文档是服务广场项目的执行入口。所有开发和接续工作先读根目录 `README.md`，再按本文档推进。

全项目依赖顺序和业务开发准入以 `docs/project-management/dependency-driven-master-plan-v1.md` 为准。

## 一、当前阶段

- 服务广场两层标准已经定版：服务接入清单 `service-plaza.v1` 和页面动作清单 `service-plaza.action.v1`。
- 单页 20 个动作已全部目录驱动；测试环境现场验收为 20 项、20 个唯一 ID，规划项统一禁用。
- 服务目录 9 项和页面动作 20 项已通过后端 API、前端、公开 Schema 和机器基线一致性验证。
- 当前仓库已有正式 React 前端、真实登录/JWT、三项 Go API 适配层、51 项前端测试和后端全量测试。
- 三项真实写入、原子幂等、请求关联 ID 与跨用户健康数据隔离已经通过远程验收。
- 当前目标是完成 ADR 0006 的 L4-L5/F6-F8 剩余基础设施，板块暂不扩写未冻结的业务功能。

## 二、唯一执行顺序

1. 阅读根目录 `README.md`，确认架构边界和门禁规则。
2. 阅读 `project-status-one-page.md`，确认当前事实和阻塞。
3. 阅读 `current-week-command-board.md`，只领取一个最小可交付切片。
4. 开发前查看 `docs/decisions/`，不得绕过已生效的 ADR。
5. 实现、测试并留下可复核证据。
6. 更新 Handoff、问题池、门禁状态和本入口的“最近接续记录”。

不再为了推进而新增重复台账。只有新的事实、决策、风险或验收证据才能进入项目文档。

## 三、当前最小开发切片

当前最小切片是 `common-infrastructure-plan-v1.md` 的 F6 至 F8：

1. 业务 API 适配器模板与契约版本差异门禁。
2. 动作事件集中采集和功能开关。
3. 备份恢复与部署失败自动回滚演练。
4. 共享页面状态和板块接入模板收口。

## 四、门禁口径

| 门禁 | 当前结论 | 解除条件 |
| --- | --- | --- |
| F1 接口标准 | Go | 两份 v1 契约、20 项动作、9 项目录、测试环境和公开 Schema 均已验证 |
| F2 内部身份与会话 | Go | v1 信封、真实 scopes、原子验证码与远程验收通过 |
| F3 统一 API SDK | Go | 超时、取消、严格信封、关联 ID、受控重试和回归测试通过 |
| F4 内部动作与权限 | Go | 生命周期、目标协议、真实 scope 和权限审计事件通过 |
| F5 写入可靠性 | Go | 三项原子幂等、竞态、日限额和远程回放通过 |
| F6 板块并行准入 | Partial Go | 自检工具已有；适配器模板和版本差异门禁待完成 |
| F7 可观测性与配置 | Partial Go | request ID 已有；集中动作遥测和功能开关待完成 |
| F8 发布恢复 | Partial Go | 发布/备份/回滚代码已有；恢复和失败回滚演练待留证 |
| 外部合作认证 | No-Go | OIDC/PKCE、域名白名单和合规专项未完成 |

## 五、编码与 PowerShell 规则

- Markdown、JSON、YAML、HTML、CSS、JavaScript、TypeScript 使用 UTF-8 无 BOM 和 LF。
- PowerShell 脚本使用 UTF-8 BOM 和 CRLF。
- PowerShell 会话先执行 `scripts/Initialize-PowerShellUtf8.ps1`。
- 执行项目脚本优先使用 `scripts/Invoke-ProjectPowerShell.ps1`。
- 提交前运行 `scripts/Test-TextEncoding.ps1`，发现乱码、错误 BOM 或 PowerShell 解析错误时不得提交。

## 六、Handoff 最小记录

每次接续至少记录：日期、执行角色、范围、已完成、未完成、阻塞、门禁变化、验证证据、下一步和变更文件。

## 七、最近接续记录

- 日期：2026-07-10
- 执行角色：Codex 总架构与执行 Agent
- 范围：依赖驱动总计划、内部公共基础设施 A 批次、测试环境部署与远程验收
- 已完成：F1；内部 F2-F5；自检工具第一版；51 项前端测试；后端全量测试；远程幂等、隔离和关联 ID 验收；SP-H006。
- 未完成：F6-F8 剩余项、外部 OIDC/PKCE、三大板块业务需求冻结。
- 下一步：按 `current-week-command-board.md` 完成适配器模板、版本差异门禁、集中遥测、功能开关和恢复演练。
