# 服务广场接入方自检工具

接入方在提交评审前必须先运行机器校验。工具校验 UTF-8 JSON、`service-plaza.v1` Manifest、动作 Schema、重复服务 ID、分类排序位置，以及完整目录模式下的动作跨引用。

## 单个服务自检

```powershell
.\scripts\Test-ServiceIntegrationPackage.ps1 `
  -ManifestPath .\contracts\service-plaza\examples\external-partner.example.json
```

## 完整目录与动作联检

```powershell
.\scripts\Test-ServiceIntegrationPackage.ps1 `
  -ManifestPath .\path\to\service-manifests\*.json `
  -ActionsPath .\contracts\service-plaza\service-plaza-actions.v1.json `
  -CompleteCatalog
```

退出码非零即为不通过，不得通过删除字段、关闭 Schema 校验或跳过失败文件继续接入。业务 API、权限、安全与测试环境 UAT 仍需执行接入验收清单；本工具不代替业务验收。
