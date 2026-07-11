# 俱乐部联盟 H2-M1 独立会员首页页面壳任务书

- 工作项：`AIW-20260712-CLUB-MEMBER-HOME-H2`
- 上游：H2-M0 集成提交 `14a7264`
- 本检查点：只新增 `app/src/modules/club-alliance/member-home/` 页面壳、view model adapter、CSS 与测试。

## 必须实现

1. 按 M0 合同顺序渲染会员摘要、我的俱乐部、今日待办、最近活动、联盟动态、探索更多。
2. 覆盖 loading/ready/empty/partial-error/error/unauthorized/maintenance/offline。
3. 普通会员隐藏管理中心；有 `club:manage` 时仅显示附属管理入口。
4. fixtures 只用于测试；运行时组件不创建 mock、不 catch 后返回空数组、不发网络请求。
5. 320/360 单列，768+ 合理双列；键盘、焦点、aria 和局部错误可访问。

## 禁止范围

不修改 `ClubAlliancePage.tsx`、`ClubAllianceRoute.tsx`、`App.tsx` 或 CA-SC 路径；不接真实 API、不改后端、不部署。父页面挂载等待 CA-SC 前端受控集成后另行授权。
