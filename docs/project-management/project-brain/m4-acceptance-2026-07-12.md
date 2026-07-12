# Project Brain v1 M4 验收报告

日期：2026-07-12

work_id：`AIW-20260712-PROJECT-BRAIN-V1`

record_id：`IR-20260712-PROJECT-BRAIN-V1-M4`

## 结论

M1-M3 功能实现满足 v1 产品与架构范围。M4 自动化、安全和本地真实浏览器 UAT 通过；正式 Project Brain 审计仍准确报告权威项目事实中的 3 个 error 与 7 个 warning，因此驾驶舱总体显示 `No-Go`，没有把项目事实伪装成 Go。

## 自动化与构建

- Python M2：10/10 tests passed。
- React/Vitest：23 files / 221 tests passed。
- TypeScript + Vite `test-server` build：passed。
- TypeScript + Vite production build：passed。
- production `dist` Project Brain snapshot assets：0。
- test-server 显式装配快照 SHA-256 与权威 generated 快照一致。
- 全量服务合同、implementation record、UTF-8 与 `git diff --check` 门禁通过。

## 浏览器 UAT

环境：本地 test-server 制品，Vite preview，路由 `/internal/project-brain`。本地根路径覆盖仅用于排除正式 `/app/service-plaza/` 部署前缀对 preview 的影响，源码与业务制品逻辑未改变。

### 桌面

- viewport client width：1265px。
- `scrollWidth=clientWidth=1265`，无横向溢出。
- H1：`和奥堂项目大脑`；verdict：`暂不可推进`。
- 区块：正在推进、模块全景、待独立验收、待你决定、风险。
- 可追溯卡片：20；写入类控件：0；浏览器 warning/error：0。
- footer 展示生成时间、来源提交、新鲜度与只读说明。

### 360px

- 初次验收 `scrollWidth=362`、`clientWidth=345`，判定 No-Go。
- 根因：footer 的 40 字符来源提交哈希未允许任意位置断行。
- 修复：`overflow-wrap:anywhere`；复验 `scrollWidth=clientWidth=345`，无横向溢出。
- verdict 仍为 `暂不可推进`；写入类控件：0。

## 安全审计

- 扫描 47 个 Project Brain/本分支变更文件：private key、Bearer、JWT、手机号模式发现 0。
- snapshot/audit 严格输出合约通过；禁止输出 `workspace_path`、`repository_root`、password、authorization、api_key、private_key。
- 页面不包含批准、部署、删除、修改、表单或输入控件。
- 普通 production 构建不包含快照资产；不授权生产发布、真实账号、真实健康或支付数据。

## 残余事实

- `PB-INTEGRATED-EVIDENCE` 3 项：属于其他权威工作项缺 Handoff，不在 Project Brain 范围内篡改。
- `PB-WORK-NEXT` 7 项：属于现有活动工作项下一检查点缺失，保持 warning。
- 上述事实使驾驶舱保持 No-Go；不构成 Project Brain 生成、验证、只读展示或安全边界失败。

## PB-A01 至 PB-A16

PB-A01/A02：M1 Go；PB-A03 至 PB-A08、PB-A13：M2 tests/安全输出通过；PB-A09 至 PB-A12、PB-A14：M3 tests、双视口 UAT 与双模式构建通过；PB-A15：UTF-8 通过；PB-A16：checklist、exam、IR、Handoff 齐全。最终 integrated 状态须以受控集成提交存在为最后证据。
