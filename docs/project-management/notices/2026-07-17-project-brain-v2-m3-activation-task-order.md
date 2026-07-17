# Project Brain v2 M3 老板只读驾驶舱激活任务令

- 日期：2026-07-17
- work item：`AIW-20260717-PROJECT-BRAIN-V2-M3-ACTIVATION`
- exact base：`65863009f9b950985c8850cc65d86a426ba128dd`
- branch：`codex/project-brain-v2-m3-activation`
- workspace：`C:/Users/shugo/Documents/APP系统/.codex-worktrees/project-brain-v2-m3-activation`

## 目标

只激活M3治理并预登记一个独立dashboard工作项。M3候选必须把M2的不可变合成快照转换为服务端授权的老板只读视图，证明权限、解释性、禁止敏感下钻和默认拒绝导出；本任务不编写dashboard代码。

## 激活候选的7类allowed paths

1. `contracts/foundation/agent-collaboration.v1.json`
2. 本任务令
3. `docs/project-management/project-brain-v2/task-comprehension-receipt-m3-activation.md`
4. `docs/project-management/project-brain-v2/handoff-m3-activation.md`
5. `contracts/foundation/development-checklists/2026-07-17-project-brain-v2-m3-activation*.json`
6. `contracts/foundation/governance-exams/2026-07-17-project-brain-v2-m3-activation*.json`
7. `contracts/foundation/implementation-records/2026-07-17-project-brain-v2-m3-activation*.json`

不得增加第八类路径。

## M3 implementation工作项的8类allowed paths

1. `project_brain_v2/dashboard/**`
2. `contracts/project-brain/v2/dashboard/**`
3. `docs/project-management/notices/2026-07-17-project-brain-v2-m3-dashboard-task-order.md`
4. `docs/project-management/project-brain-v2/task-comprehension-receipt-m3.md`
5. `docs/project-management/project-brain-v2/handoff-m3.md`
6. `contracts/foundation/development-checklists/2026-07-17-project-brain-v2-m3-dashboard*.json`
7. `contracts/foundation/governance-exams/2026-07-17-project-brain-v2-m3-dashboard*.json`
8. `contracts/foundation/implementation-records/2026-07-17-project-brain-v2-m3-dashboard*.json`

## M3必须证明

- 只读取M2已验证的不可变synthetic snapshot/run/audit证据；
- 服务端授权真实生效，不把隐藏菜单或客户端路由当安全边界；
- 未授权角色、匿名请求、direct URL、API和export均失败关闭；
- UI显示截至时间、口径版本、状态、authority、来源、Owner与证据；
- `Unknown/No-Go`有原因、责任Owner和不可用于当前决策提示；
- 无行级会员、健康、资金、客服或关系下钻；
- 无写回、审批、重算、改状态、源系统操作或导出能力；
- `boss_dashboard_enabled=false`与全部M2生产开关保持不变。

## 仍然No-Go

真实数据、凭据、网络、共享App路由、external auth接线、export、notification、deploy、真实timer、production以及M4-M5全部No-Go。

## 角色与门禁

- developer：Project Brain v2 M3 activation governance owner
- reviewer：independent platform reviewer
- approver：项目最高负责人
- integration owner：平台集成负责人

current checklist、Exam100、verified IR、collaboration、总合同、UTF-8、scope、secret0、fresh authority和独立Go齐全后才允许受控集成。代码存在、界面截图或自测不能替代独立验收。
