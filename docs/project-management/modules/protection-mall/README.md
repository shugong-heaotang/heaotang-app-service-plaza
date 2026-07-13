# 保障商城子项目

## 当前目标

商城提前开发但不提前上线。当前仅执行 `M0 R3 correction`：纠正模块内部依赖合同和模块证据所有权，不编写交易业务代码。

## 当前工作项

- `AIW-20260712-PROTECTION-MALL-M0-R3-CORRECTION`
- 分支：`codex/protection-mall-m0-r3-correction`
- 当前状态：Active，等待平台会签与独立验收

## 冻结边界

- `service_id/action_id=protection-mall`
- 路由：`/services/protection-mall`
- 返回：`/services`
- 会话：`shared_session`
- 遥测：`service_plaza.protection_mall.open`
- 生命周期：`planned`

`mall.api.v1` 必须采用统一信封、request/correlation ID、真实权限来源、原子幂等、脱敏审计、关键配置失败关闭和向后兼容演进。

## 非目标

- 不修改服务广场受保护契约。
- 不开发商城业务代码。
- 不部署，不接入真实支付，不处理真实会员数据。
- 不接管、cherry-pick、reset 或整体复制旧 `6bce98f` 与旧脏工作树。
- 不在 foundation 目录创建商城模块检查单、考试或实施记录。

## 必读入口

1. 根 `AGENTS.md`、`README.md`、`CONSTRAINTS.md`。
2. `docs/project-management/notices/2026-07-12-protection-mall-m0-task-order.md`。
3. `contracts/modules/protection-mall/internal-dependencies.v2.json`。
4. `docs/project-management/modules/protection-mall/handoff-m0.md`。

## 下一授权

R3 通过平台会签和独立验收后，项目最高负责人才能另立并激活 M1 精确代码工作项。支付安全、资金状态机、回调验签和对账继续阻塞上线。
