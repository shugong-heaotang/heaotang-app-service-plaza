# Project Brain v2 M2 G0 remediation activation Handoff

- exact base：`6ad2e7e1930f60dfe174397c480a9feefdd53c93`
- work item：`AIW-20260717-PROJECT-BRAIN-V2-M2-G0-REMEDIATION-ACTIVATION`
- 当前状态：activation candidate；不是authority，不是runtime修复

## 候选只完成

- 证明PDCAR scope correction已在authority释放registry；
- 登记activation integrated与formal remediation active的条件式状态；
- 把formal修复限制为两项runtime文件和六类自身治理证据；
- 冻结G0合法/非法分支、G1不回归、历史证据不改写和M3复验要求。

## 独立验收

必须深比较registry只新增两项、其他152项和顶层字段不变；验证PDCAR仍active且不拥有registry、Dayi项目完整保留、两项PB scope不与现有active工作重叠；检查7类activation、8类formal、current checklist、Exam100、IR、总合同、UTF-8、diff、secret0和fresh authority。

R1 exact candidate `4221004dddf75ce6e9eb6b26e61849652cd2f6b9`内容门禁通过，但因authority推进到`6ad2e7e1930f60dfe174397c480a9feefdd53c93`，独立验收以P1 freshness No-Go收口，未推送、未集成。本R2从新authority重建并重新生成current checklist、Exam和IR；开发者门禁取得后仍需独立reviewer复验，不能由writer自授Go。

R2 writer门禁结果：registry深比较`152 unchanged / 2 added / top-level 0`，PDCAR active且registry_owned=false，Dayi逐字段保持不变；collaboration通过；current checklist 26/26；Exam100；IR、总合同、1612文件UTF-8和diff通过；候选为7文件/7类activation路径、越界0、secret0；最终fetch时remote authority仍为`6ad2e7e1930f60dfe174397c480a9feefdd53c93`。

## 后续边界

activation独立Go并受控进入authority后，才创建formal remediation工作树。formal修复独立Go并进入新authority后，才能在该authority上重放M3 R2并寻求M3整体Acceptance；不自动授权M4、部署或production。
