# 和奥堂前置能力标准 v1

## 目的

把“前置工作已经做过”升级为“下游可以稳定依赖的标准能力”。任何公共成果只有同时具备契约、实现、自动化门禁、环境证据和变更规则，才能登记为 `verified` 或 `deployed`。

核心原则：前置层相对稳定并持续固化，业务层允许持续变化并不断增加。下游只能依赖前置层的公开承诺；如果某项“依赖”频繁跟随单一业务变化，它就不应留在前置层。正式决策见 ADR 0007。

## 标准能力包

每项前置能力必须在 `contracts/foundation/foundation-capabilities.v1.json` 登记：

1. 唯一 `capability_id` 和主版本。
2. 所属 L0-L5 层级、Owner 角色和当前状态。
3. 明确的 `depends_on`，不得循环或引用不存在的能力。
4. 对下游承诺的 `provides`，不混入板块专属业务逻辑。
5. 至少一个完成门禁及可读取证据。
6. `locked` 或 `backward-compatible` 变更策略。
7. 最近一次真实验证日期。

状态含义：`draft` 仅设计；`implemented` 只有实现；`verified` 已通过自动化和恢复类实测；`deployed` 已在测试环境运行；`deprecated` 不允许新板块依赖。业务准入只接受 `verified` 或 `deployed`。

## 业务依赖声明

每个板块冻结需求时新增一份 `module-dependencies.v1` 文件，只声明所需能力 ID 和最低主版本。平台工具检查能力是否存在、状态是否可用、版本是否满足；未通过时板块保持 No-Go，不允许复制一套公共实现绕过。

## 固化和变更规则

- 完成能力：实现、测试、部署/演练和证据齐全后才能升状态。
- 兼容变更：保持能力 ID 与主版本，必须通过契约差异和下游回归。
- 破坏性变更：新建主版本，保留旧版本迁移窗口并记录 ADR。
- 证据失效：立即把能力降为 `implemented` 或 `draft`，暂停依赖它的新增业务。
- 根因问题：修复公共能力本身并回归所有依赖者，不允许业务侧临时绕行。

## 自动检查

```powershell
python -X utf8 scripts/validate_foundation_dependencies.py contracts/foundation/foundation-capabilities.v1.json
```

该检查会拒绝重复 ID、未知依赖、依赖环、非法版本/状态和缺失证据。后续三个核心板块的需求冻结以此注册表为统一前置基线。
