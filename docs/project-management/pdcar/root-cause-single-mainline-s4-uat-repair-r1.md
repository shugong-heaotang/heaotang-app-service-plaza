# S4 UAT 六路由产品缺陷根因记录

## 症状与因果链

1. P004/P007：`App.tsx` 将 `/services/:serviceKey` 交给仅支持三个 key 的 `CoreServicePage`，活动广场和 AI 助手因缺少显式映射落入 NotFound。
2. P011：路由表缺少 `/member-home/` 精确入口，页面无法触达。
3. P008：Project Brain 请求 `/project-brain/project-brain.snapshot.json`，测试服回退返回 SPA HTML；仓库虽有生成 JSON，但 Vite 构建未复制，解析首字符 `<` 失败。
4. P009/P010：认证包装和内部状态面板重复声明同一 `data-page-state='authentication-required'`，造成唯一性断言计数为 2；applications 访客态又复用“自建俱乐部”标题，缺少路由身份。

## 系统性修复方向

- 为计划服务提供显式、可测的路由映射与页面身份，不依赖未知 key 回退。
- 增加会员首页精确路由并覆盖入口测试。
- 将生成的 Project Brain snapshot 纳入确定性构建产物，并验证 JSON content-type/body。
- 认证状态只保留一个权威 DOM 标记；子路由标题由 route kind 决定。

## 防复发门

对六个失败路由做 desktop/mobile DOM、导航、网络和截图复验；对五个已通过路由做新鲜烟测；构建产物检查 snapshot；路由测试覆盖显式映射、未知 key、认证态唯一性和子路由身份。P0/P1 必须为 0。

## G1 治理证据两次触发闭环

G1 中先以不符合校验器精确常量的自定义 attestation 生成了 100 分试卷；修正 attestation 后 checklist SHA 改变，试卷全目录门禁依法拒绝。根因是执行顺序漏了“先独立验证 completed checklist，再生成随机试卷”的不可变快照门。旧试卷尚未提交、验收且与无效 checklist 声明绑定，已从本轮瞬态证据中移除；未改写为通过、未作为 retry 复用。随后在 checklist validation Go 后重新生成 attempt-1，8/8、100 分，checklist、exam、implementation-record 三门联合验证通过。

防复发顺序冻结为：完成 checklist -> 运行 `validate_development_checklists.py` -> 冻结 checklist SHA -> 生成/提交 exam -> 运行 `validate_governance_exams.py` -> 形成 implementation record。任何 checklist 字节变化必须在新试卷前发生，试卷生成后禁止修改其绑定 checklist。
