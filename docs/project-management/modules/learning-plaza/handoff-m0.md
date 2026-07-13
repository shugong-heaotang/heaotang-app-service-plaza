# 学习广场 M0-R2 Handoff

日期：2026-07-13
提交方：学习广场持续开发负责人
接收方：学习广场独立验收负责人
状态：原 M0 候选因项目层级前提改变而被取代；M0-R2 为 `handoff-ready candidate`，尚未独立验收

## 已完成

- 原 M0 合同、清单、考试和实现记录保留为历史证据，不再作为当前架构结论。
- M0-R2 current checklist 28/28，治理考试 100/100。
- `requirements-v3.0.md` 与 ADR 0001 已确认学习广场为独立通用学习平台。
- 内部应用、连接能力、外部项目、四种审核模式、知识商品边界、Nova 权限、成长事件和首个课程闭环已合同化。
- 参考 Nova 资产继续只作固定哈希输入，Nova 仓库不再被视为学习广场运行时所有者。

## 未完成与风险

- 独立验收未执行，因此不能给 M0-R2 Go。
- 五个真实连接端口尚无 owner 签署，保持 `provisional/fail-closed`。
- 内容版权、统一资源 ID、审核委员会成员、真实数据留存和订单权益规则尚未冻结到运行时。
- 未实现前端、API、数据库、支付、测试服或生产能力。

## 独立验收命令

```powershell
python -X utf8 contracts/modules/learning-plaza/m0-r2/validate_learning_plaza_m0_r2.py
python -X utf8 scripts/validate_module_internal_dependencies.py contracts/foundation/module-internal-dependencies.v1.schema.json contracts/modules/learning-plaza/internal-dependencies.v1.json --project-root .
python -X utf8 scripts/validate_development_checklists.py contracts/foundation/development-checklist.v1.schema.json contracts/modules/learning-plaza/development-checklists --project-root . --require-current
python -X utf8 scripts/validate_governance_exams.py contracts/foundation/governance-exam.v1.schema.json contracts/foundation/governance-exam-bank.v1.schema.json contracts/foundation/governance-exam-bank.v1.json contracts/modules/learning-plaza/governance-exams --project-root .
python -X utf8 scripts/validate_implementation_records.py contracts/foundation/implementation-record.v1.schema.json contracts/modules/learning-plaza/implementation-records --project-root .
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/Test-TextEncoding.ps1
git diff --check b2237a10e9e697045ea8ce1f82671cfac91806fc..HEAD
```

## 下一授权

独立验收 Go 后，由平台集成负责人受控合入。随后先派发 M1 独立项目骨架（应用注册、路由、权限、数据所有权和连接器），紧接着派发课程提交到成长投影的首个闭环。部署和上线仍不授权。
