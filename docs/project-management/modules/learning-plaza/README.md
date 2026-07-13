# 学习广场

学习广场是生命导航的学习执行层：把成长方向转换为资源、路径、共学和可验证成果。当前检查点为 M0，只交付版本化合同、确定性 fixtures 和离线验证，不包含正式页面、API、数据库、部署或上线。

## 核心板块

1. 学习资源：`article/course/book/note/live/replay`。
2. 学习路径：把资源组织为有序成长步骤。
3. 课程与进度：只允许受控状态转换并保证重复请求幂等。
4. 俱乐部共学：俱乐部是共学组织容器，但不得越过会员可见性。
5. 学习成果：完成事实生成版本化事件，不直接写生命导航数据。
6. Nova 辅助：只能使用当前用户可见且带引用的资料，不代替用户接受路径、提交成果或加入俱乐部。

## M0 边界

- `execution.mode=mock-only`、`environment=non-production`。
- 跨模块端口在真实 owner/version 未确认前为 `provisional`，调用必须失败关闭。
- 读书是学习资源类型，不在 M0 建完整阅读器。
- 可执行入口：`python -X utf8 contracts/modules/learning-plaza/m0/validate_learning_plaza_m0.py --self-test`。

下一检查点：独立验收 M0；Go 后另行派发 M1 最小真实闭环。
