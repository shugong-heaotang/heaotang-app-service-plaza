# 学习广场 M0-R3 独立验收 No-Go

日期：2026-07-13

候选：`11a1f9369f23dfbc63e05044f2eba7ff9b65fb11`

基线：`44325310f4bddfc8ddcb4b1f6e02402cc719c001`

## 通过项

- 精确提交、PR head/base、三点 diff 范围、merge-tree、历史证据原字节和 R3 治理时序均通过。
- M0-R3 34 fixtures、旧 M0 16 fixtures、依赖、治理、UTF-8、diff-check 与敏感信息门禁均通过。

## 唯一阻断

`validate_contract()` 同时返回 Schema 和手写 invariant 错误，mutation gate 又单独计算 Schema 后把该混合结果命名为 `invariant_errors`。剔除 `schema:` 错误后，外部项目替换、目录 owner 对调、双关审核绕过和端口 ID 漂移四类 mutation 的独立 invariant 数量均为 0；只有端口提前 verified 被独立 invariant 拒绝。

因此 M0-R3 的“5 类 mutation 均由 Schema/invariant/fixture 三层拒绝”声明为假绿，候选不得合并或激活 M1。M0-R4 必须拆分 Schema 与 invariant 计算，为五类变异建立独立 invariant，并重新独立验收。
