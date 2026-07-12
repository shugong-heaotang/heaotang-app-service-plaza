# 和奥堂 Project Brain v1 分阶段开发任务书

## M0 设计与授权

交付：需求书、架构、数据示例、验收矩阵、专用工作项。  
门禁：权威基线明确；工作范围无重叠；起飞检查和考试通过。  
非目标：不修改业务代码。

## M1 权威入口与事实模型

交付：

- `PROJECT-BRAIN.md`
- Project Brain README
- 四类 JSON Schema 和首批真实登记
- 引用路径验证测试

检查点结论：从入口能够定位全部首批权威来源；所有 JSON 通过模式验证；未知信息明确标识。

## M2 聚合器与治理审计

交付：

- 只读聚合程序
- 十类审计规则
- 快照与审计报告
- 正常、缺失、过期、冲突和越权测试夹具

检查点结论：任何 error 均返回非零；无证据完成、重复权威和高风险角色冲突不能被报告为 Go。

## M3 老板只读驾驶舱

交付：

- 内部 Project Brain 路由
- 总览、模块、任务、风险、决策和验收区块
- 来源追溯与生成时间
- 桌面和手机响应式测试

检查点结论：页面只读；不影响现有服务路由；缺数据呈现 Unknown；测试构建通过。

## M4 独立验收与集成

交付：

- 自动化测试、构建和编码门禁
- 安全审计
- 浏览器 UAT 证据
- 实施记录和 Handoff
- 独立验收结论

只有独立验收为 Go 且集成提交存在，工作项才允许标记为 integrated。

## 建议工作项边界

第一项工作建议只覆盖文档和 Project Brain 新目录，不修改现有 `App.tsx`：

```text
PROJECT-BRAIN.md
docs/project-management/project-brain
contracts/project-brain
```

第二项覆盖聚合程序：

```text
scripts/build_project_brain.py
scripts/validate_project_brain.py
scripts/tests/test_project_brain.py
```

第三项覆盖驾驶舱：

```text
app/src/modules/project-brain
app/src/App.tsx
app/src/App.test.tsx
```

因 `App.tsx` 可能与其他前端工作项重叠，必须由平台集成负责人另行确认后才激活第三项。
