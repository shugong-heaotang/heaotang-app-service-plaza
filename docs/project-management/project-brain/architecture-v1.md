# 和奥堂 Project Brain v1 技术架构

## 1. 架构决策

第一版采用“仓库事实源 + 离线聚合器 + 静态只读驾驶舱”。

```text
Markdown / JSON 权威来源
          │
          ▼
Python 聚合与审计
          │
          ├── audit-report.json
          └── project-brain.snapshot.json
                         │
                         ▼
                 React 只读驾驶舱
```

不使用数据库。原因是第一版事实量小、需要 Git 追溯、现有权威来源都在仓库中。未来只有在多用户实时编辑成为明确需求后才评估数据库。

## 2. 权威来源

| 事实 | 权威来源 |
|---|---|
| Agent 工作项 | `contracts/foundation/agent-collaboration.v1.json` |
| 实施证据 | `contracts/**/implementation-records/*.json` |
| 架构决定 | `docs/decisions/*.md` |
| 模块依赖 | `contracts/foundation/module-dependencies` 与 `contracts/modules` |
| Project Brain 模块索引 | `contracts/project-brain/modules.v1.json` |
| 知识地图 | `contracts/project-brain/knowledge-sources.v1.json` |
| 待裁决事项 | `contracts/project-brain/decisions.v1.json` |
| 风险 | `contracts/project-brain/risks.v1.json` |

## 3. 计划新增路径

```text
PROJECT-BRAIN.md
docs/project-management/project-brain/
  README.md
  requirements-v1.md
  architecture-v1.md
  acceptance-v1.md
  handoff-v1.md
contracts/project-brain/
  *.schema.json
  modules.v1.json
  knowledge-sources.v1.json
  decisions.v1.json
  risks.v1.json
  generated/project-brain.snapshot.json
  generated/project-brain.audit.json
scripts/
  build_project_brain.py
  validate_project_brain.py
  tests/test_project_brain.py
app/src/modules/project-brain/
  ProjectBrainPage.tsx
  ProjectBrainPage.test.tsx
  projectBrainApi.ts
  projectBrain.css
```

## 4. 数据流

1. 聚合器只读打开权威文件。
2. 验证 JSON 模式、引用路径和状态完整性。
3. 规范化为不含秘密的快照。
4. 审计器输出 errors、warnings、unknowns。
5. 有 error 时命令返回失败，快照总体结论为 No-Go。
6. React 页面只读取已生成快照，不在浏览器中扫描仓库。

## 5. 快照模型

快照顶层包含：

- `generated_at`
- `source_commit`
- `overall_verdict`
- `source_freshness`
- `modules`
- `work_summary`
- `pending_decisions`
- `risks`
- `acceptance_queue`
- `recent_integrations`
- `audit_summary`

## 6. 安全边界

- 构建器采用允许字段清单，不把任意源字段复制到前端。
- 路径必须位于仓库内，拒绝 `..` 越界和绝对外部路径。
- 不读取 `.env`、密钥、测试账号内容或生产日志。
- 驾驶舱不包含写入 API。
- 默认仅测试构建启用入口；正式开放需单独权限 ADR 和安全验收。

## 7. 兼容策略

- 所有 Project Brain 合约采用显式 `contract_version`。
- 第一版只做向后兼容扩展。
- 破坏性字段变化必须升主版本并记录 ADR。
- 原有协作登记和实施记录不因 Project Brain 改名或迁移。

## 8. 关键前提与重审条件

- 前提：Project Brain 初期由少量 Agent 和一名项目负责人使用。
- 前提：事实以 Git 仓库为主，不要求多人实时编辑。
- 前提：驾驶舱只读即可满足第一版目标。
- 重审：出现多人并发编辑、跨仓库实时同步或大量非结构化检索需求时，重新评估后端数据库和检索服务。
