# 俱乐部联盟 CA-H0 Base Conformance 报告

- 日期：2026-07-11
- 范围：CA-H0 base contracts；不含 CA-H1、业务 API、页面实现或环境验收
- 起始 HEAD：`0db14ad`（已包含平台验收权威集成 `59b8a47`）
- 工作项：`AIW-20260711-CLUB-FOUNDATION-DISPATCH`
- 检查单：`FC-20260711-CLUB-ALLIANCE-F0-H0-STANDARDS`
- 考试：`EX-20260711-CLUB-ALLIANCE-F0-H0-STANDARDS-1`，score=100
- 结论：H0 base conformance 33/33 Pass；完整 H0 Go 仍为 No-Go

## 验证结果

1. 所有模块 JSON 均可由 Python `json` 严格解析。
2. category registry、capability catalog、homepage、relationship、error catalog 的 Draft 2020-12 Schema 自检通过，实例对各自 Schema 零错误。
3. H0-B001～B033 全部执行，33/33 Pass。
4. error catalog 中 fixture 使用的错误 ID 全部存在且唯一。
5. 四入口从上游 action 合同派生；管理入口单独解析；模块未复制展示值。
6. `D-CA-003` 仍为 Pending，SC selector 保持 `executable=false`。
7. Payment/Withdrawal/Refund/Subscription 在四个 profile 中均为 forbidden。
8. `club-federation` 使用独立关系，FamilyAlliance 复用与失败开放均由负例拒绝。

## 执行命令

```powershell
python -X utf8 -m json.tool <each-module-json>
python -X utf8 contracts/modules/club-alliance/conformance/test_club_alliance_contracts.py
```

Schema 验证使用仓库已批准并锁定的 `jsonschema` Draft 2020-12 validator，对五组 Schema/实例逐一执行 `check_schema` 和 `iter_errors`。

## H0-B001～B033 汇总

```text
SUMMARY passed=33 total=33
```

覆盖范围包括：上游不可解析、入口缺失/重复/越界、排序冲突、管理混类、展示字段复制、未知/重复 category、Pending selector 可执行、能力 owner/contract/dependency/evidence/readiness 缺失、required/forbidden 冲突、商业误启用、路由与 query 失败关闭、关系伪装、FamilyAlliance 复用、未版本化政策、失败开放、决策缺失及未知异常。

## 证据 SHA-256

| Artifact | SHA-256 |
| --- | --- |
| upstream actions | `183c62a931cd0395521e38379e4246588bb97b7bb1b857b2d379cb8ead7580eb` |
| upstream schema | `ef7b685f9cac99c31ae15b9f90a50ff457a837ad417c45987c96e69c4388b5ff` |
| category registry | `56bb3858d65e0e79bf9afaca1e46cfef68d986d741fa8407af089f5f3b46e21d` |
| category schema | `f91f1411047bfe02ad58786402270a4b82a08b3196d8cf0417e815cc21b15b61` |
| capability catalog | `07a89b6971a1bb604dd28eed5cfd4a776a78e650e3d6861b3825bdf83817476d` |
| capability schema | `9248f5287d9f169117780aa7e1a996bddab700a37c0c58874e911b6b5e2e1b34` |
| homepage | `afbf87ba5a902b01b6f57a44c6e904223be708b0d211d2ff5b54a607173bc6e7` |
| homepage schema | `e105496ee3eb2b98ee114f83105ce67aa441010cb4446d2ec435f7f247627763` |
| relationship | `042b8ea0db4c566bfc2d1615f45c40b57d60d87a563db7c1ce36bb627d349d8c` |
| relationship schema | `460e315ca772653713a7a2c6c695b5e8ed76447d339acaf82fdd2c295be73a70` |
| error catalog | `2f5018cf2ac45dc36db8c998ef77fce27261bd2618c7dc60870400cd32c0eae4` |
| error schema | `64a04d2f1f743f96367046029d408d93fad4ab4801fc5c41ddede16ffdc9b342` |
| fixtures | `ea7c3a99ba49cd2b6d959eb2d5cb8864beaf4464ed96b366cb6cd7b2390fbc21` |
| validator | `07fa1944a7e77f8ee1eed800883a0c276f200587eea719c28cb7cf78457f6fac` |

## 未关闭项

- 平台正在发布向后兼容的 module internal dependencies v2；该公共依赖只阻塞新依赖图最终化与 H0 Handoff。
- `D-CA-003` 必须在完整 H0 Go 前由项目负责人裁决。
- 本报告不是环境、发布或运营证据，不得提升为 release-go 或 operations-go。
