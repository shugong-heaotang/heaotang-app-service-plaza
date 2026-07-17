# Project Brain v2 M1 事实合同 Handoff

- 提交角色：Project Brain v2 M1 project owner
- 接收角色：independent Project Brain v2 M1 reviewer
- work item：`AIW-20260716-PROJECT-BRAIN-V2-M1-FACT-CONTRACTS`
- record：`IR-20260716-PROJECT-BRAIN-V2-M1-FACT-CONTRACTS`
- registered base：`86ab20f8928a6d70195edb3879fbe7083c20a0f9`
- resumed authority：`8e89ceda79827ee24fa115b2e993ba1c3f529aaa`
- 当前结论：M1 contract candidate；不是 integrated，不是 runtime，不是生产授权

## 已完成

- current checklist 26/26、governance exam attempt 1 score 100；
- 事实 catalog、来源映射、结果合同和隐私阈值 Schema；
- 2 项真实 G0 治理权威映射和 1 项 synthetic-only G1 验证映射；
- 标准阈值 20、高风险阈值 50、最多 2 维、按 5 取整、低于阈值抑制；
- 4 个 synthetic 正向/失败关闭样例；
- 10 个负例及精确错误码；
- 独立 contract validator 和 10 项回归测试；
- 所有来源 `runtime_enabled=false`，package `runtime_enabled=false`、`production_enabled=false`。

## 明确未完成与未授权

没有真实经营源、真实数据、行级数据、凭据、环境、scheduler、snapshot、alert、dashboard、export、notification、App 路由、部署或 production。没有修改 Project Brain v1、源系统、平台 runtime scripts 或 registry。M2-M5 继续 No-Go。

## 独立 reviewer 必须复验

1. exact candidate 直接基于 review 时 fresh authority；
2. diff 只有 registry 登记的 7 类 allowed paths；
3. 3 个 fact 均只有一个 authority/source owner，source map 逐项匹配；
4. 所有 source `read_only`、`write_capability=none`、`runtime_enabled=false`；
5. G1 只有 synthetic fixture、source disabled、production ineligible、decision unusable；
6. 阈值策略版本化，低样本、敏感分类、禁用维度、拼接和下钻失败关闭；
7. `Unknown/No-Go` 必须 value null 且不可用于决策；
8. 10/10 负例均以预期错误码拒绝，10/10 回归通过；
9. checklist/exam/IR、总合同、UTF-8、diff-check、secret0、scope 和 freshness 全部通过；
10. 候选不存在 runtime、真实数据、部署或生产授权。

任一 Unknown、authority 漂移、路径越界、真实数据或权限扩大均为 `No-Go`。

## 首轮独立验收与返工记录

首个 immutable candidate `367a8d4ef3020300d16a1c1e64e90ba24cebe932` 已由独立 reviewer 判定 `Acceptance No-Go / no-integrate`。外部报告 SHA-256 为 `38e5e46a39e61042c65477480280afff0e2077a7322d61bf309942eeba0f9656`。阻塞事实为：高风险 50 人阈值未机器选择、freshness 可自报绕过、object 数值可绕过按 5 取整、合法 undersized No-Go 无法表达。

本轮 remediation 保留该失败提交和报告，不 amend、不覆盖。新 candidate 增加 risk tier 契约匹配、SLO/time 复算、对象数值叶子取整和合法 undersized No-Go 正例及变异测试。必须重新执行完整门禁并另行独立验收；首轮 review 不能复用为 Go。

## 下一动作

独立 reviewer 文件化 Go 后，平台集成负责人可普通 fast-forward 集成 M1。M1 integrated 后也只解锁 M2 的另行激活治理；不得直接实现或启用定时刷新，更不得进入 M3 驾驶舱或 production。
