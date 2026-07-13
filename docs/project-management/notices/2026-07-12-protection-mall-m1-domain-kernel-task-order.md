# 保障商城 M1 纯领域运行核任务书

日期：2026-07-12

后端工作项 `AIW-20260712-PROTECTION-MALL-M1-DOMAIN-BACKEND`：商城后端负责人，branch `codex/protection-mall-m1-domain-backend`，worktree `C:/Users/shugo/Documents/worktrees/heaotang-protection-mall-m1-domain-backend`，base `e41265905815082433e040412f3dd6b6b33dfede`。

APP证据工作项 `AIW-20260712-PROTECTION-MALL-M1-DOMAIN-EVIDENCE`：平台集成负责人，branch `codex/protection-mall-m1-domain-evidence`，worktree `C:/Users/shugo/Documents/worktrees/heaotang-protection-mall-m1-domain-evidence`，base `7a3f254bebe18f37a7b85163b096f37b68612900`。

唯一检查点：用Go实现未挂路由的纯领域核，包括责任主体校验、库存/订单/履约/售后/权益回滚状态机、scope与资源归属判断、Idempotency-Key判定和稳定错误码。只允许内存合成状态与单元测试；覆盖M1原11项案例及并发同键、同键异载荷、乱序事件、重复补偿、补偿失败关闭、跨资源越权和无可信scope来源。

禁止路由、数据库、网络、支付、真实资金、回调、退款对账、迁移、部署、真实会员/商家数据、Nova推荐、跨模块订单和GraphRAG。

完成定义：定向及全量Go test、go vet、gofmt、并发安全审查、secret scan和diff通过；APP伴随项形成current checklist、exam100、跨仓库commit/合同映射、IR和Handoff；平台独立复核后才可集成。
