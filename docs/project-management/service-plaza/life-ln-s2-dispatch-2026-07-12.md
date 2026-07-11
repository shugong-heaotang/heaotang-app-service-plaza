# 生命导航 LN-S2 P0/P1 正式派发报告

## 结论

- 平台工作项：`AIW-20260712-LIFE-LN-S2-DISPATCH`
- 模块工作项：`AIW-20260712-LIFE-LN-S2-P0-P1`
- 通知：`LN-S2-TASK-20260712-001`
- Handoff：`SP-H033`
- 平台 branch/worktree：`codex/life-ln-s2-dispatch` / `C:/Users/shugo/Documents/worktrees/heaotang-life-ln-s2-dispatch`
- 模块 branch/worktree：`codex/life-navigation-ln-s2-p0-p1` / `C:/Users/shugo/Documents/worktrees/heaotang-life-ln-s2-p0-p1`
- 基线：`7d261d8276c4d72883598f72a8dbaac8a48837b1`
- 状态：平台正式派发文件已形成，待受控集成和模块 final-base 激活；模块仍未签收

## 平台治理

- preflight：ready；
- checklist：`FC-20260712-LIFE-LN-S2-DISPATCH`，26/26，current SHA mismatch 0；
- exam：`EX-20260712-LIFE-LN-S2-DISPATCH-1`，score 100；
- IR：`IR-20260712-LIFE-LN-S2-DISPATCH`。

## 根因范围

LN-S2 解决的是 `dimension_id` 缺少版本化权威注册表和服务端 selector 的系统性缺口。现有 `/life-nav/dimensions` 返回过宽且配置异常回退代码默认，不得冒充新窄目录或失败关闭标准。P0/P1 只冻结事实、决策包和合同；不修改产品代码。

## 当前决策状态

- `dimension.decision`：Pending / blocked-local；
- `registry_frozen=false`；
- selector `executable=false`；
- 旧 `yun mapping_target=null`。

该 Pending 只阻塞 executable selector、前后端编码和环境验收，不阻塞 P0/P1 Schema 结构、窄目录和失败关闭负例。

## 合成数据

固定 seed `HEAOTANG-LN-S2-20260712-V1`，草稿合成包当前 SHA-256 `82dfd8a2c511895eb819a1c7911433c42f237efef1bb218b160fc2eab1d8af08`。模块必须重新计算并 review-transform；允许固定版本 Faker/确定性工具，禁止真实个人数据、申请正文和凭据。

## 下一步

1. 本派发提交受控集成。
2. 模块工作树快进至 final integration HEAD 并核验 clean。
3. 独立 activation commit 将模块工作项 planned -> active，平台派发工作项 integrated。
4. 生命导航二负责人完成模块 preflight、current checklist、考试100、receipt 后进入 P0/P1。
