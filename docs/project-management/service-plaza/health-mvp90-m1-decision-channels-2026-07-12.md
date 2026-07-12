# 健康大管家 M1 决策通道派发报告

- platform_work_id：`AIW-20260712-HEALTH-M1-DECISION-CHANNELS-DISPATCH`
- professional_work_id：`AIW-20260712-HEALTH-M1-PROFESSIONAL-SIGNOFF`
- security_work_id：`AIW-20260712-HEALTH-M1-SECURITY-FREEZE`
- 当前结论：两个正式决策通道已建立；派发集成并激活前保持只读

最终治理证据：R2 checklist 28/28、current SHA mismatch 0、R2 exam score 100。R1 在专业机器证据路径补齐前形成，保留为历史快照，不用于最终授权。

## 决策窗口

- 专业会签：`019f54a1-2847-7a71-b0ea-ee1ec403f29b`
- 平台安全：`019f54a1-6140-7690-ae1d-c96672f104bc`

任务窗口负责接收、整理和复核，不改变法定/组织责任。专业协调 Agent 不得代替医生集团专业负责人签字；平台安全负责人不得替专业或隐私角色裁决其范围。

## 隔离和依赖

- 专业分支/工作树：`codex/health-m1-professional-signoff` / `C:/Users/shugo/Documents/worktrees/heaotang-health-m1-professional-signoff`。
- 安全分支/工作树：`codex/health-m1-security-freeze` / `C:/Users/shugo/Documents/worktrees/heaotang-health-m1-security-freeze`。
- 两个工作树均从 `ef66b98113862d4b75bfe96df2966db52d65fddf` 创建并核验 clean。
- 两项路径互不重叠；M1 module item 继续 planned。

## 激活顺序

1. 本派发完成 checklist 28/28、exam100、IR 和总门禁后受控集成。
2. 两个工作树快进最终 APP integration HEAD，核验 clean。
3. 以独立 activation commit 将两项 planned 转 active；M1 module item仍保持 planned。
4. 两责任流分别提交 decision packet/receipt/checklist/exam100/IR。
5. 平台联合复核三项 Accepted 后，才评估 M1 module activation。

任何一项仍 Pending 只阻塞依赖它的 M1 可执行内容，不得反向阻塞无关项目，也不得降低门禁。
