# 健康大管家 R1 跨模块需求与原型冻结任务书

状态：正式激活；仅执行 `R1-C1` 需求、信息架构、责任边界与跨模块交互合同冻结。

## 工作项

- work_id：`AIW-20260713-HEALTH-R1-CROSS-MODULE-FREEZE`
- record_id：`IR-20260713-HEALTH-R1-CROSS-MODULE-FREEZE-C1`
- owner：`Health Manager continuous development agent`
- owner_role：健康大管家负责人
- branch：`codex/health-r1-cross-module-freeze`
- worktree：`C:/Users/shugo/Documents/worktrees/heaotang-health-r1-cross-module-freeze`
- base：`5c1069b134747ae5a702ae677457c2422d3137da`

## 权威需求输入

- `C:/Users/shugo/Documents/项目最高负责人/health-cross-module-requirements/健康大管家-大益健康馆-学习广场-健康俱乐部需求补充-v1.0.md`
- SHA-256：`FC07676F9D0AB0DBAF1A4575457E4D1A67D642D1C483187E28A5B2C64E2A9012`
- 资料仓 `C:/Users/shugo/Documents/New project` 仅只读；现有 staged、modified、untracked 文件不得写入、清理、重置或提交。

## R1-C1 最小交付

1. 冻结大益健康馆首页七个入口及纵向健康服务、横向健康参与两条路径。
2. 冻结健康大管家、学习广场、俱乐部联盟、医生集团/平台目录、合规医疗机构的数据权威和责任边界。
3. 冻结跨模块统一模式：`展示最小摘要 + 跳转权威模块 + 会员确认回传`。
4. 形成版本化 JSON 合同、Schema、正例与负例 conformance。
5. 明确隐私、医疗质量、安全和运营会签均为 Pending；R1-C1 不把需求冻结升级为业务实现授权。

## 精确允许路径

- `docs/project-management/modules/health-manager/health-manager-r1-cross-module-freeze.md`
- `docs/project-management/modules/health-manager/health-manager-r1-cross-module-freeze-receipt.md`
- `docs/project-management/modules/health-manager/health-manager-r1-cross-module-freeze-handoff.md`
- `contracts/modules/health-manager/r1/cross-module-freeze.v1.json`
- `contracts/modules/health-manager/r1/cross-module-freeze.v1.schema.json`
- `contracts/modules/health-manager/r1/conformance/test_health_r1_cross_module_freeze.py`
- `contracts/modules/health-manager/development-checklists/2026-07-13-health-r1-cross-module-freeze*.json`
- `contracts/modules/health-manager/governance-exams/2026-07-13-health-r1-cross-module-freeze*.json`
- `contracts/modules/health-manager/implementation-records/2026-07-13-health-r1-cross-module-freeze*.json`

## 持续 No-Go

禁止前后端业务代码、共享路由与样式、API、数据库、真实身份、真实会员、真实健康数据、互联网诊疗、诊断、处方、改药、收费、支付、测试服部署、生产和不可逆操作。AI 不得独立关闭专业或紧急风险；医生培训认证不得替代法定执业资质；任何商业费用不得改变医疗安全排序。

## 门禁顺序

ownership/preflight → current checklist 逐项真实阅读 → 随机治理考试 100 分 → 合同/Schema/文档/负例 → conformance 与两层依赖验证 → implementation record/Handoff → collaboration/总合同/UTF-8/diff/范围/安全 → commit/push → 独立验收或受控集成。
