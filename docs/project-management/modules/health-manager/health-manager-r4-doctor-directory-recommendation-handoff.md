# 健康大管家 R4-C1 Handoff

- work_id：`AIW-20260714-HEALTH-R4-DOCTOR-DIRECTORY-RECOMMENDATION-CONTRACTS`
- record_id：`IR-20260714-HEALTH-R4-DOCTOR-DIRECTORY-RECOMMENDATION-C1`
- checkpoint：R4-C1 医生目录与受约束推荐合同和负例
- status：`handoff-ready / awaiting independent review`
- executable：`false`

## Completed

1. 冻结医生目录十四项最低字段与医生集团治理目录权威边界。
2. 冻结身份、医师资格、执业证书、执业机构、执业范围、诊疗科目、服务方式、可接诊和质量状态的默认拒绝硬门禁。
3. 冻结七段推荐顺序、线上/线下安全分流、质量治理、培训仅限同等条件并列和会员偏好不得越过安全边界。
4. 冻结推荐解释、证据引用、不确定性、人工复核、投诉/质量暂停、退出与重新进入机制。
5. 冻结商业中立和 AI 边界，禁止付费、竞价、佣金、广告改变医疗排序，禁止 AI 创建资质/标签、诊断、接诊或关闭专业/紧急风险。
6. 增加 Draft 2020-12 Schema、语义基线和 17 个可执行负例；19/19 conformance 通过。

## Verified

- current checklist 28/28、当前治理 SHA 匹配；governance exam attempt 1=100。
- `python -X utf8 -m unittest contracts.modules.health-manager.r4.conformance.test_health_r4_doctor_directory_recommendation -v`：19/19 passed。
- 需求补充 SHA-256：`fc07676f9d0ab0dbaf1a4575457e4d1a67d642d1c483187e28a5b2c64e2a9012`。
- 字节级 UTF-8 复核确认中文源文件代码点正确；一次工具输出乱码仅为显示层问题，未改写正确源文件。

## Pending

- 医疗质量：真实医生资质目录、核验责任、质量政策和退出执行。
- 隐私法律：真实身份、真实健康数据和互联网诊疗授权。
- 平台安全：共享运行时、API、数据库和环境。
- 健康馆运营：真实会员试点、公开目录展示和服务运营。
- does_not_block：R4 合成合同一致性、负例、独立验收和受控集成。

## No-Go

前后端、共享运行时、API、数据库、真实医生/身份/会员/健康数据、互联网诊疗、诊断、处方、改药、冒充医生、疗效承诺、公开医生排名、付费医疗排序、收费、支付、测试服、生产和不可逆操作均未授权。

## 下一门禁

独立 reviewer 从 exact commit 复跑 19 项 conformance、current checklist/exam、两层依赖、IR、UTF-8、diff、范围、秘密与敏感模式门禁；Go 后由平台受控集成并收口 R4，再另立 R5 工作项。
