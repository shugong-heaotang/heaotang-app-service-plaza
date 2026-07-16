# 健康大管家项目入口当前状态收口任务书

状态：正式激活；本轮只执行 ownership/preflight、current checklist 和随机治理考试 100，README 实现与防漂移断言留给后续独立检查点。

## 工作项

- work_id：`AIW-20260717-HEALTH-README-CURRENT-STATE-CLOSEOUT`
- record_id：`IR-20260717-HEALTH-README-CURRENT-STATE-CLOSEOUT-C1`
- owner：`Health Manager continuous development agent`
- owner_role：健康大管家负责人
- branch：`codex/health-manager-readme-current-state-closeout`
- worktree：`C:/Users/shugo/Documents/worktrees/heaotang-health-manager-readme-current-state-closeout`
- base：`cf802602c5adb0ad0940e20abf1b1bcf88083581`

## 根因与目标

`docs/project-management/modules/health-manager/README.md` 当前 SHA-256 为 `9cb68a63c1d59e31292071058d40df9c01034268168247c1e3194b0fa8d0288f`，仍把 `health-mvp90-m0` 写成当前切片，并宣称 M0 是唯一 active、M1 及以后 No-Go。平台注册表当前无健康 active 工作项，R1-R5 十个实现/验收工作项均已 `integrated`。本工作项只修复项目入口与权威注册表的当前状态漂移，不重开历史阶段，不扩大医疗或运行时授权。

后续实现必须：

1. 把项目入口更新为 R1-R5 离线、合成、`synthetic_only=true`、`executable=false` 已受控集成，健康 active 工作项以注册表实时状态为准。
2. 明确真实身份、真实健康数据、互联网诊疗、收费/支付、测试服、生产和不可逆操作继续 No-Go。
3. 增加可执行防漂移断言，至少拒绝 README 把已收口的历史切片继续宣称为唯一 active，或把 R1-R5 合成完成误写为真实医疗/部署 Go。
4. 形成同一 `record_id` 的 implementation record、Handoff、正负测试、范围/秘密/UTF-8 证据，并在 commit/push 后等待独立验收与受控集成。

## 精确允许路径

- `docs/project-management/modules/health-manager/README.md`
- `docs/project-management/modules/health-manager/health-manager-readme-current-state-closeout-handoff.md`
- `contracts/modules/health-manager/conformance/test_health_manager_readme_current_state.py`
- `contracts/modules/health-manager/development-checklists/2026-07-17-health-manager-readme-current-state-closeout*.json`
- `contracts/modules/health-manager/governance-exams/2026-07-17-health-manager-readme-current-state-closeout*.json`
- `contracts/modules/health-manager/implementation-records/2026-07-17-health-manager-readme-current-state-closeout*.json`

## 本检查点完成条件

1. authority local/origin/GitHub remote exact HEAD 一致且 authority clean。
2. 注册表 work item、owner、base、branch、worktree、allowed paths 无冲突；独立 worktree 从 activation commit 建立且 clean。
3. 平台 preflight 为 `ready`；以 `ModuleId=health-manager` 生成当期 checklist，逐项真实阅读并记录当前 SHA-256。
4. 随机治理考试 8/8、score=100；失败试卷保持不可变并按补课流程重考。
5. 本检查点只提交 checklist/exam 治理证据，不修改 README、测试、IR 或 Handoff。

## Pending、does_not_block 与 No-Go

- Pending：README 实现、防漂移断言、IR/Handoff、commit/push、独立验收与受控集成。
- does_not_block：R1-R5 离线/合成完成态、既有 13/16/17/19/23 项验收证据、其他无重叠项目。
- No-Go：复用或改写历史 R1-R5 工作项；前后端、共享运行时、API、数据库、真实身份/会员/健康数据、互联网诊疗、诊断/处方/改药、收费/支付、测试服、生产和不可逆操作。

`C:/Users/shugo/Documents/New project` 全部 staged、modified、untracked 用户文件保持只读，不得写入、清理、重置或提交。
