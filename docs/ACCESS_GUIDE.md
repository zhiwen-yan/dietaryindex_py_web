# DietaryIndex 接入方式

项目提供六种入口，共享同一套 `dietaryindex` 核心计算实现：Python、CLI、FastAPI、Next.js Web、Electron 和 MCP。

## 1. Windows 桌面软件

适合希望在本地完成上传、映射、计算和结果下载的研究者。

开发模式先运行 `scripts\prepare_desktop_runtime.ps1`，再在 `electron_app` 中运行 `npm start`；正式用户使用 `DietaryIndexElectronSetup-0.3.0.exe` 安装。

Electron 会在本机启动 Next.js 界面与 FastAPI 计算服务，使用随机会话令牌、回环地址、沙箱渲染进程和受限导航策略。

## 2. Next.js 网页

使用 Docker Compose 同时启动网站和 API：

```bash
docker compose up --build -d
```

- 网站：`http://127.0.0.1:3003`
- API 文档：`http://127.0.0.1:8001/docs`

## 3. Python 与 CLI

```bash
pip install -e .[all]
dietaryindex-cli catalog
dietaryindex-cli detail --index HEI2020
```

Python 可通过 `preview_file`、`suggest_mapping` 和 `run_compute` 调用统一服务层。

## 4. FastAPI

```bash
uvicorn dietaryindex_api.app:app --host 127.0.0.1 --port 8000
```

核心入口包括指数目录、文件上传与预览、字段映射、计算任务、结果下载以及 FII 查询。公网部署时应开启 API 密钥、HTTPS、上传大小限制和运行目录清理策略。

## 5. Electron

Electron 只负责桌面宿主与本地服务生命周期；Next.js、FastAPI 和 Python 计算引擎与 Web 版共用。关闭窗口时，Electron 会终止它启动的本地子进程。

## 6. MCP

Windows 安装包附带 `DietaryIndexMCP.exe`，可注册为 STDIO MCP 服务供 Codex 使用。文件输入受允许根目录、单文件/总大小和文件数量限制，结果只能写入配置的输出根目录。
