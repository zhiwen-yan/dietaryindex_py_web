"use client";

import { createContext, ReactNode, useContext, useEffect, useMemo, useState } from "react";

export type Language = "zh" | "en";

type LanguageContextValue = {
  language: Language;
  isEnglish: boolean;
  setLanguage: (language: Language) => void;
};

const LanguageContext = createContext<LanguageContextValue | null>(null);

function applyLanguageAttr(language: Language) {
  const next = language === "en" ? "en" : "zh-CN";
  if (document.documentElement.lang !== next) {
    document.documentElement.lang = next;
  }
}

export function LanguageProvider({ children }: { children: ReactNode }) {
  const [language, setLanguageState] = useState<Language>("en");

  useEffect(() => {
    const fromUrl = new URLSearchParams(window.location.search).get("lang");
    const fromStorage = window.localStorage.getItem("dietaryindex-language");
    const initial = fromUrl === "en" || fromUrl === "zh"
      ? fromUrl
      : fromStorage === "en" || fromStorage === "zh"
        ? fromStorage
        : "en";
    setLanguageState(initial);
    applyLanguageAttr(initial);
  }, []);

  function setLanguage(next: Language) {
    setLanguageState(next);
    window.localStorage.setItem("dietaryindex-language", next);
    applyLanguageAttr(next);
    const url = new URL(window.location.href);
    url.searchParams.set("lang", next);
    window.history.replaceState({}, "", url);
  }

  const value = useMemo(() => ({ language, isEnglish: language === "en", setLanguage }), [language]);
  return <LanguageContext.Provider value={value}>{children}</LanguageContext.Provider>;
}

export function useLanguage() {
  const value = useContext(LanguageContext);
  if (!value) throw new Error("useLanguage must be used inside LanguageProvider");
  return value;
}
