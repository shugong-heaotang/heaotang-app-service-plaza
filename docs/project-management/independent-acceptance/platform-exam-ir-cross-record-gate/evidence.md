# 治理考试与实施记录跨记录门禁独立验收证据

## 结论

**Go**：平台治理独立测试负责人对 exact source `3b4bd0c7c78c78be5b592b894e795053f169fa14` 的失败关闭行为、受控集成 `757de99e4dfa4a7467a0de6e1a66d6e030ba7f09` 的提交关系，以及授权集成 `60ff58d0be2c4f80a1e8c9c32a534113e1b384ae` 的 reviewer 权限链完成独立复验。

本结论仅证明上述 exact source/integration 满足本轮治理验收条件。它不修改 registry 状态，不等同于生产、真实用户、支付、真实资金、不可逆数据或 NOVA 激活授权。

## 身份、提交与独立性

| 项目 | 精确值 |
| --- | --- |
| work item | `AIW-20260714-PLATFORM-EXAM-IR-CROSS-RECORD-INDEPENDENT-ACCEPTANCE` |
| owner | `Platform governance independent test agent` |
| owner_role | 平台治理独立测试负责人 |
| reviewer_role | APP 总架构独立验收负责人 |
| evidence base / start HEAD | `757de99e4dfa4a7467a0de6e1a66d6e030ba7f09` |
| reviewed source | `3b4bd0c7c78c78be5b592b894e795053f169fa14` |
| source parent / implementation base | `2535a6bf0b59a308dce0e73fd58071be52353ed8` |
| reviewed controlled integration | `757de99e4dfa4a7467a0de6e1a66d6e030ba7f09` |
| reviewer authorization integration | `60ff58d0be2c4f80a1e8c9c32a534113e1b384ae` |

Git 关系复验：source 的唯一父提交为 `2535a6bf...`；source 是 integration 的第二父历史且为其 ancestor；integration 是 authorization 的第一父历史且为其 ancestor。

独立性声明：本 owner 未实现 source `3b4bd0c7...`，未执行 integration `757de99e...`，也不执行本 evidence 分支的后续平台集成。owner 只进行了只读独立测试，并在 R5 预先授权的 reviewer namespace 内固化证据。

## 授权范围

本工作项只创建以下五个文件：

- `docs/project-management/independent-acceptance/platform-exam-ir-cross-record-gate/evidence.md`
- `docs/project-management/independent-acceptance/platform-exam-ir-cross-record-gate/task-order.md`
- `docs/project-management/independent-acceptance/platform-exam-ir-cross-record-gate/development-checklist-r1.json`
- `docs/project-management/independent-acceptance/platform-exam-ir-cross-record-gate/governance-exam-attempt-1.json`
- `docs/project-management/independent-acceptance/platform-exam-ir-cross-record-gate/implementation-record-r1.json`

source 相对 implementation base 的10个路径也已独立核对为10/10授权；没有 registry、NOVA、Protection Mall 或业务代码改动。本 evidence 工作项没有修改 `contracts/foundation`、`scripts`、validator、商城九文件或部署配置。

## 四类跨记录失败关闭

定向执行 `scripts.tests.test_validate_implementation_records` 与 `scripts.tests.test_validate_governance_exams`，共8项全部通过：

| 场景 | 预期 | 实际 |
| --- | --- | --- |
| same record、`status=passed`、`score=100` | 放行 | Pass |
| IR 声称 verified，但同 record exam 为 `failed/75` | 失败关闭并报告实际状态 | Reject，错误包含 `status=failed, score=75` |
| exam `record_id` 与 IR 不同 | 失败关闭并报告实际 record | Reject |
| exam 缺失 | 失败关闭 | Reject |

定向结果：`Ran 8 tests ... OK`。失败记录没有被修改、删除或改写为通过。

## Activity 历史格式兼容负例

`record_directories(..., include_module_records=True)` 明确发现 `contracts/modules/activity/implementation-records`。当前 Activity 非 canonical IR 在共同 checklist/exam 链接约束下基线错误数为0；在临时目录只把其 exam 改为 `failed/75` 后，validator 精确拒绝：

```text
IR-20260713-ACTIVITY-V3-M0: governance exam must be passed with score 100 for the same record_id (actual record_id=IR-20260713-ACTIVITY-V3-M0, status=failed, score=75)
```

因此，模块历史字段不执行 foundation 完整 Schema 不构成 Activity 整体豁免；所有模块 IR 仍必须满足同 record、completed checklist、passed/100 exam 的共同约束。

## Protection Mall 九文件只读现场

- worktree：`C:/Users/shugo/Documents/worktrees/heaotang-protection-mall-m2-catalog-evidence`
- HEAD：`f332c7e45bc09b520505f5c4a509c567e16f2ffa`
- 现场：6个 ` M`、3个 `??`，dirty count=9
- validator：`validate_implementation_records.py --include-module-records`
- exit code：1
- 精确错误：`IR-20260713-PROTECTION-MALL-M2-CATALOG-R2` 的实际 exam 为同 record `status=failed, score=75`

fingerprint 口径：读取 `git -c core.quotepath=false status --porcelain=v1 -z` 的完整 raw bytes（含末尾 NUL）并先送入 SHA-256；再按 Git 原序对每条 `entry[3:]` 的 UTF-8 path 原字节和对应文件内容 SHA-256 的32字节 binary digest依次更新；文件不存在时更新字节 `<missing>`；最后取 hexdigest。

| 检查 | 运行前 | 运行后 |
| --- | --- | --- |
| dirty count | 9 | 9 |
| fingerprint | `ae3f55b13652daa4597c6b5ca79ab415d6e675e51696fa6825cd73cc27ea954d` | `ae3f55b13652daa4597c6b5ca79ab415d6e675e51696fa6825cd73cc27ea954d` |
| raw Git status | 基准 | 完全相同 |
| 九文件路径/状态/SHA-256 | 基准 | 完全相同 |

逐文件 SHA-256：

| 状态 | 路径 | SHA-256 |
| --- | --- | --- |
| ` M` | `contracts/modules/protection-mall/m2/catalog/catalog.v1.json` | `80ca85c9006fe45cb75d3a26d3c741c06e4e07cfb803a961d9ec2ea128dbc76d` |
| ` M` | `contracts/modules/protection-mall/m2/catalog/catalog.v1.schema.json` | `351d08f2b6964233d9508afe0193491fbd132302900f984a7cff6b4a8baad330` |
| ` M` | `contracts/modules/protection-mall/m2/catalog/fixtures/cases.v1.json` | `c7021855770bdc2346ed635d99a4ffc9e986e3722c76dec4c50a5f96aa10d8e7` |
| ` M` | `contracts/modules/protection-mall/m2/catalog/validate_catalog_contracts.py` | `f7ab0c925bd5a33cbeef4ee9525848517d1f571ec5a7c4e0e8f7bdaacef9de1a` |
| ` M` | `docs/project-management/modules/protection-mall/handoff-m2.md` | `e0537bf00dfcaece777be318e091601725ad34c617660f0d6b9d2e771d353d92` |
| ` M` | `docs/project-management/modules/protection-mall/m2-catalog-evidence.md` | `59667c531c1d61281e9792f21a596210654da4c582ba34aa22937bc5363876e8` |
| `??` | `contracts/modules/protection-mall/development-checklists/2026-07-13-protection-mall-m2-catalog-r2.json` | `88795fe208bee2fd1a0c00e4c630744b798c6b265ec50eefd40ec59a519a8097` |
| `??` | `contracts/modules/protection-mall/governance-exams/2026-07-13-protection-mall-m2-catalog-r2-attempt-1.json` | `8d8ae30fa551bcb390dd9ab9d12d1d39661232fec77a181c6202b21977d6dc46` |
| `??` | `contracts/modules/protection-mall/implementation-records/2026-07-13-protection-mall-m2-catalog-r2.json` | `4a846fbacf5c54a39d090ad6e0be8bb10e8e46e1b93817e83eec0c691f9036a2` |

该复验没有清理、暂存、覆盖或修改商城工作树。

## 全量治理测试与既有 inventory 失败

- exact source `3b4bd0c7...`：79项，78通过，1项失败。
- exact implementation base `2535a6bf...`：同一测试 `test_new_foundation_checklists_require_explicit_platform_scope` 失败，均为27条历史 foundation checklist/registry 对账错误，首条均为旧 NOVA API checklist 授权不匹配。
- reviewed integration `757de99e...`：79项，78通过，1项同名 inventory 测试失败；因另一 integration parent 新增 registry-dispatch R4 历史 checklist，当前错误明细为28条。失败测试类别未增加，source专项8项和总合同均通过。

这项 inventory 债务在 source/base 上已存在，不是 source `3b4bd0c7...` 引入；integration 的第28条来自并行授权链历史快照。该事实不被隐藏，也不被用来豁免本候选专项缺陷。修复 inventory 需要独立 registry/platform-scope 工作项，本 reviewer 无权修改。

## Service Plaza 总合同与自动覆盖边界

`scripts/Test-ServicePlazaContracts.ps1` 在 reviewed integration 上通过，输出包括：

- agent collaboration、development checklist、governance exam、implementation record 门禁通过；
- governance exam 使用 `--include-module-attempts`；
- implementation record 使用 `--include-module-records`；
- 自动递归覆盖 foundation 与 `contracts/modules/*/{governance-exams,implementation-records}`；
- 工程工具链、基础依赖和其余 Service Plaza 合同通过。

总合同不会自动扫描 `docs/project-management/independent-acceptance/...` reviewer namespace。本目录 checklist、exam、IR 采用显式 exact-file validator 验证；本报告不把总合同通过冒充为 reviewer namespace 自动覆盖。

## Reviewer 治理与关闭门禁

- `Test-AgentDevelopmentPreflight.ps1`：`status=ready`
- current checklist：26/26，全部为当前 SHA-256，`module_id=null`
- governance exam attempt 1：8/8，`score=100`、`status=passed`
- 显式 reviewer checklist/exam/IR validators：通过
- 五个 JSON/Markdown 文件 JSON解析与 UTF-8：通过
- `Test-TextEncoding.ps1`、`git diff --check`：通过
- allowed-path scope：五个变更文件全部授权，越界0
- secret-pattern audit：没有真实凭据、Token、私钥或密码发现
- reviewer branch push 后由远端精确一致性检查确认

最终 `evidence.md` SHA-256 在文件定稿后计算并随提交 exact、远端状态一起报告给平台集成负责人；hash 不写回本文件，避免自引用改变摘要。

## 被审根因、影响与回滚

source Handoff 的根因记录 `RI-EXAM-IR-CROSS-RECORD-CLAIM` 完整包含 identity、symptom、exact stop、causal chain、impact、systemic fix、prevention、proof 和 recurrence action。最早可控根因为旧总门禁只扫描 foundation IR，模块 IR 未进入共同 exam linkage 检查。

- blocks：商城治理证据 acceptance，直至 failed/75 不能被 verified/exam100 声明掩盖。
- does_not_block：商城后端 exact candidate 保存、NOVA 既有离线回归、其他隔离工作。
- rejected workaround：不改写失败试卷、不删除商城脏文件、不只改 Handoff 文案。
- rollback：回退 source/integration 可恢复旧行为，但不得删除失败考试或商城现场证据；回滚会重新打开错误放行风险，因此只能在新的受控平台交易中执行。

## Handoff 与下一授权

formal independent acceptance evidence 完成后，由 APP 总架构独立验收负责人复核本 evidence exact commit/hash；Go 后交平台集成负责人受控合并并更新 cross-record 与 reviewer work item 生命周期。owner 不自行更新 registry、不自行集成，也不激活 NOVA。
