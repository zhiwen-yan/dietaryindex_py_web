import { Suspense } from "react";

import { CalculatorWorkbench } from "@/components/calculator-workbench";

export default function CalculatorPage() {
  return <Suspense fallback={<div className="content-page"><div className="notice">正在加载计算工作台…</div></div>}><CalculatorWorkbench /></Suspense>;
}
