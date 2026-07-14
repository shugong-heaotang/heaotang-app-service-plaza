# NOVA Overlay R2 独立验收正式证据

日期：2026-07-14
工作项：`AIW-20260714-PLATFORM-NOVA-OVERLAY-R2-INDEPENDENT-ACCEPTANCE`
实施记录：`IR-20260714-PLATFORM-NOVA-OVERLAY-R2-INDEPENDENT-ACCEPTANCE-R1`

## 结论

**独立技术结论：Go；生命周期终态仍须 APP 总架构独立验收负责人裁定。**

平台治理独立测试负责人已对实现源 `59a988df0d7d1a13ac4dd9ad48da62d5c0340534`、受控集成 `81f6bc8a7e1bc872f1689099a704768495deb009` 和当前权威 `dc8a52a4bcc130c6cdb4da55d5d015cdf501ba16` 完成只读复验。实现范围 19/19、实现前后 registry 字节不变、定向 22/22、完整 Python 92/92、编码、差异、秘密与 Git 关系均通过；reviewer 基线和当前权威的 Service Plaza 总合同均通过。

本结论不修改 registry，不等同于部署、生产、真实用户、真实数据、支付、真实资金或不可逆操作授权，也不允许本负责人自行集成。

## 身份、授权与独立性

| 项目 | 精确值 |
| --- | --- |
| reviewer branch | `codex/platform-nova-overlay-r2-independent-acceptance` |
| registered base / start HEAD | `0c420c3448a9e6399410cb6c230b43c243b0471c` |
| reviewed source | `59a988df0d7d1a13ac4dd9ad48da62d5c0340534` |
| source implementation base | `fb29b857a5476a62cc882bf6bf407e67febcacf9` |
| source last parent | `60a0694f87dd22c0a8def74b91d99d3b8dac84f8` |
| controlled integration | `81f6bc8a7e1bc872f1689099a704768495deb009` |
| integration first parent | `ea3c70c8bea4904b455455ffc7c6e29821de2705` |
| current authority | `dc8a52a4bcc130c6cdb4da55d5d015cdf501ba16` |

本 owner 未实现 source，未执行 controlled integration，也不会集成本证据分支。全部写入严格限制在已登记的 reviewer namespace 五种文件模式内。

## R8 No-Go 与 R10 新授权链

- R8 exact `6eabd60ba1b33e6608cdc3ded7d735ac18622b47` 被独立 No-Go：其 checklist 绑定修改前 registry hash，且当时 authority 已出现交接响应 SLA 问题。
- revert `76f90aaf2abd118c27d8d4264269f09096eae9b4` 完整恢复 R8 authority tree；R8 checklist、exam、IR 均未复用或改写。
- R9 关闭逾期 handoff 后，authority 成为 `0c420c3448a9e6399410cb6c230b43c243b0471c`。
- 项目最高负责人重新授权 R10；R10 source `854863f0c7649838e44128743fa3e24ff89bc638` 由双父合并 `dc8a52a4bcc130c6cdb4da55d5d015cdf501ba16` 受控进入权威，并将本 reviewer item 登记为 active。

因此本证据使用全新的 current checklist 和 exam，不继承 R8 的任何授权结论。

## 实现范围与 registry 不变量

以注册基线 `fb29b857...` 对比 source `59a988d...`：

- 实际变更：19 个文件。
- 逐路径匹配登记的 17 条 allowed patterns：19/19。
- 越界路径：0。
- source 中 19 个文件在 controlled integration 中逐 blob 相同：19/19。
- registry 在 implementation base 和 source 的 SHA-256 均为 `c4a1c8865c5ca4dd769caefefd10ea7a06808617736ed39c0b165cee4fc9c53c`，字节数均为 332228，逐字节相同。
- integration registry 与其第一父 `ea3c70c8...` 逐字节相同，SHA-256 为 `bbe39aa588d71c0f0c42011bb30377724b9fd616982255dc43827551ebac015e`。

这证明候选没有自行写 registry，也没有在 merge 中覆盖 authority registry。

## 独立回归

| 门禁 | 结果 |
| --- | --- |
| `python -X utf8 -m unittest scripts.tests.test_validate_governance_reading_list scripts.tests.test_new_agent_development_checklist -v` | 22/22，OK |
| `python -X utf8 -m unittest discover -s scripts/tests -p 'test_*.py' -v` | 92/92，OK |
| source `scripts/Test-TextEncoding.ps1` | 1436 files，Pass |
| source `git diff --check fb29b857...59a988d` | Pass |
| reviewer base `scripts/Test-ServicePlazaContracts.ps1` | Pass |
| current authority `dc8a52a...` 的 `scripts/Test-ServicePlazaContracts.ps1` | Pass |
| reviewer preflight | `status=ready` |
| reviewer current checklist | 26/26 completed，validator Pass |
| reviewer governance exam | attempt 1，8/8，score 100，passed |

定向 22 项覆盖正式 reading-list/schema、NOVA 与 Protection Mall overlay 激活前失败关闭、动态 module checklist、legacy cutoff、post-cutoff platform identity、task-order/work-id 绑定。完整 92 项覆盖当前 scripts 测试集合。

## 历史 source 的当前时钟总门禁说明

不得把历史 source 的当前时钟总门禁写成通过。对 `59a988d...` 历史快照在 2026-07-14 复验时直接运行 `scripts/Test-ServicePlazaContracts.ps1`，唯一失败为：

```text
AIW-20260713-DELIVERY-FLOW-OPTIMIZATION-INDEPENDENT-ACCEPTANCE: DELIVERY_HANDOFF_RESPONSE_SLA_EXCEEDED
```

受影响的是 source 快照中另一个 delivery-flow supporting item；其 `handoff_requested_at=2026-07-14T05:41:23+08:00`，当时没有 first response。该状态不是 NOVA 19 文件候选引入，也不改变 NOVA 定向/全量代码测试结果。

为验证时间因果，使用 source 提交时钟 `2026-07-14T08:34:49+08:00` 对同一不可变 registry 执行结构门禁和 delivery-flow validator，结构错误 0、flow 错误 0。其后 R9 已正式关闭该逾期 handoff；reviewer base `0c420c3...` 与当前 authority `dc8a52a...` 按当前时钟运行总合同均通过。

本报告不消除该历史事实，也不把时钟锚定验证冒充当前 source total pass。是否接受“候选未引入、当前权威已关闭”的影响边界，由 APP 总架构独立验收负责人最终裁定。

## Git 父子、祖先与远端

- source 的最后提交父为 `60a0694...`；完整实现范围由 registered base `fb29b857...` 至 source 三提交组成。
- controlled integration 的父为 `ea3c70c8...` 与 `59a988d...`；source 是第二父且为 integration 的 ancestor。
- integration 是当前远端 authority `dc8a52a...` 的 ancestor。
- `origin/codex/platform-nova-overlay-r2` 包含 source；`origin/codex/platform-governance` 包含 integration，且当前远端 exact 为 `dc8a52a...`。

## 安全、编码与证据边界

对 source 19 文件及 reviewer namespace 执行高置信秘密扫描，覆盖私钥头、GitHub/OpenAI/Slack token 形态、AWS access key、JWT 和明显的密码/secret/token 赋值；结果 0 hit。没有读取、输出或写入生产凭据。

本 reviewer namespace 最终只能包含：

- `evidence.md`
- `task-order.md`
- `development-checklist-r1.json`
- `governance-exam-attempt-1.json`
- `implementation-record-r1.json`

最终定稿后重新执行 exact-file JSON/IR/checklist/exam validators、UTF-8、scope、registry 零写、secret、`git diff --check`，并计算 `evidence.md` SHA-256。摘要不写回本文件，避免自引用改变哈希。

## Handoff 与下一授权

APP 总架构独立验收负责人复核本 exact evidence commit、历史时钟限定和 SHA-256，并给出 Go/No-Go。若 Go，仅由平台集成负责人受控集成并更新生命周期；本 owner 不修改 registry、不自行集成，也不触达部署、生产、真实数据或资金。
