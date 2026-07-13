# 平台权威集成推送新鲜度门禁 R2 任务书

- work_id: `AIW-20260713-PLATFORM-INTEGRATION-FRESHNESS-GATE-R2`
- owner: 平台集成负责人
- branch: `codex/platform-integration-freshness-gate-r2`
- worktree: `C:/Users/shugo/Documents/APP系统/.codex-worktrees/platform-integration-freshness-gate-r2`
- activation base: `6f4f9048458b4458cb163b148cce924991bf81fc`
- recurrence: second occurrence

## Objective

在不丢弃远端健康链或本地活动链的前提下，关闭第二次平台集成分叉的系统性根因：缺少统一、失败关闭、带 expected lease 的权威推送门禁。

## Scope

1. 固化两次分叉证据、影响扫描和根因链。
2. 在 recurring issue 中登记第二次复发。
3. 建立版本化 push policy、Schema、验证器和 PowerShell gate。
4. 用临时本地 Git/Bare Remote 验证 fresh、push、stale expected、diverged、behind、dirty、wrong branch 等正负例。
5. 独立复核 Go 后，才允许在同一受控工作项中合并 `bb9e7171db17c0010a46b2dcc50b3c73a61723a3`，逐项调和 registry，并通过 freshness gate 推送新权威 HEAD。

## Prohibited

- 禁止 reset、force-push without lease、checkout 覆盖、删除提交或把任一单边 registry 作为调和结果。
- 独立复核前禁止真实分支调和和权威推送。
- 禁止健康 F2-1/F3/P3、活动业务扩权、真实数据、环境、医疗、资金、部署和生产。
- 第三次复发必须升级 ADR、CONSTRAINTS 和全依赖审计。
