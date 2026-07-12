# H2-M3 浏览器通道恢复证据

- case_id：`CMH-M3-BR-RESUME-003`
- time：`2026-07-12 15:57:52 +08:00` / `2026-07-12T07:57:52Z`
- base URL：`https://heaotang.cn`
- target：`/app/service-plaza/services/club-alliance/`
- session class：无凭据、未读取会话内容
- mutation：0
- secrets：`none-recorded`

| 字段 | 证据 |
| --- | --- |
| action | 应用内浏览器新建标签并直达目标路由；随后只读 DOM 和页面属性 |
| expected | 浏览器控制通道可用；目标路由可读取；若会员首页已进入目标态，应存在唯一 `data-member-home-state` |
| actual | URL 精确到达目标；title=`和奥堂 - 服务广场`；可读 DOM；页面 heading 为“俱乐部联盟 / 选择俱乐部服务”；`data-member-home-state` 数量为 0 |
| assets | JS=`/app/service-plaza/assets/index-DCYGiKy4.js`；CSS=`/app/service-plaza/assets/index-D_DJf1LN.css` |
| responsive | viewport 1280x720；body/document scrollWidth 均为 1265；本动作未发现页面级横向溢出 |
| visible structure | 四类入口与管理附属入口可见；当前是标准俱乐部首页结构，不是可判定的会员首页 DOM |
| network | 未读取 Authorization；未提交表单；未调用业务写接口；Statsig 初始化超时继续归类为浏览器插件控制噪声，不作为产品失败 |
| telemetry | 未触发用户动作，不要求业务 action event |
| server correlation | 本只读动作未建立 Nginx/API/DB 三方关联；待部署/会话条件核对后补 |
| result | `Partial Pass / Member-home Unverified` |
| root cause | 浏览器 control-channel 已恢复；当前剩余问题转为部署路由或会话进入条件待核对，不能继续归因为浏览器不可用 |
| next_action | 核对 deployed asset 与批准 M3 基线；确认会员首页进入条件。未确认前不登录、不请求 OTP、不执行 fixture、不重复部署 |

本证据只证明浏览器通道恢复和现有无凭据页面事实，不证明四身份 UAT、会员首页、权限或 lifecycle 场景通过。
