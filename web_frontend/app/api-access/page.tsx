"use client";

import { useEffect, useState } from "react";

import { useLanguage } from "@/components/language-context";

const ENDPOINTS = [
  ["GET", "/v1/indices", "Index catalog", "指标目录"],
  ["GET", "/v1/indices/{index_key}", "Index definition", "指标定义"],
  ["POST", "/v1/uploads", "Upload and preview", "上传与预览"],
  ["GET", "/v1/uploads/{upload_id}/preview", "Uploaded-file preview", "已上传文件预览"],
  ["POST", "/v1/mapping/suggest", "Suggest column mapping", "字段映射建议"],
  ["POST", "/v1/mapping/validate", "Validate column mapping", "验证字段映射"],
  ["POST", "/v1/compute", "Submit calculation", "提交计算"],
  ["GET", "/v1/jobs/{job_id}", "Poll job status", "轮询任务状态"],
  ["GET", "/v1/fii/search?q=apple", "Search the FII database", "检索 FII 数据库"],
  ["GET", "/v1/fii/foods/{fdcd}/peers", "Compare foods in a group", "比较同组食物"],
  ["GET", "/v1/fii/export", "Export the FII database", "导出 FII 数据库"],
] as const;

export default function ApiAccessPage() {
  const { isEnglish } = useLanguage();
  const tr = (zh: string, en: string) => isEnglish ? en : zh;
  const [apiRoot, setApiRoot] = useState("http://127.0.0.1:8001");

  useEffect(() => {
    let active = true;
    fetch("/api/runtime-config", { cache: "no-store" })
      .then((response) => response.json())
      .then((config: { apiBaseUrl?: string | null }) => {
        if (active && config.apiBaseUrl) {
          setApiRoot(config.apiBaseUrl);
        } else if (active) {
          setApiRoot(`${window.location.protocol}//${window.location.hostname}:8001`);
        }
      })
      .catch(() => {
        if (active) {
          setApiRoot(`${window.location.protocol}//${window.location.hostname}:8001`);
        }
      });
    return () => {
      active = false;
    };
  }, []);

  const pythonPackage = `from dietaryindex import preview_file, suggest_mapping, run_compute

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
print(result["summary_stats"])`;

  const cliExample = `dietaryindex-cli catalog
dietaryindex-cli detail --index HEI2020
dietaryindex-cli preview --input data.csv
dietaryindex-cli suggest-mapping --index HEI2020 --input data.csv
dietaryindex-cli compute --index HEI2020 --input data.csv --auto-map --output-dir results
dietaryindex-cli compute --index DII --mode block --input block_export.csv --output-dir results`;

  const apiExample = `import requests

base = "${apiRoot}/v1"

with open("data.csv", "rb") as file:
    upload = requests.post(f"{base}/uploads", files={"file": file}).json()

mapping_info = requests.post(
    f"{base}/mapping/suggest",
    json={"index_key": "HEI2020", "columns": upload["preview"]["columns"]},
).json()

mapping = {
    key: value["column"]
    for key, value in mapping_info["suggestions"].items()
    if value["column"]
}

job = requests.post(
    f"{base}/compute",
    json={
        "index_key": "HEI2020",
        "mode": "general",
        "upload_id": upload["upload_id"],
        "mapping": mapping,
    },
).json()
print(job)`;

  const codexPrompt = isEnglish
    ? `Use the DietaryIndex API at ${apiRoot}.
1. Upload my data file.
2. Preview the columns.
3. Suggest a mapping for ACS2020.
4. Submit the calculation job.
5. Poll the job until it finishes, then summarize and download the result.`
    : `请使用 ${apiRoot} 的 DietaryIndex API。
1. 上传我的数据文件。
2. 预览列名。
3. 为 ACS2020 生成字段映射建议。
4. 提交计算任务。
5. 轮询任务直到完成，然后总结并下载结果。`;

  const specialModeExample = `from dietaryindex import run_compute

result = run_compute(
    index_key="PHDI",
    mode="nhanes_fped",
    file_paths={
        "fped_path": "fped_dr1tot.sas7bdat",
        "nutrient_path": "DR1TOT_H.XPT",
        "demo_path": "DEMO_H.XPT",
    },
    options={"score_version": "reconstructed"},
    output_dir="results_phdi",
)`;

  return (
    <div className="site-page api-access-page">
      <section className="hero-banner api-access-hero">
        <h1>🧩 {tr("API / Codex 接入", "API / Codex Access")}</h1>
        <div className="hero-subtitle">{tr("一次实现，网页、脚本、Codex 都能复用。", "Build once, call everywhere.")}</div>
        <div className="hero-tagline"><p>{tr("平台提供 Python 包、CLI 和 REST API 三层入口，可用于指标查询、文件预览、字段映射、分数计算、任务轮询和 FII 检索。", "The platform provides Python package, CLI, and REST API access for index lookup, file preview, mapping, computation, job polling, and FII search.")}</p></div>
      </section>

      <div className="api-action-row">
        <a className="button primary" href={`${apiRoot}/docs`} target="_blank" rel="noreferrer">{tr("打开交互式 API 文档", "Open interactive API docs")} ↗</a>
        <a className="button secondary" href={`${apiRoot}/openapi.json`} target="_blank" rel="noreferrer">{tr("查看 / 下载 OpenAPI JSON", "View / download OpenAPI JSON")} ↗</a>
        <a className="button secondary" href={`${apiRoot}/healthz`} target="_blank" rel="noreferrer">{tr("健康检查", "Health check")} ↗</a>
      </div>

      <section className="api-section-card">
        <div className="api-section-heading"><span>01</span><div><h2>{tr("当前可用能力", "Available capabilities")}</h2><p>{tr("页面给出常用入口；完整参数模型和在线调用请进入 Swagger。", "This page lists common routes. Use Swagger for complete schemas and live requests.")}</p></div></div>
        <div className="endpoint-grid">{ENDPOINTS.map(([method, path, en, zh]) => <div className="endpoint-row" key={`${method}-${path}`}><b className={`method-badge method-${method.toLowerCase()}`}>{method}</b><code>{path}</code><span>{isEnglish ? en : zh}</span></div>)}</div>
      </section>

      <section className="api-section-card">
        <div className="api-section-heading"><span>02</span><div><h2>{tr("启动与鉴权", "Run and authenticate")}</h2><p>{tr("Docker 环境已经映射到主机 8001 端口；以下命令用于直接启动开发服务。", "Docker exposes the service on host port 8001; the command below starts a development server directly.")}</p></div></div>
        <CopyCode code="uvicorn dietaryindex_api.app:app --host 127.0.0.1 --port 8000 --reload" language="bash" isEnglish={isEnglish} />
        <div className="api-path-strip"><span>Swagger <code>{apiRoot}/docs</code></span><span>OpenAPI <code>{apiRoot}/openapi.json</code></span><span>Health <code>{apiRoot}/healthz</code></span></div>
        <div className="warning-box"><strong>{tr("生产环境鉴权", "Production authentication")}</strong><p>{tr("设置 DIETARYINDEX_API_KEY 和 DIETARYINDEX_REQUIRE_API_KEY=true，之后所有 /v1 请求携带 x-api-key 请求头。", "Set DIETARYINDEX_API_KEY and DIETARYINDEX_REQUIRE_API_KEY=true, then send the x-api-key header with every /v1 request.")}</p></div>
      </section>

      <section className="api-section-card">
        <div className="api-section-heading"><span>03</span><div><h2>{tr("接入示例", "Integration examples")}</h2><p>{tr("按使用场景选择一种入口，代码可直接复制后修改。", "Choose an entry point for your workflow, then copy and adapt the example.")}</p></div></div>
        <div className="integration-grid">
          <ExampleCard title={tr("Python 包模式", "Python package")} description={tr("适合同一 Python 环境内直接计算，不经过 HTTP。", "Run calculations directly in the same Python environment without HTTP.")} code={pythonPackage} language="python" isEnglish={isEnglish} />
          <ExampleCard title={tr("CLI 模式", "CLI")} description={tr("适合终端、批处理和自动化脚本。", "Best for terminals, batch processing, and automation.")} code={cliExample} language="bash" isEnglish={isEnglish} />
          <ExampleCard title={tr("REST API（Python）", "REST API (Python)")} description={tr("适合其他网站、服务或远程任务调用。", "Use from other sites, services, or remote jobs.")} code={apiExample} language="python" isEnglish={isEnglish} />
          <ExampleCard title={tr("Codex 提示词模板", "Codex prompt template")} description={tr("把文件交给 Codex，并让它按统一 API 流程完成计算。", "Give Codex a file and ask it to follow the unified API workflow.")} code={codexPrompt} language="text" isEnglish={isEnglish} />
        </div>
      </section>

      <section className="api-section-card">
        <div className="api-section-heading"><span>04</span><div><h2>{tr("NHANES / 专用模式", "NHANES / specialized modes")}</h2><p>{tr("ASA24、DHQ3、BLOCK 使用单文件入口；NHANES 多文件流程通过 file_paths 传入文件角色。", "ASA24, DHQ3, and BLOCK use a single file; NHANES workflows pass file roles through file_paths.")}</p></div></div>
        <CopyCode code={specialModeExample} language="python" isEnglish={isEnglish} />
      </section>

      <section className="api-section-card deployment-note">
        <div className="api-section-heading"><span>05</span><div><h2>{tr("部署建议", "Deployment notes")}</h2><p>{tr("公网部署使用 Next.js 作为交互前端、FastAPI 作为稳定服务层，统一置于反向代理之后，并持久化 runtime_data/uploads 与 runtime_data/results。", "For public deployment, use Next.js as the interactive frontend and FastAPI as the stable service layer behind one reverse proxy, with persistent runtime_data/uploads and runtime_data/results.")}</p></div></div>
      </section>
    </div>
  );
}

function ExampleCard({ title, description, code, language, isEnglish }: { title: string; description: string; code: string; language: string; isEnglish: boolean }) {
  return <article className="integration-card"><h3>{title}</h3><p>{description}</p><CopyCode code={code} language={language} isEnglish={isEnglish} /></article>;
}

function CopyCode({ code, language, isEnglish }: { code: string; language: string; isEnglish: boolean }) {
  const [copied, setCopied] = useState(false);
  async function copy() {
    await navigator.clipboard.writeText(code);
    setCopied(true);
    window.setTimeout(() => setCopied(false), 1600);
  }
  return <div className="copy-code"><div className="copy-code-toolbar"><span>{language}</span><button type="button" onClick={() => void copy()}>{copied ? (isEnglish ? "Copied" : "已复制") : (isEnglish ? "Copy" : "复制")}</button></div><pre><code>{code}</code></pre></div>;
}
