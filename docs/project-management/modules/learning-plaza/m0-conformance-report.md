# 学习广场 M0 合同验证报告

日期：2026-07-13
工作项：`AIW-20260713-LEARNING-PLAZA-M0`
结论：模块自测通过，等待独立验收；不得表述为 M0 Go 或已集成。

## 验证结果

执行：

```powershell
python -X utf8 contracts/modules/learning-plaza/m0/validate_learning_plaza_m0.py --self-test
```

结果：

- 核心合同不变量：PASS。
- 平台能力依赖：9/9 可解析，状态均为 `verified` 或 `deployed`。
- 确定性 fixtures：16/16 PASS。

正向覆盖公开资源、登录资源、俱乐部成员资源、私有本人资源、正常进度转换、带引用 Nova、已验证端口和首次完成事件。

负向覆盖匿名访问登录资源、非成员访问俱乐部资源、跨用户私有资源、跳过进度、无引用 Nova、Nova 代执行、provisional 端口调用和重复完成事件。

## 边界结论

- 参考 Nova 实现的 6 条验收通过，但不等于平台模块已集成。
- 四个跨模块端口均为 `provisional`，M0 只验证失败关闭，不执行真实调用。
- 完成事实只产生 `learning.outcome.completed.v1` 事件，不直接写生命导航数据库。
- M1 仍需独立确认内容版权、资源 owner、俱乐部会员端口、Nova 引用端口和完成事件消费者。
