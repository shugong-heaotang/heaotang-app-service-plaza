# 俱乐部 type+category 服务端权威筛选

日期：2026-07-11

D-CA-003 已由项目负责人 Accepted：SC=`standard+general`，PC=`standard+charity`。平台发布 `club-category-filter.v1` 合同、Schema、validator 和混合 fixture；前端本地伪筛选被明确禁止。

后端工作项 `AIW-20260711-CLUB-CATEGORY-AUTHORITY-BACKEND` 使用独立仓库、分支和工作树，只允许 club search 的 handler/service/tests。平台治理提交不证明后端已实现。

H0 Full Go 条件：Accepted 决策与 ADR 集成；后端 category 参数和组合筛选实现；非法/空白/不支持 category 稳定失败关闭；general/charity/family/direct/health/federation 混合数据零串类；分页和计数保持服务端权威；后端定向测试、总合同门禁和测试环境 HTTP 验收通过。CA-H1 与四类业务仍需后续独立授权。
