# Project Brain M1-R3 证据真实性根因闭环

日期：2026-07-12
record_id：`IR-20260712-PROJECT-BRAIN-V1-M1-R3`
状态：整改完成，等待独立复验

## 精确症状

提交 `e982bedaf91ecd914a029ac9a7c561663d179b2a` 的 R2 Handoff 与 implementation record 声称 `git diff --check` 通过，但从权威基线 `f31f67f1613b7c97c9f46969d7c3eb59cdc0e46c` 检查该提交时，`delivery-plan-v1.md` 第 5、6 行和 `handoff-v1.md` 第 3 至 7 行共报告 7 处 trailing whitespace。该声明与可复现命令结果不一致，因此独立验收为 No-Go。

## 因果链

1. R2 记录只保存了“git diff --check”文字结论，没有固定基线、目标提交和输出。
2. 验收时实际需要检查的是完整迁入差异 `f31f67f..HEAD`，而非未明确范围的局部工作区检查。
3. 缺少“证据命令必须带精确范围并由独立验收重跑”的关闭门禁，使错误的通过声明进入 IR/Handoff。

## 影响扫描

- 受影响：R2 Handoff 与 R2 implementation record 中关于 diff 门禁通过的可信度；M1 结论不得提升为 Go。
- 未受影响：旧 R2 checklist、exam、implementation record 及 invalidated snapshots 均保持历史 blob 不变；R3 不改写旧证据。
- 范围审计：R3 仅修改当前工作项 allowed paths；没有修改 `scripts/`、`app/` 或任何 SC remediation 路径。

## 系统性修复

- 删除 7 处行尾空白并对完整基线差异重跑检查。
- 四类 Schema 与首批数据补齐独立验收指出的字段，item 采用 `additionalProperties=false`。
- 模块状态来源固定到可机器解析的 JSON Pointer 或可精确查找的 Markdown 字段；Nova 不虚构工作项或 active 状态。
- R3 IR 与 Handoff 只记录真实执行结果，状态保持 `implemented` / No-Go pending independent review。

## 防复发门禁

提交前和独立复验必须执行：

```powershell
git diff --check f31f67f1613b7c97c9f46969d7c3eb59cdc0e46c..HEAD
```

如果正在检查尚未提交的 R3 工作区，还必须执行：

```powershell
git diff --check f31f67f1613b7c97c9f46969d7c3eb59cdc0e46c
```

任一命令有输出或非零退出即失败关闭；IR/Handoff 不得写“通过”。

## 复验证据

- R3 提交前工作区门禁、提交后 `f31f67f..HEAD` 门禁及其真实结果记录在 R3 implementation record 和 Handoff。
- 四类 Schema、来源定位、Service Plaza contracts、checklist SHA、exam 引用链、UTF-8、敏感信息与 allowed scope 均须独立重跑。
- 最终结论仍由 Project Brain 项目负责人独立复核；本闭环不自行声明 M1 Go。
