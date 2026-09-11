"use client";

import { useLanguage } from "@/components/language-context";

export function SiteFooter() {
  const { isEnglish } = useLanguage();

  return <footer className="app-footer">
    <span>dietaryindex v0.3.0 | Python compute engine | Next.js + FastAPI</span>
    <span className="footer-links">
      <a href="/downloads/DietaryIndexElectronSetup-0.3.0.exe">{isEnglish ? "Windows Installer" : "Windows 安装包"}</a>
      <a href="/downloads/dietaryindex-0.3.0-source.zip">{isEnglish ? "AGPL Source" : "AGPL 源码"}</a>
      <a href="/downloads/SHA256SUMS.txt">SHA-256</a>
    </span>
  </footer>;
}
