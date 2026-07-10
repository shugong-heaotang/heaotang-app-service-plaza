# 服务广场单页动作契约 v1

协议标识：`service-plaza.action.v1`

本契约把服务广场单页中所有可操作控件统一为 20 项动作。它补充 `service-plaza.v1` 服务清单：服务清单描述“接入什么服务”，动作契约描述“页面上的哪一个控件以什么方式进入服务或执行平台动作”。

机器可读文件：

- Schema：`contracts/service-plaza/service-plaza-action.schema.json`
- 20 项基线清单：`contracts/service-plaza/service-plaza-actions.v1.json`

## 1. 字段标准

| 字段 | 规则 |
| --- | --- |
| `action_id` | 页面动作稳定唯一标识，发布后不得复用于其他动作 |
| `region` | `topbar`、`core_services`、`club_alliance`、`common_services`、`primary_navigation` |
| `sort_order` | 页面读取顺序，固定按 10 递增；不得用视觉 CSS 顺序覆盖语义顺序 |
| `label` | 用户可见或辅助技术可读名称 |
| `action_type` | `service_entry`、`service_variant`、`platform_command`、`primary_navigation` |
| `target` | `/` 开头的站内路由、审核后的 `https://` 地址或平台 `heaotang://` 命令 |
| `lifecycle_status` | `active`、`preview`、`planned`、`maintenance`、`offline` |
| `access` | 认证交接方式和最小 Scope；描述目标能力要求，不代表页面必须隐藏入口 |
| `service_id` | 可选；动作属于一个服务时必须与服务清单中的标识一致 |
| `return_target` | 完成、取消或失败后受平台治理的返回路径，本页动作统一为 `/services` |
| `telemetry_event` | 稳定、非敏感、逐动作唯一的行为事件名 |

## 2. 生命周期行为

- `active`、`preview`：允许执行导航或命令；`preview` 必须显示试用状态。
- `planned`：可以显示规划状态，但不得执行目标跳转或伪装成已交付能力。
- `maintenance`：保留入口并显示维护说明，不执行正式业务动作。
- `offline`：停止执行；是否继续展示由平台下线策略决定。
- 生命周期状态不能通过前端临时逻辑绕过，动作清单和页面行为必须一致。

## 3. 20 项逐项映射

| # | `action_id` | 区域 | 标签 | 类型 | 目标 | 状态 | `service_id` |
| ---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | `page-ai-assistant` | 顶部 | 页面 AI 助手 | 平台命令 | `heaotang://ai-assistant?context=service-plaza` | planned | — |
| 2 | `life-navigation` | 核心服务 | 生命导航 | 服务入口 | `/services/life-navigation` | active | `life-navigation` |
| 3 | `club-alliance` | 俱乐部联盟 | 俱乐部联盟 | 服务入口 | `/services/club-alliance` | active | `club-alliance` |
| 4 | `club-manage` | 俱乐部联盟 | 管理中心 | 服务变体 | `/services/club-alliance?view=manage` | preview | `club-alliance` |
| 5 | `public-benefit-club` | 俱乐部联盟 | 公益俱乐部 | 服务变体 | 俱乐部分类路由 | active | `club-alliance` |
| 6 | `self-created-club` | 俱乐部联盟 | 自建俱乐部 | 服务变体 | 俱乐部分类路由 | active | `club-alliance` |
| 7 | `family-club` | 俱乐部联盟 | 家庭俱乐部 | 服务变体 | 俱乐部分类路由 | active | `club-alliance` |
| 8 | `club-federation` | 俱乐部联盟 | 俱乐部友联体 | 服务变体 | 俱乐部分类路由 | active | `club-alliance` |
| 9 | `health-manager` | 核心服务 | 健康大管家 | 服务入口 | `/services/health-manager` | active | `health-manager` |
| 10 | `common-more` | 常用服务 | 更多 | 平台命令 | `heaotang://service-plaza/more` | planned | — |
| 11 | `activity-plaza` | 常用服务 | 活动广场 | 服务入口 | `/services/activity-plaza` | planned | `activity-plaza` |
| 12 | `network-center` | 常用服务 | 人脉中心 | 服务入口 | `/services/network-center` | planned | `network-center` |
| 13 | `protection-mall` | 常用服务 | 保障商城 | 服务入口 | `/services/protection-mall` | planned | `protection-mall` |
| 14 | `secondhand-market` | 常用服务 | 二手集市 | 服务入口 | `/services/secondhand-market` | planned | `secondhand-market` |
| 15 | `ai-assistant` | 常用服务 | AI | 服务入口 | `/services/ai-assistant` | planned | `ai-assistant` |
| 16 | `learning-plaza` | 常用服务 | 学习广场 | 服务入口 | `/services/learning-plaza` | planned | `learning-plaza` |
| 17 | `primary-home` | 主导航 | 首页 | 主导航 | `/` | planned | — |
| 18 | `primary-services` | 主导航 | 服务 | 主导航 | `/services` | active | — |
| 19 | `primary-discover` | 主导航 | 发现 | 主导航 | `/discover` | planned | — |
| 20 | `primary-profile` | 主导航 | 我的 | 主导航 | `/me` | planned | — |

分类路由的完整 URI 编码值以机器清单为准，禁止由显示文本临时拼接。

## 4. 计数与唯一性门禁

Schema 使用 20 个有序 `prefixItems` 固定动作位置、`action_id` 和 `sort_order`，同时设置 `minItems=20`、`maxItems=20` 和 `items=false`。因此缺项、增项、重复 ID、错序或排序漂移都会校验失败。

快速计数检查：

```powershell
$contract = Get-Content -LiteralPath contracts/service-plaza/service-plaza-actions.v1.json -Raw -Encoding UTF8 | ConvertFrom-Json
if ($contract.actions.Count -ne $contract.expected_action_count -or $contract.actions.Count -ne 20) {
    throw "服务广场动作数量必须为 20"
}
if (($contract.actions.action_id | Sort-Object -Unique).Count -ne 20) {
    throw "服务广场 action_id 必须逐项唯一"
}
```

正式门禁必须执行 JSON Schema Draft 2020-12 校验，不能只做数量检查。

## 5. 变更规则

- 调整标签、目标、权限、状态或事件名时，平台集成负责人必须评估对现有实现和埋点的兼容性。
- 新增、删除或重排这 20 项属于页面动作基线变更，必须先更新 Schema、清单、映射文档和测试证据。
- 改变核心信息架构、核心服务范围或底部主导航属于重大变更，按 ADR 0005 交由 APP 总架构负责人审批。
- 任何动作进入 `active` 前必须验证目标、权限、返回路径和遥测事件；未验证不能推断为通过。
