# CA-SC 自建俱乐部测试环境 T0 验收任务书

- work_id：`AIW-20260712-CLUB-SC-T0-ACCEPTANCE`
- owner / role：`Codex platform integration agent` / 平台集成负责人
- upstream APP / backend：`ea45d82d24b9eff907ba5401e8d0a2f11151224e` / `a998812cf44dc449d85b726706d4ae2573179860`
- branch / worktree：`codex/club-sc-t0-acceptance` / `C:/Users/shugo/Documents/worktrees/heaotang-club-sc-t0-acceptance`
- environment：测试环境 `https://heaotang.cn`
- fixed seed：`HEAOTANG-CA-SC-20260712-V1`
- status：派发文件已生成；只有派发提交受控集成、工作树从最终 integration HEAD 创建且 registry 转 active 后才正式下达。

## 授权与范围

本任务书独立授权测试环境内可回滚的确定性合成数据、部署和 UAT，取代 P0/P1 阶段“test_environment 尚未授权”的历史状态；生产、真实数据、真实资金继续 No-Go。

1. 从标准首页进入自建俱乐部，列表仅返回 `type=standard AND category=general`，分页在服务端过滤后计算。
2. 专用详情 `/api/v1/clubs/self-created/:id` 只返回 active standard+general 安全 DTO。
3. 合成登录用户提交加入申请，验证首次、同载荷重放、异载荷冲突、并发单 pending 和本人状态隔离。
4. 浏览器验证列表/详情/申请状态、直达/刷新/后退/返回、320/360/768/桌面、键盘/焦点/aria。

## 数据、安全与恢复

- 只使用两个合成用户 A/B；不得保存真实手机号、OTP、JWT、cookie 或完整用户标识。
- 登录前确认每个账号至少两次可用验证码请求容量；不得绕过限流。
- fixture 单事务创建并带唯一 run 标识；只清理当前 run。混合 general/charity/family/direct/other/inactive，证明零串类。
- 部署前备份数据库和前端制品，记录哈希、远端/本地位置和 rollback target；部署后验证 `/health?json=1`、`/ready`、catalog/actions 和认证 smoke。
- 必须在安全环境验证数据库恢复和前后端回滚；部署成功不等于 T0 Go。
- allowlist：catalog/actions、SC search/detail/join/my-applications、最小认证；denylist：create/review/member/role/payment/charity/federation 写接口。
- Nginx/API/DB 证据只保留 correlation、error_id 和 user 空/非空事实，禁止落凭据和敏感正文。
- 动态详情深链必须真实验证直达与刷新 SPA 200。

## 精确允许路径

- `contracts/foundation/agent-collaboration.v1.json`
- `contracts/foundation/development-checklists/2026-07-12-club-sc-t0-acceptance*.json`
- `contracts/foundation/governance-exams/2026-07-12-club-sc-t0-acceptance*.json`
- `contracts/foundation/implementation-records/2026-07-12-club-sc-t0-acceptance*.json`
- `contracts/modules/club-alliance/internal-dependencies.v1.json`
- `docs/project-management/modules/club-alliance/self-created/internal-dependencies.v1.json`
- `docs/project-management/modules/club-alliance/self-created/CA-SC-handoff.md`
- `docs/project-management/modules/club-alliance/self-created/acceptance/`
- `docs/project-management/service-plaza/handoff-log.md`
- `scripts/Manage-ClubSelfCreatedT0Fixture.ps1`
- `scripts/Invoke-ClubSelfCreatedT0Acceptance.ps1`
- `scripts/Test-ClubSelfCreatedT0Safety.ps1`

不得修改其他前端、后端源码、Schema、公共契约或 H2 路径。若发现产品缺陷，登记根因并建立独立修复工作项。

## 必备证据与判定

验收目录至少包含 plan、environment、fixture-manifest、deployment、rollback、api-results、browser-uat、network、db、security、go-no-go、receipt。所有结论引用 exact commit、命令、expected/actual、时间和脱敏证据。任何未关闭 Blocker/Major 为 No-Go；只有自动化、真实 HTTP、浏览器、恢复回滚、治理和 Handoff 全通过才可宣布 T0 Go。
