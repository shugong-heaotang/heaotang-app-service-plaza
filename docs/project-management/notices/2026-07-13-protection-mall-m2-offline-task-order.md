# 保障商城 M2 离线内部开发包任务书

## 顺序

1. A `AIW-20260713-PROTECTION-MALL-M2-CATALOG-SOLUTION` 与伴随 Evidence 立即激活。
2. C `AIW-20260713-PROTECTION-MALL-M2-PORTS-SIMULATION` 为 planned；A 准入证据完成或平台治理容量释放后转 active，可与 A 合同阶段并行。
3. B `AIW-20260713-PROTECTION-MALL-M2-ORDER-FULFILLMENT` 为 planned；仅在 A 的目录、价格和权益快照合同受控集成后激活，并从最新后端 integration 建立干净工作树。

## A 首检查点（2–4小时）

- 统一商品、服务、课程、活动的目录条目与责任主体。
- 场景馆聚合；会员方案组合、替换和预算校验。
- 价格快照、权益快照及不可变性；责任主体失败关闭。
- 纯 Go 领域对象、内存 repository、合成 fixture；正负、权限、并发和不可变性测试。
- 后端只允许 `catalog_m2.go` 与 `catalog_m2_test.go`；APP Evidence 只允许任务登记中的合同、schema、fixture、checklist、exam、IR、Handoff路径。

## 统一 No-Go

真实数据库迁移、路由、网络、支付/退款/对账/回调、真实资金、真实会员或商家数据、短信推送、生产 Nova、部署、服务广场 lifecycle 和上线全部禁止。

## 验收

current checklist逐项全文读取、exam100；versioned contracts/schema/fixtures；Go定向及全量test、vet、race、gofmt、secret、diff、UTF-8；同record_id IR/Handoff；独立验收后受控集成。
