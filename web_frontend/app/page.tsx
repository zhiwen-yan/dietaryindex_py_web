"use client";

import Link from "next/link";

import { HomeFiiSpotlight, HomeFoodGallery } from "@/components/home-fii-sections";
import { IndexExplorer } from "@/components/index-explorer";
import { useLanguage } from "@/components/language-context";

export default function HomePage() {
  const { isEnglish } = useLanguage();
  const steps = isEnglish
    ? [["1", "Select Index", "Choose a dietary index from the sidebar"], ["2", "Upload Data", "Select a mode and upload raw or prepared files"], ["3", "Compute & Export", "Map variables, run scoring, and export results"]]
    : [["1", "选择指标", "从侧边栏进入对应膳食指数"], ["2", "上传数据", "选择模式并上传原始或整理文件"], ["3", "计算与导出", "映射变量、运行评分并导出结果"]];
  const uploadModes = isEnglish
    ? [["🧾", "General", "CSV / Excel", "Manual column mapping"], ["📦", "NHANES FPED", "2005+", ".sas7bdat + .XPT"], ["📦", "NHANES MPED", "1999–2004", "equiv.txt + .XPT"], ["📁", "ASA24", "Totals.csv", "Automatic aggregation"], ["📝", "DHQ3 / BLOCK", "FFQ raw data", "One-step computation"]]
    : [["🧾", "通用模式", "CSV / Excel", "手动列名映射"], ["📦", "NHANES FPED", "2005 年后", ".sas7bdat + .XPT"], ["📦", "NHANES MPED", "1999–2004", "equiv.txt + .XPT"], ["📁", "ASA24", "Totals.csv", "系统自动汇总"], ["📝", "DHQ3 / BLOCK", "FFQ 原始数据", "一步式计算"]];
  return (
    <div className="site-page">
      <section className="hero-banner">
        <h1>{isEnglish ? "Dietary Index Calculation Platform" : "膳食指数计算平台"}</h1>
        <div className="hero-subtitle">DietaryIndex</div>
        <div className="hero-tagline"><p>{isEnglish ? "A unified workspace for dietary scoring, NHANES / ASA24 / FFQ uploads, and FII food lookup." : "一个整合膳食指数计算、NHANES / ASA24 / FFQ 上传流程与 FII 食物检索的统一平台。"}</p><p>{isEnglish ? "Currently includes 22 pages covering core indices, family pages, and the FII database." : "当前已整合 22 个页面，覆盖核心指数、专题家族页和 FII 数据库。"}</p></div>
      </section>

      <HomeFiiSpotlight />

      <section className="section-card">
        <div className="section-title">🧩 {isEnglish ? "API / Codex Access" : "API / Codex 接入"}</div>
        <p>{isEnglish ? "FastAPI provides index metadata, file previews, mapping suggestions, compute jobs, downloads, and FII lookup." : "平台通过 FastAPI 提供指标元数据、文件预览、映射建议、计算任务、结果下载与 FII 检索。"}</p>
        <div className="info-box compact"><p>{isEnglish ? "Next.js handles interaction; all calculations continue to use the dietaryindex Python engine." : "Next.js 只负责页面交互；所有计算继续调用同一套 dietaryindex Python 内核。"}</p></div>
        <Link className="tool-cta" href="/calculator">{isEnglish ? "Open Compute Page →" : "进入统一计算页 →"}</Link>
      </section>

      <HomeFoodGallery />
      <IndexExplorer />

      <section className="step-flow" id="usage-guide">
        {steps.map(([number, title, copy], index) => (
          <div className="step-flow-fragment" key={number}><div className="step-item"><div className="step-number">{number}</div><div className="step-text">{title}<small>{copy}</small></div></div>{index < 2 && <div className="step-arrow">→</div>}</div>
        ))}
      </section>

      <section className="section-card">
        <div className="section-title">📛 {isEnglish ? "Supported Data Upload Modes" : "支持的数据上传模式"}</div>
        <div className="upload-mode-grid">
          {uploadModes.map(([icon, name, line1, line2]) => (
            <article key={name}><span>{icon}</span><strong>{name}</strong><small>{line1}<br />{line2}</small></article>
          ))}
        </div>
      </section>
    </div>
  );
}
