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
- 3 个 synthetic 正向/失败关闭样例；
- 10 个负例及精确错误码；
- 独立 contract validator 和 6 项回归测试；
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
8. 10/10 负例均以预期错误码拒绝，6/6 回归通过；
9. checklist/exam/IR、总合同、UTF-8、diff-check、secret0、scope 和 freshness 全部通过；
10. 候选不存在 runtime、真实数据、部署或生产授权。

任一 Unknown、authority 漂移、路径越界、真实数据或权限扩大均为 `No-Go`。

## 下一动作

独立 reviewer 文件化 Go 后，平台集成负责人可普通 fast-forward 集成 M1。M1 integrated 后也只解锁 M2 的另行激活治理；不得直接实现或启用定时刷新，更不得进入 M3 驾驶舱或 production。
