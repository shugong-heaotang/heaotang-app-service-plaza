# Project Brain v2 M3 老板只读驾驶舱实现任务令

- 日期：2026-07-17
- work item：`AIW-20260717-PROJECT-BRAIN-V2-M3-BOSS-DASHBOARD`
- authority / R3 exact start：`d1531daed440d4776c22f58c127710eb20eb2128`
- R1 `b5b09398858c39531e4ae9d42c2aa82ab21e626f`与R2 `545f1386c4421929be560caf36e6060f2a061499`保持不可变历史；R3只在已集成M2根因修复的新authority上重建并复验。
- branch：`codex/project-brain-v2-m3-dashboard`
- workspace：`C:/Users/shugo/Documents/APP系统/.codex-worktrees/project-brain-v2-m3-dashboard`

## 交付目标

实现一个不挂网络路由、仅消费M2合成不可变证据的老板只读驾驶舱候选。候选必须包含服务端会话验证、授权决策、M2 audit/run/snapshot一致性读取、安全视图模型、状态解释、只读API响应和无脚本HTML渲染，并以负向/变异测试证明禁止未授权访问、导出、行级下钻和写操作。

## 8类exact allowed paths

1. `project_brain_v2/dashboard/**`
2. `contracts/project-brain/v2/dashboard/**`
3. 本任务令
4. `docs/project-management/project-brain-v2/task-comprehension-receipt-m3.md`
5. `docs/project-management/project-brain-v2/handoff-m3.md`
6. `contracts/foundation/development-checklists/2026-07-17-project-brain-v2-m3-dashboard*.json`
7. `contracts/foundation/governance-exams/2026-07-17-project-brain-v2-m3-dashboard*.json`
8. `contracts/foundation/implementation-records/2026-07-17-project-brain-v2-m3-dashboard*.json`

## 运行与安全合同

- 默认策略文件必须`enabled=false`、`production_enabled=false`、`network_route_enabled=false`、`real_sources_enabled=false`、`export_enabled=false`、`source_writes_enabled=false`；未知字段拒绝。
- 仅`offline_synthetic_test`且策略明确`enabled=true`时，允许在进程内调用handler；不得监听端口或导入网络服务器。
- 会话由服务端HMAC验证器校验签名、audience、subject、roles、issued_at、expires_at和nonce；无token、伪造、过期、错audience均拒绝。
- dashboard角色必须同时满足平台allowlist和对应M1 fact的`allowed_roles`；客户端参数不能自行提升角色。
- 页面和API仅支持GET；`/dashboard/export`、任一export参数、POST/PUT/PATCH/DELETE以及未知路径失败关闭。
- 读取M2 state必须验证路径隔离、audit hash chain、run record、content-addressed snapshot、JSON Schema以及fact catalog/source map一致性。
- 只展示聚合安全值；G1重新核对阈值、维度和禁用下钻；禁止任何行级或被禁止字段。
- 每张卡必须包含状态、原因、截至时间、口径版本、authority、source owner、classification、证据hash及决策可用性提示。
- `Unknown/No-Go`必须显示原因、Owner和“不可用于当前决策”；可显示最后可信快照时必须显著标记stale。
- HTML必须转义所有动态内容、无脚本、无表单、无链接式操作、无导出按钮、具备基础可访问性和响应式布局。

## 明确禁止

不得修改M1/M2、Project Brain v1、registry、App、公共scripts或共享路由；不得接真实数据、凭据、网络或external auth；不得启用M2 `boss_dashboard_enabled`；不得部署、发送通知、导出、执行真实timer或production；不得激活M4-M5。

## 验收

至少证明：合法角色page/API成功；匿名/未授权/伪造/过期/错audience拒绝；direct URL不绕过；export和写方法拒绝；audit/run/snapshot/definition篡改拒绝；G1小样本、危险维度和行级结构拒绝；Unknown/No-Go解释；HTML转义、无脚本/表单/导出；默认策略关闭；无网络/写入能力；M2与M1回归不退化。

developer、independent reviewer、approver和integration owner保持分离。开发者门禁通过后只形成candidate；独立Go后才允许受控集成。
