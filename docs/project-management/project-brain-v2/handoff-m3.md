# Project Brain v2 M3 Handoff

- work item：`AIW-20260717-PROJECT-BRAIN-V2-M3-BOSS-DASHBOARD`
- R3 exact start authority：`d1531daed440d4776c22f58c127710eb20eb2128`
- 当前结论：R1 exact `b5b09398858c39531e4ae9d42c2aa82ab21e626f`与R2 exact `545f1386c4421929be560caf36e6060f2a061499`均保留历史结论且未集成。M2 G0 remediation `d1531daed440d4776c22f58c127710eb20eb2128`已独立Go并进入authority；R3从该authority重建M3内容，必须重新完成全部门禁与独立整体验收。当前不是accepted、pushed、integrated、deployed或production。

## 目标证据

- 服务端签名会话与角色授权；
- M2 audit/run/snapshot只读一致性验证；
- 安全聚合view model与Unknown/No-Go解释；
- 只读page/API与无脚本HTML；
- direct URL/API/export/write/tamper/privacy负例；
- 默认关闭、无network/server/source-write/real-source能力。

## 已交付实现

- 固定版本dashboard policy、server-session claims和overview Schema；仓库默认策略在`production`形态下强制全关闭。
- 注入式32字节以上HMAC密钥、固定算法、issuer/audience/subject/roles/iat/exp/nonce服务端验证；nonce必须再通过注入的服务端校验器。
- 对M2 `audit.jsonl`、immutable run record、content-addressed snapshot、last-trusted pointer、M1 fact catalog/source map/privacy policy执行独立只读复核。
- 所有事实按M1 `allowed_roles`二次过滤；G1重新检查阈值、`rounding_base`、维度、禁止字段、synthetic和`decision_usable=false`。
- `Unknown/No-Go`可解释；只允许显著标记为`LAST TRUSTED · STALE`的历史安全聚合，不把历史值改写成当前Trusted。
- 进程内GET page/API、无脚本/表单/操作链接HTML、CSP/no-store；匿名、伪造、过期、错audience、错角色、direct URL、export、写方法和未知路径失败关闭。

## 开发者验证

- current checklist：26/26，attestation exact，current checkpoint识别为completed。
- governance exam：attempt 1，100分。
- M3 R2 tests：48/48 passed（含完整重哈希后把G1值改为121、119、120.5的舍入负例、bucket舍入负例、definition漂移、小样本、危险维度、行级结构、audit/run/snapshot/pointer篡改、权限与导出负例，以及上游G0缺陷最小复现）。
- 历史R2证据：M2 regression 35/35；M1 regression 20/20。R3必须以集成后的M2 43项重新执行，不沿用这些数字作为当前证据。
- M3合同门禁：default-off、offline、no network/process/source-write import通过。

## R1 独立审查与 R2 整改

- reviewer冻结对象：`b5b09398858c39531e4ae9d42c2aa82ab21e626f`；报告SHA-256：`7f8514fc08c6931e0c9166133a01404ae74fde914728db2cfbd959668be879df`。
- R1结论：M3实现候选自身`No-Go`；M3整体Acceptance `No-Go`；`P0=0 / P1=2 / P2=0`；禁止push/integration。
- M3自身P1：重算snapshot/run/audit/pointer完整hash链后，违规G1值121仍被R1当作Trusted接受。
- R2系统修复：从当前M1 privacy policy读取正整数`rounding_base`，对每个G1标量或安全bucket数值叶执行舍入校验；策略无效或数值不满足舍入时失败关闭为`ROUNDING_POLICY_FAILED`。
- R2防复发证据：完整重哈希121、119、120.5三个标量篡改均被拒绝；未舍入bucket值也被拒绝；合法120继续Trusted。
- 上游P1没有在M3越界修复，继续由下述独立M2 remediation负责。R2提交、自测或候选存在均不替代新的exact独立验收。

## Root Cause Closeout Record：PBV2-M2-G0-PRIVACY-THRESHOLD-001

以下 symptom、causal chain 与原 verdict 是R1/R2历史证据；当前resolution以本节末尾及R3证据为准，不改写旧No-Go。

### Identity

- owner：Project Brain v2 M2 remediation runtime owner（已完成独立Go与受控集成）
- first_seen / recurrence_count：2026-07-17 / 1
- affected_checkpoint：M2 trusted G0 refresh、M3 boss dashboard Acceptance

### Evidence

- symptom：`trusted-g0-synthetic.json`经M2 `RefreshEngine.run`返回`No-Go / PRIVACY_THRESHOLD_FAILED / snapshot_hash=null`。
- exact stop：`project_brain_v2/runtime/engine.py::_evaluate`对全部`Trusted`先选择high或standard最小样本；G0的`privacy_risk_tier=not_applicable`被错误落入standard阈值，且随后还要求`privacy_threshold == pass`。
- expected / actual：G0应按M1合同要求使用`sample_size=null`与`privacy_threshold=not_applicable`并可形成Trusted合成快照；实际无法生成任何G0 Trusted快照。
- product evidence：两个核心治理事实`governance.work_items.status_counts`和`governance.implementation_records.verification_counts`均为G0，因此老板驾驶舱当前只能把它们显示为未刷新Unknown，不能展示Trusted治理经营事实。
- tool/environment：M3测试`test_inherited_m2_g0_threshold_blocker_is_reproduced`稳定复现；M1已有`test_g0_cannot_claim_privacy_threshold_result`，证明G0不得伪装G1阈值结果。

### Causal chain

1. 因为M1把G0明确建模为`not_applicable`且无样本量，所以合法G0 fixture使用`sample_size=null`。
2. 因为M2 `_evaluate`仅区分`high`与“其他”，所以G0被套用standard minimum group size。
3. 因为M2 35项测试的Trusted主路径只覆盖G1，所以该跨分类分支缺口未被验收发现。
4. 因为M3必须复用M2不可变证据而不得伪造或改写状态，所以M3不能局部绕过；最早可控原因是M2分类分支与缺失的G0 runtime回归测试。

### Impact

- affected paths：`project_brain_v2/runtime/engine.py`、`project_brain_v2/runtime/tests/test_engine.py`及所有消费G0快照的M3视图。
- security/data/release：失败关闭，没有敏感数据泄露或源写入；影响是核心治理事实不可用和错误No-Go，不是安全放宽。
- blocks：M3独立Acceptance Go、M3受控集成、M4激活。
- does_not_block：M3安全内核/合同/权限负例继续验证，Project Brain v1、M1合同、M2 G1合成路径及所有非PB隔离项目。

### Resolution and prevention

- rejected workaround：不得在G0伪造sample size、把`not_applicable`改成`pass`、在M3把No-Go提升Trusted，或修改M3验收标准。
- systemic fix：另建M2 remediation工作项；G0只接受`privacy_threshold=not_applicable`且不执行样本阈值，G1继续按risk tier执行阈值；其他Trusted checks仍完整执行。
- prevention gate：新增G0 Trusted正例生成snapshot/pointer/audit、G0伪造sample/privacy result负例、G1 high/standard阈值与rounding回归，并复跑M2 35项、M1 20项与M3 48项。
- compatibility/rollback：不改变M1合同、既有G1结果、快照Schema或历史证据；修复提交可普通回退，历史错误No-Go保持不可变。
- historical verdict：`Fail` for M3 R1/R2 overall Acceptance；M3 implementation当时为`Conditional Pass`等待上游修复。
- resolution：M2 activation R2与formal remediation均已独立Go并受控集成；authority=`d1531daed440d4776c22f58c127710eb20eb2128`，M2 43/43、M1 20/20、独立变异20/20。
- next authorization：本R3在新authority上重跑M3 exact candidate整体验收；只有R3独立Go并受控集成后，才允许另建registry closeout，M4-M5仍不自动授权。

## R3 developer evidence

- M3 dashboard与权限/读取/舍入/篡改回归：48/48；旧“复现G0阻塞”用例已改为证明集成后的合法G0为Trusted并可被只读overview验证；
- M2 remediation：43/43；M1合同与变异：20/20；M3/M2/M1合同validator均通过；
- current checklist 26/26、Exam100、collaboration、IR、总合同、1642文件UTF-8和diff通过；
- exact scope 25文件、8类登记路径、越界0、secret0；最终fetch时remote authority与local base均为`d1531daed440d4776c22f58c127710eb20eb2128`。

这些仍是writer证据，不构成R3整体Go；必须由独立reviewer对新exact candidate重新执行安全、可用性和freshness验收。

## 后续边界

开发者自测不构成M3 Go。只有exact candidate独立安全与可用性验收Go、freshness和受控集成后，M3实现才进入authority；registry收口仍需单独工作项。M4-M5及真实数据、auth接线、route、部署、timer和production继续No-Go。
