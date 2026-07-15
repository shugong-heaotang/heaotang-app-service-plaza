# Project Brain v2 M0 独立验收标准

## 1. Go 条件

1. M0 任务令、八份 `project-brain-v2` 项目治理文档、ADR0021 以及同 record 的 checklist、exam100、verified IR 齐全。
2. 章程明确项目最高负责人、项目负责人、事实 Owner、独立 reviewer、approver、integration owner 和安全发布角色。
3. v1 单一权威、只读、无回写、显式 `Unknown/No-Go` 与失败关闭被完整继承。
4. 首期仅允许项目治理事实和条件准入的去标识经营聚合。
5. 行级会员、健康、交易资金、客服数据及秘密明确禁止。
6. 来源映射包含 authority、owner、freshness、quality、classification、permitted use、evidence 和 failure state。
7. scheduler 与 dashboard 均只读；不存在源系统写端口。
8. production routes、snapshots、jobs、dashboard、export 默认关闭。
9. 明确 `code integration != production enablement`。
10. 权限、审计、发布、禁用和回滚原则完整。
11. M1-M5 每阶段都有解锁条件、独立验收和 No-Go 边界。
12. 总合同、UTF-8、scope exact13、secret0、freshness 全部通过。
13. Handoff 明确“候选、未集成、未生产”，并由独立 reviewer 接收。

## 2. 必须判 No-Go 的负例

出现以下任一情况，M0 必须判定 No-Go：

- 文档允许行级会员、健康、交易资金或客服内容进入首期。
- 把“聚合”视为无需阈值和重识别审查。
- 来源缺失时沿用未标注旧值或由 AI 猜测。
- dashboard 或 scheduler 存在回写、审批、改状态或源系统变更权。
- 前端隐藏被当作权限控制。
- 生产开关默认打开。
- 普通生产构建自动携带或生成真实快照。
- 将提交、推送、合并或构建当作生产批准。
- developer 自行替代独立 reviewer。
- M1-M5 被 M0 一次性授权。
- 缺少可验证 Handoff、IR 或 current governance evidence。

## 3. 独立验收方法

独立 reviewer 必须：

1. 逐项读取 M0 内容和证据；
2. 验证 checklist/exam/IR record ID 一致；
3. 检查所有禁止范围；
4. 搜索写回、生产默认打开和行级敏感数据授权；
5. 验证 M1-M5 解锁边界；
6. 运行合同、编码、范围、秘密和 freshness 门禁；
7. 给出逐项引用精确文件的结论。

未知或无法复核的项目不得推断为通过。

## 4. 结论格式

结论只能是：

- `Go`：所有 M0 条件均由当前证据证明；
- `Conditional Go`：仅允许明确的下一治理动作，不得冒充 M0 完成；
- `No-Go`：存在范围、安全、权威、证据或门禁失败。

M0 Go 只允许进入 M1 立项，不授权 M1 以外阶段或任何生产动作。

## 5. 角色分离

- developer：Project Brain v2 project owner
- reviewer：independent Project Brain v2 reviewer
- approver：项目最高负责人
- integration owner：平台集成负责人

reviewer 不参与实现；developer 不修改 registry 或执行最终集成；integration owner 不替代独立验收。
