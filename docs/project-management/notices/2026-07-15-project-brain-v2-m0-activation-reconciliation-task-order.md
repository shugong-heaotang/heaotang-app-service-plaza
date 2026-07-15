# Project Brain v2 M0 activation 权威漂移调和 R1 任务令

- 日期：2026-07-15
- work item：`AIW-20260715-PROJECT-BRAIN-V2-M0-ACTIVATION-RECONCILIATION-R1`
- exact authority base：`5d5a46271c4c343f95d723e75666ced7dbc10119`
- independently accepted source：`f3767b7e34b3d8fb16ad0af955f7d0ac46de935d`
- merge base：`36b245871dd95d53964fb20cf4c30a05ceb89a77`

## 目标

只调和 activation 治理证据进入新权威：原样恢复 source 的 9 个非 registry blob，完整保留新权威 Mall 两项修改与三项新增，并语义合并 registry。不得实现 Project Brain v2 M0 内容。

## 状态语义

本候选可记录 reconciliation `integrated`、activation `integrated`、operations `active`，但这些状态仅在候选经独立 reviewer 判定 Go，并由平台集成负责人以普通 fast-forward 纳入 authority 后生效。候选分支、提交或自测不等于权威集成、M0 完成、部署或生产授权。

operations 保持 `base_commit=36b245871dd95d53964fb20cf4c30a05ceb89a77`、`started_with_clean_worktree=true`、`preexisting_changes_acknowledged=false`。M0 未完成；M1-M5、App、scripts、Project Brain v1、SC remediation、真实数据、凭据、环境、部署和 production 均为 No-Go。

## 角色分离

- developer：Project Brain v2 activation reconciliation agent
- reviewer：independent Project Brain v2 reviewer
- approver：项目最高负责人
- integration owner：平台集成负责人

## 完成门禁

preflight、collaboration schema、current checklist、随机考试 100、verified IR、总合同、UTF-8、14/14 scope、secret 0、freshness 全部通过；提交并仅推送候选分支。远端 authority、source、merge-base、9 个 blob、Mall 五项变化、范围或任一门禁漂移时立即失败关闭。