"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

import { apiFetch } from "@/lib/api";
import { useLanguage } from "@/components/language-context";
import type { FiiFood, FiiSummary } from "@/lib/types";

export const QUICK_FOODS = [
  { query: "apple", label: "Apple", icon: "/food-icons/apple.png" },
  { query: "banana", label: "Banana", icon: "/food-icons/banana.png" },
  { query: "yogurt", label: "Yogurt", icon: "/food-icons/yogurt.png" },
  { query: "coffee", label: "Coffee", icon: "/food-icons/coffee.png" },
  { query: "broccoli", label: "Broccoli", icon: "/food-icons/broccoli.png" },
  { query: "avocado", label: "Avocado", icon: "/food-icons/avocado.png" },
];

export function HomeFiiSpotlight() {
  const { isEnglish } = useLanguage();
  const [summary, setSummary] = useState<FiiSummary | null>(null);
  const [examples, setExamples] = useState<FiiFood[]>([]);

  useEffect(() => {
    apiFetch<FiiSummary>("/v1/fii/summary").then(setSummary).catch(() => undefined);
    Promise.all(QUICK_FOODS.slice(0, 3).map((item) => apiFetch<{ items: FiiFood[] }>(`/v1/fii/search?q=${item.query}&limit=1`)))
      .then((payloads) => setExamples(payloads.flatMap((payload) => payload.items)))
      .catch(() => undefined);
  }, []);

  return (
    <section className="section-card tool-spotlight">
      <div className="tool-spotlight-grid">
        <div className="tool-copy">
          <div className="tool-eyebrow">{isEnglish ? "New public lookup tool" : "新公开检索工具"}</div>
          <div className="tool-title">🗂️ {isEnglish ? "FII Food Database" : "FII 食物数据库"}</div>
          <div className="tool-desc">{isEnglish ? "Use English food names or 8-digit USDA/FNDDS FDCD codes to inspect food-level FII values." : "使用英文食物名称或 USDA/FNDDS 的 8 位 FDCD 编码，查看食物层级 FII 数值。"}</div>
          <div className="tool-actions"><Link className="tool-cta" href="/fii">{isEnglish ? "Open Database →" : "进入数据库 →"}</Link></div>
          <div className="tool-note">{isEnglish ? "USDA / FNDDS English data are connected; Chinese-name search is not yet available." : "当前接入 USDA / FNDDS 英文数据；中文名称检索尚未开放。"}</div>
        </div>
        <div className="tool-meta">
          <div className="tool-stat-grid">
            <div className="tool-stat"><span>{isEnglish ? "Food entries" : "食物条目"}</span><strong>{summary?.foods.toLocaleString() ?? "—"}</strong></div>
            <div className="tool-stat"><span>{isEnglish ? "Food groups" : "食物分组"}</span><strong>{summary?.groups ?? "—"}</strong></div>
            <div className="tool-stat"><span>{isEnglish ? "Anti-inflammatory" : "偏抗炎"}</span><strong>{summary?.anti.toLocaleString() ?? "—"}</strong></div>
            <div className="tool-stat"><span>{isEnglish ? "Pro-inflammatory" : "偏促炎"}</span><strong>{summary?.pro.toLocaleString() ?? "—"}</strong></div>
          </div>
          <div className="tool-preview"><div className="tool-preview-title">{isEnglish ? "Quick examples" : "快速示例"}</div><div className="food-chip-grid">
            {examples.map((item) => <div className={`food-chip ${item.direction}`} key={item.fdcd}><div className="food-chip-name">{item.food}</div><div className="food-chip-score">FII {item.fii.toFixed(3)}</div></div>)}
          </div></div>
        </div>
      </div>
    </section>
  );
}

export function HomeFoodGallery() {
  const { isEnglish } = useLanguage();
  return (
    <section className="plain-section">
      <h3>{isEnglish ? "Quick Food Lookup" : "快速食物检索"}</h3>
      <p className="caption">{isEnglish ? "Click a food card to open the FII database and run the query." : "点击食物卡片进入 FII 数据库并自动检索。"}</p>
      <div className="quick-food-grid">
        {QUICK_FOODS.map((item) => (
          <article className="quick-food-card" key={item.query}>
            <img src={item.icon} alt={item.label} />
            <strong>{item.label}</strong>
            <span>USDA / FNDDS food lookup</span>
            <Link className="site-button" href={`/fii?q=${encodeURIComponent(item.query)}`}>Search {item.label}</Link>
          </article>
        ))}
      </div>
    </section>
  );
}
