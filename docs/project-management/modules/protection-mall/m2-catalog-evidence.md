# 保障商城 M2 目录领域核接管收口证据

## R3 结论

`R3 independent acceptance Go / awaiting controlled integration`。后端候选 `22073cd8ddeff48a4f679ffcd41a2686d8ea3ba5` 相对基线 `7745174024c2b80403ddfebcf29cd1b563eef6d7` 只修改获准的 `catalog_m2.go` 与 `catalog_m2_test.go`，工作树干净；APP Evidence 精确候选为 `673447d7df28fdcb8db75bd837cf9519f496d7df`。

前序 Evidence 提交 `f332c7e45bc09b520505f5c4a509c567e16f2ffa` 仅通过结构性校验，未精确映射后端已冻结的 scope、错误码、权益和所有者语义。R2 虽补齐语义，但治理考试仅 75 分；失败试卷保持不可变。本 R3 重新完成 29/29 current checklist 与 100 分考试后接管收口。

## 已验证范围

- 商品、服务、课程、活动四类统一目录和场景馆聚合。
- 责任主体完整性、卖家资源归属、跨卖家权限、可信 scope 来源，以及俱乐部商城保障权益失败关闭。
- 价格与权益快照首次保存后不可变，返回值与计划快照不共享可变引用。
- 会员方案组合、替换、预算、币种、整数溢出与计划所有者校验；`catalog:plan:any` 代办不会改变原方案 OwnerID。
- 内存 repository 并发读写竞态验证。
- 商品必须映射 physical，服务、课程、活动必须映射 service；目录项必含 `contract_version` 和 `title`。
- `protection_mall` 目录快照可以带保障权益，但实际授予仍严格等待 M1 的 `order_completed && after_sale_closed`；`club_mall` 目录保障权益一律以 `MALL_BENEFIT_FORBIDDEN` 失败关闭。

## 实施侧验证

- `go test ./plugins/mall-plugin -run M2Catalog -count=1`：通过。
- `go test -race ./plugins/mall-plugin -run M2Catalog -count=1`：通过。
- `go test ./...`：通过。
- `go vet ./...`：通过。
- `gofmt -d`、`git diff --check`：通过。
- `validate_catalog_contracts.py`：Schema、12 个稳定错误码和 18 个具名合成 fixture 均逐项断言，涵盖不可信 scope、类型映射、跨卖家、权益、快照、预算、币种、溢出、重复、替换、所有者和并发。
- R3 checklist：29/29 current；R3 exam attempt 1：100 分。

## 独立验收记录

- reviewer role：`APP总架构独立验收负责人`。
- reviewed at：`2026-07-15T23:18:15+08:00`。
- verdict：后端 exact `22073cd8ddeff48a4f679ffcd41a2686d8ea3ba5` 为 Go；APP Evidence exact `673447d7df28fdcb8db75bd837cf9519f496d7df` 为 Go。
- 来源与隔离：后端从 Git object 导出 exact `backend-go` 快照验收，未采用已经前进的工作树 HEAD；相对登记基线只包含获准的两个 Catalog 文件。APP Evidence 工作树在验收时 HEAD exact、clean，其自身提交相对 parent 的 12 个路径全部位于 row112 授权范围。
- 后端亲跑门禁：Catalog 定向 9 项通过；`go test ./...`、Catalog race、`go vet ./...`、`gofmt -d`、`git diff --check`、scope 与 secret scan 均通过。
- APP 亲跑门禁：Catalog 合同验证通过，包含 1 个版本化合同、12 个稳定错误码与 18 个精确合成案例；Service Plaza 总合同、registry、checklist、exam、IR、Handoff、1328 文件编码、development preflight 与 secret scan 均通过。
- R3 身份语义：可信 scope 来源失败关闭；ActorID、SellerID、FulfillmentOwnerID、AfterSaleOwnerID 与 plan OwnerID 分离；跨卖家授权独立；`catalog:plan:any` 代办不改变原 plan OwnerID；快照保持不可变。
- 治理证据：R3 current checklist 29/29、exam attempt 1 为 100 分；R2 的 75 分失败试卷保持不可变。

## 最新权威兼容根因收口

- 症状：把已验候选的最终 Mall 文件集移植到 `63cee3331215970fdd437465a4bacedf28700b08` 后，Service Plaza 总门禁拒绝 `IR-20260713-PROTECTION-MALL-M2-CATALOG-R2`，原因是它没有绑定同 record_id 的 100 分试卷。
- 因果链：R2 考试只有 75 分，因此不能形成可进入权威的实施记录；若仍把 R2 superseded IR 留在模块 implementation-records 目录，当前跨记录门禁必然失败。最早可控原因是集成包错误携带了这份失败阶段 IR，而不是合同实现或校验器故障。
- 系统修复：权威集成包保留 R2 checklist 与 75 分失败试卷作为不可变历史证据，排除 R2 IR；R3 IR 直接引用失败试卷，并继续以 R3 checklist 29/29、考试 100 分和 exact 验收为唯一实施闭环。
- 影响：只影响 APP 证据的权威调和，不改变后端 `22073cd8...`、合同语义、registry、生命周期、数据库、路由、支付、真实数据或部署边界。
- 预防门禁：任何 module implementation-record 进入权威前必须通过当前 `validate_implementation_records.py --include-module-records`；失败考试可以保留，但不得伪装成可集成实施记录。

本 Go 只绑定上述两个 exact SHA，表示可进入后续受控集成，不表示已经集成，也不授权生命周期或 registry 写入。

## No-Go

未挂路由、未连接数据库或网络、未触碰支付/退款/对账/回调、真实资金、真实会员或商家数据、短信、生产 Nova、部署和上线。本 Go 不授权上述范围，也不授权 lifecycle、registry transaction 或 B 激活；上述范围必须另立工作项并独立验收。
