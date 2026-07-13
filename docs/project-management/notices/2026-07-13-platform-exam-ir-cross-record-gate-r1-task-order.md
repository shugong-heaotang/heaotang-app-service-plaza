# 平台治理考试与实施记录跨记录一致性门禁 R1 任务单

签发日期：2026-07-13
工作项：`AIW-20260713-PLATFORM-EXAM-IR-CROSS-RECORD-GATE-R1`
记录：`IR-20260713-PLATFORM-EXAM-IR-CROSS-RECORD-GATE-R1`

本项为 `platform scope`，current checklist 必须使用 `module_id=null`；这只证明平台治理范围，不授权修改 registry 或任何业务模块。

## 目标

修复考试快照、实施记录与 Handoff 可互相矛盾而仍被总门禁接受的问题。任何实施记录引用的考试必须存在，并且必须为同一 `record_id`、`status=passed`、`score=100`；失败或缺失证据必须失败关闭。

## 范围

- 平台 foundation 实施记录继续执行完整 Schema、路径和证据检查。
- 服务广场总门禁递归发现 `contracts/modules/*/implementation-records/*.json`，并对模块记录执行检查单与考试跨记录一致性检查。
- 增加同记录 100 分正向、75 分失败、record mismatch、exam missing 永久回归。
- 以保障商城 M2 九文件脏快照做只读环境负例，禁止修改或清理该工作树。

## 禁止边界

- 不修改 `agent-collaboration.v1.json`、NOVA、商城九个文件或任何业务代码。
- 不修改失败试卷，不把 75 分记录改写为通过。
- 不因历史模块实施记录的非 canonical 扩展字段降低 foundation 实施记录 Schema 门禁。
- 不部署、不触达生产、真实用户、凭据、支付或资金。

## 验收

1. 同 `record_id` 的 passed/100 考试可以支持实施记录。
2. failed/75、不同 `record_id`、缺失考试均失败关闭，错误包含实际状态。
3. 服务广场总门禁覆盖 foundation 与所有现有模块实施记录目录。
4. 当前保障商城九文件快照只读运行失败，运行前后状态和文件哈希不变。
5. 定向测试、全量治理测试、Service Plaza 合同、UTF-8、diff、secret 和授权范围检查通过。
6. 候选提交推送后等待独立验收；实施负责人不得自集成。
