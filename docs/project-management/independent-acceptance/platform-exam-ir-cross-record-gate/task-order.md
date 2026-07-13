# 平台治理考试与实施记录跨记录门禁独立验收任务单

- work_id：`AIW-20260714-PLATFORM-EXAM-IR-CROSS-RECORD-INDEPENDENT-ACCEPTANCE`
- owner：`Platform governance independent test agent`
- owner_role：平台治理独立测试负责人
- reviewer_role：APP 总架构独立验收负责人
- approver_role：项目最高负责人
- evidence base：`757de99e4dfa4a7467a0de6e1a66d6e030ba7f09`
- reviewed source：`3b4bd0c7c78c78be5b592b894e795053f169fa14`
- reviewed integration：`757de99e4dfa4a7467a0de6e1a66d6e030ba7f09`
- authorization integration：`60ff58d0be2c4f80a1e8c9c32a534113e1b384ae`

本项为 `platform scope`，current checklist 使用 `module_id=null`。这只证明独立验收证据属于平台治理范围，不授权修改 registry、foundation、scripts、validator 或任何业务模块。

## 目标

把对跨记录门禁 exact source 与受控集成的独立 Go/No-Go 文件化，保存可复验的四类失败关闭、Activity 历史非 canonical 记录、Protection Mall 九文件只读现场、全量治理测试和总合同覆盖边界证据。

## 独立性与禁止边界

- owner 未实现 source `3b4bd0c7...`，未执行 integration `757de99e...`，也不执行本证据的后续平台集成。
- 只允许创建本目录下 `evidence.md`、`task-order.md`、`development-checklist*.json`、`governance-exam*.json`、`implementation-record*.json`。
- 禁止修改 `contracts/foundation/agent-collaboration.v1.json`、其他 foundation 文件、scripts、NOVA、商城九文件、业务代码和部署配置。
- 禁止触达生产、真实用户、凭据、支付、资金或不可逆数据。
- 聊天结论不等于 formal evidence；本证据完成后仍由 APP 总架构独立验收负责人复核，再由平台集成负责人执行受控集成和状态交易。

## 验收要求

1. 精确绑定 source `3b4bd0c7...`、integration/base `757de99e...` 与 authorization `60ff58d0...`，不得混同。
2. 复验 same-record passed/100 正例，以及 failed/75、record mismatch、missing exam 三类失败关闭负例。
3. 证明 Activity 非 canonical implementation record 仍被递归发现并受共同 checklist/exam 约束；不得把历史格式兼容解释为整体豁免。
4. 对 Protection Mall 九文件脏快照执行只读负例：validator 必须 exit 1，错误包含同 record 的实际 `status=failed, score=75`，运行前后 dirty count、Git status、逐文件 SHA-256 与合并 fingerprint 不变。
5. 记录全量 Python 治理 suite `79=78 pass + 1 fail`，并在 exact base `2535a6bf...` 证明同一 inventory 测试以相同 27 条历史错误失败；不得用基线失败掩盖候选专项缺陷。
6. 运行 Service Plaza 总合同并明确边界：总合同自动递归覆盖 foundation 和 `contracts/modules/*` 的 exam/IR，但不会自动扫描本 reviewer namespace；本目录三份 JSON 必须另行显式验证。
7. 真实完成 current checklist 26/26、随机治理考试 attempt 1 得分 100，并由同 record implementation record 引用。
8. 通过显式 checklist/exam/IR validators、JSON、UTF-8、`git diff --check`、allowed scope、秘密模式与远端一致性检查；计算 `evidence.md` SHA-256 后提交并推送专用分支。
