# ADR 0021：Legacy lifecycle 使用固定收据与 Git provenance

- 状态：Proposed，等待独立验收与受控集成
- 日期：2026-07-15
- 决策者：平台交付流治理实施负责人；最终裁决保留给独立 reviewer 与项目最高负责人

## 背景

`delivery-flow-policy.v1` 以外部 Git 快照和 legacy id/state hash 防止历史状态被
静默改写，但也使合法的 legacy 终态迁移无法表达。与此同时，检查单回归把历史
兼容快照硬编码在 Python 集合中，并用可变的当前 registry 反查历史授权，新增
Network 快照和平台注册表后续检查点后稳定出现 3 个失败。

## 决策

1. 保留 v1 外部 snapshot commit/path、cutover、work-id hash 和 state hash；V2
   不改写历史锚。
2. 每次 legacy 状态事务必须由版本化 schema 和固定 SHA 的 receipt 授权。收据
   绑定 source registry、逐行 source/state hash、canonical transition hash、
   post effective-state hash 和任务通知；只接受完整 before 或完整 after，partial
   必须失败关闭。
3. `LLM-20260715-ACTIVITY-MALL-M2-R1` 当前仅是
   `authorized-not-applied`：`applied=false`、post registry/review/integration 均空。
4. 历史 checklist 兼容从 Python 静态集合迁移到 receipt：每个快照绑定 path、
   bytes SHA、record/work identity、scope、authority commit 和可用 task-order。
   新增未登记快照继续失败。
5. V2 显式继续治理 registry 中现有 `delivery-flow-policy.v1` 工作项，禁止因
   policy 升版使 WIP、时效、职责分离和 completion 门禁集合变空。

## 被拒方案

- 直接扩充 Python 例外常量：再次制造下一次漂移。
- 修改历史 passed checklist 的 `module_id`：破坏不可变考试与实施记录链。
- 直接改 legacy registry status 并重算 policy/schema：无法抵抗三联篡改。
- 只验证五行 status：会绕过 handoff owner、独立验收和 integration evidence；
  V2 只解除 legacy hash 阻塞，其余生命周期门禁仍继续失败关闭。

## 后果与回退

V2 增加一个固定 receipt 和 Git object 读取成本，但迁移范围、历史授权和篡改证据
变为机器可复核。若独立验收 No-Go，回退为不集成 J2 单一提交；authority 与 v1
保持不变，五行事务仍未执行。
