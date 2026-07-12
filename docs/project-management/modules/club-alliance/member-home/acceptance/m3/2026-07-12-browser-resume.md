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

## 追加：无会话会员首页登录壳复核

- case_id：`CMH-M3-BR-RESUME-004`
- time：`2026-07-12`（Asia/Shanghai）
- target：`/app/service-plaza/services/club-alliance/member-home`
- session class：无会话；未读取或保存 Cookie、JWT、验证码或完整账号标识
- mutation：0
- secrets：`none-recorded`

| 字段 | 证据 |
| --- | --- |
| action | 新建应用内浏览器标签，单次直达会员首页路由，再只读读取可见 DOM。 |
| actual | 浏览器标签创建、导航和 DOM 读取均成功；无会话状态呈现手机号、验证码与登录控件，未出现会员首页数据或已认证 DOM。 |
| control channel | 仍出现浏览器插件自身的 Statsig 初始化超时；页面 DOM 可读取，因此该噪声不计为 APP 请求或产品失败。 |
| conclusion | 浏览器控制通道当前可用；认证态页面矩阵仍未验证。四个合成账号的本轮一次验证码授权已耗尽，不重复发送。 |
| next action | 等待 UTC 日容量自然恢复并取得下一轮明确授权后，先重新核对容量，再按一次一账号建立会话；禁止重部署、重跑已完成 fixture 或记录任何验证码/会话秘密。 |
