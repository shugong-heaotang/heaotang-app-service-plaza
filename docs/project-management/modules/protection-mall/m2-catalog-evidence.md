# 保障商城 M2 目录领域核独立验收证据

## 结论

`Go / handoff-ready`。后端候选 `22073cd8ddeff48a4f679ffcd41a2686d8ea3ba5` 相对基线 `7745174024c2b80403ddfebcf29cd1b563eef6d7` 只修改获准的 `catalog_m2.go` 与 `catalog_m2_test.go`，工作树干净。

## 已验证范围

- 商品、服务、课程、活动四类统一目录和场景馆聚合。
- 责任主体完整性、卖家资源归属、跨卖家权限与俱乐部商城保障权益失败关闭。
- 价格与权益快照首次保存后不可变，返回值与计划快照不共享可变引用。
- 会员方案组合、替换、预算、币种、整数溢出与计划所有者校验。
- 内存 repository 并发读写竞态验证。

## 独立验证

- `go test ./plugins/mall-plugin -run M2Catalog -count=1`：通过。
- `go test -race ./plugins/mall-plugin -run M2Catalog -count=1`：通过。
- `go test ./...`：通过。
- `go vet ./...`：通过。
- `gofmt -d`、`git diff --check`：通过。
- `validate_catalog_contracts.py`：合同/schema 和 10 个合成 fixture 通过。

## No-Go

未挂路由、未连接数据库或网络、未触碰支付/退款/对账/回调、真实资金、真实会员或商家数据、短信、生产 Nova、部署和上线。上述范围必须另立工作项并独立验收。
