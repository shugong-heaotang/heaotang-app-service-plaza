# 学习广场 M0-R4 Handoff

日期：2026-07-13
提交方：学习广场持续开发负责人
接收方：学习广场独立验收负责人
状态：M0-R3 `11a1f93` 已独立 No-Go；R4 分层修正候选待重新独立验收

## 已完成

- 候选包含权威 integration `44325310f4bddfc8ddcb4b1f6e02402cc719c001`；集成前须再次校验最新性。
- 历史 M0/M0-R2/M0-R3 checklist、exam、IR 原字节移入 invalidated snapshots，不再参与 active 门禁。
- R4 checklist 28/28 完成后才生成 R4 exam；考试 100/100，时序真实可核对。
- v3 Schema 精确冻结内部应用、连接能力、外部项目、owner、审核、Nova、成长事件、课程闭环和五端口。
- fixtures 保持 34 条；Schema 错误与手写 invariant 已拆分计算。外部项目替换、目录 owner 对调、双关审核绕过、端口提前 verified、端口 ID 漂移五类 mutation 均要求 Schema/独立 invariant/fixture 三重拒绝。

## 未完成与风险

- R4 尚未重新独立验收，因此不能给 M0 Go。
- 五个真实连接端口仍无 owner/version 签署，保持 `provisional/fail-closed`。
- 若权威 integration 在验收前继续前进，必须重新同步并重建最终 current 治理证据。
- 前端、API、数据库、支付、测试服和生产均未授权。

## 独立验收命令

```powershell
python -X utf8 contracts/modules/learning-plaza/m0-r2/validate_learning_plaza_m0_r2.py
python -X utf8 contracts/modules/learning-plaza/m0/validate_learning_plaza_m0.py --self-test
python -X utf8 scripts/validate_foundation_dependencies.py contracts/foundation/foundation-capabilities.v1.json --module contracts/modules/learning-plaza/platform-dependencies.v1.json --project-root .
python -X utf8 scripts/validate_module_internal_dependencies.py contracts/foundation/module-internal-dependencies.v1.schema.json contracts/modules/learning-plaza/internal-dependencies.v1.json --project-root .
python -X utf8 scripts/validate_development_checklists.py contracts/foundation/development-checklist.v1.schema.json contracts/modules/learning-plaza/development-checklists --project-root . --require-current
python -X utf8 scripts/validate_governance_exams.py contracts/foundation/governance-exam.v1.schema.json contracts/foundation/governance-exam-bank.v1.schema.json contracts/foundation/governance-exam-bank.v1.json contracts/modules/learning-plaza/governance-exams --project-root .
python -X utf8 scripts/validate_implementation_records.py contracts/foundation/implementation-record.v1.schema.json contracts/modules/learning-plaza/implementation-records --project-root .
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/Test-TextEncoding.ps1
git diff --check 44325310f4bddfc8ddcb4b1f6e02402cc719c001...HEAD
```

## 下一授权

仅在 R4 独立验收 Go 后，由平台集成负责人从届时最新权威 integration 进行受控合并。随后才可派发 M1 独立项目骨架；部署和上线仍不授权。
