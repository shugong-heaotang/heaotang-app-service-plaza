# S4 UAT 六路由产品修复 R1 Handoff

状态：P008 部署路径根因、最小修复候选、全量测试与本地测试服构建均已独立接受；当前修复尚未提交、推送、集成或部署，P008 与全 11 路由 UAT 尚未关闭。

R3 Activation SHA-256 `DEAA23E2B2817629C986B40C94AA93E4FAB5DE5C8CD3D68F136DA6F8906949A6` 已消费并以 `P0/P1/P2=0/2/0` 失败关闭：执行者增加了全历史 checklist 门，且组合 PowerShell 未可靠传播 native nonzero。R4 Activation SHA-256 `E0B0CBEAD4525EB2F55FB14DC2FDFEE2284C9B91A7C47B5543E248DE80EED07F` 已消费一次，仅用于逐命令验证和证据冻结。R1、R2、R3 均不可复用。

- 唯一工作树和 exact base 仍为 `2df75badec2ae5f8c7b04c4c3ae2602b8d4f2ef9`，分支未漂移。
- G1 已独立接受；G1.5 registry/dependency bootstrap 已独立接受。
- registry 仍为 158 行，SHA-256 `BC408AB6BB92D9059128A4225DEAD41BA1866BBC66607824FEE138C008A3D8B7`；Junction、package-lock 与 `app/dist` absent 状态未漂移。
- G2 current checklist：26/26 completed；证据副本与源文件逐字节一致，SHA-256 `6CC05FF24F835CE0AEFE504EA90D2279E00072A27D42C34A31C92F4A6A967C77`。
- G2 Exam attempt 1：8/8，100 分。
- G2 implementation record：`contracts/foundation/implementation-records/2026-07-18-single-mainline-s4-uat-repair-r1-g2.json`。
- R4 target checklist、Exam、IR、registry 四个验证器已作为独立进程逐项返回 0；禁止的 global historical checklist 门未再次运行。
- 独立 Product G2 Activation SHA-256 `F042D2874E492E112207C72E0E155C6959ED4097688A8887645D6ACBC77C63BF` 已消费一次；恰好 10 个授权产品路径发生变化，授权外产品路径为 0。
- 六个失败路由的共同根因已修复：活动广场、Nova AI、会员首页使用显式路由；自建俱乐部访客认证态只保留一个 DOM 权威标记并显示子路由标题；Project Brain 拒绝 HTML/parser 泄漏。
- 定向测试 35/35、全量测试 254/254 均一次通过；`npm run build:test-server` 一次通过。
- 构建产物包含 `project-brain/project-brain.snapshot.json`，SHA-256 `B6FF78A47742904563213ABD0D23839C2D800BFD78F84367836DDDE359177034`；它明确声明 `source_freshness=unknown`、`overall_verdict=no-go`，没有复制或伪装旧的 current 快照。
- registry、package-lock 和 node_modules Junction 未漂移；没有依赖安装/升级、提交、推送、集成或部署。

独立 R1 Execution Acceptance 以 `P0/P1/P2=0/1/1` No-Go 关闭：`projectBrainApi.ts` 只验证顶层集合，未验证集合成员 full shape 与 summary 数值。验收 MD SHA-256 `26A875DC18673A7D5687C1BE2A2D2066C5C12BF9F9150F9E035D31052FA8E1AA`，JSON SHA-256 `4B1EC2B0BCED8639C5767CFFDD6434C4CA8A2590D7F45371D0C6FAFF5122981E`；R1 结论未复用或改写。

- R2 remediation Activation SHA-256 `AB37B4FFB87845E9547108AD25CF0501403D68F0F786C2D5C2AD988B5BBBE13B` 已在 exact fresh precheck 后消费一次，不可重试。
- Project Brain 现对 work item、module、decision、risk 的每个集合成员执行完整字段类型校验；`work_summary` 与 `audit_summary` 仅接受非负整数。
- R2 定向测试 13/13、全量测试 261/261、`build:test-server` 均各一次通过。
- 新构建快照 SHA-256 `1398C19895CE6600048C240C0C7ECEB14904ED6A2A17F4F1A5348A99D14A605B`，仍为 `source_freshness=unknown`、`overall_verdict=no-go`。
- 8 个冻结产品文件、registry SHA-256 `BC408AB6BB92D9059128A4225DEAD41BA1866BBC66607824FEE138C008A3D8B7`、package-lock SHA-256 `57FFCEB4FC63BDFFB4F89E675B34C3FE4A2C9B38037B5C75F49336D47C634DA3` 与 node_modules Junction 均未漂移。

独立 R2 Execution Acceptance 已 Go，`P0/P1/P2=0/0/1`：Acceptance MD SHA-256 `6A83EB68088494A57F2D18D3C35DFBA08FD44AE0296C1276E7D6AD5BCAD8070D`，JSON SHA-256 `061F27FBD0BE69F514FD5A34A5A33EEC0F4A6627E377821ABB4EC23810EE4382`。唯一 P2 是 G2 IR 的 title/objective 仍写“治理准备”；C1 已按验收事实将其修正为产品实施与 R2 fail-closed 修复，不改变任何产品源文件。

## P008 部署路径修复当前事实

- R5 11 路由双视口 UAT 为 20/22 通过；P008 desktop/mobile 是同一不同产品根因，独立 UAT Acceptance MD SHA-256 `324E9717A878EF6800B0AFE55E20606E2E72162C5FA589B4AC16FD511F24F063`、JSON SHA-256 `4DC9BC770054105E0AD68B61BD77BD1996E3E0851D520CF34CF28A9CD3EE6554`。
- 已验收服务器备份证明部署 snapshot 有效且位于 Service Plaza 根；客户端旧 URL 绕过 `/app/` alias，命中 `acceptance-app` SPA HTML 回退。独立 Root Cause Go SHA-256 `4D0151A34C43F1F63264B100DA20B15FBC99A15E3AA3C85B8A722E1FCB93946D`。
- 最小产品修复把 URL 固定为 `/app/service-plaza/project-brain/project-brain.snapshot.json`，并增加精确 URL 与 `credentials: same-origin` 回归；MIME、严格 JSON 与 full-shape v1 失败关闭没有放宽。
- 独立候选 Acceptance Go SHA-256 `37659B3E5D35AE3B958C3B691729C5E0DDFD89209054B94F3CFA35D365FDF4D2`；定向 13/13、全量 261/261 均一次通过。
- 独立 Build Acceptance Go SHA-256 `B74D5B1E28B6E5E74E28F08F8B7B07B4E0BCF999B295AF9364235253E3EB8298`。新构建 index 使用 `/app/service-plaza/` asset base，六个路由 index 6/6、合同副本 3/3；snapshot 699 bytes、SHA-256 `90290FAF510D1908547DCBDCED316318E283601C31685D831607B96299F9AC8C`，保持 Unknown/No-Go。

下一门：独立 record-sync Acceptance。其 Go 后才可申请本地候选提交和受控集成；随后另行部署并执行 P008 双视口、受影响扫描与全 11 路由 closure。当前无提交、推送、集成、部署或 UAT 完成声明。
