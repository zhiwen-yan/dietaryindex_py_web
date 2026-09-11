"use client";

import { FormEvent, useEffect, useState } from "react";

import { QUICK_FOODS } from "@/components/home-fii-sections";
import { useLanguage } from "@/components/language-context";
import { apiFetch, proxiedDownloadUrl } from "@/lib/api";
import type { FiiFood, FiiPeers, FiiSummary } from "@/lib/types";

const GROUP_LABELS: Record<string, string> = {
  "Supplements & Powders": "补充剂与粉剂",
  "Mixed / Prepared Foods": "混合与预制食品",
  "Oils & Fats": "油脂类",
  Beverages: "饮品",
  "Sweets & Desserts": "甜食与甜点",
  "Grains & Bakery": "谷物与烘焙",
  "Dairy & Eggs": "乳制品与蛋类",
  "Meat & Seafood": "肉类与水产",
  "Legumes, Nuts & Soy": "豆类、坚果与大豆",
  Vegetables: "蔬菜",
  Fruits: "水果",
  "Condiments & Seasonings": "调味品与香辛料",
  "Other / Uncategorized": "其他 / 未分类",
};

export default function FiiPage() {
  const { isEnglish } = useLanguage();
  const tr = (zh: string, en: string) => isEnglish ? en : zh;
  const groupLabel = (value: string) => isEnglish ? value : GROUP_LABELS[value] ?? value;
  const directionLabel = (value: string) => value === "anti" ? tr("偏抗炎", "Anti-inflammatory") : value === "pro" ? tr("偏促炎", "Pro-inflammatory") : tr("中性", "Neutral");
  const [summary, setSummary] = useState<FiiSummary | null>(null);
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<FiiFood[]>([]);
  const [selected, setSelected] = useState<FiiFood | null>(null);
  const [peers, setPeers] = useState<FiiPeers | null>(null);
  const [quickValues, setQuickValues] = useState<Record<string, FiiFood | undefined>>({});
  const [group, setGroup] = useState("");
  const [direction, setDirection] = useState("all");
  const [sortBy, setSortBy] = useState("best_match");
  const [limit, setLimit] = useState(50);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    apiFetch<FiiSummary>("/v1/fii/summary").then(setSummary).catch((err: Error) => setError(err.message));
    Promise.all(QUICK_FOODS.map((item) => apiFetch<{ items: FiiFood[] }>(`/v1/fii/search?q=${item.query}&limit=1`)))
      .then((payloads) => setQuickValues(Object.fromEntries(payloads.map((payload, index) => [QUICK_FOODS[index].query, payload.items[0]]))))
      .catch(() => undefined);
    const initialQuery = new URLSearchParams(window.location.search).get("q") ?? "";
    void search(initialQuery);
    // Initial load intentionally uses the default filter state.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    if (!selected) { setPeers(null); return; }
    apiFetch<FiiPeers>(`/v1/fii/foods/${selected.fdcd}/peers`).then(setPeers).catch(() => setPeers(null));
  }, [selected]);

  async function search(value = query) {
    const normalized = value.trim();
    if (/^\d+$/.test(normalized) && !/^\d{8}$/.test(normalized)) {
      setError(tr("FDCD 应为 8 位数字，例如 63101000。", "FDCD must contain 8 digits, for example 63101000."));
      return;
    }
    if (normalized && !/^\d{8}$/.test(normalized) && !/[a-z]/i.test(normalized)) {
      setError(tr("当前 USDA/FNDDS 数据仅支持英文食物名称或 8 位 FDCD 编码检索。", "The USDA/FNDDS dataset currently supports English food names or 8-digit FDCD codes."));
      return;
    }
    setLoading(true);
    setError("");
    try {
      const params = new URLSearchParams({ q: normalized, limit: String(limit), direction, sort_by: sortBy });
      if (group) params.set("group", group);
      const payload = await apiFetch<{ items: FiiFood[] }>(`/v1/fii/search?${params.toString()}`);
      setResults(payload.items);
      setSelected(payload.items[0] ?? null);
      setQuery(value);
      const url = new URL(window.location.href);
      if (normalized) url.searchParams.set("q", normalized); else url.searchParams.delete("q");
      window.history.replaceState({}, "", url);
    } catch (err) {
      setError(err instanceof Error ? err.message : tr("查询失败", "Search failed"));
    } finally {
      setLoading(false);
    }
  }

  function submit(event: FormEvent) { event.preventDefault(); void search(); }

  function downloadCurrentResults() {
    if (!results.length) return;
    const rows = [["FDCD", "Food", "Food Group", "FII", "FII_score", "Direction"], ...results.map((item) => [item.fdcd, item.food, item.food_group, item.fii, item.fii_score ?? "", item.direction])];
    const csv = rows.map((row) => row.map((cell) => `"${String(cell).replaceAll('"', '""')}"`).join(",")).join("\n");
    const url = URL.createObjectURL(new Blob(["\ufeff", csv], { type: "text/csv;charset=utf-8" }));
    const anchor = document.createElement("a"); anchor.href = url; anchor.download = "fii_database_search_results.csv"; anchor.click(); URL.revokeObjectURL(url);
  }

  return (
    <div className="site-page">
      <section className="hero-banner">
        <h1>🗂️ {tr("FII 食物数据库", "FII Food Database")}</h1>
        <div className="hero-subtitle">{tr("基于 USDA / FNDDS 食物条目的 FII 检索工具", "FII lookup for USDA / FNDDS food records")}</div>
        <div className="hero-tagline"><p>{tr("支持按英文食物名称或 8 位 FDCD 编码搜索、比较同类食物差异，并查看 FII/FISI 工作流使用的食物级 FII 数值。", "Search by English food name or 8-digit FDCD, compare foods in the same group, and inspect food-level FII values used by the FII/FISI workflow.")}</p></div>
      </section>

      <div className="cta-caption-row"><a className="tool-cta" href="/calculator?index=FISI">🧮 {tr("FII/FISI 计算页", "FII/FISI Calculator")}</a><p className="caption">{tr("这个页面适合查询单个食物或数据库条目；上传数据并计算总分请进入 FII/FISI 计算页。", "Use this page for individual foods and database records. To upload data and calculate scores, open the FII/FISI calculator.")}</p></div>

      <section className="metric-grid">
        <div className="metric-box"><span>{tr("食物条目", "Food records")}</span><strong>{summary?.foods.toLocaleString() ?? "—"}</strong></div>
        <div className="metric-box"><span>{tr("食物分组", "Food groups")}</span><strong>{summary?.groups ?? "—"}</strong></div>
        <div className="metric-box"><span>{tr("偏抗炎", "Anti-inflammatory")}</span><strong>{summary?.anti.toLocaleString() ?? "—"}</strong></div>
        <div className="metric-box"><span>{tr("偏促炎", "Pro-inflammatory")}</span><strong>{summary?.pro.toLocaleString() ?? "—"}</strong></div>
      </section>

      <div className="info-box"><strong>{tr("如何理解这个页面", "How to use this page")}</strong><p>{tr("FII 是基于每 100 g 食物营养组成计算得到的食物级炎症潜力分值，适合食物比较、数据库检索和 FII/FISI 支持，但不是独立临床诊断或单独健康建议。", "FII is a food-level inflammatory potential score derived from nutrient composition per 100 g. It supports food comparison and FII/FISI workflows, but is not a standalone diagnosis or health recommendation.")}</p></div>

      <section className="plain-section">
        <h3>{tr("快速搜索", "Quick search")}</h3>
        <p className="caption">{tr("点击任一食物卡片后，会自动填入搜索框，并立即刷新下方结果。", "Click a food card to populate the search box and refresh the results immediately.")}</p>
        <form className="site-search-form" onSubmit={submit}><label><span>{tr("搜索英文食物名称或 FDCD 编码", "Search an English food name or FDCD")}</span><input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Apple, raw / Banana, raw / Yogurt, plain / 63101000" /></label><button className="primary-button" disabled={loading}>{loading ? tr("查询中…", "Searching…") : tr("查询", "Search")}</button></form>
        <p className="caption">{tr("示例：Apple, raw / Banana, raw / Yogurt, plain / coffee / broccoli。当前不支持中文名称检索。", "Examples: Apple, raw / Banana, raw / Yogurt, plain / coffee / broccoli. Chinese-name search is not currently supported.")}</p>
        <div className="quick-food-grid">
          {QUICK_FOODS.map((item) => { const value = quickValues[item.query]; return <article className="quick-food-card" key={item.query}><img src={item.icon} alt={item.label} /><strong>{item.query}</strong><span>{value ? `FII ${value.fii.toFixed(3)} · ${groupLabel(value.food_group)}` : tr("正在读取…", "Loading…")}</span><button className="site-button" type="button" onClick={() => void search(item.query)}>{tr("查询", "Search")} {item.query}</button></article>; })}
        </div>
      </section>

      {error && <div className="notice error">{error}</div>}

      <section className="database-layout">
        <div className="database-main">
          <h3>{query.trim() ? tr("搜索结果", "Search results") : tr("浏览数据库", "Browse database")}</h3>
          <p className="caption">{tr(`当前显示 ${results.length} 条结果`, `Showing ${results.length} results`)}</p>
          {results.length ? <div className="data-table-wrap"><table><thead><tr><th>{tr("食物名称", "Food")}</th><th>{tr("食物分组", "Food group")}</th><th>FDCD</th><th>FII</th><th>FII_score</th><th>{tr("方向", "Direction")}</th></tr></thead><tbody>{results.map((item) => <tr className={selected?.fdcd === item.fdcd ? "selected-row" : ""} key={item.fdcd} onClick={() => setSelected(item)}><td>{item.food}</td><td>{groupLabel(item.food_group)}</td><td>{item.fdcd}</td><td>{item.fii.toFixed(4)}</td><td>{item.fii_score?.toFixed(2) ?? "—"}</td><td>{directionLabel(item.direction)}</td></tr>)}</tbody></table></div> : <div className="notice">{tr("当前搜索词或筛选条件下没有匹配到食物。", "No foods match the current query and filters.")}</div>}
          <button className="secondary-button result-download" onClick={downloadCurrentResults} disabled={!results.length}>{tr("下载当前结果", "Download current results")}</button>

          {selected && <section className="food-detail-section"><hr /><h3>{tr("食物详情", "Food details")}</h3><div className="metric-grid detail-metrics"><div className="metric-box"><span>FII</span><strong>{selected.fii.toFixed(4)}</strong></div><div className="metric-box"><span>FII_score</span><strong>{selected.fii_score?.toFixed(2) ?? "—"}</strong></div><div className="metric-box"><span>{tr("食物分组", "Food group")}</span><strong>{groupLabel(selected.food_group)}</strong></div><div className="metric-box"><span>{tr("方向", "Direction")}</span><strong>{directionLabel(selected.direction)}</strong></div></div><p><b>FDCD</b>: <code>{selected.fdcd}</code><br /><b>{tr("食物名称", "Food")}</b>: {selected.food}<br /><b>{tr("来源", "Source")}</b>: {selected.source}</p>{peers && <div className="peer-grid"><PeerTable title={tr("同组中更偏抗炎的食物", "More anti-inflammatory foods in this group")} items={peers.anti} isEnglish={isEnglish} /><PeerTable title={tr("同组中更偏促炎的食物", "More pro-inflammatory foods in this group")} items={peers.pro} isEnglish={isEnglish} /></div>}</section>}
        </div>

        <aside className="filter-panel">
          <h3>{tr("筛选器", "Filters")}</h3>
          <label><span>{tr("数据来源", "Data source")}</span><select disabled><option>USDA-FCT</option></select></label>
          <label><span>{tr("食物分组", "Food group")}</span><select value={group} onChange={(event) => setGroup(event.target.value)}><option value="">{tr("全部分组", "All groups")}</option>{summary?.group_names.map((item) => <option value={item} key={item}>{groupLabel(item)}</option>)}</select></label>
          <fieldset><legend>{tr("炎症方向", "Inflammatory direction")}</legend>{[["all", tr("全部", "All")], ["anti", tr("偏抗炎", "Anti-inflammatory")], ["pro", tr("偏促炎", "Pro-inflammatory")], ["neutral", tr("中性", "Neutral")]].map(([value, label]) => <label className="radio-row" key={value}><input type="radio" name="direction" value={value} checked={direction === value} onChange={(event) => setDirection(event.target.value)} />{label}</label>)}</fieldset>
          <label><span>{tr("排序方式", "Sort by")}</span><select value={sortBy} onChange={(event) => setSortBy(event.target.value)}><option value="best_match">{tr("最佳匹配", "Best match")}</option><option value="fii_asc">{tr("FII 最低优先", "Lowest FII")}</option><option value="fii_desc">{tr("FII 最高优先", "Highest FII")}</option><option value="score_desc">{tr("FII_score 最高优先", "Highest FII_score")}</option><option value="az">{tr("名称 A-Z", "Name A-Z")}</option></select></label>
          <label><span>{tr("结果条数", "Number of results")}：{limit}</span><input type="range" min="10" max="200" step="10" value={limit} onChange={(event) => setLimit(Number(event.target.value))} /></label>
          <button className="primary-button full-width" onClick={() => void search()}>{tr("应用筛选", "Apply filters")}</button>
          <a className="download-button" href={proxiedDownloadUrl("/v1/fii/export")}>{tr("下载 USDA FII 数据库 CSV", "Download USDA FII database CSV")}</a>
        </aside>
      </section>
    </div>
  );
}

function PeerTable({ title, items, isEnglish }: { title: string; items: FiiFood[]; isEnglish: boolean }) {
  return <div><h4>{title}</h4><div className="data-table-wrap"><table><thead><tr><th>{isEnglish ? "Food" : "食物名称"}</th><th>FII</th></tr></thead><tbody>{items.map((item) => <tr key={item.fdcd}><td>{item.food}</td><td>{item.fii.toFixed(4)}</td></tr>)}</tbody></table></div></div>;
}
