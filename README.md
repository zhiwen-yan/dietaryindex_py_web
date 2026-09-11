# DietaryIndex-Py

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://python.org)
[![License: AGPL--3.0--or--later](https://img.shields.io/badge/License-AGPL--3.0--or--later-green.svg)](LICENSE)

`dietaryindex` 是一个面向营养流行病学与膳食模式研究的 Python 项目，当前同时提供：

- Python 包
- Next.js 正式网页端
- FastAPI 接口
- CLI 命令行

它的目标不是只做“几个公式”，而是做成一个可复用的膳食指数计算平台：既适合研究者在网页里上传数据，也适合未来让外部网站、脚本、AI 工作流、Codex 或其他客户端通过 API 调用。

学术使用说明：

- 真实研究数据优先建议本地计算，不建议默认上传到公网服务器。
- 使用本项目的软件、数据库整理成果或方法实现进行科研分析时，应在论文、预印本、学位论文或报告中明确致谢并引用本项目及其关联论文。
- 当前仓库使用 `AGPL-3.0-or-later`，代码再分发或网络服务化时需要保留相应开源义务。

---

## 当前能力概览

### 已接入的核心指数

| 指数 | 英文名 | 总分 |
|---|---|---:|
| DII | Dietary Inflammatory Index | 全部45组分时理论约-13.152至+13.152 |
| HEI-2020 | Healthy Eating Index 2020 | 0-100 |
| HEI-2015 | Healthy Eating Index 2015 | 0-100 |
| AHEI | Alternative Healthy Eating Index | 0-110 |
| AHEIP | AHEI Pregnancy | 0-90 |
| DASH | DASH Diet Score | 8-40 |
| DASHI | DASH Nutrient Density Index | 0-9 |
| MED | Mediterranean Diet Score | 0-9 |
| MEDI | Mediterranean Diet Index (PREDIMED-style) | 0-11 |
| ACS2020 | American Cancer Society 2020 Index | 0-12 |
| PHDI | Planetary Health Diet Index | 0-140 |
| DI-GM | Dietary Index for Gut Microbiota | 0-14 |
| FISI | Food Inflammatory Score Index | 连续型、无固定界限 |
| PDI / hPDI / uPDI | Plant-based Diet Index family | 18-90（样本人群五分位依赖） |
| MIND | Mediterranean-DASH Intervention for Neurodegenerative Delay | 0-15 |
| DQI-I | Diet Quality Index-International | 0-100 |
| CHEI | Chinese Healthy Eating Index | 0-100 |
| DBI-07 | Diet Balance Index | DQD 0-84；另含 TS/HBS/LBS |
| GDQS | Global Diet Quality Score | 0-49 |
| WISH | World Index for Sustainability and Health | 0-130 |
| NRF9.3 | Nutrient Rich Foods Index | 默认封顶版 -300–900；另提供显式 uncapped-LIM 敏感性版本 |
| NAR | Nutrient Adequacy Ratio | 0-1 |
| MAR | Mean Adequacy Ratio | 0-100 |
| INQ | Index of Nutritional Quality | ≥0、无固定上限 |
| PRAL | Potential Renal Acid Load | 连续型、无固定界限 |
| NEAP | Net Endogenous Acid Production | 有效非负输入时≥-10.2、无固定上限 |
| EDII | Empirical Dietary Inflammatory Index（兼容键 `E_DII`） | 连续型、无固定界限 |
| CHINA-DII | China Dietary Inflammatory Index（23组分表） | 约-5.871至+5.871 |
| modified CDAI | Modified six-z Composite Dietary Antioxidant Index | 标准化和、无固定界限 |
| OBS | Oxidative Balance Score | 0-40 |

### 已支持的数据入口

完整的32个基础指数、8个显式版本和各数据入口支持情况见
[`docs/INDEX_SUPPORT_MATRIX.md`](docs/INDEX_SUPPORT_MATRIX.md)。该矩阵描述软件接口支持，
不等同于科学验证结论。

| 数据入口 | 说明 |
|---|---|
| 通用模式 | 上传 CSV / Excel，网页或服务层做字段映射 |
| NHANES FPED | 2005 年后多文件流程 |
| NHANES MPED | 1999-2004 多文件流程 |
| ASA24 | Totals.csv 自动汇总 |
| DHQ3 | 单文件快捷模式 |
| BLOCK FFQ | 单文件快捷模式 |
| FII 数据库 | USDA / FNDDS 食物级炎症潜力检索 |

---

## 你可以怎么用这个项目

### 1. 网页端用户

适合不写代码的研究者。
启动 Next.js 网站和 FastAPI 后，可以在浏览器里：

- 选择指数
- 选择上传模式
- 自动/手动映射字段
- 计算结果
- 下载结果表
- 查询 FII 数据库

### 2. Python 包用户

适合在 Notebook、分析脚本、批处理流程中调用。

### 3. API 用户

适合未来正式网站、外部前端、自动化平台、AI agent、Codex、第三方系统集成。

### 4. CLI 用户

适合本地快速批处理和服务器脚本任务。

---

## 安装

### 方式一：从本地源码安装（当前最推荐）

```bash
git clone https://github.com/zhiwen-yan/dietaryindex_py_web.git
cd dietaryindex_py
pip install -e .
```

### 方式二：安装可选能力

```bash
# NHANES / SAS / XPT 读取
pip install -e .[adapters]

# FastAPI + 上传接口
pip install -e .[api]

# 全部能力
pip install -e .[all]
```

Windows 本地一键启动入口：

- `scripts/install_local.bat`
- `scripts/start_desktop_launcher.bat`
- `scripts/start_local_api.bat`
- `scripts/start_lan_api.bat`

Windows 安装包还会自动配置 Codex MCP：安装完成后，程序会将内置的
`DietaryIndexMCP.exe` 注册为名为 `dietaryindex` 的 STDIO MCP 服务。首次安装后请
完全退出并重新打开 Codex GUI。若 Codex 当时未安装或不在 PATH 中，可稍后从开始菜单
运行“配置 DietaryIndex MCP”；注册日志位于 `%LOCALAPPDATA%\DietaryIndex\mcp-registration.log`。安装器默认只允许 MCP 读取当前用户目录，并将结果写入 `%LOCALAPPDATA%\DietaryIndex\runtime_data\mcp_results`。如数据位于其他磁盘，可用 `register_codex_mcp.ps1 -AllowedRoot 'E:\data'` 重新注册；多个目录可传入数组。

### 方式三：未来发布到 PyPI 后

下面这组命令是未来正式发布到 PyPI 后的目标用法；如果当前尚未发布，请继续使用源码安装：

```bash
pip install dietaryindex
pip install dietaryindex[api]
pip install dietaryindex[all]
```

---

## 快速开始

### Python 包：统一服务层

```python
from dietaryindex import preview_file, suggest_mapping, run_compute

preview = preview_file("data.csv")
mapping_info = suggest_mapping("HEI2020", preview["columns"])

mapping = {
    key: value["column"]
    for key, value in mapping_info["suggestions"].items()
    if value["column"]
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

### Python 包：专用模式

```python
from dietaryindex import run_compute

result = run_compute(
    index_key="PHDI",
    mode="nhanes_fped",
    file_paths={
        "fped_path": "fped_dr1tot.sas7bdat",
        "nutrient_path": "DR1TOT_H.XPT",
        "demo_path": "DEMO_H.XPT",
    },
    output_dir="results_phdi",
)
```

### CLI

```bash
dietaryindex-cli catalog
dietaryindex-cli detail --index HEI2020
dietaryindex-cli preview --input data.csv
dietaryindex-cli suggest-mapping --index HEI2020 --input data.csv
dietaryindex-cli compute --index HEI2020 --input data.csv --auto-map --output-dir results
dietaryindex-cli compute --index PHDI --mode nhanes_fped --fped-path fped_dr1tot.sas7bdat --nutrient-path DR1TOT_H.XPT --demo-path DEMO_H.XPT
```

### API

启动：

```bash
uvicorn dietaryindex_api.app:app --host 127.0.0.1 --port 8000 --reload
```

接口文档：

- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- OpenAPI: [http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json)
- Health check: [http://127.0.0.1:8000/healthz](http://127.0.0.1:8000/healthz)

---

## Web 端启动

推荐使用 Docker Compose 同时启动正式网站和 API：

```bash
docker compose up --build -d
```

默认地址：

- Next.js 正式网站: [http://127.0.0.1:3003](http://127.0.0.1:3003)
- FastAPI 文档: [http://127.0.0.1:8001/docs](http://127.0.0.1:8001/docs)

端口、API 密钥、上传大小和日志级别均可通过 `.env` 配置，参考 `.env.example`。

---

## API 能力范围

当前 API MVP 主要覆盖：

- `GET /v1/indices`
- `GET /v1/indices/{index_key}`
- `POST /v1/uploads`
- `GET /v1/uploads/{upload_id}/preview`
- `POST /v1/mapping/suggest`
- `POST /v1/mapping/validate`
- `POST /v1/compute`
- `GET /v1/jobs/{job_id}`
- `GET /v1/jobs/{job_id}/download?format=csv|xlsx`
- `GET /v1/fii/summary`
- `GET /v1/fii/search`
- `GET /v1/fii/foods/{fdcd}`

这套接口已经足够支持：

- 未来正式网页前后端分离
- 外部系统调用
- Codex / AI agent 自动上传和计算
- 本地批处理与自动报告流程

---

## FII 数据库说明

项目现在已经包含一个可检索的 FII 数据库页面，当前以美国 USDA / FNDDS 数据为基础。

适合做的事情：

- 按英文食物名称查询 apple、banana、yogurt、coffee 等食物的 FII
- 按 8 位 FDCD 编码精确查询
- 比较同类食物的相对炎症潜力
- 作为 FISI 工作流的食物级支撑层

后续可扩展方向：

- 增加中国食物成分表版本
- 增加中文食物名称、同义词和别名检索（当前版本尚不支持）
- 增加人群常见食品专题页
- 增加图形化对比和下载接口

---

## 文档

更完整的文档见：

- [接入方式说明](./docs/ACCESS_GUIDE.md)
- [学术引用说明](./docs/CITATION_GUIDE.md)
- [部署说明](./docs/DEPLOYMENT_GUIDE.md)
- [2026-09-11 计算准确性与 NHANES 配对样本审计](./docs/ACCURACY_AUDIT_2026-09-11.md)
- [发布与分发说明](./docs/RELEASE_PLAN.md)
- [正式上线前检查清单](./docs/PRELAUNCH_CHECKLIST.md)

---

## 部署建议

当前采用三层架构：

1. Next.js 正式前端
用于首页、FII 数据库、统一计算工作台和后续正式网站体验。

2. FastAPI 后端
用于指数目录、上传、映射、计算任务、结果下载和外部系统集成。

3. Python 核心计算包
作为 API、CLI、MCP 和本地研究工作流的唯一计算事实来源。

正式公网部署时建议：

- 前端：Next.js 独立容器
- 后端：FastAPI + Uvicorn，耗时任务再迁移到持久化队列
- 数据与结果目录：独立持久化卷
- 域名层：HTTPS + 反向代理

---

## 参考文献

1. Shivappa N, et al. Designing and developing a literature-derived, population-based dietary inflammatory index. *Public Health Nutrition*, 2014.
2. Krebs-Smith SM, et al. Update of the Healthy Eating Index: HEI-2015. *Journal of the Academy of Nutrition and Dietetics*, 2018.
3. Chiuve SE, et al. Alternative dietary indices both strongly predict risk of chronic disease. *Journal of Nutrition*, 2012.
4. Fung TT, et al. Adherence to a DASH-style diet and risk of coronary heart disease and stroke. *Archives of Internal Medicine*, 2008.
5. Trichopoulou A, et al. Adherence to a Mediterranean diet and survival in a Greek population. *New England Journal of Medicine*, 2003.
6. Cacau LT, et al. Development and validation of an index based on EAT-Lancet recommendations. *Journal of Nutrition*, 2021.
7. Kase BE, et al. Development and evaluation of a dietary index assessing diet-gut microbiome interactions. *Journal of Nutrition*, 2023.

---

## License

This repository is licensed under `AGPL-3.0-or-later`.

学术引用、致谢建议和待发表论文的更新方式见：

- [CITATION.cff](./CITATION.cff)
- [NOTICE](./NOTICE)
- [docs/CITATION_GUIDE.md](./docs/CITATION_GUIDE.md)

本项目建立在原始 [dietaryindex R 包](https://github.com/jamesjiadazhan/dietaryindex) 的研究思路与实现经验之上，并继续向 Python 包、网页平台、API 平台和数据库平台扩展。
