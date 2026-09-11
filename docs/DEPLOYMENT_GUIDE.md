# DietaryIndex 部署说明

## 架构

```text
Next.js 网站
      ↓ 同源代理
FastAPI
      ↓
dietaryindex 核心计算包
```

上传文件与结果保存在 `DIETARYINDEX_RUNTIME_DIR` 指定的持久化目录中。

## Docker Compose

```bash
docker compose up --build -d
```

默认地址：

- Next.js：`http://127.0.0.1:3003`
- FastAPI：`http://127.0.0.1:8001`
- Swagger：`http://127.0.0.1:8001/docs`

可在 `.env` 中配置网站端口、API 端口、API 密钥、上传大小和日志级别。

## 公网部署

- 只公开 Next.js 网站，由其服务端代理访问 FastAPI。
- 为域名启用 HTTPS。
- 设置 `DIETARYINDEX_API_KEY` 和 `DIETARYINDEX_REQUIRE_API_KEY=true`。
- 将 `runtime_data` 挂载为持久化卷，并定期清理上传与结果文件。
- 对反向代理配置请求体大小、超时、访问日志和速率限制。

## Windows 桌面版

桌面版由 Electron 启动内置 Next.js standalone 运行时与本地 FastAPI，并在沙箱渲染进程中显示界面。Electron 每次启动生成随机 API 令牌，只监听回环地址，并负责关闭其子进程。构建时运行：

```powershell
scripts\prepare_desktop_runtime.ps1
scripts\build_windows_installer.ps1
```
