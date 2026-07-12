# HM-R0 F2-FRESH-01 独立验收与受控集成

- work item: `AIW-20260713-HEALTH-R0-F2-FRESHNESS-ACCEPTANCE`
- F2-0 source: `5b51d1d1433b67219bcb1803a9383e65233b3cd6`
- freshness source: `66cc6cb9545eef461e9f20c9c93c13fe05151a0c`
- authority before acceptance: `e947d70498fbd9e1731d83d71c2aa64645c98a29`
- controlled merge: `58c3a7cd4496bc9e3c8d5e545a046135e3d5d54a`
- verdict: **F2-FRESH-01 Go**

## Independent proof

1. source 与远端模块分支一致、工作树 clean；freshness 相对 F2-0 为 9 个 allowed paths。
2. formal-freeze 当前状态为 `F1-accepted-integrated-for-development-planning`，并精确绑定 F1 source、source merge、acceptance evidence、authoritative integration 和平台验收报告。
3. C4-T06 继续为 `Exact revision`，只剩 PR #1/#2 的单独处置；F1 平台复核不再被错误列为缺失证据。
4. 27 项仍为 2 Accepted / 24 Pending with owner / 1 Exact revision；分类 7/16/4；owner 与所有 executable=false 不变。
5. valid Schema 通过；candidate 回退、缺 F1 证据、Pending 擅升、分类漂移、executable、production identity、auto-merge、P3、F3 提前收口、重新加入 F1 缺失证据等 10 类负例全部拒绝。
6. 模块 current checklist 28/28、exam100、IR、collaboration、Service Plaza 总合同、UTF-8、diff、scope、secret/control-char 通过。
7. 平台 current checklist 26/26、exam100；独立复跑证据引用、10类负例和治理门禁通过。

## Root cause closeout

- symptom: F1 已平台 Go/集成，但 formal-freeze JSON/Schema 与人工决定仍写 candidate/awaiting review。
- earliest controllable cause: F1 候选合同未定义平台 Go 后的状态回写门禁。
- systemic fix: 将 F1 acceptance 设为结构化必填对象，并在 Schema 中锁定精确 source/merge/evidence/integration/report；用负例阻止候选回退和缺证据。
- blocks closed: F2 当前真相与 Handoff 的 freshness 阻塞。
- does not close: 完整 F2 六类审计、C4-T06 PR 处置、F3/P3 和任何业务/真实活动门禁。

## Handoff boundary

本检查点只表示 freshness closeout 可以受控集成。模块工作项转 `handoff-ready`，等待平台另行裁定是否授权完整 F2-1。不得从本次 Go 推导 F2 complete、F3/P3、代码、真实数据、环境、医疗、收费、资金、部署或生产。
