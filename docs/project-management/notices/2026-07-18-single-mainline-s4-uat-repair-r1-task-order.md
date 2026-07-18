# S4 UAT 六路由产品修复 R1 任务令

- work_id: `AIW-20260718-SINGLE-MAINLINE-S4-UAT-PRODUCT-REPAIR-R1`
- owner: Codex highest owner / thread `019f72ee-3907-7b21-9498-8e918ac53aac`
- branch: `codex/single-mainline-s4-uat-repair-r1`
- base: `2df75badec2ae5f8c7b04c4c3ae2602b8d4f2ef9`
- 目标：关闭 R5 双视口 UAT 的 2 个 P0、4 个 P1 路由缺陷，并对受影响路由及既有通过路由做回归。

## 当前 G1 边界

G1 仅允许登记、任务理解、根因记录、飞行检查表、治理考试、实施记录和 Handoff。产品源码、测试、配置、构建、提交、推送、集成和部署全部禁止，必须等独立 G1 Acceptance 与另行签发的 G2 Activation。

## 后续 G2 候选范围

仅建议以下十个路径，当前不构成写权限：`app/src/App.tsx`、`app/src/App.test.tsx`、`app/src/pages/PlannedServicePage.tsx`、`app/src/modules/club-alliance/ClubAllianceRoute.tsx`、`app/src/modules/club-alliance/index.ts`、`app/src/modules/club-alliance/self-created/SelfCreatedClubPage.tsx`、`app/src/modules/club-alliance/self-created/SelfCreatedClubPage.test.tsx`、`app/src/modules/project-brain/projectBrainApi.ts`、`app/src/modules/project-brain/ProjectBrainPage.test.tsx`、`app/vite.config.ts`。

## 验收

产品阶段必须使 P004、P011 的 P0 和 P007、P008、P009、P010 的 P1 全部关闭；测试、构建、安全门、测试服部署及新鲜浏览器证据均需独立验收。任何 P0/P1 未关闭均为 No-Go。
