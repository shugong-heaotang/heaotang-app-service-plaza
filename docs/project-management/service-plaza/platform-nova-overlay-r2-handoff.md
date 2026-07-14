# 平台 NOVA overlay R2 Handoff

日期：2026-07-14（Asia/Shanghai）
工作项：`AIW-20260713-PLATFORM-NOVA-OVERLAY-R2`
实施记录：`IR-20260713-PLATFORM-NOVA-OVERLAY-R2-R2`
提交人：Platform governance bootstrap agent
接收人：平台治理独立测试负责人
当前结论：Implemented / awaiting exact-candidate independent acceptance；不是 integrated。

## Root-cause record

### Identity

- pattern_id：`RI-NEW-MODULE-CHECKLIST-BOOTSTRAP`
- title：模块先激活、后发现治理 overlay 缺失
- owner：平台集成负责人
- first_seen / recurrence_count：2026-07-12 / 3
- affected_checkpoint：NOVA Phase 5 M1 current checklist 与 synthetic E2E 治理入口

### Evidence

- symptom：`-ModuleId nova` 无注册 overlay；同权威 active Protection Mall 也无 overlay。
- exact_stop：NOVA 无法生成 current checklist；只补 NOVA 后共享门禁会在商城处红。
- reproduction：从正式 reading list 临时删除 `nova` 或 `protection-mall`，对当前 registry 执行 `validate_governance_reading_list.py --registry`，两者均非零退出。
- expected / actual：期望模块激活前已有完整课程；实际 registry 生命周期不依赖 reading list。
- product_evidence：不涉及业务运行或生产；影响是治理授权链无法成立。
- tool_or_environment_evidence：PowerShell generator 和 Python validator 均在本地离线复现；不是浏览器或网络故障。

### Causal chain

因为 R1 只在 generator 调用点验证显式 ModuleId，因此 registry 可先进入 active；因为总合同不扫描 active/handoff-ready module_id，因此缺失 overlay 未阻止派发；因此 NOVA 与 Protection Mall 同时处于已激活但课程不完整的状态。最早可控原因是激活交易缺少 registry → reading-list 共享门禁。

### Impact

- affected_modules_and_paths：NOVA、Protection Mall；完整清单见全依赖审计。
- security_data_release_impact：无生产、真实数据、资金或部署变更；release 结论不变。
- blocks：NOVA 新 current checklist、考试、IR/Handoff 与 synthetic E2E 后续治理闭环。
- does_not_block：NOVA 既有28项离线回归、商城既有候选保存、Activity 与其他无重叠模块。

### Resolution

- rejected_workaround_and_reason：拒绝只补 NOVA、删除 ModuleId、硬编码模块名单、篡改 Mall 历史证据或关闭总门禁；都会保留根因或制造假绿。
- systemic_fix：schema化唯一 reading list；generator 共用校验；总合同动态扫描 active/handoff-ready registry；补齐 NOVA 与审计必要的 Mall 最小 overlay。
- changed_contracts_code_tools：reading list/schema、Python validator、PowerShell generator、Service Plaza total gate、tests、ADR0019、CONSTRAINTS、recurring issue与审计。
- compatibility_or_migration：`fb29b857...` 为一次性 cutoff；29个历史文件/30条 finding 保留，不回写、不追认新规则；cutoff 后永久负例失败关闭。
- rollback：回退本候选所有范围内变更并保持 NOVA No-Go；不得移动 cutoff 或删负例。

### Prevention and proof

- prevention_gate：`scripts/validate_governance_reading_list.py` + `scripts/Test-ServicePlazaContracts.ps1`。
- positive_test：正式权威6个overlay、所有显式 active module gate通过；NOVA/Protection Mall generator路径与SHA正确。
- negative_test：删 NOVA、删 Mall、empty、missing、unsafe、duplicate、unknown 与 post-cutoff foundation null 均失败。
- regression_set：修订后定向22/22；全量92/92；Service Plaza total contract pass。
- environment_retest：UTF-8 1434 files pass；scope bad=0；`git diff --check` pass。
- evidence_paths_and_exact_commits：实现记录、R2 checklist/exam、审计与本Handoff；候选 exact 在提交后由接收人核对。

### Recurrence action

第三次复发已更新 `RI-NEW-MODULE-CHECKLIST-BOOTSTRAP`、`CONSTRAINTS.md`、ADR0019，并审计全部 registry module lifecycle、6个overlay、67份模块checklist及foundation cutoff inventory。

### Verdict

- Conditional Pass：本地实现和回归通过。
- unresolved_risk：第一次 central 临时集成发现并关闭 R7 固定短语误报；修订候选仍需再次对 `ea3c70c8bea4904b455455ffc7c6e29821de2705` 跑完整临时集成态门禁，随后仍需独立 reviewer Go。
- next_authorization：独立 reviewer 只读复验 exact candidate；Go 后由平台集成负责人受控集成，不由实施者改 registry。

## 精确变更边界

实际变更全部位于 registry 登记的17条 allowed patterns；未修改 `agent-collaboration.v1.json`、NOVA/Mall业务、部署、生产或历史模块证据。

## 验证命令

```powershell
python -X utf8 -m unittest scripts.tests.test_validate_governance_reading_list scripts.tests.test_new_agent_development_checklist -v
python -X utf8 -m unittest discover -s scripts/tests -p 'test_*.py' -v
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/Test-ServicePlazaContracts.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/Test-TextEncoding.ps1
git diff --check
```

## 下一步

1. 形成 exact candidate，执行 central authority merge-tree 与临时集成态全门禁。
2. 如集成态发现 `fb29b857` 后新增文件不合规，保持 No-Go 并修复当前门禁；禁止把 cutoff 后移。
3. 临时集成态通过后推送候选，交独立 reviewer；未得 Go 前不得声称 verified/integrated。
