# 学习广场 M0 Handoff

日期：2026-07-13
提交方：学习广场持续开发负责人
接收方：学习广场独立验收负责人
状态：`handoff-ready candidate`，尚未独立验收

## 已完成

- 权威任务单、动态 module overlay、唯一 active 工作项、独立分支与工作树已建立。
- current checklist 28/28，治理考试 100/100。
- 六个核心域、四级可见性、进度状态机、完成事件、Nova 引用和四个跨模块端口已合同化。
- 9 项平台依赖解析和 16 条确定性正负例自测通过。
- 参考 Nova 资产已固定提交号与 SHA-256，并明确为参考而非集成事实。

## 未完成与风险

- 独立验收未执行，因此不能给 M0 Go。
- 四个真实跨模块端口尚无 owner 签署，保持 provisional/fail-closed。
- 内容版权、统一资源 ID 和真实数据留存规则未冻结。
- 未实现前端、API、数据库、测试服或生产能力。

## 独立验收命令

```powershell
python -X utf8 contracts/modules/learning-plaza/m0/validate_learning_plaza_m0.py --self-test
python -X utf8 scripts/validate_module_internal_dependencies.py contracts/foundation/module-internal-dependencies.v1.schema.json contracts/modules/learning-plaza/internal-dependencies.v1.json --project-root .
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/Test-TextEncoding.ps1
git diff --check 9f480e2699d3cb4681bc2f8b58c33b361f352e29..HEAD
```

## 下一授权

独立验收 Go 后，由平台集成负责人受控合入，再单独派发 M1“浏览可见资源 -> 接受路径 -> 推进一项进度 -> 生成完成事件”最小真实闭环。部署和上线仍不授权。
