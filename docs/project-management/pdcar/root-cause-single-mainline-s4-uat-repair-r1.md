# S4 UAT 六路由产品缺陷根因记录

## 症状与因果链

1. P004/P007：`App.tsx` 将 `/services/:serviceKey` 交给仅支持三个 key 的 `CoreServicePage`，活动广场和 AI 助手因缺少显式映射落入 NotFound。
2. P011：路由表缺少 `/member-home/` 精确入口，页面无法触达。
3. P008：已验收的测试服部署包确实包含有效 `project-brain/project-brain.snapshot.json`；但客户端请求 `/project-brain/project-brain.snapshot.json`，该根路径没有进入 Nginx 的 `/app/` alias，而是命中 `acceptance-app` 根目录的 SPA `try_files` 回退并返回 HTML。最早可控根因是客户端 URL 与实际部署路径 `/app/service-plaza/` 不一致，不是 snapshot 未生成或未复制。
4. P009/P010：认证包装和内部状态面板重复声明同一 `data-page-state='authentication-required'`，造成唯一性断言计数为 2；applications 访客态又复用“自建俱乐部”标题，缺少路由身份。

## 系统性修复方向

- 为计划服务提供显式、可测的路由映射与页面身份，不依赖未知 key 回退。
- 增加会员首页精确路由并覆盖入口测试。
- 将 Project Brain 请求路径固定为 `/app/service-plaza/project-brain/project-brain.snapshot.json`，与测试服 `/app/` alias 和 Service Plaza 部署根一致；继续保留 MIME、严格 JSON 与完整 v1 shape 的失败关闭校验。
- 认证状态只保留一个权威 DOM 标记；子路由标题由 route kind 决定。

## 防复发门

对六个失败路由做 desktop/mobile DOM、导航、网络和截图复验；对五个已通过路由做新鲜烟测；构建产物检查 snapshot；路由测试覆盖显式映射、未知 key、认证态唯一性和子路由身份。P008 额外要求精确 fetch URL、`credentials: same-origin`、HTML-as-JSON 禁止结果和双视口回归。P0/P1 必须为 0。

## P008 二阶段根因闭环

- R5 11 路由 UAT 共 20/22 通过，唯一不同产品根因是 P008 desktop/mobile 两个 P1；独立验收 MD SHA-256 `324E9717A878EF6800B0AFE55E20606E2E72162C5FA589B4AC16FD511F24F063`。
- 已验收服务器备份证明 Nginx `location /app/` 指向 `/var/www/heaotang/app/`，而 `location /` 指向 `/var/www/heaotang/acceptance-app` 并回退 `/index.html`；独立根因复核 SHA-256 `4D0151A34C43F1F63264B100DA20B15FBC99A15E3AA3C85B8A722E1FCB93946D`，Root Cause Go、P0/P1/P2=`0/0/0`。
- 最小修复只改 `projectBrainApi.ts` 的 URL 与 `ProjectBrainPage.test.tsx` 的精确调用断言；独立候选验收 SHA-256 `37659B3E5D35AE3B958C3B691729C5E0DDFD89209054B94F3CFA35D365FDF4D2`，P0/P1/P2=`0/0/0`。
- 定向测试 13/13、全量测试 261/261 均一次通过；测试服构建一次通过。新构建 snapshot 为 699 bytes、SHA-256 `90290FAF510D1908547DCBDCED316318E283601C31685D831607B96299F9AC8C`，保持 `source_freshness=unknown`、`overall_verdict=no-go`；独立 Build Acceptance SHA-256 `B74D5B1E28B6E5E74E28F08F8B7B07B4E0BCF999B295AF9364235253E3EB8298`。
- 当前边界：修复尚未提交、集成或部署，P008 与全 11 路由 UAT 尚未关闭。上述本地 Go 不得冒充测试服产品闭环。

## G1 治理证据两次触发闭环

G1 中先以不符合校验器精确常量的自定义 attestation 生成了 100 分试卷；修正 attestation 后 checklist SHA 改变，试卷全目录门禁依法拒绝。根因是执行顺序漏了“先独立验证 completed checklist，再生成随机试卷”的不可变快照门。旧试卷尚未提交、验收且与无效 checklist 声明绑定，已从本轮瞬态证据中移除；未改写为通过、未作为 retry 复用。随后在 checklist validation Go 后重新生成 attempt-1，8/8、100 分，checklist、exam、implementation-record 三门联合验证通过。

防复发顺序冻结为：完成 checklist -> 运行 `validate_development_checklists.py` -> 冻结 checklist SHA -> 生成/提交 exam -> 运行 `validate_governance_exams.py` -> 形成 implementation record。任何 checklist 字节变化必须在新试卷前发生，试卷生成后禁止修改其绑定 checklist。
