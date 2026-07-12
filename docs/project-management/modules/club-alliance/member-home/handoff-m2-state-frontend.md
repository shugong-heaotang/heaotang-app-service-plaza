# H2 M2 会员状态分层前端修复 Handoff

- work item：AIW-20260712-CLUB-MEMBER-HOME-STATE-FRONTEND
- checkpoint：H2-M2-STATE-FRONTEND-R1
- owner：H2 frontend state agent
- status：Handoff Ready / platform review pending
- branch：codex/club-member-home-state-frontend
- base：3fc48afbbe934d9ec31d4a9c958c0dab01290031
- implementation record：IR-20260712-CLUB-MEMBER-HOME-STATE-FRONTEND-R1

## 完成内容

1. MemberClub 不再暴露含义不明的 status，改为 clubStatus 与 membershipStatus。
2. wire 只接受 club_status=active；membership_status 只接受 active 或可选 suspended。
3. 旧扁平 status 即使与新字段同时存在也失败关闭。
4. pending/rejected 申请历史、left 历史关系、dissolved membership 和 dissolved club 均不能进入当前“我的俱乐部”；统一抛出 CMH_CONTRACT_INVALID。
5. 页面同时显示“俱乐部正常”与“会员有效/会员停权”，不再把俱乐部生命周期当会员状态。
6. 负向用例覆盖字段缺失、旧字段、申请状态串流、历史关系串流和解散状态串流。

## 验证证据

- current checklist：contracts/modules/club-alliance/development-checklists/2026-07-12-club-member-home-state-frontend-r1.json（28/28）
- governance exam：contracts/modules/club-alliance/governance-exams/2026-07-12-club-member-home-state-frontend-r1-attempt-1.json（100 / passed）
- 定向测试：2 files / 33 tests passed
- 前端全量：22 files / 225 tests passed
- production build：passed
- test-server build：passed
- 服务广场总合同、治理、UTF-8、diff 和 scope：提交前复跑

## 工作树依赖

独立工作树初始没有 app/node_modules。worktree-bootstrap 核对本地 package-lock 与 C:/Users/shugo/Documents/APP系统/app/package-lock SHA 一致后，仅在本地建立 node_modules junction；未修改 package.json/package-lock。测试和双构建结束后已删除 app/node_modules junction 与首次错误命令生成的仓库根 .vite 缓存，主共享 node_modules 保持完整，提交范围不含任何依赖目录。

首次从仓库根直接调用 vitest 时未加载 app/vitest.config.ts，表现为 document/sessionStorage undefined。这是命令工作目录错误，不是产品缺陷；切换到 app 目录用批准 npm scripts 后定向和全量测试均通过，未通过修改测试环境或实现绕过。

## 未授权与未完成

- 未修改 ClubAllianceRoute、公共路由或其他页面。
- 未修改后端、数据库、部署、环境或 registry。
- 当前后端若仍返回旧 status，联合部署保持 No-Go；必须由独立后端工作项提供 club_status/membership_status 后再进入环境 UAT。
- 本 Handoff 不等于 H2 M3 Entry Go、Full Go 或生产授权。
