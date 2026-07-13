# CA-SC T0 浏览器 UAT

- 环境：`https://heaotang.cn`
- APP source：`2c4b295e6fd625a2df24957f7b8becbc28ad1dcf`
- asset：`assets/index-6r_HRkaO.js`（SHA-256 `bfe4d9848d52ce4fac6d92edc3668bd78a20c7ca853301976fc6013d52038e99`）
- backend source：`98426ff83a1218080019faa377c152a81ecca437`
- fixture run：`club-sc-t0-20260712-100100`
- secrets：none-recorded
- 当前 verdict：`Conditional Pass`（产品主链通过；仅环境 Enter 为控制通道 Unverified）

| case_id | session | action | actual | server correlation | result |
| --- | --- | --- | --- | --- | --- |
| SC-B01 | guest | 从俱乐部联盟聚焦自建入口 | 页面显示 `authentication_required`，未发 SC 业务请求 | Nginx denylist 0 | Pass |
| SC-B02 | synthetic member | 打开自建列表 | 显示 5 个 active standard+general 样本；未显示 charity/family/direct/health/inactive | search 200，total=5，zero crossover | Pass |
| SC-B03 | synthetic member | 打开详情 | 显示合同允许字段；非自建详情 404 | detail 200 / non-SC 404 | Pass |
| SC-B04 | synthetic member | 提交加入申请 | 首次 201、同载荷重放 200、异载荷 409；并发仅一条 pending | API 与 DB 交叉 | Pass |
| SC-B05 | synthetic member | 打开本人申请 | 仅显示当前登录人的 pending 申请；第二合成用户隔离 | my-applications 200 | Pass |
| SC-B06 | guest + prior member evidence | 刷新自建深链 | 新标签刷新后 URL 保持，DOM 同时存在 heading、认证状态和主导航；此前会员本人申请刷新 GET 200 | DOM + HTTP | Pass |
| SC-B07 | guest | 浏览器后退 | 从联盟聚焦页返回 `/self-created/`，heading=`自建俱乐部` | no business mutation | Pass |
| SC-B08 | guest | 顶部返回俱乐部联盟 | 到达联盟页并保持自建聚焦 + `authentication_required` | no business mutation | Pass |
| SC-B09 | guest | 底部返回俱乐部联盟 | 可见文字区域真实点击成功；href 正确 | no business mutation | Pass |
| SC-B10 | guest | 320/360/768/1280 响应式 | 各视口 `body/document width == innerWidth`，无横向滚动，heading 正常 | no business mutation | Pass |
| SC-B11 | guest | Tab / focus-visible / ARIA | 真实 Tab 后顶部返回链接成为 activeElement；`focus-visible=true`，轮廓清晰，ARIA 名称与 href 正确 | no business mutation | Pass |
| SC-B12 | guest | Enter 激活焦点链接 | 现有 in-app 与 Windows 原生通道均不能可靠证明 Enter 已传递；真实鼠标点击与自动化共享首页 Enter 已覆盖 | none | Unverified（control-channel；非产品 No-Go） |

## 控制通道与产品故障区分

- `ab.chatgpt.com` Statsig 超时不影响 DOM、URL、Nginx 或业务 API，归类为浏览器控制层外部统计噪声。
- 底部返回首次未导航是默认几何中心未命中可见文字区；链接 href、可见区域点击和实际导航均已证明。
- 刷新缺口已由新标签真实 reload 后的 heading、认证状态和主导航 DOM 关闭；不把 guest DOM 写成登录态本人申请 DOM。
- Enter 经既有通道仍不能可靠传递，按浏览器证据规则停止扩大工具尝试。它保留为控制通道 `Unverified`，不得写成环境 Pass，也不推断为产品失败。

## 完成边界

- 页面主链、刷新、后退、双返回、响应式、Tab、focus-visible、heading/status/ARIA 均有真实环境证据。
- 环境 Enter 仅为工具通道未验证；自动化回归仍是产品键盘语义证据。该限制不授权削弱未来真实人工 UAT，也不扩大 T0 范围。
