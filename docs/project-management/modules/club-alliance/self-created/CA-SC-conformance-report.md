# CA-SC P0/P1 Conformance Report

- date：2026-07-12
- verdict：Contract Handoff Ready / Platform Acceptance Pending
- seed：`HEAOTANG-CA-SC-20260712-V1`

## 覆盖

Schema 对合同和错误目录实例校验；合成矩阵覆盖精确分类、混合数据零串类、详情失败关闭、首次/重放/异载荷/并发、已有 pending、本人三状态、跨用户隔离、禁止字段与禁止能力。fixtures 仅包含虚构 ID，敏感模式扫描拒绝手机号、身份证、JWT、Bearer 和真实姓名字段。

## 验证结果

- Draft 2020-12 Schema：2/2 实例通过。
- Python conformance：15/15 通过。
- fixed seed：`HEAOTANG-CA-SC-20260712-V1`，生成器重复调用结果一致且与 committed fixture 逐字段相同。
- DTO：`intro` 通过；伪造 `description` 作为权威字段稳定失败。
- access：list/detail/join/my 全部固定为 `shared_session`；guest 不得先发 SC 业务请求。
- error：非 SC/非 active 资源使用 404 `CLUB_NOT_FOUND` 隐藏；详情/join 内部失败分别使用 500；category 使用平台权威 `CLUB_FILTER_CATEGORY_INVALID`。
- current R2 checklist：28/28，current SHA mismatch 0。
- R2 governance exam：100。

## 结论边界

本报告证明修正后的 P0/P1 合同与合成一致性；后端/前端仍须独立复核与受控集成，测试环境、发布和生产不由本报告授权。
