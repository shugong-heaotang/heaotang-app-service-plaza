# 学习广场 M0 正式启动任务单

签发日期：2026-07-13（Asia/Shanghai）  
签发角色：项目最高负责人

## 一、授权结论

批准学习广场立即进入开发准备与 M0 合同化，不以近期上线为前提。先建立可独立验证的核心板块与跨模块闭环，再据此识别平台体系缺口。

M0 允许需求合同、领域模型、接口 schema、确定性 fixtures、负面权限用例和离线验证器；不得修改 `app/src/**`、后端、数据库、部署、测试服或生产环境，不得触达真实用户、发送消息或发起支付。

## 二、工作身份

- `work_id`: `AIW-20260713-LEARNING-PLAZA-M0`
- `record_id`: `IR-20260713-LEARNING-PLAZA-M0`
- `module_id`: `learning-plaza`
- owner: 学习广场持续开发负责人
- reviewer: 学习广场独立验收负责人
- approver: 项目最高负责人
- branch: `codex/learning-plaza-m0`
- worktree: `C:\Users\shugo\Documents\worktrees\heaotang-learning-plaza-m0`
- base: `094bafdbba48c84f41611ca541c8225e4de4a8dd`

## 三、产品定位与核心板块

学习广场是生命导航的学习执行层，不是孤立课程商城。M0 固定六个核心板块：学习资源、学习路径、课程与课时、俱乐部共学、学习进度与成果、Nova 辅助学习。

首条闭环为：生命导航给出维度与目标 -> 学习广场推荐可见资源/路径 -> 用户接受并推进学习 -> 俱乐部承接共学 -> Nova 仅基于可引用资料答疑与复盘 -> 完成事实形成可回写事件。读书先作为 `book/note` 资源类型，不开发完整阅读器。

## 四、参考资产边界

参考仓库提交：`c158b2087d54e026ab385eec7850c105894b33d0`。

- 开发计划 v2.1 SHA-256：`70C879B1BA1FA45670ACAAEA8E2CAB4E815CB0F48105845E25BC58ED4A76AFF5`
- 开发文档 v2.1 SHA-256：`65D96C58E129A9652A7A0BB7A331A2E5EF0764CF80D2603E9ADD5196F90BC581`
- Python 参考实现 SHA-256：`B40B6856A0244C1057FD8BFECBC00284B6671A169679990169348FA5A5A32D1E`
- 前端参考脚本 SHA-256：`61C3477D50344DE903A97F6267008E331F9BA0E831C335C4CB4C2CCC66A1C0C3`

这些资产只证明参考实现的 6 条离线验收脚本当前通过；不证明平台路由、鉴权、数据所有权、接口版本、隐私、部署或生产可用性。

## 五、允许与保护路径

模块实施允许：

- `contracts/modules/learning-plaza/**`
- `docs/project-management/modules/learning-plaza/**`

仅平台集成负责人可修改本任务单、协作注册表和治理阅读清单。共享前端、后端、foundation 其他文件、其他模块、部署与生产配置均为保护路径。

## 六、M0 最小交付物

1. 模块 README、任务理解回执和来源追踪矩阵。
2. 平台级与模块内部依赖声明，逐项标明 owner/version/readiness。
3. 学习资源、路径、进度、成果、推荐、共学和 Nova 引用的版本化 schema。
4. 覆盖公开/登录/俱乐部/私有可见性、越权、无引用 AI、重复完成和非法状态转换的负面 fixtures。
5. 可执行离线验证器及测试。
6. current checklist、治理考试 100 分、implementation record 与 Handoff。

## 七、M0 Go 条件

工作项、分支、worktree 和路径无冲突；治理准入通过；合同/fixtures/负面用例全部通过；所有 provisional 依赖被失败关闭；开发、独立验收、批准角色分离；无业务代码、部署和真实外部动作。

M0 Go 后才可另行激活 M1。M1 建议只实现“浏览可见资源 -> 接受学习路径 -> 记录一项进度 -> 形成完成事件”的最小真实闭环，跨模块写回仍通过版本化端口，不直接写对方数据。
