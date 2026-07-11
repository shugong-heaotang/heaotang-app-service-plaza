# 健康大管家 MVP-90 M0 Conformance 报告

日期：2026-07-12

工作项：`AIW-20260711-HEALTH-MVP90-M0-CONTRACTS`

结论：`PASS for module checkpoint / platform M0 acceptance pending`

## 1. 数量与边界

| 项目 | 结果 |
|---|---:|
| 产品语义对象 | 16/16 |
| Pending with owner | 27/27；全部 `executable=false` |
| 状态机 | 6/6 |
| 角色 | 6/6；最终 scope 名称仍 Pending |
| 合成场景 | `MVP-A001`—`MVP-A015`，15/15 |
| Schema 实例 | 5/5 |
| Python conformance | 12/12 |

M0 合同明确标记为产品语义，不是 API 或数据库 Schema。没有新增前端、后端、环境、部署、真实数据或收费能力。

## 2. 合成数据与重放

- generator：`heaotang-deterministic-fixture-v1`
- algorithm：Python 标准库 `hashlib.sha256`
- seed：`HEAOTANG-HM-MVP90-M0-20260712-V1`
- environment：`non-production`
- fixture file SHA-256：`acb8609734f51d0e729f4e07b8f01d08931c7b4513183f5e501423429f74b177`
- canonical replay SHA-256：`5b4d28b987a213432764ef0af8bc3ff51ee25fa2037e2ead25adf9eba142e95a`
- 两次独立内存重放对象逐字段相同，静态文件与重放结果相同。

Faker 未在批准的锁定依赖中可用，因此没有临时安装未锁定包；采用通知允许的等价确定性标准库生成器。数据只含 `SYN-*` 引用和“合成验收数据”标识，不含真实姓名、手机号、身份证、会员 ID、OTP、JWT、cookie、病历或真实机构资料。

## 3. 正反例覆盖

通过项包括：

- 16 对象/27 Pending/6 状态机/6 角色/15 场景精确集合和唯一 ID；
- 对象引用完整、owner/version/forbidden fields 完整；
- 状态引用和迁移唯一，禁止迁移不能同时进入允许集合；
- 紧急引导不得直接恢复、资料不足不得 fail-open、AI 草案不得直接生效、不适任务不得继续鼓励；
- AI 诊断、处方、改药、疗效承诺、关闭专业/紧急风险均为禁止动作；
- 最终 scope 不得在 `C4-S04` Pending 时提前产生；
- fixture 必须 synthetic/non-production/固定 seed，场景与预期不得漂移；
- 负例覆盖缺对象、Pending executable、未知状态、禁止迁移放行、角色允许/禁止冲突、提前 scope、非合成 fixture 和敏感模式注入。

## 4. 验证命令

```powershell
C:\Users\shugo\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe -X utf8 contracts/modules/health-manager/mvp90/conformance/test_health_mvp90_contracts.py
```

结果：`Ran 12 tests ... OK`。

另外通过：module internal dependencies v2、development checklist、governance exam、implementation record、agent collaboration、UTF-8、Git diff 和 allowed-path/sensitive pattern 门禁。

最终治理证据为 R2：`FC-20260712-HEALTH-MVP90-M0-R2` 28/28、`EX-20260712-HEALTH-MVP90-M0-R2-1` 100 分、`IR-20260712-HEALTH-MVP90-M0-R2` verified。首检查点治理文件保留为不可修改的历史快照。

## 5. 尚未证明

本报告不证明专业会签、接口实现、真实权限、环境行为、消费者语言 UAT、人工接管演练、可访问性、发布或运营。上述项目保持 Pending/No-Go，并由后续独立工作项负责。
