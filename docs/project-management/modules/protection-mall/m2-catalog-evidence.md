# 保障商城 M2 目录领域核接管收口证据

## R3 结论

`R3 candidate / awaiting independent acceptance`。后端候选 `22073cd8ddeff48a4f679ffcd41a2686d8ea3ba5` 相对基线 `7745174024c2b80403ddfebcf29cd1b563eef6d7` 只修改获准的 `catalog_m2.go` 与 `catalog_m2_test.go`，工作树干净。

前序 Evidence 提交 `f332c7e45bc09b520505f5c4a509c567e16f2ffa` 仅通过结构性校验，未精确映射后端已冻结的 scope、错误码、权益和所有者语义。R2 虽补齐语义，但治理考试仅 75 分；失败试卷保持不可变，R2 实施记录标记为 superseded。本 R3 重新完成 29/29 current checklist 与 100 分考试后接管收口。

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

独立验收尚未给出 Go；在独立复跑通过前，本证据只代表可审候选，不代表已集成。

## No-Go

未挂路由、未连接数据库或网络、未触碰支付/退款/对账/回调、真实资金、真实会员或商家数据、短信、生产 Nova、部署和上线。上述范围必须另立工作项并独立验收。
