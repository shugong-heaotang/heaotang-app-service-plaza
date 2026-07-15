# 平台交付流 Legacy Lifecycle Migration V2 任务通知

- work_id：`AIW-20260715-PLATFORM-DELIVERY-FLOW-LEGACY-MIGRATION-V2`
- record_id：`IR-20260715-PLATFORM-DELIVERY-FLOW-LEGACY-MIGRATION-V2-J2`
- platform scope：`module_id=null` 的平台治理切片
- exact base：`8776166a52249c673ecaa24b4cd6b0522f4aba59`
- developer / reviewer / approver：平台交付流治理实施负责人 / 平台治理独立测试负责人 / 项目最高负责人

## 当前检查点

J2 只建立可执行、失败关闭的 Legacy V2 机制和固定授权收据，不修改
`agent-collaboration.v1.json`，不执行 Activity / Protection Mall 五行状态事务。

固定收据 `LLM-20260715-ACTIVITY-MALL-M2-R1` 必须保持：

1. v1 外部锚点、路径、cutover、legacy work-id hash 与 legacy state hash不变；
2. source registry SHA-256 绑定 J1 exact 的完整 registry；
3. 五行按 index 升序声明 `from_status` / `to_status`，canonical bytes 固定为
   `work_id<TAB>from_status<TAB>to_status<LF>`；
4. transition SHA-256 固定为
   `5dfa87a441a04eb8a24e3a4de883648780b6eaeddf2c870d831fa6ed29620939`；
5. post effective-state SHA-256 固定为
   `7f1991952dea49dff84e6378dbdc4edd22f4bf72334e0a8c08a36474fb984ec6`；
6. 本检查点 `applied=false`、`post_registry_sha256=null`，review 与 integration
   字段必须为空，禁止预填未来证据。

## J1 非状态刷新边界

J1 只对 legacy indices 109、111 的 `updated_at`、`target_date`、
`next_checkpoint`、`status_expires_at` 做真实监督刷新。两行状态保持 `active`，
legacy work-id/state hash 均不变。该事实由 J1 task order、entry checklist、exam100
和 source registry SHA 证明；固定收据不得把它冒充成已经执行的状态迁移。

## 失败关闭要求

- receipt 必须同时校验 source registry、逐行 before hash、完整五行集合、顺序、
  canonical transition hash、post effective-state hash和本任务通知 SHA；
- 缺行、增行、乱序、字段篡改、锚点漂移、source registry 漂移、提前填入 review /
  integration 或把 `applied` 改为 true，全部拒绝；
- checklist 兼容只允许由 V2 policy 中带 SHA 的不可变历史快照或 Git 引入提交中的
  registry/task-order provenance 证明，禁止扩大 Python 静态例外集合；
- 不修改历史 passed checklist / exam；不修改 registry；不执行 B 五行事务；
- 禁止业务代码、部署、生产、真实数据、资金、不可逆操作和自我验收。

## 验收

focused Legacy V2 tests、完整治理回归、Service Plaza 总合同、UTF-8、scope、secret、
registry zero-diff 与 `git diff --check` 全绿后形成单一 J2 commit，并停止等待独立验收。
