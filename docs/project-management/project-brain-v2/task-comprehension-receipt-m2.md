# Project Brain v2 M2 任务理解回执

我只实现离线、只读、生产关闭的 refresh engine。它只消费 M1 fact catalog、source map、privacy policy 和受控 synthetic fixtures；不读取真实经营数据，不访问网络，不持有凭据，不写源系统。

成功只能追加不可变 snapshot、audit 和 last-trusted pointer；失败只能追加失败审计与 alert，绝不覆盖最后可信快照。并发锁、幂等 run ID、超时、有限重试、输入/输出 hash、统一 UTC 和原因码必须机器验证。

允许路径为 registry 的八类。禁止 App/dashboard、公共 scripts、Project Brain v1、M1 合同改写、真实通知、部署和 production。developer、independent reviewer、approver、integration owner 保持分离；未知证据、越界或 authority 漂移立即 No-Go。
