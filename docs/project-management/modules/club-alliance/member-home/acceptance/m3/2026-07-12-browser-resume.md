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
| assets | JS=`/app/service-plaza/assets/index-DCYGiKy4.js`，现场 SHA-256=`ce2a254c66d46505260ef89f52c9acda0c0707a24a96d0f392cdfe42adaa3de7`，与冻结 M3 资产一致；CSS=`/app/service-plaza/assets/index-D_DJf1LN.css` |
| responsive | viewport 1280x720；body/document scrollWidth 均为 1265；本动作未发现页面级横向溢出 |
| visible structure | 四类入口与管理附属入口可见；当前是标准俱乐部首页结构，不是可判定的会员首页 DOM |
| network | 未读取 Authorization；未提交表单；未调用业务写接口；Statsig 初始化超时继续归类为浏览器插件控制噪声，不作为产品失败 |
| telemetry | 未触发用户动作，不要求业务 action event |
| server correlation | `/ready`=200；`/health?json=1` 返回 status=ok、db.connected=true、migrations=11、plugins=24。无凭据浏览动作未建立用户 API/DB 三方关联 |
| result | `Partial Pass / Member-home Unverified` |
| root cause | 浏览器 control-channel 已恢复，部署资产也与冻结 M3 hash 一致；无凭据显示标准首页符合当前前端仅在 authenticated+empty-query 时加载会员首页的实现条件 |
| next_action | 复用已批准合成身份建立可审计浏览器会话后补四身份 UAT；先重新核对 OTP 容量，禁止重复申请或读取/记录验证码和会话秘密 |

本证据只证明浏览器通道恢复和现有无凭据页面事实，不证明四身份 UAT、会员首页、权限或 lifecycle 场景通过。
