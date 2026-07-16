# 健康大管家项目入口当前状态收口 Handoff

- work_id：`AIW-20260717-HEALTH-README-CURRENT-STATE-CLOSEOUT`
- record_id：`IR-20260717-HEALTH-README-CURRENT-STATE-CLOSEOUT-C1`
- checkpoint：README 当前事实与注册表防漂移实现、正负测试和治理记录
- status：`handoff-ready / awaiting independent review`
- evidence_mode：`synthetic_only=true`、`executable=false`

## Completed

1. 将健康大管家项目入口从历史 `health-mvp90-m0` 当前切片改为 R1—R5 离线/合成合同及独立验收 10/10 已受控集成。
2. 将健康 active 工作项的唯一权威明确为 `contracts/foundation/agent-collaboration.v1.json`，README 不固定 active 数量，不复活历史工作项。
3. 明确 `integrated` 不等于真实医疗、真实数据、运行时、部署或生产 Go。
4. 保留健康、学习、俱乐部、医生目录和合规医疗机构的权威边界，以及“最小摘要 + 跳转权威模块 + 会员确认回传”的跨模块协议。
5. 新增 9 项机器 conformance，含当前正例和 7 类防漂移/授权升级负例。
6. 形成同一 `record_id` 的 current checklist、exam100 和 implementation record。

## Verified

- 平台 preflight：`ready`。
- current checklist：28/28 checked，当前 SHA-256 mismatch=0。
- governance exam attempt 1：8/8，score=100。
- 注册表：健康 active=1（仅本 freshness 项）；R1—R5 实现/验收=10/10 `integrated`。
- `python -X utf8 -m unittest contracts.modules.health-manager.conformance.test_health_manager_readme_current_state -v`：9/9 passed。
- 负例拒绝：R1—R5 状态重开、旧 M0 当前/唯一 active、删除合成边界、升级 executable、移除注册表权威、真实健康数据 Go、缺失 No-Go。

## Control-channel issue

- 沙箱 `git ls-remote` 因 GitHub SSH 22 端口策略失败；受控只读重试在 30 秒内无响应并终止。
- 影响：本轮开始时无法通过 SSH 独立刷新 GitHub remote exact HEAD。
- 已确认：authority/candidate 本地跟踪引用分别为 `86ab20f8928a6d70195edb3879fbe7083c20a0f9` 与 `2c15e5e9e65f895df6f9fb1fa71d111b7160e55a`，两工作树 clean；push 前仍必须使用 expected-remote freshness/lease 门禁。
- owner：Git/GitHub 控制通道；retry condition：网络/SSH 通道恢复，或受控 push freshness 脚本成功返回精确远端 HEAD。
- does_not_block：范围内实现、离线测试、IR/Handoff、diff/UTF-8/范围/秘密门禁和本地提交。

## Pending

- 独立 reviewer 复跑当前状态 conformance、checklist/exam/IR、依赖、UTF-8、diff、范围、秘密与敏感模式门禁。
- expected-remote lease push 成功后，平台受控集成 exact candidate commit，并将本 freshness work item 收口 `integrated`。
- 医疗质量、隐私法律、平台安全、健康馆运营的真实运行会签继续 `pending-with-owner`。
- does_not_block：R1—R5 离线/合成完成态及其他无重叠工作项。

## No-Go

真实身份、真实会员、真实健康数据、互联网诊疗、诊断、处方、改药、冒充医生、疗效承诺、收费、支付、测试服、生产、不可逆操作，以及对 `C:/Users/shugo/Documents/New project` 的任何写入、清理、重置或提交均未授权。

## Independent acceptance conditions

1. 从 exact candidate commit 复跑 9/9 conformance，并证明负例保持 fail-closed。
2. 复核 README 对注册表 10 个 R1—R5 exact work item 的 `integrated` 结论，不把当前 freshness 项或历史阶段误写成产品运行时 Go。
3. 复跑 implementation-record、两层依赖、collaboration、UTF-8、diff、allowed scope、secret 和敏感模式门禁。
4. authority remote 未漂移且 expected-remote lease 有效时，才允许受控集成；否则先关闭 freshness 根因，不猜测基线。
