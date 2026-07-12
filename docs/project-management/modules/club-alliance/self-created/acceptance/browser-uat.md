# CA-SC T0 浏览器 UAT

- 环境：`https://heaotang.cn`
- APP source：`2c4b295e6fd625a2df24957f7b8becbc28ad1dcf`
- asset：`assets/index-6r_HRkaO.js`（SHA-256 `bfe4d9848d52ce4fac6d92edc3668bd78a20c7ca853301976fc6013d52038e99`）
- fixture：`HEAOTANG-CA-SC-20260712-V1`
- secrets：none-recorded
- 当前 verdict：`No-Go / remediation`（保留已通过项；刷新 DOM 与环境 Enter 尚未验证）

| case_id | session | action | actual | server correlation | result |
| --- | --- | --- | --- | --- | --- |
| SC-B01 | guest | 从俱乐部联盟聚焦自建入口 | 页面显示 `authentication_required`，未发 SC 业务请求 | Nginx denylist 0 | Pass |
| SC-B02 | synthetic member | 打开自建列表 | 显示 5 个固定 seed active standard+general 样本；未显示 charity/family/direct/health/inactive | search 08:28:35 200 | Pass |
| SC-B03 | synthetic member | 打开详情 45 | 显示名称、简介、城市、成员数和创建时间 | detail 08:30:15 200 | Pass |
| SC-B04 | synthetic member | 提交加入申请 | 页面显示“申请已提交”；因 API 验收已创建同载荷，浏览器为幂等重放 | join 08:35:37 200 | Pass |
| SC-B05 | synthetic member | 打开本人申请 | 显示当前 run pending 申请并可返回详情 | my-applications 08:37:22 200 | Pass |
| SC-B06 | synthetic member | 刷新本人申请深链 | URL 保持；服务端再次返回 my-applications 200；刷新后 DOM 读取受控制通道超时 | my-applications 08:38:31 200 | Unverified（DOM pending） |
| SC-B07 | guest | 浏览器后退 | 从联盟聚焦页返回 `/self-created/`，heading=`自建俱乐部` | no business mutation | Pass |
| SC-B08 | guest | 顶部返回俱乐部联盟 | 到达联盟页并保持自建聚焦 + `authentication_required` | no business mutation | Pass |
| SC-B09 | guest | 底部返回俱乐部联盟 | 默认自动化点击落在拉伸框几何中心未触发；只读 `elementFromPoint` 定位可见文字区域后真实坐标点击成功 | no business mutation | Pass |
| SC-B10 | guest | 320/360/768/1280 响应式 | 各视口 `body/document width == innerWidth`，无横向滚动，heading 正常 | no business mutation | Pass |
| SC-B11 | guest | Tab / focus-visible / ARIA | 真实 Tab 后顶部返回链接成为 activeElement；`focus-visible=true`，轮廓为 `3px solid rgb(23, 107, 66)`，ARIA 名称=`返回俱乐部联盟`，href 正确 | no business mutation | Pass |
| SC-B12 | guest | Enter 激活焦点链接 | 两种 Enter 编码均由控制通道返回 sent，但 URL 未改变；原生链接真实鼠标点击已通过，自动化覆盖共享首页 Enter | none | Unverified（control-channel） |

## 控制通道与产品故障区分

- 多次出现 `ab.chatgpt.com` Statsig 10 秒超时，但 DOM、URL、Nginx 和业务 API 均继续成功；归类为浏览器控制层外部统计噪声。
- 底部返回第一次未导航不是产品缺陷：链接 `href` 正确，元素可见文字区域的真实点击成功。根因是链接布局框被拉伸，默认几何中心不在实际命中区域。
- 刷新后的页面 GET 由 Nginx 证明 200，但刷新后 DOM 读取超时；不把未取得的 DOM 证据写成通过。
- Playwright/body、DOM CUA 和 CUA 的 Tab 注入存在延迟；最终 activeElement 证明 Tab 已到达。Enter 注入无法形成导航，按控制通道限制保留 Unverified，不推断为产品失败。

## 完成边界

- 环境已覆盖 Tab、focus-visible、heading/status/ARIA；Enter 控制通道限制和刷新 DOM 都保持 Unverified，关闭前不得写成浏览器 UAT Pass。
- fixture cleanup 证据记录在 `db-evidence.json`，不改变本报告已取得的浏览器事实。
