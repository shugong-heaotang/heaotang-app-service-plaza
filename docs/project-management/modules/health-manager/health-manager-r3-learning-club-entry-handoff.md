# 健康大管家 R3-C1 Handoff

- work_id：`AIW-20260714-HEALTH-R3-LEARNING-CLUB-ENTRY-CONTRACTS`
- record_id：`IR-20260714-HEALTH-R3-LEARNING-CLUB-ENTRY-C1`
- checkpoint：R3-C1 健康学习与健康俱乐部入口合同和负例
- status：`handoff-ready / awaiting independent review`
- executable：`false`

## Completed

1. 冻结学习广场与俱乐部联盟各自四字段最小摘要 allowlist，以及服务目录已登记的权威路由。
2. 冻结“展示摘要 → 跳转权威模块 → 会员确认回传”协议；权威模块保留全部写入所有权，不共享数据库表。
3. 冻结会员确认回传的来源、版本、确认记录、责任人和目标复核字段；只形成健康管理记录候选，不自动形成医疗记录。
4. 冻结模块隔离和 AI 边界，拒绝健康大管家修改学习进度/俱乐部成员关系、俱乐部无授权读取完整健康档案及 AI 医疗越界。
5. 增加 Draft 2020-12 Schema、语义基线和 15 个可执行负例；17/17 conformance 通过。

## Verified

- current checklist 28/28、当前治理 SHA 匹配；governance exam attempt 1=100。
- `python -X utf8 -m unittest contracts.modules.health-manager.r3.conformance.test_health_r3_learning_club_entry -v`：17/17 passed。
- 需求补充 SHA-256：`fc07676f9d0ab0dbaf1a4575457e4d1a67d642d1c483187e28a5b2c64e2a9012`。

## Checklist 校验器根因记录

- issue：`R3-GATE-CURRENT-CHECKLIST-DIRECTORY-SCOPE`
- 症状：第一次把单文件传给目录型校验器，返回无 completed checklist；第二次对全部健康历史 checklist 使用 `--require-current`，历史不可变快照因治理文件后续变化而被报告 stale。
- 影响：整目录输出不能证明本次 R3 current snapshot；不影响历史快照完整性，也不允许改写历史文件。
- 已尝试：读取 CLI 与实现，确认 `directory.glob("*.json")` 会扫描全部历史；未删除、更新或弱化历史证据。
- 根因：目录级 current 校验与单一当期快照验证的输入粒度不匹配。
- owner：健康大管家持续开发 Agent。
- 关闭证据：只读复制本次 checklist 到唯一临时目录，使用同一 Schema、同一原校验器和 `--require-current` 后通过，输出 `28/28 completed`。
- does_not_block：合同、Schema、负例、IR、独立验收；blocks：若单快照 current 验证失败则禁止考试和实现。

## Pending

- 隐私法律：真实身份、真实健康数据和跨模块运行时授权。
- 医疗质量：健康内容医疗声明和专业政策执行。
- 平台安全：共享运行时、API、数据库和环境。
- 模块运营：真实学习目录、俱乐部成员关系和会员试点。
- does_not_block：R3 合成合同一致性、负例和独立验收。

## No-Go

前后端、共享运行时、API、数据库、跨模块直接写库、真实身份/会员/健康数据、互联网诊疗、诊断、处方、改药、收费、支付、测试服、生产和不可逆操作均未授权。

## 下一门禁

独立 reviewer 从 exact commit 复跑 17 项 conformance、current checklist/exam、两层依赖、IR、UTF-8、diff、范围、秘密与敏感模式门禁；Go 后由平台受控集成并收口 R3，再另立 R4 工作项。
