# Project Brain v2 M2 G0 remediation comprehension receipt

我确认本工作项只修复 M2 runtime 的 G0/G1 privacy threshold 分支，不改变事实合同、fixture、M1、M3、registry 或任何生产能力。

正确语义是：Trusted 的 freshness、quality、authorization 均必须 pass；G0 另外要求 `sample_size is None` 与 `privacy_threshold == not_applicable`；G1 要求非 boolean 整数样本达到风险等级阈值且 `privacy_threshold == pass`。其他 classification 失败关闭。

activation 集成不等于 runtime 修复完成；开发者测试不等于独立 Go；只有 exact candidate 独立验收并受控集成后，M3 才能在新 authority 上重建整体验收。真实数据、网络、部署、timer、通知、export 与 production 继续 No-Go。
