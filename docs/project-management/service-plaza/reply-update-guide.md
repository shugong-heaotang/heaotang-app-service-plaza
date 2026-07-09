# 服务广场确认结果回写指南

本指南说明确认结果形成后如何更新项目台账。当前项目不使用“发送、回执、催办”的多人链路，统一采用“确认、证据、完整性复核、台账回写、门禁复核”。

## 一、处理顺序

1. 在 `reply-intake-tracker.md` 登记确认结果。
2. 在 `reply-completeness-review.md` 判断信息是否完整。
3. 信息不完整时，登记为“待补齐”，进入 `reply-followup-cadence.md`。
4. 信息完整时，按 `reply-ledger-update-checklist.md` 逐条回写对应台账。
5. 更新 `issue-pool.md`、`round-1-signoff-checklist.md`、`phase-gate-status.md` 和 `round-1-readiness-report.md`。
6. 门禁变化必须同步 `phase-gate-evidence-matrix.md` 和 `first-integration-go-checklist.md`。

## 二、负责人和责任边界回写

| 文件 | 回写内容 |
| --- | --- |
| `owner-roster.md` | 项目负责人、平台 Agent、板块 Agent、验收 Agent 的责任边界 |
| `round-1-signoff-checklist.md` | 启动确认和签核状态 |
| `role-action-list.md` | 下一步行动和状态 |
| `issue-pool.md` | SP-I001、SP-I002 等阻塞状态 |

RPLY-001 完整后，可以先回写“项目负责人临时承担总架构推进职责”。这只解除责任边界的一部分，不解除首次真实联调 No-Go。

## 三、核心服务回写

核心服务确认完整后，更新：

- `core-service-main-action-confirmation.md`
- `round-1-handoff-forms.md`
- `module-intake-cards.md`
- `routing-and-temporary-page-spec.md`
- `test-accounts-and-data.md`
- `round-1-signoff-checklist.md`

三大核心服务责任边界、主动作、页面方案、Handoff 和验收责任未完整前，单板块 Partial Go 也不能成立。

## 四、平台条件回写

平台条件确认完整后，更新：

- `integration-checklist.md`
- `routing-and-temporary-page-spec.md`
- `test-accounts-and-data.md`
- `round-1-integration-schedule.md`
- `phase-gate-status.md`
- `round-1-readiness-report.md`

路由、账号、数据、权限、返回路径任一项缺失时，首次真实联调保持 No-Go。

## 五、门禁规则

| 条件 | 门禁状态 |
| --- | --- |
| 负责人、主动作、路由、账号、数据、Handoff 均确认且通过复核 | 首次真实联调可改为 Go |
| 单个核心服务完整满足条件，其他服务阻塞清楚 | 可评估该服务 Partial Go |
| 任一 P0 条件缺失 | 首次真实联调保持 No-Go |
| 无真实联调记录、问题关闭和验收证据 | 第一阶段验收保持 No-Go |

## 六、完成汇总模板

```text
本次处理确认结果：
已更新文件：
完整事项：
待补齐事项：
已关闭问题：
仍阻塞问题：
当前门禁：
下一步动作：
```
