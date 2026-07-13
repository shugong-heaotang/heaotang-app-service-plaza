# 俱乐部联盟 H2-M2 真实数据与正式入口任务书

- 目标：将已验收的会员首页页面壳接入真实 `GET /api/v1/clubs/member-home` 聚合接口，并挂载到俱乐部联盟无筛选首页。
- 保持 H1 边界：带 `category` 或 `view=manage` 的分类/管理入口继续走原 H1 focused 页面；不得改变动作目录权威性。

## 后端检查点

1. 新增认证、本人范围的 `GET /api/v1/clubs/member-home`；不得接受 `user_id` 查询参数。
2. 返回严格 v1 信封中的会员摘要、本人俱乐部、今日待办、最近活动、联盟动态与 `can_manage`。
3. 俱乐部类型只投影为公益、家庭、自建三类；未知类型失败关闭。
4. 无成员数据返回合法空集合；数据库错误返回稳定错误，不得用 mock 或 catch-empty 掩盖。
5. 完成 handler/service 正反例、Go 全量 test/vet 与 Handoff。

## 前端检查点

1. 无 `category`、无管理视图时加载会员首页；有 H1 query 时保持原页面。
2. 覆盖 loading、ready、empty、partial-error、error、unauthorized、maintenance、offline 映射。
3. 探索入口继续来自动作目录；管理入口只由后端 `can_manage` 决定。
4. 完成定向、全量 Vitest、生产构建及 320/360/768+ 响应式复核。

## M3 验收

部署测试环境后，以新会员、家庭俱乐部会员、多俱乐部会员、理事/管理员四类身份完成浏览器 UAT，保存路由、DOM、网络、权限和服务端关联证据；未完成不得宣称 H2 完成。
