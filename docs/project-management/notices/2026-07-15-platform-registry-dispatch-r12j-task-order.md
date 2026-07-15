# 平台注册表 R12-J 直接负责人接续与 Legacy V2 激活任务通知

- work_id：`AIW-20260714-PLATFORM-REGISTRY-DISPATCH-R1`
- 直接授权 / approver：项目最高负责人
- owner：`Platform registry dispatch agent`
- developer / reviewer：平台注册表派发授权记录人 / APP 总架构独立验收负责人
- exact base：`49e9ad923b5de60ce196bca1344206cfd1b5bbdf`
- branch：`codex/platform-r12j-expiry-bootstrap`
- workspace：`C:/Users/shugo/Documents/项目最高负责人/worktrees/heaotang-platform-r12j-expiry-bootstrap`
- priority / risk / flow：`P0 / high / governance-repair`

## 直接授权与分段边界

项目最高负责人为“18 个小时项目”直接授权 R12-J。J1 只修复九个已有工作项的真实生命周期、所有权和时效，建立不可变的 entry checklist / exam100，并激活 Legacy Migration V2。其中 NOVA Runtime 和 Health F2-1 是执行期间 current-clock 门禁暴露后由项目最高负责人明确追加授权的真实时效/终态修复。J1 不实现 V2、不生成 fixed receipt、不修改 validator/test、不 push、不集成、不自验。

J2 必须由不同的 Legacy V2 Agent 在外部 clean worktree 执行，完成 schema/policy/receipt/tests 后再停止供独立验收。

## J1 九行原子事务

1. Activity index 109 保持 `active`，只刷新真实监督时间，等待 Legacy V2 receipt/integration。
2. Mall Catalog Solution index 111 保持 `active`，同样只刷新监督窗口。
3. NOVA Runtime index 117 保持 `active`，刷新当前监督窗口并继续 TaskRuntime-to-ToolRuntime 合成 E2E。
4. NOVA API Signoff index 118 从 `handoff-ready` 真实终态化为 `cancelled/no-go/superseded-by-future-R2`；不回填伪造的准时 response。
5. NOVA Overlay index 119 保持 `handoff-ready`，记录 reviewer artifact `d09d5d0ed53343480d4e9f1100b089e6861e8613` 在 `2026-07-15T07:57:03+08:00` 的 No-Go，并把两个需修复脚本的所有权移交 Legacy V2。
6. dispatch index 123 重绑本 worktree/branch/base，只授权 registry、本通知、独立 R12-J Handoff 及 entry/final checklist/exam/IR。
7. Overlay supporting index 125 保持 `active`，只刷新监督窗口。
8. Legacy V2 index 126 从 `planned` 转 `active`，base 绑定 `49e9ad9`，接收两个 Overlay 脚本，下一检查点为 J2 fixed receipt/schema/tests。
9. Health F2-1 index 129 以 `2026-07-15T07:32:05+08:00` fresh 联合复核 No-Go 从 `handoff-ready` 转 `cancelled`；保留 synthetic audit artifact、`synthetic_only=true` / `executable=false` 边界，缺少的六域专业、隐私/法务、运营和平台联合签署交由未来独立 owner items。

## 硬性验收断言

- registry 工作项总数保持 130，不增不删；除 indices `109,111,117,118,119,123,125,126,129` 外所有行逐字段不变。
- legacy 109/111 状态不变；legacy work-id hash 保持 `64105cf520b0c971150d0491eba27967d7976aa0bad89400ececd302959d650e`，legacy state hash 保持 `b7dc23fab67191405a852301ae4f9650164bf3e619bd323587d684f1e5773aaa`。
- scope overlap、collaboration、delivery-flow、current-clock total contract、UTF-8 与 diff 必须全绿。
- entry 证据通过后不得删除或改写；J2 完成后从 J1 exact 重新全文读取生成 final checklist/exam/IR/Handoff。
- 禁止业务代码、部署、生产、真实数据、资金、不可逆操作和自我验收。
