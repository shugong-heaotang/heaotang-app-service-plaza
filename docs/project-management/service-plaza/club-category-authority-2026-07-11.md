# 俱乐部 type+category 服务端权威筛选

日期：2026-07-11

D-CA-003 已由项目负责人 Accepted：SC=`standard+general`，PC=`standard+charity`。平台发布 `club-category-filter.v1` 合同、Schema、validator 和混合 fixture；前端本地伪筛选被明确禁止。

后端工作项 `AIW-20260711-CLUB-CATEGORY-AUTHORITY-BACKEND` 使用独立仓库、分支和工作树，只允许 club search 的 handler/service/tests。实现提交 `be06897a`，独立复核发现分页 OFFSET 溢出与 `rows.Err()` 缺口后先判 No-Go；根因修复提交 `47ef91bb` 完成极值防护、迭代错误检查和分页边界回归，复核转为 Go。后端集成分支 `codex/service-plaza-phase1-integration` 的集成 HEAD 为 `47ef91bb`，两条远端分支均已推送。

本地证据：定向 club-plugin 测试、`go test ./... -count=1`、`go vet ./...`、`gofmt` 与 `git diff --check` 全部通过。测试环境于 2026-07-11 08:22（Asia/Shanghai）部署修正版；部署前备份为 `/root/heaotang-backups/20260711-082209.tar.gz`，本地副本为 `D:\Backup\heaotang-test-server\20260711-082209\test-server-state.tar.gz`，部署二进制 SHA-256 为 `4b5d29d49d64d5a8e710ddd20957d66588a31afa51d0f738f872809d4944fcb4`。`/ready` 返回 db=true、plugins=24，服务广场 20 动作运行时契约与基线一致。

认证 HTTP 验收：测试用户登录和 `/api/v1/auth/me` 通过；现有活跃数据中 general=15、health=2，general 分页第 1/2 页各 5 条且无重叠，所有结果分类精确匹配；charity 当前无活跃环境夹具，返回 total=0/items=0 且无串类，其有数据正例由混合自动化夹具证明。blank/whitespace/unknown category 均返回 400 `CLUB_FILTER_CATEGORY_INVALID`；family/direct 与 category 组合返回 400 `CLUB_FILTER_COMBINATION_UNSUPPORTED`；club-federation 作为 ClubType 返回 400 `INVALID_CLUB_TYPE`；极大 page 返回 400 `INVALID_PAGE`。

H0 Full Go 前置中的 D-CA-003、category 合同、后端实现、本地回归、部署和真实 HTTP 正反例现已关闭。模块需受控吸收本平台关闭证据，更新 v2 internal-dependencies 与 CA-F0/H0 Handoff，并由平台复核该模块提交后才能给出 H0 Full Go；CA-H1 与四类业务仍需后续独立授权。
