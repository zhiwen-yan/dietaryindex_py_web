"use client";

import { useLanguage } from "@/components/language-context";

export function SiteHeader() {
  const { isEnglish, language, setLanguage } = useLanguage();

  return (
    <header className="site-header">
      <div className="site-header-inner">
        <div className="header-platform-info">
          <a className="header-domain" href="https://dietaryindex.org" target="_blank" rel="noreferrer">dietaryindex.org</a>
          <i aria-hidden="true">·</i>
          <span>{isEnglish ? "Free computing platform for nutrition and dietary research" : "面向营养与膳食研究的免费计算平台"}</span>
          <i aria-hidden="true">·</i>
          <a className="header-contact" href="mailto:zhiwen-yan@foxmail.com">✉ zhiwen-yan@foxmail.com</a>
        </div>
        <label className="header-language">
          <span className="visually-hidden">{isEnglish ? "Language" : "语言"}</span>
          <select value={language} onChange={(event) => setLanguage(event.target.value as "zh" | "en")} aria-label={isEnglish ? "Select language" : "选择语言"}>
            <option value="zh">中文</option>
            <option value="en">English</option>
          </select>
        </label>
      </div>
    </header>
  );
}
