# 学习广场 M0-R4 架构纠偏验证报告

日期：2026-07-13
工作项：`AIW-20260713-LEARNING-PLAZA-M0`
记录：`IR-20260713-LEARNING-PLAZA-M0-R4`

本检查点验证学习广场的独立项目身份、内部应用与连接能力分层、四种审核模式、俱乐部组织权、知识商品边界、Nova 权限、成长事件所有权和课程闭环顺序；同时关闭 M0-R3 独立验收发现的 Schema/invariant 混合计数假绿。结论仅为开发方修正自测通过，重新独立验收前不得称为 Go 或已集成。

验证命令：

```powershell
python -X utf8 contracts/modules/learning-plaza/m0-r2/validate_learning_plaza_m0_r2.py
```

预期证据：架构不变量 PASS、平台依赖 9/9、确定性 fixtures 34/34、关键 mutation gates 5/5。每类非法变异必须分别触发 Schema、只含手写规则的独立 invariant 与 fixture 失败；不得把 Schema 错误重复计入 invariant。审核双开、单开和双关均强制完整发布审计；所有五个运行时端口继续 `provisional/fail-closed`。
