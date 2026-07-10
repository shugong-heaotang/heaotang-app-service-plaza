# 和奥堂 APP 服务广场 -- 总架构与开发规范

> 本文档是和奥堂 APP 服务广场项目的**唯一总入口**。
> 所有板块负责人、平台集成负责人、开发 Agent 在开始任何工作前，必须全文阅读本文档。
>
> **总架构负责人：** Codex（总架构 Agent）
> **最后更新：** 2026-07-10
> **部署测试服务器：** `https://heaotang.cn`

---

## 0. AI 开发强制启动顺序

任何人员或编程 Agent 第一次进入本项目，必须按顺序读取，未完成不得修改代码：

1. `AGENTS.md`：当前工作区不可违反的执行约束。
2. 本 `README.md`：项目边界、架构和当前开发入口。
3. `CONSTRAINTS.md`：根因优先、稳定依赖、配置双人审批、两次触发和实现记录硬约束。
4. `docs/project-management/service-plaza/project-status-one-page.md` 与 `docs/project-management/dependency-driven-master-plan-v1.md`：当前真实状态和执行顺序。
5. `contracts/foundation/foundation-capabilities.v1.json`：平台级能力依赖。
6. `contracts/foundation/engineering-standards.v1.json` 与 `docs/project-management/engineering-toolchain-standard-v1.md`：批准工具链和编码原则。
7. `contracts/foundation/recurring-issues.v1.json`：已经重复发生、不得再次局部修补的问题模式。
8. `contracts/foundation/agent-collaboration.v1.json` 与 `docs/project-management/ai-coding-incident-lessons-2026-07-10.md`：当前工作项所有权、隔离范围和外部事故防线。
9. `docs/project-management/recursive-project-governance-v1.md`：大小项目同制、父子职责和分段验收。
10. `docs/decisions/` 中与任务相关的 ADR，尤其 0007 至 0018。
11. 所属板块的项目 README、任务通知、`contracts/foundation/module-dependencies/*.json` 和 `contracts/modules/<module>/internal-dependencies.v1.json`。
12. `contracts/foundation/implementation-records/` 与对应 Handoff：前序实现依据和交接证据。

开始工作前运行：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/Test-AgentDevelopmentPreflight.ps1
```

随后确认自己拥有 `agent-collaboration.v1` 中唯一活动工作项，并使用 `scripts/New-AgentDevelopmentChecklist.ps1` 为本次实现生成逐项待勾选清单。脚本不会自动勾选；读取每个文件后记录 `checked=true`、`checked_at` 和当前哈希。历史清单保留当时快照，但不能被新任务复用；新任务始终重新读取和考试。

检查单完成后必须使用 `scripts/New-AgentGovernanceExam.ps1` 随机抽取 8 道场景题，并通过 `scripts/Submit-AgentGovernanceExam.ps1` 提交答案。必须 100 分；失败试卷保留，重读补课来源后生成下一次随机试卷。推荐统一执行 `$heaotang-project-preflight` Skill。

结束切片前必须运行契约、测试、构建和 UTF-8 门禁，并提交 `implementation-record.v1`。文档存在不代表已经采用；实现记录必须列出本次实际读取的治理输入。

---

## 1. 项目概述

**服务广场**是和奥堂 APP 的核心一级页面，位于底部导航"服务"入口。它承载三大核心服务（生命导航、俱乐部联盟、健康大管家）和常用服务入口。

### 1.1 当前阶段目标

当前阶段**不是继续调整服务广场架构**，而是在既定架构下**尽快完成系统主链路闭环**。

### 1.2 核心原则

| 原则 | 说明 |
|------|------|
| 结构锁定 | 服务广场布局已定版，不再调整核心信息架构 |
| 统一接入 | 各板块不能自行修改服务广场页面结构 |
| 单一入口 | 所有 Agent 按本 README 第 0 节读取治理基线，再读任务入口 |
| Handoff 强制 | 每个阶段切换必须有 Handoff 记录 |
| 门禁驱动 | 所有决策由 Go/Partial Go/No-Go 门禁驱动 |
| 大小项目同制 | 每个板块和重要切片均作为独立子项目，按短检查点交付 |

---

## 2. 架构决策（已定版）

### 2.1 服务广场布局（ADR 0001）

页面结构（从上到下）：页面标题区（商标+服务广场+AI按钮）-> 生命导航 -> 俱乐部联盟体系行 -> 健康服务主卡 -> 常用服务宫格

### 2.2 三大核心服务确认

生命导航：提交导航申请 | 俱乐部联盟：申请加入俱乐部 | 健康大管家：提交健康咨询

### 2.3 临时承接页决策（ADR 0003）

第一轮联调允许使用临时承接页。页面必须标注状态、包含主动作、支持权限状态展示、能返回服务广场。

---

## 3. 角色与职责

| 角色 | 主要责任 | 核心产出 |
|------|----------|----------|
| APP 总架构负责人 | 架构边界、主链路、跨板块规则和最终裁决 | 架构决策记录、验收结论 |
| 平台集成负责人 | 接口、路由、权限、联调、发布和问题关闭 | 接口清单、联调清单 |
| 各板块负责人 | 本板块内容、流程、页面、数据和验收 | 板块接入卡、Handoff 记录 |

### 3.1 Agent 分工

规划 Agent：拆阶段排优先级 | 执行 Agent：按清单推进 | 文档 Agent：更新规范记录 | 审计 Agent：检查一致性 | 决策 Agent：识别裁决事项

### 3.2 项目推进入口顺序

START-HERE.md -> agent-coordination-board.md -> current-week-command-board.md -> 门禁状态检查 -> 执行

---

## 4. Agent 协同机制

采用单人决策 + Agent 协同 + 本地台帐推进。Agent 之间通过文件、门禁和审计记录完成交接。

### Agent 交接格式

每次接续必须记录：处理日期、Agent、范围、已完成、未完成、阻塞、门禁变化、下一步建议、已更新文件。

### 升级规则

板块资料缺失 -> 板块 Agent 当日未补 -> 升级到项目负责人 | 接口/路由权限不清 -> 平台 Agent 当日未解决 -> 升级

---

## 5. Handoff 交接机制（强制）

每个板块从需求到上线都必须提交 Handoff 记录。没有 Handoff 记录不能进入下一阶段。

各阶段补充字段：需求给开发（接入卡+主动作+路由+权限+数据+验收标准）| 开发给联调（接口文档+路由+账号+数据+问题）| 联调给测试（测试范围+路径+异常+风险+验收负责人）| 测试给上线（上线内容+影响+回滚+验证项）

---

## 6. 质量管理规则

### Handoff 质量复核
- 提交人/接收人/提交时间必须填写
- 已完成/未完成/依赖/阻塞必须明确
- 平台可接收结论需明确

### 台帐一致性与门禁审计
每日推进结束、形成确认结果、Handoff 被退回、门禁变化时必须审计。

### 门禁证据矩阵
每个门禁的 Go/No-Go 必须有证据支撑。

---

## 7. 路由方案与临时承接页规范

路由统一使用 services 命名空间，三大核心服务路由：life-navigation、club-alliance、health-manager。

测试服务器：47.94.159.60 | 临时承接页：/app/service-plaza-temp.html | Go API：8080 端口 | 管理员：管理员测试账号（凭据通过安全渠道获取） | 权限：三级（公开/JWT/管理员）

---

## 8. 门禁状态与决策框架

平台 L0-L5：Go | 三大板块第一切片 development：Go | 三大板块 acceptance：Partial Go | 外部合作：No-Go | 第一阶段综合验收：No-Go

---

## 9. 工具与 Skills 评估

现有 Skills 已覆盖部署、验收、安全审计、浏览器验证、决策记录、PowerShell UTF-8 和外部专家建议。GitHub Plugin 已可用于后续 PR、CI 和安全审查；启用远程 Agent 协作前仍需现场确认分支保护、CodeQL、Secret Scanning 和依赖扫描设置。

---

## 10. 项目当前状态

服务广场正式前端、9 服务/20 动作契约、三大核心路由和 L0-L5 公共底座已在测试环境运行。三大板块第一切片已形成平台依赖、内部依赖和人类可读契约，均达到 development Go、acceptance Partial Go。

### 当前 P0 阻塞

- 平台内部开发无 P0 阻塞。
- 外部合作因 OIDC/PKCE、域名白名单、数据协议和退出方案未完成保持 No-Go。
- 第一阶段综合验收等待三大板块具体业务切片和跨板块主链路完成。

---

## 11. 下一步行动清单

1. 项目负责人协调首个具体板块；建议先做生命导航“申请与本人历史”最小切片。
2. 为首板块创建独立工作项、`codex/` 分支、工作树和模块起飞检查单。
3. 按已冻结契约实现、测试、部署和验收，不修改服务广场定版结构。
4. 依次关闭俱乐部本人申请状态、健康咨询历史等 acceptance Partial Go 缺口。
5. 完成跨板块主链路、压力、安全、恢复和第一阶段综合验收。

---

## 附录

关键文件：START-HERE.md、project-status-one-page.md、agent-coordination-board.md、current-week-command-board.md、phase-gate-status.md、first-integration-go-checklist.md

项目文档位于 docs/project-management/service-plaza/ 目录下。

### 正式前端工程

正式前端位于 `app/`，使用 React、TypeScript 和 Vite。当前提供 `/services` 及三大核心服务路由。

```powershell
cd app
npm install
npm test
npm run build
```

### Windows UTF-8 工作流

仓库编码规则由 `.editorconfig` 和 `.gitattributes` 统一约束。PowerShell 5.1 读取中文文件前先初始化 UTF-8 环境：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/Initialize-PowerShellUtf8.ps1
```

提交前执行编码门禁：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/Test-TextEncoding.ps1
```
