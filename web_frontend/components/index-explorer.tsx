"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";

import { apiFetch } from "@/lib/api";
import { useLanguage } from "@/components/language-context";
import type { CatalogResponse, IndexCatalogItem } from "@/lib/types";

type CardConfig = { key: string; name: string; icon: string; score?: string; href?: string };

const FEATURED: CardConfig[] = [
  { key: "DII", name: "DII", icon: "🔥" },
  { key: "HEI2020", name: "HEI-2020", icon: "📊" },
  { key: "AHEI", name: "AHEI", icon: "💜" },
  { key: "DASH", name: "DASH", icon: "💚" },
];

const PAGE_CARDS: CardConfig[] = [
  { key: "DII", name: "DII", icon: "🔥" },
  { key: "FISI", name: "FII / FISI", icon: "🧪" },
  { key: "FII_DATABASE", name: "FII Database", icon: "🗂️", score: "lookup", href: "/fii" },
  { key: "HEI2020", name: "HEI-2020", icon: "📊" },
  { key: "HEI2015", name: "HEI-2015", icon: "📈" },
  { key: "AHEI", name: "AHEI", icon: "💜" },
  { key: "AHEIP", name: "AHEIP", icon: "🤰" },
  { key: "DASH", name: "DASH", icon: "💚" },
  { key: "DASHI", name: "DASHI", icon: "🫀" },
  { key: "ACS2020", name: "ACS2020", icon: "🎗️" },
  { key: "MED", name: "MED", icon: "🫒" },
  { key: "MEDI", name: "MEDI", icon: "🌊" },
  { key: "PDI", name: "PDI 家族", icon: "🌱" },
  { key: "PHDI", name: "PHDI", icon: "🌍" },
  { key: "MIND", name: "MIND / DQI-I", icon: "🧠" },
  { key: "CHEI", name: "CHEI / DBI / CHINA-DII", icon: "🇨🇳" },
  { key: "GDQS", name: "GDQS / WISH", icon: "🌐" },
  { key: "NRF", name: "NRF / NAR / MAR / INQ", icon: "🔬" },
  { key: "PRAL", name: "PRAL / NEAP", icon: "⚗️" },
  { key: "CDAI", name: "CDAI / OBS", icon: "🛡️" },
  { key: "E_DII", name: "E-DII", icon: "🧬" },
  { key: "DI_GM", name: "DI-GM", icon: "🦠" },
];

export function IndexExplorer() {
  const { isEnglish } = useLanguage();
  const [items, setItems] = useState<IndexCatalogItem[]>([]);
  const [status, setStatus] = useState<"loading" | "ready" | "error">("loading");

  useEffect(() => {
    apiFetch<CatalogResponse>("/v1/indices")
      .then((payload) => { setItems(payload.items); setStatus("ready"); })
      .catch(() => setStatus("error"));
  }, []);

  const byKey = useMemo(() => new Map(items.map((item) => [item.index_key, item])), [items]);

  return (
    <>
      {status === "loading" && <div className="notice">{isEnglish ? "Loading the index catalog…" : "正在读取指数目录…"}</div>}
      {status === "error" && <div className="notice error">{isEnglish ? "The API is unavailable. Check the FastAPI service." : "API 暂不可用，请检查 FastAPI 服务。"}</div>}

      <section className="section-card">
        <div className="section-title">🌟 {isEnglish ? "Featured Indices" : "核心指数"}</div>
        <div className="idx-grid-4">
          {FEATURED.map((config) => <FeaturedCard config={config} item={byKey.get(config.key)} isEnglish={isEnglish} key={config.key} />)}
        </div>
      </section>

      <section className="section-card">
        <div className="section-title">🌿 {isEnglish ? "Plant-based Spotlight" : "植物性膳食专题"}</div>
        <p>{isEnglish ? "Use PDI / hPDI / uPDI for within-sample rankings; use PHDI for alignment with planetary-health targets." : "如果关注样本内部排序与比较，使用 PDI / hPDI / uPDI；如果关注行星健康目标一致性，使用 PHDI。"}</p>
        <div className="info-box compact"><p>{isEnglish ? "The PDI family uses sample-relative rankings; PHDI uses fixed targets aligned with EAT-Lancet." : "PDI 家族属于样本内相对排序评分；PHDI 属于与 EAT-Lancet 对齐的固定目标评分框架。"}</p></div>
        <div className="idx-grid-3">
          {PAGE_CARDS.filter((card) => ["PDI", "PHDI"].includes(card.key)).map((config) => <HorizontalCard config={config} item={byKey.get(config.key)} isEnglish={isEnglish} key={config.key} />)}
        </div>
      </section>

      <section className="section-card">
        <div className="section-title">📚 {isEnglish ? `All ${PAGE_CARDS.length} Pages` : `全部 ${PAGE_CARDS.length} 个页面`}</div>
        <div className="idx-grid-3">
          {PAGE_CARDS.map((config) => <HorizontalCard config={config} item={byKey.get(config.key)} isEnglish={isEnglish} key={config.key} />)}
        </div>
      </section>

      {status === "ready" && <p className="catalog-note">{isEnglish ? `FastAPI currently registers ${items.length} compute entries, organized into topic groups on this site.` : `FastAPI 当前登记 ${items.length} 个计算入口，并在本站按专题分组展示。`}</p>}
    </>
  );
}

function hrefFor(config: CardConfig) {
  return config.href ?? `/calculator?index=${encodeURIComponent(config.key)}`;
}

function scoreFor(config: CardConfig, item: IndexCatalogItem | undefined, isEnglish: boolean) {
  if (config.score) return config.score;
  return item?.score_scale ?? (isEnglish ? "score scale unavailable" : "分值尺度未提供");
}

function FeaturedCard({ config, item, isEnglish }: { config: CardConfig; item?: IndexCatalogItem; isEnglish: boolean }) {
  return <article className="index-card-wrapper"><div className="index-card featured"><div className="card-icon">{config.icon}</div><div className="card-name">{config.name}</div><div className="card-eng">{item ? (isEnglish ? item.title_en : item.title_zh) : (isEnglish ? "Loading index information" : "正在读取指数信息")}</div><span className="card-score">{isEnglish ? "Score" : "总分"} {scoreFor(config, item, isEnglish)}</span><div className="card-desc">{item ? (isEnglish ? item.description_en : item.description_zh) : ""}</div></div><div className="card-button-wrapper"><Link className="idx-btn" href={hrefFor(config)}>{isEnglish ? `Compute ${config.name} →` : `进入 ${config.name} 计算 →`}</Link></div></article>;
}

function HorizontalCard({ config, item, isEnglish }: { config: CardConfig; item?: IndexCatalogItem; isEnglish: boolean }) {
  const special = config.key === "FII_DATABASE";
  const title = special ? (isEnglish ? "FII Food Database" : "FII 食物数据库") : item ? (isEnglish ? item.title_en : item.title_zh) : (isEnglish ? "Topic calculator" : "专题计算页");
  const description = special ? (isEnglish ? "Look up food-level FII by English food name or FDCD." : "按英文食物名称或 FDCD 检索食物级 FII。") : item ? (isEnglish ? item.description_en : item.description_zh) : (isEnglish ? "Uses the unified FastAPI compute service." : "使用统一 FastAPI 计算服务。");
  return <article className="index-card-wrapper"><div className="index-card-h"><div className="card-h-row"><div className="card-h-icon">{config.icon}</div><div className="card-h-info"><div className="card-h-name">{config.name}</div><div className="card-h-meta">{title} · {isEnglish ? "Score" : "总分"} {scoreFor(config, item, isEnglish)}</div></div></div><div className="card-h-desc">{description}</div></div><div className="card-button-wrapper"><Link className="idx-btn" href={hrefFor(config)}>{special ? (isEnglish ? "Open Database →" : "进入数据库 →") : (isEnglish ? "Open Page →" : "进入页面 →")}</Link></div></article>;
}
