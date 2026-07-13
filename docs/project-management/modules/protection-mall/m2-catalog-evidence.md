# 保障商城 M2 目录领域核 Evidence R2

## 结论

`Handoff-ready / pending independent review`。原 Evidence `f332c7e45bc09b520505f5c4a509c567e16f2ffa` 仅通过结构检查，但与后端稳定 scope、错误码和权益语义存在漂移，已被 R2 取代且不得集成。后端候选仍为 `22073cd8ddeff48a4f679ffcd41a2686d8ea3ba5`。

## 已验证范围

- 商品、服务、课程、活动四类统一目录和场景馆聚合。
- 责任主体完整性、卖家资源归属、跨卖家权限与俱乐部商城保障权益失败关闭。
- 价格与权益快照首次保存后不可变，返回值与计划快照不共享可变引用。
- 会员方案使用 `catalog:plan`，方案所有者绑定可信 actor；`catalog:plan:any` 代办必须保留原所有者。
- 会员方案组合、替换、预算、币种、整数溢出与跨会员失败关闭。
- `product → physical`，`service/course/activity → service`；俱乐部商城保障权益失败关闭。
- 保障商城目录快照可描述保障权益，但实际发放仍延后至订单完成且售后关闭。
- 内存 repository 并发读写竞态验证。

## 独立验证

- `go test ./plugins/mall-plugin -run M2Catalog -count=1`：通过。
- `go test -race ./plugins/mall-plugin -run M2Catalog -count=1`：通过。
- `go test ./...`：通过。
- `go vet ./...`：通过。
- `gofmt -d`、`git diff --check`：通过。
- `validate_catalog_contracts.py`：合同/schema、完整稳定错误集合和 19 个逐项强断言合成 fixture 通过。
- R2 只修改登记的 7 条 Evidence 路径；旧 checklist/exam 保持不可变。

## No-Go

未挂路由、未连接数据库或网络、未触碰支付/退款/对账/回调、真实资金、真实会员或商家数据、短信、生产 Nova、部署和上线。上述范围必须另立工作项并独立验收。
