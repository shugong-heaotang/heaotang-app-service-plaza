# 服务广场板块事实提交工作表

日期：2026-07-09

本文件把 `module-fact-submission-action-pack.md` 中 FE-MOD-001 至 FE-MOD-003 的板块事实要求转成可填写工作表，用于准备 `fact-evidence-submission-packet.md` 的板块事实提交包。它不替代真实板块确认、页面、权限、后台处理、测试数据或验收责任证据。板块事实的接收和退回标准见 `module-fact-evidence-intake.md`。

## 一、使用规则

1. 本工作表只填写事实，不填写宣传描述、推荐项或待办。
2. 推荐主动作可以作为默认准备口径，但没有确认来源时仍保持待补事实。
3. 平台路由、账号、数据和返回路径仍按 `platform-fact-submission-worksheet.md` 处理，板块事实不能替代平台事实。
4. 板块事实通过后只进入 FE-MOD 复核，不自动关闭 Handoff，也不自动解除首次真实联调 No-Go。
5. 三个板块均未形成真实事实前，FE-BATCH-002 保持已核查但未接收。

## 二、FE-MOD-001 生命导航

| 字段 | 填写内容 | 当前状态 |
| --- | --- | --- |
| 是否采用推荐主动作“提交导航申请” | 待补事实 | 待提交 |
| 主动作确认来源 | 待补事实 | 待提交 |
| 页面方案 | 待补事实 | 待提交 |
| 页面或路由 | 待补事实 | 待提交 |
| 登录要求 | 待补事实 | 待提交 |
| 会员权限规则 | 待补事实 | 待提交 |
| 无权限状态 | 待补事实 | 待提交 |
| 后台处理方式 | 待补事实 | 待提交 |
| 正常测试数据 | 待补事实 | 待提交 |
| 空状态测试数据 | 待补事实 | 待提交 |
| 异常测试数据 | 待补事实 | 待提交 |
| 验收责任 | 待补事实 | 待提交 |
| 证据位置 | 待补事实 | 待提交 |
| 回写文件 | `core-service-main-action-confirmation.md`、`module-intake-cards.md`、`fact-evidence-submission-packet.md` | 待回写 |

## 三、FE-MOD-002 俱乐部联盟

| 字段 | 填写内容 | 当前状态 |
| --- | --- | --- |
| 是否采用推荐主动作“申请加入俱乐部” | 待补事实 | 待提交 |
| 主动作确认来源 | 待补事实 | 待提交 |
| 页面方案 | 待补事实 | 待提交 |
| 页面或路由 | 待补事实 | 待提交 |
| 登录要求 | 待补事实 | 待提交 |
| 会员权限规则 | 待补事实 | 待提交 |
| 无权限状态 | 待补事实 | 待提交 |
| 审核规则 | 待补事实 | 待提交 |
| 管理中心附属操作边界 | 待补事实 | 待提交 |
| 后台处理方式 | 待补事实 | 待提交 |
| 正常测试数据 | 待补事实 | 待提交 |
| 空状态测试数据 | 待补事实 | 待提交 |
| 异常测试数据 | 待补事实 | 待提交 |
| 验收责任 | 待补事实 | 待提交 |
| 证据位置 | 待补事实 | 待提交 |
| 回写文件 | `core-service-main-action-confirmation.md`、`module-intake-cards.md`、`fact-evidence-submission-packet.md` | 待回写 |

## 四、FE-MOD-003 健康大管家

| 字段 | 填写内容 | 当前状态 |
| --- | --- | --- |
| 是否采用推荐主动作“提交健康咨询” | 待补事实 | 待提交 |
| 主动作确认来源 | 待补事实 | 待提交 |
| 页面方案 | 待补事实 | 待提交 |
| 页面或路由 | 待补事实 | 待提交 |
| 登录要求 | 待补事实 | 待提交 |
| 会员权限规则 | 待补事实 | 待提交 |
| 无权限状态 | 待补事实 | 待提交 |
| 后台处理路径 | 待补事实 | 待提交 |
| 正常测试数据 | 待补事实 | 待提交 |
| 空状态测试数据 | 待补事实 | 待提交 |
| 异常测试数据 | 待补事实 | 待提交 |
| 验收责任 | 待补事实 | 待提交 |
| 证据位置 | 待补事实 | 待提交 |
| 回写文件 | `core-service-main-action-confirmation.md`、`module-intake-cards.md`、`fact-evidence-submission-packet.md` | 待回写 |

## 五、提交判断

| 检查项 | 当前判断 | 动作 |
| --- | --- | --- |
| FE-MOD-001 是否具备事实 | 否 | 待补事实 |
| FE-MOD-002 是否具备事实 | 否 | 待补事实 |
| FE-MOD-003 是否具备事实 | 否 | 待补事实 |
| 板块事实接收表是否通过 | 否 | `module-fact-evidence-intake.md` 当前均待提交 |
| 是否允许提交板块事实包 | 否 | 不填写提交结论为待复核 |
| 是否允许触发 Handoff 质量复核 | 否 | 等待板块事实和平台事实 |
| 是否允许触发 FE-GATE | 否 | 继续 No-Go |

## 六、回写关系

| 来源 | 目标 | 当前动作 |
| --- | --- | --- |
| 本工作表 | `fact-evidence-submission-packet.md` 板块事实提交包 | 三项板块事实完整后再填写 |
| `fact-evidence-submission-packet.md` | `fact-evidence-intake-review.md` FE-MOD-001 至 FE-MOD-003 | 提交后进入待复核或退回补充 |
| `fact-evidence-intake-review.md` | `fact-evidence-review-run-log.md` FR-MOD | 审计 Agent 复核 |
| FR-MOD 复核结果 | `handoff-quality-review.md`、`phase-gate-evidence-matrix.md`、`first-integration-go-checklist.md` | 只作为 Handoff 和门禁判断输入，不自动 Go |
