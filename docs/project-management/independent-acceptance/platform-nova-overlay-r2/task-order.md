# NOVA Overlay R2 独立验收正式证据任务书

日期：2026-07-14
工作项：`AIW-20260714-PLATFORM-NOVA-OVERLAY-R2-INDEPENDENT-ACCEPTANCE`
实施记录：`IR-20260714-PLATFORM-NOVA-OVERLAY-R2-INDEPENDENT-ACCEPTANCE-R1`
执行角色：平台治理独立测试负责人
独立复核角色：APP 总架构独立验收负责人

## 授权链

- 登记基线与本工作树固定在 `0c420c3448a9e6399410cb6c230b43c243b0471c`，分支为 `codex/platform-nova-overlay-r2-independent-acceptance`。
- R8 候选 `6eabd60` 的独立结论为 No-Go，已被完整回退；R8 的检查单、考试或聊天结论均不能授权本任务。
- 项目最高负责人重新授权 R10。R10 将本工作项以 `active` 状态登记，并已受控集成到权威提交 `dc8a52a4bcc130c6cdb4da55d5d015cdf501ba16`。
- 被验收的实现源提交为 `59a988df0d7d1a13ac4dd9ad48da62d5c0340534`；其受控集成提交为 `81f6bc8a7e1bc872f1689099a704768495deb009`。

## 唯一允许范围

只允许写入 `docs/project-management/independent-acceptance/platform-nova-overlay-r2/` 下：

- `evidence.md`
- `task-order.md`
- `development-checklist*.json`
- `governance-exam*.json`
- `implementation-record*.json`

禁止修改协作登记表、候选实现、测试脚本、权威分支、部署、生产、真实数据或资金；本负责人不得自行集成。

## 必须独立复验的门禁

1. 实现源相对父提交的路径范围必须为 19/19，并与任务授权范围逐项相符。
2. 实现源前后 `contracts/foundation/agent-collaboration.v1.json` 字节必须完全不变。
3. NOVA Overlay R2 定向回归 22/22；完整 Python 回归 92/92。
4. `scripts/Test-ServicePlazaContracts.ps1`、`scripts/Test-TextEncoding.ps1` 与 `git diff --check` 全部通过。
5. 对实现源、集成提交与本证据范围执行高置信秘密扫描，不得出现真实凭据。
6. 核验实现源、集成提交的父子关系、祖先关系、远端可读性及远端权威提交。
7. 固化 R8 No-Go 与 R10 新授权链，禁止把历史失败抹除或复用。

## 完成条件

当前检查单 26/26、随机治理考试 100 分、全部独立门禁通过、证据和实施记录有效、变更严格留在唯一允许范围；随后仅提交并推送本 reviewer 分支，等待 APP 总架构独立复核和平台受控集成。
