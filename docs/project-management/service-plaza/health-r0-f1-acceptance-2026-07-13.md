# HM-R0 F1 独立验收与受控集成

- 工作项：`AIW-20260713-HEALTH-R0-F1-ACCEPTANCE`
- 模块工作项：`AIW-20260712-HEALTH-R0-FORMAL-FREEZE`
- 独立复核 source：`384436c719396d0a0105f448716ef37aa8ba7ab8`
- 权威集成前基线：`cd2bbae681767262994f53cd1fecd3c2e35bdd1d`
- F1 source 受控合并提交：`fb1b882091209897d9f618659ce02733d670b53e`
- 裁定：**F1 Go / Accepted for development planning**

## 独立证据

1. source 与远端模块分支一致，工作树干净；merge-base 为已授权 F1 基线 `1927ae133fdd70117f5358dc3485492781b7bc23`。
2. 相对授权基线仅新增 6 个允许路径，旧 F0、Draft PR #1/#2、F2/P3 均未修改。
3. 27 项决定 ID、顺序和对象被 Schema 精确锁定：`2 Accepted / 24 Pending with owner / 1 Exact revision`；分类为 `7 blocks-development / 16 blocks-real-data-environment / 4 does-not-block-synthetic`。
4. Draft 2020-12 valid instance 通过；删减、重复、额外、未知、乱序、擅自提升 Pending、修改分类或证据、提升 executable、生产身份、自动合并、P3、缺 owner、缺 revision payload、源提交漂移等 15 类负例全部拒绝。
5. 模块 F1 checklist 28/28、current SHA mismatch=0；完成检查单、生成试卷、提交试卷的因果时序正确；考试 attempt 1 为 100 分；IR、协作登记、总合同、UTF-8、diff、scope 和敏感模式检查通过。
6. 平台首轮 checklist 使用了非精确 attestation，绑定的 attempt 1 虽为 100 分但不授权集成；两份原始记录保持不可变并移入 invalidated snapshots。平台 R2 checklist 26/26，R2 随机治理考试 attempt 1 为 100 分，作为当前有效准入。

## 权威边界

本次 Go 只确认 HM-R0 可作为开发规划冻结依据，且所有决定仍遵守各自状态。`executable=false`，production identity 仍 Pending，Draft PR #1/#2 继续只读且不自动合并。

以下事项继续 No-Go：F2、P3、共享业务实现、前后端/API/数据库、真实身份/会员/健康数据、环境、医疗服务、收费、资金、部署和生产。后续阶段必须另行派发，不得从本次 F1 Go 自动推导授权。

## Handoff

- 接收方：健康大管家负责人、项目最高负责人。
- 模块工作项在 F1 收口后转为 `handoff-ready`，等待新的阶段裁定；不自动进入 F2/P3。
- 权威最终 HEAD 以平台完成本报告、IR 与 registry 收口后推送到 `codex/service-plaza-phase1-integration` 的精确远端提交为准。
