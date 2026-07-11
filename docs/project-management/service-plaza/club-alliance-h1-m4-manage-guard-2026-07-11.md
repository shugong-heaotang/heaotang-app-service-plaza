# CA-H1-M4-B002 管理入口权限失败关闭根因修复

日期：2026-07-11
状态：本地实现与自动化验证完成，待提交、受控集成、部署和环境复验

## 现象与根因

测试环境中，合成普通会员点击管理中心后，动作事件正确记录
`club-manage / blocked / scope_required`，但浏览器仍进入 `?view=manage`，页面显示普通首页。

根因由两部分组成：

1. `ActionControl` 对内部 `Link/NavLink` 在权限拒绝后仍允许默认导航。
2. `ClubAllianceRoute` 只解析 category，未解析上游 `club-manage` 的 view target。

## 修复边界

- 只有 `scope_required` 阻止内部链接默认导航；`authentication_required` 继续进入既有承接页。
- 管理 view 从上游动作 target 解析，不新增本地展示真相源。
- direct view 按共享 evaluator 产生 authentication/scope/focused 状态。
- 不修改后端、业务 API、Schema、部署或四类业务逻辑。

## 自动化证据

- 定向：3 files / 61 tests passed。
- 前端全量：18 files / 155 tests passed。
- production build：passed。
- test-server build：passed。
- 首次全量回归发现“阻止所有未授权导航”破坏生命导航承接页，已按
  authentication 与 scope 两类原因分层修正后全量通过。

测试在系统临时隔离仓库镜像执行，使用主仓锁文件对应的现有 `node_modules`；
未修改依赖、锁文件或正式工作树。独立工作树依赖自举缺口另列平台工具后续项，
不在本缺陷范围内临时扩写脚本。

## 剩余门禁

1. 完成治理、合同、UTF-8 与差异检查。
2. 提交、推送并受控集成。
3. 重新构建和部署测试环境前端。
4. 复验普通会员点击管理中心保持原 URL、blocked/scope_required 三方证据；
   direct `view=manage` 显示 scope_required。
5. M4 最终复核后才能给出 H1 Full Go。
