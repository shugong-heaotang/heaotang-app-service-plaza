# 服务广场平台事实回填与复核路径控制记录

日期：2026-07-10

本文件用于说明 FE-PLAT-001 环境与路由事实一旦形成后，如何从“待提交”进入“待复核”。它不制造事实，也不替代 `fact-evidence-submission-packet.md`、`fact-evidence-intake-review.md` 或 `fact-evidence-review-run-log.md`。

## 一、当前结论

| 项目 | 结论 |
| --- | --- |
| 控制范围 | FE-PLAT-001 / EV-PLAT-001 / P0-RUN-001 / FR-PLAT-001 |
| 当前状态 | 待提交 |
| 当前是否允许待复核 | 否 |
| 当前是否允许 FR-PLAT-001 复核 | 否 |
| 当前门禁影响 | 首次真实联调 No-Go；第一阶段验收 No-Go |
| 本记录作用 | 定义真实证据出现后的回填、接收、复核和退回路径 |

## 二、进入回填的最低事实

| 字段 | 最低事实要求 | 不可接收内容 |
| --- | --- | --- |
| 环境名称 | 明确是联调、测试或临时验收环境 | 只写“测试环境待定” |
| 环境地址 | 可访问地址、部署说明或本地可复核启动方式 | 只有口头说明或待补链接 |
| 服务广场入口 | App 或前端工程中的入口位置、导航位置或页面路径 | 只有产品原型截图 |
| 生命导航路由 | 正式路由或临时承接页实现位置 | 只有 `/services/life-navigation` 建议 |
| 俱乐部联盟路由 | 正式路由或临时承接页实现位置 | 只有 `/services/club-alliance` 建议 |
| 健康大管家路由 | 正式路由或临时承接页实现位置 | 只有 `/services/health-manager` 建议 |
| 第一轮采用方案 | 明确第一轮采用正式路由还是临时承接页 | 只写“建议临时页” |
| 证据位置 | 文件路径、部署链接、截图或日志位置，能被复核 | 只有台账、ADR 或空模板 |

## 三、回填顺序

| 顺序 | 动作 | 回填文件 | 完成条件 |
| --- | --- | --- | --- |
| 1 | 填写 FE-PLAT-001 原始事实 | `platform-fact-submission-worksheet.md` | 八个字段都有真实事实和证据位置 |
| 2 | 同步路由与入口事实 | `routing-and-temporary-page-spec.md`、`integration-checklist.md` | 建议路由被真实实现或临时页实现替代 |
| 3 | 同步平台条件证据 | `platform-condition-evidence-runbook.md` | EV-PLAT-001 从缺口说明变为有证据位置 |
| 4 | 填写平台事实提交包 | `fact-evidence-submission-packet.md` | 提交包字段完整，目标回写文件明确 |
| 5 | 接收状态进入待复核 | `fact-evidence-intake-review.md` | FE-PLAT-001 从待提交改为待复核 |
| 6 | 启动审计复核 | `fact-evidence-review-run-log.md` | FR-PLAT-001 从未提交改为按事实复核 |
| 7 | 门禁只接收复核结果 | `phase-gate-evidence-matrix.md`、`first-integration-go-checklist.md` | 仅作为门禁输入，不自动解除 No-Go |

## 四、退回条件

| 退回场景 | 退回结论 | 下一步 |
| --- | --- | --- |
| 缺环境地址 | FE-PLAT-001 保持待提交 | 补环境地址或部署说明 |
| 缺服务广场入口 | FE-PLAT-001 保持待提交 | 补入口位置和访问方式 |
| 三个核心服务任一缺路由或临时页实现 | FE-PLAT-001 保持待提交 | 补缺失服务的实现位置 |
| 只有建议路由、原型、ADR 或台账 | 不接收为待复核事实 | 回到 `day-1-environment-route-run-record.md` 结论 |
| 提交包字段不完整 | 退回补充 | 回填 `platform-fact-submission-worksheet.md` |
| 证据位置不可复核 | 退回补充 | 补可访问链接、文件路径、截图或日志 |
| 目标回写文件不明确 | 退回补充 | 补回写文件和对应字段 |

## 五、允许触发 FR-PLAT-001 的条件

| 条件 | 是否必须 |
| --- | --- |
| FE-PLAT-001 八个字段均有事实 | 是 |
| 至少一个可复核证据位置能证明环境和入口 | 是 |
| 三大核心服务均有正式路由或临时承接页实现位置 | 是 |
| `platform-fact-submission-worksheet.md` 已回填 | 是 |
| `fact-evidence-submission-packet.md` 平台事实提交包已填写 | 是 |
| `fact-evidence-intake-review.md` 已从待提交改为待复核 | 是 |
| FE-PLAT-002 至 FE-PLAT-005 全部完成 | 否；但未完成时仍不能触发 FE-GATE |

## 六、门禁边界

| 事项 | 规则 |
| --- | --- |
| FR-PLAT-001 通过 | 只证明 FE-PLAT-001 环境与路由事实已通过复核 |
| FE-PLAT-001 通过但 FE-PLAT-002 至 FE-PLAT-005 未通过 | 首次真实联调仍 No-Go |
| FE-PLAT 全部通过但 FE-MOD 或 FE-HO 未通过 | 首次真实联调仍 No-Go |
| FE-PLAT、FE-MOD、FE-HO 全部通过 | 先进入 FE-GATE 触发判定，不自动 Go |
| FE-GATE 未通过 | 不进入真实联调，不触发 FE-ACC |

## 七、当前执行结论

截至 2026-07-10，本回填路径已建立，但 FE-PLAT-001 仍未具备可回填事实。当前不得把 `fact-evidence-submission-packet.md` 平台事实提交包写为待复核，不得把 `fact-evidence-intake-review.md` 的 FE-PLAT-001 改为待复核，不得启动 `fact-evidence-review-run-log.md` 的 FR-PLAT-001。首次真实联调和第一阶段验收继续 No-Go。
