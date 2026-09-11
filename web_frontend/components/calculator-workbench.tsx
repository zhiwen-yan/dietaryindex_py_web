"use client";

import { useEffect, useMemo, useState } from "react";
import { useSearchParams } from "next/navigation";

import { apiFetch, proxiedDownloadUrl, waitForJob } from "@/lib/api";
import { baseIndexKey, groupForIndex, versionKeysForIndex } from "@/lib/index-groups";
import { nhanesCycleOptions, nhanesFileGuide } from "@/lib/nhanes-file-guide";
import { useLanguage } from "@/components/language-context";
import type { CatalogResponse, FileSpec, IndexDetail, Job, MappingResponse, ModeDefinition, UploadResponse } from "@/lib/types";

type UploadMap = Record<string, UploadResponse>;
type CycleUpload = { id: number; label: string; files: Record<string, File | null>; uploads: UploadMap };
const DEMO_ROW_COUNT = 12;

function demoValue(name: string, unit: string | null | undefined, row: number, defaultValue: string | number | null | undefined) {
  const key = name.toLowerCase();
  const normalizedUnit = (unit ?? "").toLowerCase();
  if (key === "respondent_id") return row + 1;
  if (key === "repeat_num") return Number(defaultValue ?? 1);
  if (key === "gender" || key === "sex") return row % 2 === 0 ? 1 : 2;
  if (key === "age") return 28 + row * 3;
  if (key === "reference_energy_kcal") return Number(defaultValue ?? 2000);
  if (key.includes("total_kcal") || key === "energy" || key === "kcal" || normalizedUnit.includes("kcal/day")) return 1750 + row * 75;
  if (key === "bmi") return 20.5 + row * 0.55;
  if (key.includes("physical_activity")) return 350 + row * 125;
  if (key.includes("drinks_per_year")) return 8 + row * 8;
  if (key.includes("drinks_per_day")) return 0.2 + row * 0.12;
  if (key === "cotinine") return 0.1 + row * 0.35;
  if (normalizedUnit.includes("binary")) return row % 2;
  if (normalizedUnit.includes("ratio")) return 1.05 + row * 0.12;
  if (normalizedUnit.includes("%") || key.includes("pct") || key.includes("percent")) return 5 + row * 0.65;
  if (normalizedUnit.includes("met-min")) return 350 + row * 125;
  if (normalizedUnit.includes("mg")) {
    if (key.includes("sodium")) return 1600 + row * 85;
    if (key.includes("calcium")) return 650 + row * 35;
    if (key.includes("magnesium")) return 240 + row * 18;
    return 12 + row * 2.5;
  }
  if (normalizedUnit.includes("μg") || normalizedUnit.includes("ug") || normalizedUnit.includes("re")) return 45 + row * 7;
  if (normalizedUnit.includes("serving") || normalizedUnit.includes("cup") || normalizedUnit.includes("oz") || normalizedUnit.includes("drink") || normalizedUnit.includes("tsp") || normalizedUnit.includes("tbsp") || normalizedUnit.includes("sp/")) return 0.35 + row * 0.16;
  if (normalizedUnit === "g" || normalizedUnit.includes("g/day") || normalizedUnit.includes("g/1000") || normalizedUnit.includes("g/2000")) return 8 + row * 2.4;
  if (normalizedUnit.includes("item")) return 1 + (row % 6);
  if (typeof defaultValue === "number") return defaultValue;
  return 0.5 + row * 0.18;
}

function createDemoFile(detail: IndexDetail) {
  const headers = detail.fields.map((field) => field.name);
  const rows = Array.from({ length: DEMO_ROW_COUNT }, (_, row) => detail.fields.map((field) => demoValue(field.name, field.unit, row, field.default)));
  const csv = [headers, ...rows].map((values) => values.map((value) => {
    const displayValue = typeof value === "number" && !Number.isInteger(value) ? value.toFixed(3) : value;
    return `"${String(displayValue).replaceAll('"', '""')}"`;
  }).join(",")).join("\n");
  return new File(["\ufeff", csv], `${detail.index_key.toLowerCase()}-demo-data.csv`, { type: "text/csv;charset=utf-8" });
}

export function CalculatorWorkbench() {
  const { isEnglish } = useLanguage();
  const tr = (zh: string, en: string) => isEnglish ? en : zh;
  const searchParams = useSearchParams();
  const requestedIndex = searchParams.get("index") || "HEI2020";
  const [catalog, setCatalog] = useState<CatalogResponse | null>(null);
  const [indexKey, setIndexKey] = useState(requestedIndex);
  const [detail, setDetail] = useState<IndexDetail | null>(null);
  const [mode, setMode] = useState("general");
  const [files, setFiles] = useState<Record<string, File | null>>({});
  const [uploads, setUploads] = useState<UploadMap>({});
  const [mapping, setMapping] = useState<Record<string, string>>({});
  const [fisiVariant, setFisiVariant] = useState("fisi34");
  const [cycles, setCycles] = useState<CycleUpload[]>([{ id: 1, label: "2017-2018", files: {}, uploads: {} }]);
  const [activeCycleId, setActiveCycleId] = useState(1);
  const [job, setJob] = useState<Job | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    apiFetch<CatalogResponse>("/v1/indices").then(setCatalog).catch((err: Error) => setError(err.message));
  }, []);

  useEffect(() => {
    setIndexKey(requestedIndex);
  }, [requestedIndex]);

  useEffect(() => {
    setBusy(true);
    setError("");
    apiFetch<IndexDetail>(`/v1/indices/${encodeURIComponent(indexKey)}`)
      .then((payload) => {
        setDetail(payload);
        setMode(payload.supported_modes.includes("general") ? "general" : payload.supported_modes[0]);
        setFiles({}); setUploads({}); setMapping({}); setCycles([{ id: 1, label: "2017-2018", files: {}, uploads: {} }]); setActiveCycleId(1); setJob(null);
      })
      .catch((err: Error) => setError(err.message))
      .finally(() => setBusy(false));
  }, [indexKey]);

  const modeDefinition: ModeDefinition | undefined = catalog?.modes[mode];
  const multiCycleMode = mode === "nhanes_fped" || mode === "nhanes_mped";
  const cycleOptions = useMemo(() => nhanesCycleOptions(mode), [mode]);
  const baseKey = useMemo(() => baseIndexKey(indexKey), [indexKey]);
  const groupIndexKeys = useMemo(() => groupForIndex(baseKey), [baseKey]);
  const selectableItems = useMemo(
    () => catalog?.items.filter((item) => groupIndexKeys.includes(item.index_key as never)) ?? [],
    [catalog, groupIndexKeys],
  );
  const versionIndexKeys = useMemo(() => versionKeysForIndex(baseKey), [baseKey]);
  const versionItems = useMemo(
    () => catalog?.items.filter((item) => versionIndexKeys.includes(item.index_key as never)) ?? [],
    [catalog, versionIndexKeys],
  );
  const showIndexSelect = !catalog || selectableItems.length !== 1;
  const specs = detail?.mode_specs[mode] ?? [];
  const requirement = detail?.mode_requirements[mode];
  const fisi1Mode = indexKey === "FISI" && fisiVariant === "fisi1";
  const visibleSpecs = useMemo(
    () => {
      if (indexKey === "FISI" && multiCycleMode) {
        const keys = fisi1Mode
          ? ["nutrient_path", "nutrient_ind_path", "nutrient_path2", "nutrient_ind_path2", "demo_path"]
          : ["nutrient_path", "nutrient_path2", "demo_path"];
        return specs.filter((spec) => keys.includes(spec.key));
      }
      return requirement?.visible_file_keys
        ? specs.filter((spec) => requirement.visible_file_keys?.includes(spec.key))
        : specs;
    },
    [fisi1Mode, indexKey, multiCycleMode, requirement, specs],
  );
  const primaryPreview = multiCycleMode ? (cycles[0]?.uploads.input?.preview ?? Object.values(cycles[0]?.uploads ?? {})[0]?.preview) : (uploads.input?.preview ?? Object.values(uploads)[0]?.preview);
  const columns = primaryPreview?.columns ?? [];
  const requiredKeys = useMemo(
    () => fisi1Mode && multiCycleMode
      ? ["nutrient_path", "nutrient_ind_path"]
      : requirement?.required_file_keys ?? specs.filter((spec) => spec.required).map((spec) => spec.key),
    [fisi1Mode, multiCycleMode, requirement, specs],
  );
  const activeCycle = cycles.find((cycle) => cycle.id === activeCycleId) ?? cycles[0];
  const day1Specs = visibleSpecs.filter((spec) => !spec.key.endsWith("2") && !["demo_path", "mped_per_100_gram_path", "wjfrt"].includes(spec.key));
  const day2Specs = visibleSpecs.filter((spec) => spec.key.endsWith("2"));
  const sharedSpecs = visibleSpecs.filter((spec) => ["demo_path", "mped_per_100_gram_path", "wjfrt"].includes(spec.key));

  const requiredReady = useMemo(() => {
    return multiCycleMode
      ? cycles.length > 0 && cycles.every((cycle) => requiredKeys.every((key) => Boolean(cycle.files[key])))
      : requiredKeys.every((key) => Boolean(files[key]));
  }, [cycles, files, multiCycleMode, requiredKeys]);
  const hasFiles = multiCycleMode ? cycles.some((cycle) => Object.keys(cycle.files).length > 0) : Object.keys(files).length > 0;
  const hasUploads = multiCycleMode ? cycles.some((cycle) => Object.keys(cycle.uploads).length > 0) : Object.keys(uploads).length > 0;
  const computeOptions = indexKey === "FISI" ? { fisi_variant: fisiVariant } : {};

  async function uploadOne(key: string, file: File): Promise<UploadResponse> {
    const form = new FormData();
    form.append("file", file);
    return apiFetch<UploadResponse>("/v1/uploads", { method: "POST", body: form });
  }

  function changeMode(nextMode: string) {
    const firstCycle = nhanesCycleOptions(nextMode)[0]?.value ?? "2017-2018";
    if (!["nhanes_fped", "nhanes_mped"].includes(nextMode) && fisiVariant === "fisi1") {
      setFisiVariant("fisi34");
    }
    setMode(nextMode);
    setFiles({}); setUploads({}); setMapping({}); setCycles([{ id: 1, label: firstCycle, files: {}, uploads: {} }]); setActiveCycleId(1); setJob(null); setError("");
  }

  function changeFisiVariant(nextVariant: string) {
    setFisiVariant(nextVariant);
    setFiles({});
    setUploads({});
    setMapping({});
    setCycles((current) => current.map((cycle) => ({ ...cycle, files: {}, uploads: {} })));
    setJob(null);
    setError("");
  }

  function updateCycle(id: number, update: Partial<CycleUpload>) {
    setCycles((current) => current.map((cycle) => cycle.id === id ? { ...cycle, ...update } : cycle));
  }

  function selectCycle(id: number, label: string) {
    setCycles((current) => current.map((cycle) => cycle.id === id ? { ...cycle, label, files: {}, uploads: {} } : cycle));
    setJob(null);
  }

  function addCycle() {
    const used = new Set(cycles.map((cycle) => cycle.label));
    const next = cycleOptions.find((option) => !used.has(option.value));
    if (!next) return;
    const id = Math.max(...cycles.map((item) => item.id)) + 1;
    setCycles((current) => [...current, { id, label: next.value, files: {}, uploads: {} }]);
    setActiveCycleId(id);
  }

  function removeCycle(id: number) {
    const remaining = cycles.filter((cycle) => cycle.id !== id);
    setCycles(remaining);
    if (activeCycleId === id && remaining.length) setActiveCycleId(remaining[0].id);
  }

  function downloadDemoData() {
    if (!detail) return;
    const file = createDemoFile(detail);
    const url = URL.createObjectURL(file);
    const anchor = document.createElement("a");
    anchor.href = url; anchor.download = file.name; anchor.click();
    URL.revokeObjectURL(url);
  }

  async function runDemo() {
    if (!detail) return;
    if (fisi1Mode) {
      setError(tr(
        "FISI1 需要 NHANES 营养素总表与个体食物表，不能使用通用单文件测试数据。",
        "FISI1 requires NHANES nutrient-total and individual-food files and cannot use the general single-file demo.",
      ));
      return;
    }
    if (!detail.supported_modes.includes("general")) {
      setError(tr("当前指数不支持通用测试数据模式。", "This index does not support the general demo-data mode."));
      return;
    }
    setBusy(true); setError(""); setJob(null);
    try {
      const file = createDemoFile(detail);
      const uploaded = await uploadOne("input", file);
      if (uploaded.preview.error) throw new Error(uploaded.preview.error.message);
      const demoMapping = Object.fromEntries(detail.fields.map((field) => [field.name, field.name]));
      setMode("general");
      setFiles({ input: file });
      setUploads({ input: uploaded });
      setMapping(demoMapping);
      const submitted = await apiFetch<Job>("/v1/compute", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ index_key: indexKey, mode: "general", upload_id: uploaded.upload_id, mapping: demoMapping, options: computeOptions }),
      });
      setJob(submitted);
      const finished = await waitForJob(submitted.job_id, setJob);
      if (finished.status === "failed") throw new Error(finished.error?.message || tr("测试计算失败", "Demo calculation failed"));
    } catch (err) {
      setError(err instanceof Error ? err.message : tr("测试计算失败", "Demo calculation failed"));
    } finally { setBusy(false); }
  }

  async function prepare() {
    if (!requiredReady) { setError(tr("请先选择所有必需文件。", "Please select all required files.")); return; }
    setBusy(true); setError(""); setJob(null);
    try {
      if (multiCycleMode) {
        const nextCycles = await Promise.all(cycles.map(async (cycle) => {
          const entries = await Promise.all(Object.entries(cycle.files).filter((entry): entry is [string, File] => Boolean(entry[1])).map(async ([key, file]) => [key, await uploadOne(key, file)] as const));
          return { ...cycle, uploads: Object.fromEntries(entries) };
        }));
        setCycles(nextCycles);
        return;
      }
      const entries = await Promise.all(Object.entries(files).filter((entry): entry is [string, File] => Boolean(entry[1])).map(async ([key, file]) => [key, await uploadOne(key, file)] as const));
      const nextUploads = Object.fromEntries(entries);
      if (indexKey === "AHEI" && mode === "dhq3") {
        const preview = nextUploads.input?.preview ?? Object.values(nextUploads)[0]?.preview;
        if (!preview || preview.error) throw new Error(preview?.error?.message || tr("无法预览 DHQ3 文件", "Unable to preview the DHQ3 file"));
        if (!preview.columns.includes("Food ID")) {
          throw new Error(tr(
            "AHEI 的 DHQ3 模式必须上传 detail.csv，且文件中必须包含 “Food ID” 列。Total Daily Results 请改用通用模式。",
            "AHEI in DHQ3 mode requires detail.csv with a “Food ID” column. Use general mode for Total Daily Results.",
          ));
        }
      }
      if (mode === "general") {
        const preview = nextUploads.input?.preview;
        if (!preview || preview.error) throw new Error(preview?.error?.message || tr("无法预览上传文件", "Unable to preview the uploaded file"));
        const suggested = await apiFetch<MappingResponse>("/v1/mapping/suggest", { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ index_key: indexKey, columns: preview.columns }) });
        setMapping(Object.fromEntries(Object.entries(suggested.suggestions).map(([field, meta]) => [field, meta.column ?? ""])));
      }
      setUploads(nextUploads);
    } catch (err) {
      setError(err instanceof Error ? err.message : tr("文件准备失败", "File preparation failed"));
    } finally { setBusy(false); }
  }

  async function compute() {
    if (!hasUploads) { setError(tr("请先上传并检查文件。", "Please upload and inspect the files first.")); return; }
    setBusy(true); setError(""); setJob(null);
    try {
      if (mode === "general") {
        const validation = await apiFetch<{ valid: boolean; missing_required: string[]; unknown_columns: unknown[] }>("/v1/mapping/validate", { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ index_key: indexKey, columns, mapping }) });
        if (!validation.valid) throw new Error(`${tr("字段映射未完成", "Column mapping is incomplete")}: ${validation.missing_required.join(", ") || tr("存在未知列", "unknown columns remain")}`);
      }
      const singleFile = requirement?.single_file ?? specs.length === 1;
      const payload = multiCycleMode
        ? { index_key: indexKey, mode, cycles: cycles.map((cycle, index) => ({ label: cycle.label.trim() || `${tr("周期", "Cycle")} ${index + 1}`, upload_ids: Object.fromEntries(Object.entries(cycle.uploads).map(([key, value]) => [key, value.upload_id])) })), options: computeOptions }
        : singleFile
        ? { index_key: indexKey, mode, upload_id: uploads.input?.upload_id ?? Object.values(uploads)[0]?.upload_id, mapping, options: computeOptions }
        : { index_key: indexKey, mode, upload_ids: Object.fromEntries(Object.entries(uploads).map(([key, value]) => [key, value.upload_id])), mapping, options: computeOptions };
      const submitted = await apiFetch<Job>("/v1/compute", { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify(payload) });
      setJob(submitted);
      const finished = await waitForJob(submitted.job_id, setJob);
      if (finished.status === "failed") throw new Error(finished.error?.message || tr("计算失败", "Calculation failed"));
    } catch (err) {
      setError(err instanceof Error ? err.message : tr("计算失败", "Calculation failed"));
    } finally { setBusy(false); }
  }

  function renderCycleSpec(spec: FileSpec) {
    if (!activeCycle) return null;
    const required = requiredKeys.includes(spec.key);
    const guide = nhanesFileGuide(spec.key, activeCycle.label, mode);
    return <div className={`upload-field ${required ? "is-required" : "is-optional"}`} key={spec.key}><span>{isEnglish ? spec.label_en : spec.label_zh}<i className={required ? "" : "optional"}>{required ? tr("必需", "Required") : tr("可选", "Optional")}</i></span><small>{isEnglish ? spec.description_en : spec.description_zh}</small>{guide && <div className={`nhanes-file-guide${guide.unavailable ? " is-unavailable" : ""}`}><span>{guide.naming === "fixed" ? tr("官方文件名", "Official filename") : tr("推荐文件名", "Recommended filename")}</span><code>{guide.filename}</code>{guide.url && <a href={guide.url} target="_blank" rel="noreferrer">{guide.source === "usda" ? "USDA FPED" : "CDC NHANES"} {tr("下载", "Download")}</a>}</div>}<div className="custom-file-picker"><label><input type="file" accept={spec.accepted_extensions.join(",")} onChange={(e) => updateCycle(activeCycle.id, { files: { ...activeCycle.files, [spec.key]: e.target.files?.[0] ?? null } })} /><span>{tr("选择文件", "Choose file")}</span></label><b>{activeCycle.files[spec.key]?.name || tr("未选择文件", "No file selected")}</b></div><em>{tr("支持", "Accepted")}: {spec.accepted_extensions.join(" / ")}</em></div>;
  }

  return (
    <div className="site-page calculator-page" id="calculator-top">
      <section className="hero-banner"><h1>🥗 {detail?.index_key.replaceAll("_", "-") ?? tr("膳食指数", "Dietary Index")} {tr("计算页", "Calculator")}</h1><div className="hero-subtitle">{(isEnglish ? detail?.title_en : detail?.title_zh) ?? tr("正在读取指数定义", "Loading index definition")}</div><div className="hero-tagline"><p>{(isEnglish ? detail?.description_en : detail?.description_zh) ?? tr("选择数据模式、上传文件并完成字段映射。", "Select a data mode, upload files, and map columns.")}</p></div></section>

      <div className="page-tool-row"><span className="caption">{tr("计算由 dietaryindex Python 内核执行，Next.js 仅负责交互。", "Calculations run in the dietaryindex Python engine; Next.js provides the interface.")}</span><div className="demo-actions">{detail?.references?.length ? <a className="reference-jump-button" href="#index-references"><span>📚</span>{tr(`查看权威参考文献（${detail.references.length} 篇）`, `View authoritative references (${detail.references.length})`)}<b>↓</b></a> : null}<button className="button secondary" type="button" disabled={!detail || busy || fisi1Mode} title={fisi1Mode ? tr("FISI1 请使用下方 NHANES 原始文件上传区", "For FISI1, use the NHANES file upload area below") : undefined} onClick={downloadDemoData}>{tr("下载当前指数测试数据", "Download demo data")}</button><button className="button primary" type="button" disabled={!detail || busy || fisi1Mode} title={fisi1Mode ? tr("FISI1 请使用下方 NHANES 原始文件上传区", "For FISI1, use the NHANES file upload area below") : undefined} onClick={() => void runDemo()}>{busy ? tr("正在计算…", "Calculating…") : tr("测试数据一键计算", "One-click demo calculation")}</button></div></div>

      <div className="step-indicator"><div className="step active">1. {tr("选择指数", "Select index")}</div><div className={`step ${hasFiles ? "active" : ""}`}>2. {tr("上传数据", "Upload data")}</div><div className={`step ${hasUploads ? "active" : ""}`}>3. {tr("字段映射", "Map columns")}</div><div className={`step ${job?.status === "succeeded" ? "active" : ""}`}>4. {tr("计算与导出", "Calculate & export")}</div></div>

      <section className="workbench-grid">
        <aside className="control-card">
          <div className="step-label"><b>01</b><span>{tr("选择计算方案", "Choose calculation")}</span></div>
          <label><span>{selectableItems.length > 1 ? tr("同族指标", "Family indices") : tr("计算指标", "Index")}</span>{showIndexSelect ? <select value={baseKey} onChange={(e) => setIndexKey(e.target.value)} disabled={!catalog || busy}>{selectableItems.map((item) => <option key={item.index_key} value={item.index_key}>{item.index_key.replaceAll("_", "-")} · {isEnglish ? item.title_en : item.title_zh}</option>)}</select> : <div className="static-index-value">{baseKey.replaceAll("_", "-")}{selectableItems[0] ? ` · ${isEnglish ? selectableItems[0].title_en : selectableItems[0].title_zh}` : ""}</div>}</label>
          {versionItems.length > 1 && <label><span>{tr("版本", "Version")}</span><select value={indexKey} onChange={(e) => setIndexKey(e.target.value)} disabled={!catalog || busy}>{versionItems.map((item) => <option key={item.index_key} value={item.index_key}>{item.index_key.replaceAll("_", "-")} · {isEnglish ? item.title_en : item.title_zh}</option>)}</select></label>}
          <label><span>{tr("数据模式", "Data mode")}</span><select value={mode} onChange={(e) => changeMode(e.target.value)} disabled={!detail || busy}>{detail?.supported_modes.map((item) => <option key={item} value={item}>{(isEnglish ? catalog?.modes[item]?.label_en : catalog?.modes[item]?.label_zh) ?? item}</option>)}</select></label>
          {indexKey === "FISI" && <label><span>{tr("FISI 算法版本", "FISI algorithm version")}</span><select value={fisiVariant} onChange={(e) => changeFisiVariant(e.target.value)} disabled={!detail || busy}><option value="fisi1" disabled={!multiCycleMode}>{tr("FISI1 · 食物层评分（内置 FII 食物库）", "FISI1 · food-level score (built-in FII food database)")}{!multiCycleMode ? tr("（仅 NHANES）", " (NHANES only)") : ""}</option><option value="fisi34">{tr("FISI34 · 34 成分（USDA NRV）", "FISI34 · 34 components (USDA NRV)")}</option><option value="fisi26_china">{tr("FISI26 China · 26 成分（中国 NRV）", "FISI26 China · 26 components (China NRV)")}</option><option value="fisi26_usda">{tr("FISI26 USDA · 26 成分（USDA NRV）", "FISI26 USDA · 26 components (USDA NRV)")}</option></select><small className="mode-description">{fisiVariant === "fisi1" ? tr("食物层算法：按个体食物摄入克数与内置 FII 食物值计算，仅适用于 NHANES 原始文件模式。", "Food-level algorithm based on individual food grams and the built-in food FII values; available for raw NHANES modes.") : fisiVariant === "fisi34" ? tr("原始完整算法：34 个非黄酮营养成分，采用 USDA 参考值。", "Original full algorithm: 34 non-flavonoid components with USDA reference values.") : fisiVariant === "fisi26_china" ? tr("26 成分算法，采用中国 DRI/NRV 参考值。", "26-component algorithm using China DRI/NRV reference values.") : tr("26 成分算法，采用 USDA 参考值。", "26-component algorithm using USDA reference values.")}</small></label>}
          {modeDefinition && <p className="mode-description">{isEnglish ? modeDefinition.description_en : modeDefinition.description_zh}</p>}
          {detail?.supported_modes.length === 1 && detail.supported_modes[0] === "general" && <p className="mode-support-note">{tr("该指标目前没有经过验证的原始 NHANES 文件适配器。请上传已整理好的指标字段；系统不会展示尚未实现的模式。", "This index does not yet have a validated raw-NHANES adapter. Upload prepared index fields; unimplemented modes are not shown.")}</p>}
          {(isEnglish ? requirement?.notes_en : requirement?.notes_zh) && <div className="inline-tip">{fisi1Mode && multiCycleMode ? tr("FISI1：Day 1 营养素总表和个体食物表均为必需；Day 2 两张表可选，但必须成对上传。系统自动使用内置 FII 食物数据库。", "FISI1: Day 1 nutrient totals and individual foods are both required. The two Day 2 files are optional but must be uploaded together. The built-in food FII database is used automatically.") : isEnglish ? requirement?.notes_en : requirement?.notes_zh}</div>}

          <div className="step-label"><b>02</b><span>{tr("上传数据文件", "Upload data files")}</span></div>
          {multiCycleMode && activeCycle ? <div className="cycle-workspace"><div className="cycle-tabs" role="tablist" aria-label={tr("已选择的 NHANES 周期", "Selected NHANES cycles")}>{cycles.map((cycle) => { const completed = requiredKeys.filter((key) => Boolean(cycle.files[key])).length; return <button type="button" role="tab" aria-selected={cycle.id === activeCycle.id} className={cycle.id === activeCycle.id ? "active" : ""} key={cycle.id} onClick={() => setActiveCycleId(cycle.id)}><strong>{cycle.label}</strong><span>{completed}/{requiredKeys.length} {tr("必需文件", "required")}</span></button>; })}<button className="add-cycle-tab" type="button" disabled={busy || cycles.length >= cycleOptions.length} onClick={addCycle}>＋ {cycles.length >= cycleOptions.length ? tr("已全部添加", "All added") : tr("新增周期", "Add cycle")}</button></div><div className="cycle-upload-card"><div className="cycle-upload-heading"><strong>{tr("当前周期", "Current cycle")}</strong><select aria-label={tr("选择 NHANES 周期", "Select NHANES cycle")} value={activeCycle.label} onChange={(e) => selectCycle(activeCycle.id, e.target.value)}>{cycleOptions.map((option) => <option key={option.value} value={option.value} disabled={cycles.some((item) => item.id !== activeCycle.id && item.label === option.value)}>{option.value}{option.suffix ? `（${tr("文件后缀", "file suffix")} ${option.suffix}）` : ""}</option>)}</select>{cycles.length > 1 && <button className="button secondary" type="button" onClick={() => removeCycle(activeCycle.id)}>{tr("移除本周期", "Remove cycle")}</button>}</div><p className="mode-description">{tr("上方标签切换周期；页面一次只显示当前周期的文件。", "Use the tabs above to switch cycles; only the current cycle's files are shown.")}</p><div className="day-requirement-summary"><strong>{tr("本指标最低要求", "Minimum required for this index")}</strong><span>{visibleSpecs.filter((spec) => requiredKeys.includes(spec.key)).map((spec) => isEnglish ? spec.label_en : spec.label_zh).join("、")}</span><small>{tr("Day 2 文件均为可选；提供 Day 2 后系统计算两天平均结果。", "All Day 2 files are optional; when supplied, the system calculates a two-day average.")}</small></div>{sharedSpecs.length > 0 && <section className="recall-day-section shared-files"><h3><b>{tr("公共", "Shared")}</b><span>{tr("人口学与公共辅助文件", "Demographic and shared supporting files")}</span><i>{tr("可选", "Optional")}</i></h3><div className="upload-list">{sharedSpecs.map(renderCycleSpec)}</div></section>}<section className="recall-day-section day-one"><h3><b>Day 1</b><span>{tr("第一天回顾文件", "First recall-day files")}</span><i>{day1Specs.some((spec) => requiredKeys.includes(spec.key)) ? tr("包含必需文件", "Contains required files") : tr("可选", "Optional")}</i></h3><div className="upload-list">{day1Specs.map(renderCycleSpec)}</div></section>{day2Specs.length > 0 && <section className="recall-day-section day-two"><h3><b>Day 2</b><span>{tr("第二天回顾文件", "Second recall-day files")}</span><i>{tr("全部可选", "All optional")}</i></h3><div className="upload-list">{day2Specs.map(renderCycleSpec)}</div></section>}</div></div> : <div className="upload-list">{visibleSpecs.map((spec) => <div className="upload-field" key={spec.key}><span>{isEnglish ? spec.label_en : spec.label_zh}{spec.required && <i>{tr("必需", "Required")}</i>}</span><small>{isEnglish ? spec.description_en : spec.description_zh}</small><div className="custom-file-picker"><label><input type="file" accept={spec.accepted_extensions.join(",")} onChange={(e) => setFiles((current) => ({ ...current, [spec.key]: e.target.files?.[0] ?? null }))} /><span>{tr("选择文件", "Choose file")}</span></label><b>{files[spec.key]?.name || tr("未选择文件", "No file selected")}</b></div><em>{tr("支持", "Accepted")}: {spec.accepted_extensions.join(" / ")}</em></div>)}</div>}
          <button className="button primary full" disabled={busy || !requiredReady} onClick={() => void prepare()}>{busy ? tr("处理中…", "Processing…") : hasUploads ? tr("重新上传并检查", "Upload and inspect again") : tr("上传并检查字段", "Upload and inspect columns")}</button>
        </aside>

        <div className="workbench-main">
          <section className="definition-card"><div><span className="index-code">{detail?.index_key.replaceAll("_", "-") ?? "—"}</span><h2>{(isEnglish ? detail?.title_en : detail?.title_zh) ?? tr("正在读取指数定义", "Loading index definition")}</h2><p>{isEnglish ? detail?.description_en : detail?.description_zh}</p></div><dl><div><dt>{tr("输出字段", "Output fields")}</dt><dd>{fisi1Mode ? "FISI1" : detail?.output_cols.join(", ") || "—"}</dd></div><div><dt>{tr("分值尺度", "Score scale")}</dt><dd>{detail?.score_scale ?? "—"}</dd></div></dl></section>

          {error && <div className="notice error">{error}</div>}

          {primaryPreview && !primaryPreview.error && <section className="table-card"><div className="card-title"><div><span className="eyebrow">DATA PREVIEW</span><h2>{tr("数据预览", "Data preview")}</h2></div><b>{primaryPreview.rows.toLocaleString()} {tr("行", "rows")} · {primaryPreview.columns.length} {tr("列", "columns")}</b></div><PreviewTable rows={primaryPreview.preview} columns={primaryPreview.columns} /></section>}

          {mode === "general" && primaryPreview && detail && <section className="mapping-card"><div className="card-title"><div><span className="eyebrow">COLUMN MAPPING</span><h2>{tr("字段映射", "Column mapping")}</h2></div><b>{Object.values(mapping).filter(Boolean).length}/{detail.fields.length}</b></div><div className="mapping-list">{detail.fields.map((field) => <label key={field.name}><span><strong>{isEnglish ? field.label_en : field.label_zh}</strong><small>{field.name}{field.unit ? ` · ${field.unit}` : ""}</small></span><select value={mapping[field.name] ?? ""} onChange={(e) => setMapping((current) => ({ ...current, [field.name]: e.target.value }))}><option value="">{field.required ? tr("请选择必需字段", "Select a required column") : tr("不映射（可选）", "Do not map (optional)")}</option>{columns.map((column) => <option value={column} key={column}>{column}</option>)}</select><i className={field.required ? "required-dot" : "optional-dot"}>{field.required ? tr("必需", "Required") : tr("可选", "Optional")}</i></label>)}</div></section>}

          {hasUploads && <section className="compute-bar"><div><strong>{tr("文件已准备完成", "Files are ready")}</strong><span>{mode === "general" ? tr("确认字段映射后提交计算。", "Confirm the mapping, then submit the calculation.") : multiCycleMode ? tr("各周期将独立计算，再按 NHANES_CYCLE 合并结果。", "Each cycle will be calculated independently, then combined with NHANES_CYCLE.") : tr("当前模式将使用适配器自动处理文件。", "The adapter will process files automatically in this mode.")}</span></div><button className="button primary" disabled={busy} onClick={() => void compute()}>{busy ? tr("计算中…", "Calculating…") : tr("提交计算", "Submit calculation")}</button></section>}

          {job && <JobResult job={job} isEnglish={isEnglish} />}
        </div>
      </section>
      {detail?.references?.length ? <section className="references-card" id="index-references" aria-labelledby="index-references-title"><div className="references-heading"><div><span className="eyebrow">AUTHORITATIVE LITERATURE</span><h2 id="index-references-title">📚 {tr("参考文献", "References")}</h2><p>{tr("以下为该指标的开发、评分或权威验证文献。点击 DOI / PubMed 可打开原文记录。", "Authoritative development, scoring, or validation sources for this index. Open DOI / PubMed for the source record.")}</p></div><a href="#calculator-top">{tr("↑ 返回顶部", "↑ Back to top")}</a></div><ol className="reference-list">{detail.references.map((reference, index) => <li key={`${reference.doi || reference.pmid || reference.title}-${index}`}><div className="reference-role">{isEnglish ? reference.role_en : reference.role_zh}</div><p><strong>{reference.authors}.</strong> {reference.title}. <em>{reference.journal}</em>. {reference.year}{reference.volume_pages ? `; ${reference.volume_pages}` : ""}.</p><div className="reference-links">{reference.doi ? <a href={`https://doi.org/${reference.doi}`} target="_blank" rel="noreferrer">DOI: {reference.doi} ↗</a> : null}{reference.pmid ? <a href={`https://pubmed.ncbi.nlm.nih.gov/${reference.pmid}/`} target="_blank" rel="noreferrer">PubMed: {reference.pmid} ↗</a> : null}{!reference.doi && !reference.pmid && reference.url ? <a href={reference.url} target="_blank" rel="noreferrer">{tr("查看权威来源", "View authoritative source")} ↗</a> : null}</div></li>)}</ol></section> : null}
    </div>
  );
}

function PreviewTable({ rows, columns }: { rows: Record<string, unknown>[]; columns: string[] }) {
  const visible = columns.slice(0, 8);
  return <div className="data-table-wrap"><table><thead><tr>{visible.map((column) => <th key={column}>{column}</th>)}</tr></thead><tbody>{rows.slice(0, 5).map((row, index) => <tr key={index}>{visible.map((column) => <td key={column}>{String(row[column] ?? "")}</td>)}</tr>)}</tbody></table></div>;
}

function JobResult({ job, isEnglish }: { job: Job; isEnglish: boolean }) {
  const result = job.result;
  const tr = (zh: string, en: string) => isEnglish ? en : zh;
  const statusLabel = job.status === "succeeded" ? tr("成功", "Succeeded") : job.status === "failed" ? tr("失败", "Failed") : job.status === "running" ? tr("运行中", "Running") : tr("排队中", "Queued");
  return <section className={`result-card status-${job.status}`}><div className="card-title"><div><span className="eyebrow">COMPUTE JOB</span><h2>{job.status === "succeeded" ? tr("计算完成", "Calculation complete") : job.status === "failed" ? tr("计算失败", "Calculation failed") : tr("正在计算", "Calculating")}</h2></div><span className="status-pill">{statusLabel}</span></div>{job.error && <div className="notice error">{job.error.type}: {job.error.message}</div>}{result && <><div className="result-metrics"><div><span>{tr("样本数", "Samples")}</span><strong>{result.rows}</strong></div><div><span>{tr("主要输出", "Primary output")}</span><strong>{result.primary_output_column ?? "—"}</strong></div><div><span>{tr("均值", "Mean")}</span><strong>{result.summary_stats?.mean?.toFixed(3) ?? "—"}</strong></div><div><span>{tr("范围", "Range")}</span><strong>{result.summary_stats?.min?.toFixed(2) ?? "—"} – {result.summary_stats?.max?.toFixed(2) ?? "—"}</strong></div></div><div className="result-preview-heading"><strong>{tr("结果预览", "Result preview")}</strong><span>{tr("仅显示前 5 行、前 8 列；下载文件包含全部数据", "Showing only the first 5 rows and 8 columns; downloads contain the complete result")}</span></div><PreviewTable rows={result.preview} columns={result.columns} />{result.downloads && <div className="download-row"><a className="button primary" href={proxiedDownloadUrl(result.downloads.csv)}>{tr("下载完整 CSV", "Download full CSV")}</a><a className="button secondary" href={proxiedDownloadUrl(result.downloads.xlsx)}>{tr("下载完整 Excel", "Download full Excel")}</a></div>}</>}</section>;
}
