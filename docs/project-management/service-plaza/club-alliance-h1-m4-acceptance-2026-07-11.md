# 俱乐部联盟 CA-H1 M4 验收执行记录

- work_id：`AIW-20260711-CLUB-ALLIANCE-H1-M4-ACCEPTANCE`
- branch/worktree：`codex/club-alliance-h1-m4-acceptance` / `C:/Users/shugo/Documents/worktrees/heaotang-club-h1-m4-acceptance`
- base：`91547b3db4a8a92537ff19193f2e2a6740318ccd`
- 当前阶段：部署 Pass；`CA-H1-M4-B001` resolved；浏览器 UAT In Progress / No-Go。
- 证据：`docs/project-management/modules/club-alliance/acceptance/CA-H1-M4-frontend-uat.md`。

本工作项只验收标准首页/页面壳，不调用 club search/create/join/member 等业务 API。网络证据分别记录模块 catalog/actions、APP 公共 feature-flags 和业务 denylist；部署、备份、回滚、浏览器、权限、遥测和八态未全部闭环前不得判 M4 Go。

`CA-H1-M4-B001` 已由 backend `c4319c206add11f92d763b13b63be8ab2e47679e` 和 APP evidence `ee8dec915ed890ed9fdc732fa6eacb1c3902ed3e` 关闭；测试环境通过不同管理员双审启用。公益、自建、家庭、友联体四分类的 guest blocked 均已取得页面/Nginx/数据库三方证据，稳定为 `blocked / authentication_required / user_id=null`，且未调用俱乐部业务 API。登录 activated、缺 `club:manage` blocked 与完整导航/键盘仍未完成，因此 M4 尚未 Go。
