# 学习广场 M0-R2 独立验收 No-Go

日期：2026-07-13
验收角色：学习广场独立验收负责人
验收对象：`53c7c4be2043118d091ed3b2c5c750c46a490c49`
目标 base：`029650f79c1d1cefa57b316df75af1c4c592c746`
结论：**No-Go**

## 已通过

- PR 三点差异 25 个文件，全部位于学习广场两个允许目录。
- 无冲突合并树保留 base 的 foundation 与 activity 文件。
- 当前 v3 合同人工语义正确；原 27 条 fixtures、旧 M0 16 条回归、UTF-8、diff 和敏感模式扫描通过。

## 阻断

1. 合入目标 base 后，M0/M0-R2 checklist 对 `agent-collaboration.v1.json` 的 SHA 均过期。
2. M0 与 M0-R2 考试完成时间早于 checklist 完成时间，不满足 ADR 0017 的真实因果顺序。
3. 五类非法变异均产生 `schema_errors=0, invariant_errors=0, fixture_failures=0`：外部项目替换、知识/非知识目录 owner 对调、双关审核绕过、端口提前 verified、端口 ID 漂移。

## 允许的下一步

只允许形成 M0-R3 修正候选：同步最新权威基线、保留历史失效证据、重新完成 checklist 后考试、强化 Schema/validator/fixtures，并重新独立验收。当前对象不得合并或激活 M1。
