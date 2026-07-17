# Project Brain v2 M2 只读刷新任务令

- work item：`AIW-20260717-PROJECT-BRAIN-V2-M2-READONLY-REFRESH`
- exact authority/base：`701519ea1130b6620607de753aa03a7d93953f0b`
- branch：`codex/project-brain-v2-m2-runtime`

## 交付结果

实现可运行的离线只读 refresh engine：从 M1 allowlist 合同与 synthetic fixture 读取，生成内容寻址的不可变 snapshot、append-only run audit 和 fail-closed alert；具备幂等 run ID、单实例锁、超时、有限重试、失败不覆盖 last-trusted pointer、禁用和回滚演练。

## allowed paths

仅 registry 登记的八类路径：`project_brain_v2/**`、`contracts/project-brain/v2/runtime/**`、本任务令、M2 receipt、M2 Handoff、对应 checklist/exam/IR。

## 禁止范围

不得接真实业务源、网络端点、凭据或环境；不得修改 M1 合同、Project Brain v1、公共 scripts、App/dashboard；不得部署、发送真实通知或启用 production。所有运行都必须显式 `production_enabled=false`，默认 disabled。

## 验收

必须覆盖成功、幂等重放、并发锁、有限重试、超时、来源缺失、stale、权限/authority冲突、小样本、snapshot篡改、失败不覆盖、禁用、回滚和审计哈希链；独立 reviewer Go 后才可集成。M3 仍需另行激活。
