# 健康大管家 M1 C4-S04 安全冻结任务通知书

- notice_id：`HM-M1-SECURITY-FREEZE-TASK-20260712-001`
- work_id：`AIW-20260712-HEALTH-M1-SECURITY-FREEZE`
- decision_thread：`019f54a1-6140-7690-ae1d-c96672f104bc`
- owner/signer：平台安全负责人
- 状态：正式派发后由 planned 转 active

## 目标

冻结 M1 首检查点的精确主体、资源、动作、资源级服务端拒绝矩阵、最小审计字段、威胁模型、可证伪前提和复审触发。只形成安全合同与决策证据，不实现接口或业务。

## 工作区与允许路径

- branch：`codex/health-m1-security-freeze`
- worktree：`C:/Users/shugo/Documents/worktrees/heaotang-health-m1-security-freeze`
- registration base：`ef66b98113862d4b75bfe96df2966db52d65fddf`
- 最终 base：派发集成后的 exact APP HEAD

只允许修改 registry 中本工作项列明的 security freeze 文档、receipt、`security-authorization.v1` JSON/Schema 和专属 checklist/exam/IR。禁止业务代码、接口实现、数据库、环境、部署和真实健康数据。

## 主体、资源与动作

主体至少包括：成年会员本人、无服务关系人员、健康管理师、医生、平台支持/安全审计角色、AI runtime。资源至少包括：授权、档案项、测评会话、目标、计划及版本、任务、反馈、检查/复盘、成长记录、审计事件。

每个动作必须绑定资源所有权、有效授权、服务关系、角色/资质、状态和用途；AI runtime 只能在已授权目的内读取最小上下文并生成草案，不得成为业务授权主体或独立写入最终专业结论。

## 服务端拒绝矩阵

至少覆盖：未登录、非本人、跨会员、无服务关系、角色不足、资质缺失/过期、授权缺失/撤回/过期、资源状态冲突、版本冲突、模板未批准/过期、资料不足、风险/不适、幂等冲突和审计写入失败。每项给出 HTTP/领域 error_id、fail-closed 状态、是否写审计和恢复条件。

## 审计与威胁模型

最小审计字段：actor_ref（脱敏引用）、actor_role、action、resource_type/ref、purpose、authorization_version、policy/template version、outcome、reason/error_id、occurred_at、correlation_id、request/idempotency reference。禁止健康正文、OTP、JWT、cookie、secret、完整手机号/身份证和不必要个人标识。

威胁模型至少覆盖越权读取/写入、跨会员 IDOR、失效授权继续使用、角色/资质伪装、AI 提示注入与越权工具调用、模板/策略供应链篡改、重放/并发、审计绕过、敏感日志、数据枚举和前端绕过。

## 决策规则

证据必须包含 decision maker、date、scope、version、`Accepted | Exact revision | Pending with owner`、premises、falsification evidence、review trigger/date、兼容/迁移影响和禁止替代方案。任何依赖未冻结时保持不可执行；不得用前端隐藏、管理员万能权限或“以后补服务端校验”换取 Accepted。
