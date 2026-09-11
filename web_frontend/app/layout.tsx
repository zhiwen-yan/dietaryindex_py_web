import type { Metadata } from "next";
import { Suspense, type ReactNode } from "react";

import { LanguageProvider } from "@/components/language-context";
import { SiteFooter } from "@/components/site-footer";
import { SiteHeader } from "@/components/site-header";
import { SiteSidebar } from "@/components/site-sidebar";
import "./globals.css";

export const metadata: Metadata = {
  title: "DietaryIndex | Evidence-based Dietary Scoring Platform",
  description: "A unified platform for dietary index calculation, FII food lookup, and research data processing.",
};

export default function RootLayout({ children }: Readonly<{ children: ReactNode }>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body suppressHydrationWarning>
        <LanguageProvider>
          <div className="page-frame">
            <Suspense fallback={null}><SiteSidebar /></Suspense>
            <div className="app-content">
              <SiteHeader />
              <main>{children}</main>
              <SiteFooter />
            </div>
          </div>
        </LanguageProvider>
      </body>
    </html>
  );
}
