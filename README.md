# DietaryIndex-Py

[![Version](https://img.shields.io/badge/version-0.3.0-blue)](https://github.com/zhiwen-yan/dietaryindex_py_web/releases)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://python.org)
[![License: AGPL--3.0--or--later](https://img.shields.io/badge/License-AGPL--3.0--or--later-green.svg)](LICENSE)

**English** | [中文](#chinese)

DietaryIndex-Py is a reusable dietary-index calculation platform for nutritional epidemiology and dietary-pattern research. Version 0.3.0 provides a Python package, command-line interface, FastAPI service, production Next.js website, Windows desktop application, and a seven-tool MCP server for Codex-compatible workflows.

- Website: [dietaryindex.org](https://dietaryindex.org)
- Windows installer: [DietaryIndexElectronSetup-0.3.0.exe](https://dietaryindex.org/downloads/DietaryIndexElectronSetup-0.3.0.exe)
- AGPL source archive: [dietaryindex-0.3.0-source.zip](https://dietaryindex.org/downloads/dietaryindex-0.3.0-source.zip)
- Checksums: [SHA256SUMS.txt](https://dietaryindex.org/downloads/SHA256SUMS.txt)

The website and desktop application open in English by default and can be switched to Chinese. A saved language preference or an explicit `?lang=en` / `?lang=zh` query takes precedence.

## Scientific-use notes

- Prefer local computation for real research datasets; do not upload sensitive data to a public service by default.
- When this software, its curated databases, or its methodological implementation contributes to research, acknowledge and cite the project and the relevant original methods.
- The repository is licensed under `AGPL-3.0-or-later`. Redistribution and network-hosted modified versions must comply with the corresponding source-disclosure obligations.
- The support matrix describes software interfaces, not independent scientific validation. See the accuracy audit and original publications before drawing research conclusions.

## What is included

- **40 calculator entries:** 32 base indices plus eight explicit input variants.
- **Input workflows:** general CSV/Excel mapping, NHANES FPED, NHANES MPED, ASA24, DHQ3, and Block FFQ.
- **FII database:** searchable USDA/FNDDS food-level inflammatory-potential data.
- **One calculation core:** shared by Python, CLI, API, desktop, and MCP interfaces.
- **Local-first desktop:** Electron UI with a bundled FastAPI sidecar and Next.js standalone runtime.
- **Codex MCP:** seven tools with configurable input-root, file-size, total-input, structured-payload, and output-root limits.

The 32 base indices include DII, HEI-2020, HEI-2015, AHEI, AHEI-P, DASH, DASHI, MED, MEDI, ACS2020, PHDI, DI-GM, FISI, PDI, hPDI, uPDI, MIND, DQI-I, CHEI, DBI-07, GDQS, WISH, NRF9.3, NAR, MAR, INQ, PRAL, NEAP, EDII, CHINA-DII, modified CDAI, and OBS. See the [index and input-mode support matrix](docs/INDEX_SUPPORT_MATRIX.md) for score ranges, exact keys, eight versioned variants, and mode coverage.

## Installation

### From source

```bash
git clone https://github.com/zhiwen-yan/dietaryindex_py_web.git
cd dietaryindex_py_web
python -m pip install -e .
```

Optional dependency groups:

```bash
# NHANES/SAS/XPT adapters
python -m pip install -e ".[adapters]"

# FastAPI, uploads, and spreadsheet support
python -m pip install -e ".[api]"

# API, adapters, spreadsheet support, and MCP
python -m pip install -e ".[all]"
```

The package has not been documented here as a published PyPI release. Until a release is confirmed on PyPI, install it from source rather than assuming `pip install dietaryindex` provides version 0.3.0.

### Windows desktop application

Download and run the [0.3.0 Windows installer](https://dietaryindex.org/downloads/DietaryIndexElectronSetup-0.3.0.exe). The current public installer is unsigned, so Windows SmartScreen may show an unknown-publisher warning; verify the SHA-256 checksum before installation.

The installer includes `DietaryIndexMCP.exe` and attempts to register it as the `dietaryindex` STDIO MCP service when Codex CLI is available. Restart Codex after the first installation. Registration logs are written to `%LOCALAPPDATA%\DietaryIndex\mcp-registration.log`.

By default, MCP input is restricted to the current user's profile and results are restricted to `%LOCALAPPDATA%\DietaryIndex\runtime_data\mcp_results`. To allow another data directory, run the installed `register_codex_mcp.ps1` script again, for example:

```powershell
.\register_codex_mcp.ps1 -AllowedRoot 'E:\research-data'
```

Uninstalling the application removes its MCP registration. Source-tree Windows helpers are available under `scripts/`, including `install_local.bat`, `start_desktop_launcher.bat`, `start_local_api.bat`, and `start_lan_api.bat`.

## Quick start

### Python service layer

```python
from dietaryindex import preview_file, run_compute, suggest_mapping

preview = preview_file("data.csv")
mapping_info = suggest_mapping("HEI2020", preview["columns"])
mapping = {
    key: suggestion["column"]
    for key, suggestion in mapping_info["suggestions"].items()
    if suggestion["column"]
}

result = run_compute(
    index_key="HEI2020",
    mode="general",
    file_path="data.csv",
    mapping=mapping,
    output_dir="results",
)
print(result["summary_stats"])
```

### CLI

```bash
dietaryindex-cli catalog
dietaryindex-cli detail --index HEI2020
dietaryindex-cli preview --input data.csv
dietaryindex-cli suggest-mapping --index HEI2020 --input data.csv
dietaryindex-cli compute --index HEI2020 --input data.csv --auto-map --output-dir results
```

### Local API

```bash
uvicorn dietaryindex_api.app:app --host 127.0.0.1 --port 8000 --reload
```

- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- OpenAPI: [http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json)
- Health check: [http://127.0.0.1:8000/healthz](http://127.0.0.1:8000/healthz)

## Docker deployment

For local development, Docker Compose builds both the Next.js site and FastAPI service:

```bash
docker compose up --build -d
```

The default local ports are `http://127.0.0.1:3003` for the site and `http://127.0.0.1:8001/docs` for API documentation. The development Compose file exposes only the site to the LAN; the API remains bound to loopback.

Production uses `docker-compose.production.yml`, immutable 0.3.0 image tags, loopback-only bindings for both services, persistent runtime data, and a required API key supplied through a protected `.env` file:

```bash
docker compose --env-file .env -f docker-compose.production.yml up -d
```

Do not commit production API keys. Refer to [.env.example](.env.example) and the [deployment guide](docs/DEPLOYMENT_GUIDE.md).

## API and MCP surfaces

The FastAPI service provides:

- index catalog and metadata: `GET /v1/indices`, `GET /v1/indices/{index_key}`
- uploads and preview: `POST /v1/uploads`, `GET /v1/uploads/{upload_id}/preview`
- mapping: `POST /v1/mapping/suggest`, `POST /v1/mapping/validate`
- calculation and results: `POST /v1/compute`, `GET /v1/jobs/{job_id}`, `GET /v1/jobs/{job_id}/download?format=csv|xlsx`
- FII data: `GET /v1/fii/summary`, `GET /v1/fii/search`, `GET /v1/fii/foods/{fdcd}`, `GET /v1/fii/foods/{fdcd}/peers`, `GET /v1/fii/export`

When `DIETARYINDEX_REQUIRE_API_KEY=true`, all `/v1` requests require a valid `x-api-key` header. `/healthz`, `/docs`, and `/openapi.json` remain available for service health and local documentation.

The MCP server exposes exactly seven tools: `list_indices`, `get_index`, `preview_dataset`, `suggest_dataset_mapping`, `compute_index`, `search_fii_foods`, and `get_fii_food`.

## Documentation

- [Access guide](docs/ACCESS_GUIDE.md)
- [Citation guide](docs/CITATION_GUIDE.md)
- [Deployment guide](docs/DEPLOYMENT_GUIDE.md)
- [Index support matrix](docs/INDEX_SUPPORT_MATRIX.md)
- [2026-09-11 accuracy and paired-NHANES audit](docs/ACCURACY_AUDIT_2026-09-11.md)
- [Release and distribution plan](docs/RELEASE_PLAN.md)
- [Pre-launch checklist](docs/PRELAUNCH_CHECKLIST.md)

## Architecture

The Next.js frontend handles the public site, FII search, and calculator. FastAPI handles metadata, uploads, mapping, calculation jobs, downloads, and integrations. The Python package is the single calculation source used by the API, CLI, MCP server, and local research workflows. The Electron application packages the frontend and API sidecar for local Windows use.

## License and attribution

This repository is licensed under `AGPL-3.0-or-later`. See [CITATION.cff](CITATION.cff), [NOTICE](NOTICE), and the [citation guide](docs/CITATION_GUIDE.md).

The project builds on the research ideas and implementation experience of the original [dietaryindex R package](https://github.com/jamesjiadazhan/dietaryindex), extending them into Python, web, API, desktop, MCP, and food-database workflows.

---

<a id="chinese"></a>

## 中文说明

[English](#dietaryindex-py) | **中文**

DietaryIndex-Py 是面向营养流行病学与膳食模式研究的可复用膳食指数计算平台。0.3.0 版提供 Python 包、命令行、FastAPI 服务、正式 Next.js 网站、Windows 桌面应用，以及可用于 Codex 工作流的 7 工具 MCP 服务。

- 正式网站：[dietaryindex.org](https://dietaryindex.org)
- Windows 安装包：[DietaryIndexElectronSetup-0.3.0.exe](https://dietaryindex.org/downloads/DietaryIndexElectronSetup-0.3.0.exe)
- AGPL 源码包：[dietaryindex-0.3.0-source.zip](https://dietaryindex.org/downloads/dietaryindex-0.3.0-source.zip)
- 校验文件：[SHA256SUMS.txt](https://dietaryindex.org/downloads/SHA256SUMS.txt)

网站和桌面应用默认显示英文，可以切换为中文；已经保存的语言偏好或明确的 `?lang=en` / `?lang=zh` 参数优先。

### 学术使用说明

- 真实研究数据优先在本地计算，不建议默认上传到公网服务。
- 使用本软件、整理后的数据库或方法实现开展研究时，应致谢并引用本项目及对应的原始方法文献。
- 仓库采用 `AGPL-3.0-or-later`；再分发或提供修改后的网络服务时，应履行相应的源码公开义务。
- 支持矩阵描述的是软件接口，不等同于独立的科学验证结论；研究解释前请同时查阅准确性审计和原始文献。

### 当前组成

- **40 个计算入口：**32 个基础指数和 8 个显式输入版本。
- **数据入口：**通用 CSV/Excel 字段映射、NHANES FPED、NHANES MPED、ASA24、DHQ3 和 Block FFQ。
- **FII 数据库：**可检索的 USDA/FNDDS 食物级炎症潜力数据。
- **统一计算核心：**Python、CLI、API、桌面端和 MCP 共用同一套计算实现。
- **本地优先桌面端：**Electron 界面，内置 FastAPI sidecar 和 Next.js standalone runtime。
- **Codex MCP：**7 个工具，并限制输入目录、单文件大小、总输入量、结构化参数和结果目录。

32 个基础指数包括 DII、HEI-2020、HEI-2015、AHEI、AHEI-P、DASH、DASHI、MED、MEDI、ACS2020、PHDI、DI-GM、FISI、PDI、hPDI、uPDI、MIND、DQI-I、CHEI、DBI-07、GDQS、WISH、NRF9.3、NAR、MAR、INQ、PRAL、NEAP、EDII、CHINA-DII、modified CDAI 和 OBS。各指数分值范围、程序键名、8 个显式版本及输入模式支持情况见[指数与输入模式支持矩阵](docs/INDEX_SUPPORT_MATRIX.md)。

### 安装

从源码安装：

```bash
git clone https://github.com/zhiwen-yan/dietaryindex_py_web.git
cd dietaryindex_py_web
python -m pip install -e .
```

可选依赖：

```bash
# NHANES/SAS/XPT 读取
python -m pip install -e ".[adapters]"

# FastAPI、上传和电子表格支持
python -m pip install -e ".[api]"

# API、适配器、电子表格和 MCP
python -m pip install -e ".[all]"
```

本说明没有把 0.3.0 标记为已经发布到 PyPI。在确认 PyPI 正式发布前，请使用源码安装，不要默认 `pip install dietaryindex` 得到的就是 0.3.0。

Windows 用户可直接下载 [0.3.0 安装包](https://dietaryindex.org/downloads/DietaryIndexElectronSetup-0.3.0.exe)。当前公开安装包未签名，Windows SmartScreen 可能提示未知发布者；安装前请核对 SHA-256。

安装包包含 `DietaryIndexMCP.exe`。检测到 Codex CLI 时，安装器会尝试将其注册为名为 `dietaryindex` 的 STDIO MCP 服务；首次安装后请完全退出并重新打开 Codex。注册日志位于 `%LOCALAPPDATA%\DietaryIndex\mcp-registration.log`。默认只允许 MCP 读取当前用户目录，结果只能写入 `%LOCALAPPDATA%\DietaryIndex\runtime_data\mcp_results`。如需增加数据目录，可在安装目录重新执行：

```powershell
.\register_codex_mcp.ps1 -AllowedRoot 'E:\research-data'
```

卸载应用时会移除 MCP 注册。源码中的 Windows 辅助入口位于 `scripts/`，包括 `install_local.bat`、`start_desktop_launcher.bat`、`start_local_api.bat` 和 `start_lan_api.bat`。

### 快速开始

Python 统一服务层：

```python
from dietaryindex import preview_file, run_compute, suggest_mapping

preview = preview_file("data.csv")
mapping_info = suggest_mapping("HEI2020", preview["columns"])
mapping = {
    key: suggestion["column"]
    for key, suggestion in mapping_info["suggestions"].items()
    if suggestion["column"]
}

result = run_compute(
    index_key="HEI2020",
    mode="general",
    file_path="data.csv",
    mapping=mapping,
    output_dir="results",
)
print(result["summary_stats"])
```

CLI：

```bash
dietaryindex-cli catalog
dietaryindex-cli detail --index HEI2020
dietaryindex-cli preview --input data.csv
dietaryindex-cli suggest-mapping --index HEI2020 --input data.csv
dietaryindex-cli compute --index HEI2020 --input data.csv --auto-map --output-dir results
```

本地 API：

```bash
uvicorn dietaryindex_api.app:app --host 127.0.0.1 --port 8000 --reload
```

- Swagger UI：[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- OpenAPI：[http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json)
- 健康检查：[http://127.0.0.1:8000/healthz](http://127.0.0.1:8000/healthz)

### Docker 部署

本地开发可用 Docker Compose 构建并启动 Next.js 网站和 FastAPI：

```bash
docker compose up --build -d
```

默认网站地址为 `http://127.0.0.1:3003`，API 文档为 `http://127.0.0.1:8001/docs`。开发 Compose 只把网站开放到局域网，API 仍只绑定本机回环地址。

生产环境使用 `docker-compose.production.yml`：固定 0.3.0 镜像标签、两个服务均只绑定回环地址、运行数据持久化，并要求通过受保护的 `.env` 提供 API 密钥。

```bash
docker compose --env-file .env -f docker-compose.production.yml up -d
```

不要提交生产 API 密钥。配置项见 [.env.example](.env.example) 和[部署说明](docs/DEPLOYMENT_GUIDE.md)。

### API 与 MCP 范围

FastAPI 当前提供：

- 指数目录：`GET /v1/indices`、`GET /v1/indices/{index_key}`
- 上传与预览：`POST /v1/uploads`、`GET /v1/uploads/{upload_id}/preview`
- 字段映射：`POST /v1/mapping/suggest`、`POST /v1/mapping/validate`
- 计算与结果：`POST /v1/compute`、`GET /v1/jobs/{job_id}`、`GET /v1/jobs/{job_id}/download?format=csv|xlsx`
- FII：`GET /v1/fii/summary`、`GET /v1/fii/search`、`GET /v1/fii/foods/{fdcd}`、`GET /v1/fii/foods/{fdcd}/peers`、`GET /v1/fii/export`

当 `DIETARYINDEX_REQUIRE_API_KEY=true` 时，所有 `/v1` 请求必须提供有效的 `x-api-key` 请求头；`/healthz`、`/docs` 和 `/openapi.json` 仍用于健康检查和本地接口说明。

MCP 服务准确提供 7 个工具：`list_indices`、`get_index`、`preview_dataset`、`suggest_dataset_mapping`、`compute_index`、`search_fii_foods` 和 `get_fii_food`。

### 文档

- [接入方式说明](docs/ACCESS_GUIDE.md)
- [学术引用说明](docs/CITATION_GUIDE.md)
- [部署说明](docs/DEPLOYMENT_GUIDE.md)
- [指数支持矩阵](docs/INDEX_SUPPORT_MATRIX.md)
- [2026-09-11 计算准确性与 NHANES 配对样本审计](docs/ACCURACY_AUDIT_2026-09-11.md)
- [发布与分发说明](docs/RELEASE_PLAN.md)
- [正式上线前检查清单](docs/PRELAUNCH_CHECKLIST.md)

### 架构

Next.js 前端负责公开网站、FII 检索和计算器；FastAPI 负责元数据、上传、映射、计算任务、结果下载和系统集成；Python 包是 API、CLI、MCP 和本地研究流程共用的唯一计算事实来源；Electron 应用把前端和 API sidecar 封装为本地 Windows 应用。

### 许可证与致谢

本仓库采用 `AGPL-3.0-or-later`。详见 [CITATION.cff](CITATION.cff)、[NOTICE](NOTICE) 和[学术引用说明](docs/CITATION_GUIDE.md)。

本项目建立在原始 [dietaryindex R 包](https://github.com/jamesjiadazhan/dietaryindex) 的研究思路与实现经验之上，并扩展到 Python、Web、API、桌面端、MCP 和食物数据库工作流。
