# LN-S2 P0/P1 Base Contract Conformance Report

- date：2026-07-12
- work_id：`AIW-20260712-LIFE-LN-S2-P0-P1`
- verdict：`Base Contract Go / Executable No-Go / Environment Not Authorized`
- seed：`HEAOTANG-LN-S2-20260712-V1`
- source synthetic SHA-256：`82dfd8a2c511895eb819a1c7911433c42f237efef1bb218b160fc2eab1d8af08`

## 结果

| 门禁 | 结果 |
| --- | --- |
| 四组 Draft 2020-12 Schema 实例 | 4/4 Pass |
| 标准库 conformance | 12/12 Pass |
| 唯一 dimension ID / sort order | Pass |
| Pending / frozen=false / executable=false | Pass |
| 旧 `yun mapping_target=null` | Pass |
| 窄目录字段与禁止字段隔离 | Pass |
| 缺配置、读取失败、空/非法、重复、未知、停用、版本不兼容 | 全部稳定 fail-closed |
| 合成 seed / non-production / 销毁策略 | Pass |
| 手机、邮件、Bearer、JWT 模式扫描 | Pass |

canonical hashes 由 `test_life_dimension_contracts.py` 每次输出并用于重放比较。fixtures 只包含合成维度引用，不包含真实个人或申请正文。

## 未关闭边界

`D-LN-S2-001` 仍 Pending，所以注册表不是权威业务注册表，selector 不可执行。现有宽 `GET dimensions`、代码默认目录回退和 POST 服务端 selector 只登记为后续差距；本检查点不修改后端或环境，也不把本地 conformance 冒充测试环境验收。
