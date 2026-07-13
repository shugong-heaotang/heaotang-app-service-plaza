# 新模块治理冷启动历史影响审计（2026-07-13）

## 审计结论

全量只读扫描 `contracts/modules/*/development-checklists/*.json` 后，发现且仅发现四份完成态模块检查单使用 `module_id=null`。四份均只有 26 项 core 输入，没有模块 overlay。历史文件保持原字节，不在本工作项中改写。

这四份证据能够证明当时完成了 core 治理阅读和考试，但不能证明执行者读取了所属模块 overlay。因此原有业务或合同结论不自动撤销，也不能继续把它们当作“模块治理输入完整”的证据；对应模块下一次实质切片必须使用已注册的非空 `module_id` 重新认证，必要时由独立验收人决定是否补做原切片复验。

## 已确认影响

| 模块 | 工作记录 | 检查单路径 | 状态 | module_id | items | 影响与建议 |
| --- | --- | --- | --- | --- | ---: | --- |
| network | `IR-20260712-NETWORK-CANONICAL-OWNER-DECISION-R1` | `contracts/modules/network/development-checklists/2026-07-12-network-canonical-owner-r1.json` | completed | null | 26 | canonical owner 决策保留；后续人脉实质切片必须在注册 network overlay 后重新认证，独立评估是否补验原裁决。 |
| protection-mall | `IR-20260712-PROTECTION-MALL-M0-R3-CORRECTION` | `contracts/modules/protection-mall/development-checklists/2026-07-12-protection-mall-m0-r3-correction.json` | completed | null | 26 | M0 R3 历史结论保留但模块治理证据不完整；后续商城切片不得复用。 |
| protection-mall | `IR-20260712-PROTECTION-MALL-M1-CONTRACTS` | `contracts/modules/protection-mall/development-checklists/2026-07-12-protection-mall-m1-contracts.json` | completed | null | 26 | M1 合同结论不自动撤销；需要在下一次合同变更前建立 protection-mall overlay 并重新认证。 |
| protection-mall | `IR-20260712-PROTECTION-MALL-M1-DOMAIN-EVIDENCE` | `contracts/modules/protection-mall/development-checklists/2026-07-12-protection-mall-m1-domain-evidence.json` | completed | null | 26 | 跨仓领域证据保留；不再作为未来模块起飞依据。 |

## 其他扫描结果

- 非空 `module_id` 的完成态模块检查单均能在当前 `governance-reading-list.v1.json` 找到注册项。
- 已注册模块的完成态检查单均包含其对应 overlay，没有发现未知 module_id 或缺失 overlay 输入。
- 平台级检查单位于 `contracts/foundation/development-checklists/`，允许 `module_id=null`；其平台范围仍由 registry/task order 和受保护路径共同证明。
- 未发现除上表四份之外的模块目录 core-only 完成态检查单。

## 预防门禁

`scripts/tests/test_new_agent_development_checklist.py` 现在执行以下共享规则：

1. 新增模块从 reading list 动态注册，不再维护第二份硬编码名单。
2. 模块目录下完成态检查单必须设置非空、已注册的 `module_id`。
3. 其 items 必须包含对应 overlay。
4. 上表四份历史例外使用精确路径固定；例外集合增加、减少或被静默改写都会使测试失败。
5. 平台级任务继续兼容 `module_id=null`，但不能把模块证据写入 foundation 目录以规避模块门禁。

## 后续责任

- 平台集成负责人维护动态 reading list 与共享门禁。
- Network 和 Protection Mall 负责人在下一实质切片前分别补建模块 bootstrap overlay。
- 独立验收负责人根据原切片风险决定是否追加复验，不允许改写历史 checklist 制造合规。
