# CA-SC T0 测试环境验收计划

- work item：`AIW-20260712-CLUB-SC-T0-ACCEPTANCE`
- record：`IR-20260712-CLUB-SC-T0-ACCEPTANCE-R2`
- APP source：`2c4b295e6fd625a2df24957f7b8becbc28ad1dcf`（包含权威 activation `4bb430a`）
- backend source：`a998812cf44dc449d85b726706d4ae2573179860`
- environment：`https://heaotang.cn`
- fixture seed：`HEAOTANG-CA-SC-20260712-V1`

## 执行顺序

1. 本地定向测试、测试服构建、合同与静态安全门禁。
2. 记录部署前 health/ready、制品 SHA 和目标版本。
3. 使用既有备份脚本备份测试数据库、二进制、启动文件和前端制品。
4. 部署 backend integration 和 APP 测试服构建，验证 health/ready/catalog/actions。
5. Apply 固定 seed 合成 fixture；只写入两个合成用户和 10 个带固定 code 的合成俱乐部。
6. 真实 HTTP 验证权威筛选、详情、幂等、并发和跨用户隔离。
7. 浏览器验证首页进入、列表/详情/本人状态、直达/刷新/后退/返回、响应式和可访问性。
8. 核对 Nginx/API/DB 脱敏证据与 denylist 零请求。
9. 清理当前 fixture，验证恢复和模拟回滚；形成最终 Go/No-Go。

任何 Blocker/Major 立即停止下游，保存证据并关闭根因；不得通过改验收口径、直接改 DB 业务结果或跳过认证换取通过。
