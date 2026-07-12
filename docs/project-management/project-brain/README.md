# Project Brain v1

## 当前阶段

第一版建立全 APP 统一知识入口、四类结构化事实、自动治理审计和项目负责人只读驾驶舱。

## 权威文件

| 类别 | 位置 |
|---|---|
| 产品需求 | `requirements-v1.md` |
| 技术架构 | `architecture-v1.md` |
| 开发检查点 | `delivery-plan-v1.md` |
| 验收标准 | `acceptance-v1.md` |
| 模块与知识事实 | `contracts/project-brain/` |
| Agent 工作事实 | `contracts/foundation/agent-collaboration.v1.json` |
| 架构决定 | `docs/decisions/` |

## 当前边界

- 只读、内部使用、失败关闭。
- 不保存密码、令牌、健康明细、手机号或支付明细。
- 不增加第二套任务状态。
- 首期不使用数据库或向量检索。

## 聚合与审计运行方式

```powershell
python -X utf8 scripts/build_project_brain.py `
  --project-root . `
  --snapshot contracts/project-brain/generated/project-brain.snapshot.json `
  --audit contracts/project-brain/generated/project-brain.audit.json
```

审计出现 error 时返回非零，禁止把结果标记为 Go。

## 内部驾驶舱

- 开发/测试路由：`/internal/project-brain`
- test-server 制品必须显式把已验证快照装配到 `/project-brain/project-brain.snapshot.json`
- 普通 production 构建重定向内部路由且不包含快照资产
- 页面只读；缺失或读取失败显示 Unknown；审计 No-Go 不得提升
