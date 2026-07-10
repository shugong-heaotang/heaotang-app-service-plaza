# 和奥堂服务广场正式前端

本目录是服务广场正式前端工程。页面结构遵循 ADR 0001，临时状态闭环遵循 ADR 0003。

## 开发命令

```powershell
npm install
npm run dev
npm test
npm run build
npm run preview
```

## 当前路由

| 路由 | 页面 |
| --- | --- |
| `/services` | 服务广场 |
| `/services/life-navigation` | 生命导航 |
| `/services/club-alliance` | 俱乐部联盟 |
| `/services/health-manager` | 健康大管家 |

## 接口边界

当前已在 `src/infrastructure/submissionRepository.ts` 实现真实 Go API 适配器：

- 生命导航：`POST /api/v1/life-nav/records`
- 俱乐部联盟：`POST /api/v1/clubs/:id/join`
- 健康大管家：`POST /api/v1/health/consultations`

正式模式要求先通过 `/api/auth/login` 登录并在当前浏览器会话中保存 JWT。测试模式使用模拟适配器，避免自动化测试写入远程数据。

本地开发通过 Vite `/api` 代理连接测试服务器，具体配置见 `.env.example`。

禁止在前端代码、截图、测试或文档中写入真实密码、令牌或个人敏感数据。
