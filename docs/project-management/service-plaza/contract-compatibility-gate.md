# 服务广场契约版本差异门禁

## 目的

本门禁落实 `service-integration-version-policy.md`：同一主版本中的候选契约必须兼容已经发布的契约。它补充现有 JSON Schema 有效性校验，不替代、关闭或放宽 Schema 门禁。

## 覆盖范围

工具 `scripts/check_service_plaza_contract_compatibility.py` 支持三类 JSON：

- `action-baseline`：阻断动作删除、数量改变、重排、`sort_order` 占位复用、目标、动作类型、服务绑定、返回路径、遥测标识、认证与 scope 边界改变，以及 active 动作被停用。
- `service-manifest`：阻断服务 ID、入口、提供方、认证、scope、隐私、业务 API 版本边界改变、能力删除，以及 active 服务被停用。
- `json-schema`：阻断必填字段新增、属性或定义删除、类型或枚举缩小、上下界收紧、正则新增或改变、禁止额外属性、要求数组唯一等使旧合法数据失效的变化。

无法证明兼容的约束变化按破坏性变化处理。破坏性变化必须发布新主版本并经过 APP 总架构负责人审批，不能修改测试或跳过门禁来保留原主版本。

## 本地运行

运行正负样例和相对上一提交的三份正式契约差异：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/Test-ServicePlazaContractCompatibility.ps1
```

指定发布基线：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/Test-ServicePlazaContractCompatibility.ps1 -BaseRef origin/main
```

直接比较两个文件并取得机器可读结果：

```powershell
python -X utf8 scripts/check_service_plaza_contract_compatibility.py old.json new.json --kind action-baseline --format json
```

退出码 `0` 表示兼容，`1` 表示发现破坏性差异，`2` 表示输入、类型或基线不可读取。每项差异包含规则代码、JSON Pointer 和旧新边界说明。

## CI 行为

GitHub Actions 使用 PR 的 base SHA；普通 push 使用事件的 before SHA。首次引入、基线中尚不存在的契约只运行样例测试和现有 Schema 门禁，之后每次修改都必须与 Git 基线比较。CI 保留 `Test-ServicePlazaContracts.ps1` 和接入包校验两个现有步骤。

## 实施证据与接续

- 日期：2026-07-10
- 执行角色：F6 契约版本差异门禁 Agent
- 范围：`scripts/`、`contracts/service-plaza/compatibility-fixtures/`、`.github/` 和本文档。
- 已完成：三类差异检测、7 项正负与真实 Git blob 测试、PowerShell 5.1 包装器和 GitHub Actions 调用。
- 未完成：首次提交前仓库 Git 基线尚无三份契约，因此本地 `HEAD` 验证按设计标记为新引入；合并后后续修改将执行真实版本差异。
- 阻塞：无。
- 门禁变化：F6 的“版本差异门禁”实现完成；F6 整体状态仍由总计划中其他准入项共同决定。
- 验证证据：兼容性测试 7/7；现有动作 Schema 门禁通过；工作区 220 个文本文件编码门禁通过；工作流 YAML 可解析；包装器 BOM 已确认。
- 下一步：平台集成负责人以正式发布提交或 tag 作为 `BaseRef` 运行一次发布前验证，并将结果纳入 F6 总验收。
