# S4 UAT 六路由产品修复 R1 任务理解

## 目的

本工作项不是继续摊大饼，而是在唯一候选 `2df75b...` 上关闭已由 R5 不可变证据确认的六个路由缺陷，修通“可访问、可识别、状态唯一、静态数据可读”的主通道。

## 已知事实

- R5 证据完整性 Go：54 文件、22 actions、22 screenshots、126 audit rows。
- 产品 UAT No-Go：P004 `/activity-plaza/` 与 P011 `/member-home/` 为 P0；P007 `/ai-assistant/`、P008 `/internal/project-brain/`、P009 `/self-created/`、P010 `/self-created/applications/` 为 P1。
- P001、P002、P003、P005、P006 双视口已通过，后续作为非回归烟测。
- 当前 G1 只建立治理闭环，不写产品。

## 执行顺序

1. 完成治理阅读、检查表和同记录 100 分考试。
2. 形成 G1 实施记录与 Handoff，取得独立 G1 Acceptance。
3. 另行取得 G2 产品路径和命令授权。
4. 最小修复、单元测试、全量测试、构建和安全门。
5. 独立候选验收、全新部署门、受影响路由双视口回归与最终 Record。

## 停止条件

权限、路径、HEAD、registry 漂移；检查表不完整；考试低于 100；未授权产品写入；同一门禁第二次失败；真实资金、生产、敏感数据或不可逆操作。
