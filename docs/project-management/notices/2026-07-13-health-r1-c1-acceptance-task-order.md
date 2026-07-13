# 健康大管家 R1-C1 独立验收与受控集成任务书

- work_id: `AIW-20260713-HEALTH-R1-C1-ACCEPTANCE`
- owner: Codex platform integration agent
- branch: `codex/health-r1-c1-acceptance`
- worktree: `C:/Users/shugo/Documents/worktrees/heaotang-health-r1-c1-acceptance`
- authority base: `a4b83a9f02e0163458dc971d9e0d41d3c0f55779`
- candidate source: `e50d48c4dd28307f9f09170ad1466c3b20064b26`
- module work item: `AIW-20260713-HEALTH-R1-CROSS-MODULE-FREEZE`

## Objective

独立复核 R1-C1 的需求与原型冻结证据；若全部门禁为 Go，从精确 authority base 显式保留权威 registry 全量状态、加入 R1 模块项并受控合并候选，随后用 expected-remote lease 推送权威集成分支。

## Required gates

1. ownership/preflight、当期 checklist、随机治理考试 100。
2. candidate exact commit、本地/远端一致、clean、9 个路径均在模块 allowed paths 内。
3. 需求补充 SHA-256、Schema、13 项正负 conformance、模块 checklist/exam/IR/Handoff 独立复核。
4. `agent-collaboration.v1.json` 不采用任一侧整文件覆盖；保留 authority 全部工作项，并只显式加入 R1 模块工作项。
5. collaboration、依赖、总合同、UTF-8、diff、范围、秘密和安全门禁全部通过。
6. 平台 IR/Handoff、commit、expected-remote lease push；最终将平台和 R1 模块工作项收口为 `integrated`。

## Prohibited

- 禁止普通冲突自动取 ours/theirs、reset、无 lease 强推、覆盖或丢弃 authority 现有商城及其他模块状态。
- 禁止把 E2E 工作项从候选旧 registry 顺带带入 authority；其处置需独立结论。
- 禁止修改 R1 模块产物来让验收通过，禁止自降测试、Schema、安全或验收口径。
- 禁止 R2 业务实现、共享前后端/API/数据库、真实身份或健康数据、互联网诊疗、医疗决策、收费、资金、部署和生产。

## Verdict boundary

R1-C1 Go 只冻结合成、离线、`executable=false` 的 IA、责任边界、跨模块协议与验收负例。隐私法律、医疗质量、平台安全及健康馆运营会签可保持 Pending；这些 Pending 不阻止 R2 合同与负例规划，但 R2 active 实现必须在 R1 受控集成后另立工作项。
