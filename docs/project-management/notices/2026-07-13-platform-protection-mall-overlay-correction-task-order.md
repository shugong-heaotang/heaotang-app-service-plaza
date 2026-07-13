# 平台 Protection Mall overlay correction 任务书

本工作项属于 platform scope，治理检查单必须使用 `module_id=null`；不得借平台工作项写入商城模块证据。

工作项：`AIW-20260713-PLATFORM-PROTECTION-MALL-OVERLAY-CORRECTION`

只允许在 `governance-reading-list.v1.json` 的 `module_overlays` 增加 `protection-mall`，引用商城 README、M2 离线任务书和 `internal-dependencies.v2.json`；并在既有动态模块测试中覆盖正向 SHA、unknown/empty/missing 失败关闭及 life/club/health/activity/learning-plaza 回归。

不得修改商城 Evidence 或后端工作树。source commit 必须由未参与实现的独立 reviewer 复验后，才能由平台受控集成。
