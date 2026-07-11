# CA-H1-M4-B002 管理入口权限失败关闭根因修复任务书

- 工作项：`AIW-20260711-CLUB-ALLIANCE-H1-M4-MANAGE-GUARD`
- 负责人：平台集成负责人
- 基线：`eb763f0a7342effb46a5bd0cc6a729a29cafeb26`
- 分支：`codex/club-h1-m4-manage-guard`
- 阶段：CA-H1 M4 阻断缺陷 B002；不包含俱乐部业务实现

## 目标

关闭测试环境发现的权限不一致：普通已登录用户点击管理中心时，遥测已正确记录
`blocked/scope_required`，但内部链接仍默认跳转到 `?view=manage`，而页面路由又忽略
`view`，最终显示首页而不是失败关闭状态。

## 必须实现

1. 已登录但缺少 scope 的内部链接必须阻止默认导航，同时保留 blocked 遥测和权限事件。
2. 未登录的 shared-session 入口继续允许进入登录或无权限承接页，不得破坏生命导航等既有主链。
3. `view=manage` 必须由上游 `club-manage` target 确定性解析。
4. guest 直达管理视图显示 `authentication_required`；已登录缺 `club:manage` 显示
   `scope_required`；具备该 scope 才进入 management focused 状态。
5. 空白、未知、重复或与 category 混用的 view 必须使用稳定错误 ID 失败关闭。
6. 管理入口仍是附属入口，不得变成第五类，也不得调用任何俱乐部业务 API。

## 验收

- ActionControl 回归证明 scope 缺失不导航、权限通过仍按合同目标导航。
- adapter 回归证明管理 target、合法 view 和全部负例。
- Route/Page 回归证明三种身份状态、blocked 遥测、URL 与页面状态一致。
- 定向测试、前端全量测试、生产构建、测试服构建、服务广场合同、治理、UTF-8 和
  `git diff --check` 全部通过。
- 修复提交集成和部署后，M4 必须重新执行页面、事件和服务端记录三方 UAT；本地通过不等于 M4 Go。

## 禁止范围

禁止后端、Schema、四类俱乐部业务、生产、真实资金、权限提升、重复验证码申请以及放宽验收标准。
