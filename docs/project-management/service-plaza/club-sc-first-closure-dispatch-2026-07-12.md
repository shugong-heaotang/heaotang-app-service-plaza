# CA-SC 自建俱乐部首个会员侧闭环派发报告

## Outcome

`CA-SC-P0/P1` 可以立即启动，不需要新增用户业务裁决。后端与前端实现必须等待合同 Go，并分别使用独立工作项、分支和工作树。

## Evidence

- APP authoritative base：`d186e5fc0140546e2ccab5eefe0feb99a58e5ee4`。
- backend authoritative base：`c4319c206add11f92d763b13b63be8ab2e47679e`。
- H0 Full Go、H1 M4 Go、D-CA-003 Accepted。
- 后端定向复跑 7 项通过：category search、本人申请、join 幂等和隔离。
- 前端 H1 相关 4 文件 60 tests 通过；父首页仍保持 catalog/actions only。

## Root-cause gaps

1. 通用详情按任意 ID 返回 Club，未限制 active+standard+general；SC 直接访问可能串入公益、家庭或非 active 数据。
2. 旧通用前端使用 `/api/v1/clubs` 与本地分类展示，缺少详情、分页、本人状态、稳定错误和重放模型，不能复用。
3. 历史 README、旧任务书和 Handoff 存在 D-CA-003 Pending、type-only、M3 等陈旧口径；新通知明确 supersedes，模块 P0/P1 必须同步修正权威入口。

## Work packages

- `AIW-20260712-CLUB-SC-P0-P1-CONTRACTS`：模块合同、Schema、合成 conformance 与依赖；planned，派发集成后激活。
- `AIW-20260712-CLUB-SC-FIRST-CLOSURE-BACKEND`：详情边界与必要状态 DTO；planned，Contract Go 后激活。
- `AIW-20260712-CLUB-SC-FIRST-CLOSURE-FRONTEND`：SC 专属页面与 adapter；planned，Contract/Backend Go 后激活。

## Does not block

P0/P1 合同、fixtures、错误目录和 conformance 可以立即推进；后端既有 search/join/my 能力继续作为输入。创建、审核、成员管理和资金能力不属于本目标，不影响首闭环。

## Next gate

平台派发 checklist 26/26、考试100、正式通知、IR 和 SP-H034 受控集成；随后从最终集成基线创建模块合同工作树，核验 clean/base/ownership 后转 active。

