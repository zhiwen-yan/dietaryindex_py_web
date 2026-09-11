"use client";

import Link from "next/link";
import { usePathname, useSearchParams } from "next/navigation";
import { useEffect, useState } from "react";

import { useLanguage } from "@/components/language-context";

type NavItem = { label: string; labelEn?: string; href: string; icon?: string };
type NavGroup = { label: string; labelEn: string; items: NavItem[] };

const calculator = (index: string) => `/calculator?index=${encodeURIComponent(index)}`;

const NAV_GROUPS: NavGroup[] = [
  { label: "炎症指标", labelEn: "Inflammatory Family", items: [
    { label: "FII 数据库", labelEn: "FII Database", href: "/fii" },
    { label: "DII", href: calculator("DII") },
    { label: "FII / FISI", href: calculator("FISI") },
    { label: "E-DII", href: calculator("E_DII") },
  ] },
  { label: "HEI 系列", labelEn: "HEI Series", items: [
    { label: "HEI-2020", href: calculator("HEI2020") },
    { label: "HEI-2015", href: calculator("HEI2015") },
  ] },
  { label: "替代健康指数", labelEn: "Alternative Healthy Family", items: [
    { label: "AHEI", href: calculator("AHEI") },
    { label: "AHEIP", href: calculator("AHEIP") },
  ] },
  { label: "疾病预防指数", labelEn: "Disease Prevention Family", items: [
    { label: "DASH", href: calculator("DASH") },
    { label: "DASHI", href: calculator("DASHI") },
    { label: "ACS2020", href: calculator("ACS2020") },
  ] },
  { label: "膳食模式指数", labelEn: "Dietary Pattern Family", items: [
    { label: "MED", href: calculator("MED") },
    { label: "MEDI", href: calculator("MEDI") },
  ] },
  { label: "植物性膳食家族", labelEn: "Plant-based Family", items: [
    { label: "PDI 家族", labelEn: "PDI Family", href: calculator("PDI") },
    { label: "PHDI", href: calculator("PHDI") },
  ] },
  { label: "经典质量指数", labelEn: "Classic Quality Family", items: [
    { label: "MIND / DQI-I", href: calculator("MIND") },
  ] },
  { label: "中国本土化指数", labelEn: "China-localized Family", items: [
    { label: "CHEI / DBI / CHINA-DII", href: calculator("CHEI") },
  ] },
  { label: "可持续与全球适用", labelEn: "Sustainable and Global", items: [
    { label: "GDQS / WISH", href: calculator("GDQS") },
  ] },
  { label: "营养密度家族", labelEn: "Nutrient Density Family", items: [
    { label: "NRF / NAR / MAR / INQ", href: calculator("NRF") },
  ] },
  { label: "酸负荷家族", labelEn: "Acid Load Family", items: [
    { label: "PRAL / NEAP", href: calculator("PRAL") },
  ] },
  { label: "抗氧化与氧化平衡", labelEn: "Antioxidant Balance", items: [
    { label: "CDAI / OBS", href: calculator("CDAI") },
  ] },
  { label: "新兴指数", labelEn: "Emerging Indices", items: [
    { label: "DI-GM", href: calculator("DI_GM") },
  ] },
];

export function SiteSidebar() {
  const pathname = usePathname();
  const searchParams = useSearchParams();
  const currentIndex = searchParams.get("index");
  const { isEnglish } = useLanguage();
  const [open, setOpen] = useState(false);

  useEffect(() => {
    setOpen(false);
  }, [pathname]);

  return (
    <>
      <button className="sidebar-toggle" type="button" onClick={() => setOpen((value) => !value)} aria-label={isEnglish ? "Toggle navigation" : "切换导航"}>☰</button>
      {open && <button className="sidebar-backdrop" type="button" aria-label={isEnglish ? "Close navigation" : "关闭导航"} onClick={() => setOpen(false)} />}
      <aside className={`app-sidebar ${open ? "is-open" : ""}`}>
        <div className="sidebar-scroll">
          <Link href="/" className="sidebar-brand"><span className="brand-icon">🥗</span><span className="brand-text">DietaryIndex</span></Link>
          <div className="sidebar-subtitle">{isEnglish ? "Dietary Index Platform" : "膳食指数计算平台"}</div>
          <hr />
          <Link className={`sidebar-link home-link ${pathname === "/" ? "active" : ""}`} href="/"><span>🏠</span>{isEnglish ? "Home" : "首页"}</Link>
          {NAV_GROUPS.map((group) => (
            <nav className="sidebar-group" key={group.label} aria-label={isEnglish ? group.labelEn : group.label}>
              <div className="sidebar-cat-label">{isEnglish ? group.labelEn : group.label}</div>
              {group.items.map((item) => (
                <Link className={`sidebar-link ${isActiveNavItem(item.href, pathname, currentIndex) ? "active" : ""}`} href={item.href} key={`${group.label}-${item.label}`}>{isEnglish ? item.labelEn ?? item.label : item.label}</Link>
              ))}
            </nav>
          ))}
          <hr />
          <Link className={`sidebar-link ${pathname === "/api-access" ? "active" : ""}`} href="/api-access"><span>🧩</span>{isEnglish ? "API / Codex Access" : "API / Codex 接入"}</Link>
          <Link className="sidebar-link" href="/#usage-guide"><span>📘</span>{isEnglish ? "User Guide" : "使用指南"}</Link>
          <div className="sidebar-version">dietaryindex v0.3.0 · Next.js + FastAPI</div>
        </div>
      </aside>
    </>
  );
}

function isActiveNavItem(href: string, pathname: string, currentIndex: string | null) {
  if (!href.startsWith("/calculator?")) return href === pathname;
  const expectedIndex = new URLSearchParams(href.split("?")[1]).get("index");
  return pathname === "/calculator" && expectedIndex === currentIndex;
}
