# CA-SC P0/P1 验收矩阵

| ID | 验收条件 | 预期 |
|---|---|---|
| SC-C00 | access | list/detail/join/my 均为 `shared_session`；guest 失败关闭且不发业务请求 |
| SC-C01 | selector | 精确 `standard+general` |
| SC-C02 | 混合列表 | charity/health/trade/family/direct 零串类 |
| SC-C03 | 列表分页 | 过滤后计算 total/items，默认 1/20、size<=100 |
| SC-C04 | 详情边界 | 非 active/standard/general 与不存在资源统一 404 `CLUB_NOT_FOUND`；内部读取故障 500 `CLUB_DETAIL_UNAVAILABLE` |
| SC-C05 | DTO | 使用 `intro`，拒绝 `description`；敏感内部字段不出现 |
| SC-C06 | join 首次 | 201 且单一 pending |
| SC-C07 | join 重放 | 同键同载荷 200 + replay header |
| SC-C08 | join 冲突 | 同键异载荷 409 |
| SC-C09 | 并发 | 最终至多一个 pending |
| SC-C10 | 本人状态 | pending/approved/rejected，ID 倒序 |
| SC-C11 | 跨用户 | A/B 零泄漏，query user_id 无效 |
| SC-C12 | 禁止范围 | create/review/member/payment 等不可达 |
| SC-C13 | 合成安全 | 固定 seed、无真实 PII/凭据/生产数据 |
| SC-C14 | 治理 | checklist/exam/IR/Handoff/current SHA 全通过 |
| SC-C15 | 错误一致性 | category 使用权威 `CLUB_FILTER_CATEGORY_INVALID`；join 内部故障 500 `CLUB_JOIN_UNAVAILABLE` |
| SC-C16 | fixture replay | 固定 seed 生成器输出与 committed `cases.v1.json` 逐字段完全一致 |

任何 Blocker 或未接受 Major 均为 No-Go。P0/P1 Go 只允许后端下一切片，不代表环境、发布或完整业务 Go。
