# 健康大管家 MVP-90 M1 P1 Conformance 报告

- 日期：2026-07-12
- 范围：成年合成会员 PDCAR 合同
- 数据：固定 seed 合成数据，不含真实身份或真实健康数据
- 结论：11 tests PASS；P1 Exact revision 已完成，等待平台独立复核

## 数量与追踪

| 项目 | 结果 |
| --- | --- |
| PDCAR 纵切步骤 | 10/10 |
| M0 对象引用 | 全部存在 |
| M0 状态迁移引用 | 全部存在 |
| M0 角色引用 | 全部存在 |
| C4-S04 拒绝条件引用 | 全部存在 |
| C4-H01 动作边界 | 17/17，三角色决策逐项一致 |
| C4-H01 失败关闭 | 17/17 与签署源逐字一致 |
| C4-H01 转介责任 | 17/17 与签署源逐字一致 |
| MVP 场景 | 15/15，与 M0 及专业复核一致 |
| 场景安全/禁止/停止语义 | 15/15 三组字段与专业 Accepted 源逐字一致 |
| 固定 seed 夹具 | 15/15，全部 `syn-*` 标识 |

## 测试命令

```powershell
python -X utf8 contracts/modules/health-manager/mvp90-m1/conformance/test_health_mvp90_m1_contracts.py
```

结果：`Ran 11 tests ... OK`。

## 负向验证

测试会拒绝：

- 缺少任一 PDCAR 步骤；
- 缺少任一专业动作；
- 缺少任一 MVP 场景；
- `synthetic_only=false`；
- 纵切 `executable=true`。
- 任一专业边界的失败关闭或转介责任漂移；
- 任一专业边界 `source_pointer` 指向错误 action；
- 任一场景的安全结果、禁止结果或停止/转介条件漂移；
- 任一场景的专业或 M0 源指针指向错误 scenario；
- fixture 重复、缺失、错误配对或 member/request 引用不唯一。

## P1-XR-01—03 根因关闭记录

### Identity

- pattern_id：`HM-M1-P1-SIGNED-SEMANTIC-DRIFT`
- title：复制签署语义但 conformance 未逐字段锁源
- owner：健康大管家负责人
- first_seen / recurrence_count：2026-07-12 / 1
- affected_checkpoint：P1

### Evidence

- symptom：原 P1 测试全绿，但 17 项失败关闭、17 项转介责任和 15 场景三组安全语义均为自由英文改写；fixture 无独立 Schema。
- exact_stop：平台 `P1-XR-01`、`P1-XR-02` 阻断，`P1-XR-03` 要求补强。
- reproduction：将任一复制字段或源指针改为其他非空值，旧测试仍可通过。
- expected / actual：应逐字段等于签署源；实际只验证 ID、标题和状态。
- product_evidence：签署源未改变，缺陷仅存在于派生机器合同及验证门禁。
- tool_or_environment_evidence：本地 Python/jsonschema 正常，非工具故障。

### Causal chain

因为 P1 派生合同保存了自由翻译，因此产生第二真相源；因为旧 conformance 只锁 ID/状态，因此安全语义漂移仍可全绿。最早可控原因是缺少“解析 source pointer 并逐字段相等”的跨合同门禁。

### Impact

- affected_modules_and_paths：仅 M1 professional-boundaries、synthetic scenarios、fixtures 与 conformance。
- security_data_release_impact：未进入业务实现、环境或真实数据，无生产影响。
- blocks：P1 Go 与后续检查点。
- does_not_block：已签署 C4-H01、窄模板和 15 场景本身。

### Resolution

- rejected_workaround_and_reason：不接受继续保留自由翻译再用说明文档解释，因为它仍是未受保护的第二真相源。
- systemic_fix：派生合同直接复制签署源原文字段；测试解析 JSON Pointer 并逐项强制相等；fixture 增加 Schema 和 exact/unique 门禁。
- changed_contracts_code_tools：不修改签署源，只修改 P1 派生合同、fixture Schema、conformance 和证据。
- compatibility_or_migration：P1 尚未集成，无业务迁移；原 R2 保留为历史缺陷快照。
- rollback：回退本次 P1 修订会重新打开 P1-XR-01—03，不能用于进入下游。

### Prevention and proof

- prevention_gate：`test_health_mvp90_m1_contracts.py` 的源指针解析、逐字段相等、fixture exact/unique 正负例。
- positive_test：当前 17/17、15/15 与 15 fixtures 全部通过。
- negative_test：字段漂移、错误指针、重复 fixture 和重复引用全部被拒绝。
- regression_set：M0 对象/状态/角色、安全拒绝、Pending 门禁及原 8 项测试继续通过。
- environment_retest：不适用；环境仍 No-Go。
- evidence_paths_and_exact_commits：本报告、P1 R3 IR 和后续 exact source commit。

### Recurrence action and verdict

- first：模块内登记并建立本地防复发门禁；未修改平台受保护 recurring registry。
- verdict：Pass candidate，等待平台独立复核。
- unresolved_risk：共享实现、隐私法律、真实数据和生产仍未授权。
- next_authorization：平台 P1 Go。

## 未证明事项

本报告不证明 API、数据库、共享前后端、环境、部署、真实会员、真实健康数据、收费或生产可用；也不把窄模板扩大为全量 C4-H06。
