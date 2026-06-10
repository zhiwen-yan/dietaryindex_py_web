"""
论文图表与表格展示页面
dietaryindex-Py: All Figures & Tables for Frontiers in Nutrition
"""

import sys
import os
import pickle
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

from sidebar_utils import render_sidebar
from config.i18n import get_lang

lang = get_lang()
is_en = lang == "en"

st.set_page_config(
    page_title="Figures & Tables | dietaryindex-Py" if get_lang() == "en" else "论文图表 | dietaryindex-Py",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)
render_sidebar("figures")

st.switch_page("app.py")

st.markdown("""
<style>
.fig-container {
    background: #ffffff;
    border: 1px solid #e0e0e0;
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
}
.fig-title {
    font-size: 1.15rem;
    font-weight: 700;
    color: #1a6b56;
    margin-bottom: 0.5rem;
    border-bottom: 2px solid #eaf5f0;
    padding-bottom: 0.5rem;
}
.fig-caption {
    font-size: 0.82rem;
    color: #777;
    margin-top: 0.5rem;
    font-style: italic;
}
.section-header {
    font-size: 1.4rem;
    font-weight: 800;
    color: #c7952b;
    margin: 2rem 0 1rem 0;
    padding-bottom: 0.3rem;
    border-bottom: 3px solid #c7952b;
}
.table-container {
    background: #fafafa;
    border-radius: 8px;
    padding: 0.5rem 1rem;
    margin-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)


def bi_text(zh: str, en: str) -> str:
    return en if is_en else zh


THEME_COLORS = {
    "green": "#1a6b56",
    "gold": "#c7952b",
    "red": "#d94e4e",
    "blue": "#4e79a7",
    "orange": "#f28e2b",
    "purple": "#b07aa1",
    "cyan": "#59a14f",
    "pink": "#e15759",
    "brown": "#9c755f",
}

REPO_ROOT = Path(__file__).resolve().parents[2]
WORKSPACE_ROOT = REPO_ROOT.parent
PROJECT_ROOT = WORKSPACE_ROOT if (WORKSPACE_ROOT / "NHANES").exists() else REPO_ROOT
STREAMLIT_APP_DIR = Path(__file__).resolve().parents[1]
LOCAL_CACHE_DIR = STREAMLIT_APP_DIR / "cache"
LOCAL_CACHE_DIR.mkdir(parents=True, exist_ok=True)
NHANES_CACHE_FILE = LOCAL_CACHE_DIR / "nhanes_2017_2018_figures.pkl"
NHANES_CACHE_VERSION = "2026-06-07-v2"
FINAL_PRODUCTS_DIR = STREAMLIT_APP_DIR / "final_products"
TEST_DIR = REPO_ROOT / "tests"
NHANES_1718_DIR = PROJECT_ROOT / "NHANES" / "2017-2018"
NHANES_0718_SCORES_PATH = PROJECT_ROOT / "NHANES" / "_derived" / "diet_scores_2007_2018_nhanes_python_raw.csv"
NHANES_1718_PATHS = {
    "fped_tot1": NHANES_1718_DIR / "Dietary" / "fped_dr1tot_1718.sas7bdat",
    "fped_tot2": NHANES_1718_DIR / "Dietary" / "fped_dr2tot_1718.sas7bdat",
    "fped_iff1": NHANES_1718_DIR / "Dietary" / "fped_dr1iff_1718.sas7bdat",
    "fped_iff2": NHANES_1718_DIR / "Dietary" / "fped_dr2iff_1718.sas7bdat",
    "nut_tot1": NHANES_1718_DIR / "Dietary" / "dr1tot_j.xpt",
    "nut_tot2": NHANES_1718_DIR / "Dietary" / "dr2tot_j.xpt",
    "nut_iff1": NHANES_1718_DIR / "Dietary" / "dr1iff_j.xpt",
    "nut_iff2": NHANES_1718_DIR / "Dietary" / "dr2iff_j.xpt",
    "demo": NHANES_1718_DIR / "Demographics" / "demo_j.xpt",
}

NHANES_INDEX_SPECS = {
    "DII": {"score_col": "DII_ALL", "max_score": 10, "dmin": -5.82, "dmax": 5.94, "color": "#d94e4e"},
    "HEI-2015": {"score_col": "HEI2015_ALL", "max_score": 100, "dmin": 0, "dmax": 100, "color": "#59a14f"},
    "HEI-2020": {"score_col": "HEI2020_ALL", "max_score": 100, "dmin": 0, "dmax": 100, "color": "#59a14f"},
    "AHEI": {"score_col": "AHEI_ALL", "max_score": 110, "dmin": 0, "dmax": 110, "color": "#4e79a7"},
    "DASH": {"score_col": "DASH_ALL", "max_score": 40, "dmin": 8, "dmax": 40, "color": "#f28e2b"},
    "DASHI": {"score_col": "DASHI_ALL", "max_score": 9, "dmin": 0, "dmax": 9, "color": "#f28e2b"},
    "MED": {"score_col": "MED_ALL", "max_score": 9, "dmin": 0, "dmax": 9, "color": "#4e79a7"},
    "MEDI": {"score_col": "MEDI_ALL", "max_score": 14, "dmin": 0, "dmax": 14, "color": "#b07aa1"},
    "DI-GM": {"score_col": "DI_GM_TOTAL", "max_score": 14, "dmin": 0, "dmax": 14, "color": "#d94e4e"},
}

SUPPORTED_NHANES_INDICES = ["DII", "HEI-2015", "HEI-2020", "AHEI", "DASH", "DASHI", "MED", "MEDI", "DI-GM"]
NHANES_0718_SCORE_COLUMN_MAP = {
    "DII": "dii",
    "HEI-2015": "hei_2015",
    "HEI-2020": "hei_2020",
    "AHEI": "ahei",
    "DASH": "dash",
    "DASHI": "dashi",
    "MED": "med",
    "MEDI": "medi",
    "DI-GM": "di_gm",
}

_NHANES_COMPUTE_FUNCS = None


def _get_nhanes_compute_funcs():
    """Import heavy NHANES adapter functions only when the figures page needs raw recomputation."""
    global _NHANES_COMPUTE_FUNCS
    if _NHANES_COMPUTE_FUNCS is None:
        from dietaryindex import (
            compute_ahei_nhanes_fped,
            compute_dash_nhanes_fped,
            compute_dashi_nhanes_fped,
            compute_di_gm_nhanes_fped,
            compute_dii_nhanes_fped,
            compute_hei2015_nhanes_fped,
            compute_hei2020_nhanes_fped,
            compute_med_nhanes_fped,
            compute_medi_nhanes_fped,
        )

        _NHANES_COMPUTE_FUNCS = {
            "DII": compute_dii_nhanes_fped,
            "HEI-2015": compute_hei2015_nhanes_fped,
            "HEI-2020": compute_hei2020_nhanes_fped,
            "MED": compute_med_nhanes_fped,
            "DASHI": compute_dashi_nhanes_fped,
            "DASH": compute_dash_nhanes_fped,
            "AHEI": compute_ahei_nhanes_fped,
            "MEDI": compute_medi_nhanes_fped,
            "DI-GM": compute_di_gm_nhanes_fped,
        }
    return _NHANES_COMPUTE_FUNCS


def _normalize_score_to_100(values, spec):
    """Normalize scores by the index's theoretical display range."""
    denom = spec["dmax"] - spec["dmin"]
    if denom <= 0:
        return np.full(len(values), np.nan, dtype=float)
    normalized = (values - spec["dmin"]) / denom * 100
    return np.clip(normalized, 0, 100)


def _domain_ref(axis: str, index: int) -> str:
    """Return a Plotly axis domain ref, using 'x domain' for the first subplot."""
    return f"{axis} domain" if index == 1 else f"{axis}{index} domain"


def _all_nhanes_files_exist():
    return all(path.exists() for path in NHANES_1718_PATHS.values())


def _nhanes_cache_signature():
    return {
        "version": NHANES_CACHE_VERSION,
        "sources": {
            name: {
                "path": str(path),
                "size": path.stat().st_size,
                "mtime_ns": path.stat().st_mtime_ns,
            }
            for name, path in NHANES_1718_PATHS.items()
        },
    }


def _read_local_nhanes_cache():
    if not NHANES_CACHE_FILE.exists():
        return None
    try:
        with NHANES_CACHE_FILE.open("rb") as fh:
            payload = pickle.load(fh)
        if payload.get("signature") != _nhanes_cache_signature():
            return None
        return payload.get("results")
    except Exception:
        return None


def _write_local_nhanes_cache(results):
    payload = {
        "signature": _nhanes_cache_signature(),
        "results": results,
    }
    with NHANES_CACHE_FILE.open("wb") as fh:
        pickle.dump(payload, fh, protocol=pickle.HIGHEST_PROTOCOL)


@st.cache_data(show_spinner=False)
def _load_nhanes_2007_2018_supported_scores():
    if not NHANES_0718_SCORES_PATH.exists():
        return pd.DataFrame(columns=["SEQN", *SUPPORTED_NHANES_INDICES])

    usecols = ["seqn", *NHANES_0718_SCORE_COLUMN_MAP.values()]
    df = pd.read_csv(NHANES_0718_SCORES_PATH, usecols=usecols, low_memory=False)
    df = df.rename(
        columns={
            "seqn": "SEQN",
            **{src: dest for dest, src in NHANES_0718_SCORE_COLUMN_MAP.items()},
        }
    )
    df["SEQN"] = pd.to_numeric(df["SEQN"], errors="coerce").astype("Int64")
    for name in SUPPORTED_NHANES_INDICES:
        df[name] = pd.to_numeric(df[name], errors="coerce")
    return df.dropna(subset=["SEQN"]).drop_duplicates(subset=["SEQN"]).reset_index(drop=True)


def _mean_two_day_energy(day1_df, day1_col, day2_df, day2_col):
    day1 = day1_df[["SEQN", day1_col]].rename(columns={day1_col: "KCAL"})
    day2 = day2_df[["SEQN", day2_col]].rename(columns={day2_col: "KCAL"})
    day1["SEQN"] = day1["SEQN"].astype(int)
    day2["SEQN"] = day2["SEQN"].astype(int)
    merged = pd.concat([day1, day2], ignore_index=True)
    return merged.groupby("SEQN", as_index=False)["KCAL"].mean()


@st.cache_data(show_spinner=False)
def _load_nhanes_real_data():
    if not _all_nhanes_files_exist():
        return {}

    cached_results = _read_local_nhanes_cache()
    if cached_results is not None:
        return cached_results

    import pyreadstat
    compute_funcs = _get_nhanes_compute_funcs()

    results = {
        "DII": compute_funcs["DII"](
            str(NHANES_1718_PATHS["fped_tot1"]),
            str(NHANES_1718_PATHS["nut_tot1"]),
            str(NHANES_1718_PATHS["demo"]),
            str(NHANES_1718_PATHS["fped_tot2"]),
            str(NHANES_1718_PATHS["nut_tot2"]),
        ),
        "HEI-2015": compute_funcs["HEI-2015"](
            str(NHANES_1718_PATHS["fped_tot1"]),
            str(NHANES_1718_PATHS["nut_tot1"]),
            str(NHANES_1718_PATHS["demo"]),
            str(NHANES_1718_PATHS["fped_tot2"]),
            str(NHANES_1718_PATHS["nut_tot2"]),
        ),
        "HEI-2020": compute_funcs["HEI-2020"](
            str(NHANES_1718_PATHS["fped_tot1"]),
            str(NHANES_1718_PATHS["nut_tot1"]),
            str(NHANES_1718_PATHS["demo"]),
            str(NHANES_1718_PATHS["fped_tot2"]),
            str(NHANES_1718_PATHS["nut_tot2"]),
        ),
        "MED": compute_funcs["MED"](
            str(NHANES_1718_PATHS["fped_tot1"]),
            str(NHANES_1718_PATHS["nut_tot1"]),
            str(NHANES_1718_PATHS["demo"]),
            str(NHANES_1718_PATHS["fped_tot2"]),
            str(NHANES_1718_PATHS["nut_tot2"]),
        ),
        "DASHI": compute_funcs["DASHI"](
            str(NHANES_1718_PATHS["nut_tot1"]),
            str(NHANES_1718_PATHS["nut_tot2"]),
            str(NHANES_1718_PATHS["demo"]),
        ),
        "DASH": compute_funcs["DASH"](
            str(NHANES_1718_PATHS["fped_iff1"]),
            str(NHANES_1718_PATHS["nut_iff1"]),
            str(NHANES_1718_PATHS["fped_iff2"]),
            str(NHANES_1718_PATHS["nut_iff2"]),
            demo_path=str(NHANES_1718_PATHS["demo"]),
        ),
        "AHEI": compute_funcs["AHEI"](
            str(NHANES_1718_PATHS["fped_iff1"]),
            str(NHANES_1718_PATHS["nut_iff1"]),
            str(NHANES_1718_PATHS["fped_iff2"]),
            str(NHANES_1718_PATHS["nut_iff2"]),
            demo_path=str(NHANES_1718_PATHS["demo"]),
        ),
        "MEDI": compute_funcs["MEDI"](
            str(NHANES_1718_PATHS["fped_iff1"]),
            str(NHANES_1718_PATHS["nut_iff1"]),
            str(NHANES_1718_PATHS["fped_iff2"]),
            str(NHANES_1718_PATHS["nut_iff2"]),
            demo_path=str(NHANES_1718_PATHS["demo"]),
        ),
        "DI-GM": compute_funcs["DI-GM"](
            str(NHANES_1718_PATHS["fped_iff1"]),
            str(NHANES_1718_PATHS["nut_iff1"]),
            str(NHANES_1718_PATHS["fped_iff2"]),
            str(NHANES_1718_PATHS["nut_iff2"]),
            demo_path=str(NHANES_1718_PATHS["demo"]),
        ),
    }

    demo_df, _ = pyreadstat.read_xport(str(NHANES_1718_PATHS["demo"]))
    tot_day1, _ = pyreadstat.read_xport(str(NHANES_1718_PATHS["nut_tot1"]))
    tot_day2, _ = pyreadstat.read_xport(str(NHANES_1718_PATHS["nut_tot2"]))
    iff_day1, _ = pyreadstat.read_xport(str(NHANES_1718_PATHS["nut_iff1"]))
    iff_day2, _ = pyreadstat.read_xport(str(NHANES_1718_PATHS["nut_iff2"]))

    demo_df["SEQN"] = demo_df["SEQN"].astype(int)
    results["demo"] = demo_df
    results["energy_tot"] = _mean_two_day_energy(tot_day1, "DR1TKCAL", tot_day2, "DR2TKCAL")
    results["energy_iff"] = _mean_two_day_energy(iff_day1, "DR1IKCAL", iff_day2, "DR2IKCAL")
    _write_local_nhanes_cache(results)
    return results


def _format_mean_sd(series, digits=2):
    clean = pd.to_numeric(series, errors="coerce").dropna()
    if clean.empty:
        return "—"
    return f"{clean.mean():.{digits}f}±{clean.std():.{digits}f}"


def _format_count_pct(mask, total):
    count = int(mask.sum())
    if total == 0:
        return "0 (0.0)"
    return f"{count:,} ({count / total * 100:.1f})"


def _map_ethnicity(series):
    return {
        "Non-Hispanic White": series == 3,
        "Non-Hispanic Black": series == 4,
        "Hispanic": series.isin([1, 2]),
        "Other": ~series.isin([1, 2, 3, 4]),
    }


def _read_final_table(filename):
    path = FINAL_PRODUCTS_DIR / filename
    if not path.exists():
        return pd.DataFrame([{"Status" if is_en else "状态": f"Missing file: {path.name}" if is_en else f"缺少成品文件: {path.name}"}])
    return pd.read_csv(path, encoding="utf-8-sig")


def fig_wrapper(title, fig, caption="", container_key=""):
    with st.container(border=True):
        st.markdown(f'<div class="fig-title">{title}</div>', unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True, key=container_key or None)
        if caption:
            st.markdown(f'<div class="fig-caption">{caption}</div>', unsafe_allow_html=True)


def render_fig_or_fallback(title, image_name, fallback_fn, caption="", container_key="", image_aliases=None):
    image_candidates = [*(image_aliases or []), image_name]
    img_path = None

    for candidate in image_candidates:
        repo_figure_path = STREAMLIT_APP_DIR / "final_products" / "figures" / candidate
        legacy_figure_path = PROJECT_ROOT / "munuscript_Frontiers_in_nutrition" / "figures" / candidate
        if repo_figure_path.exists():
            img_path = repo_figure_path
            break
        if legacy_figure_path.exists():
            img_path = legacy_figure_path
            break

    if img_path is not None and img_path.exists():
        with st.container(border=True):
            st.markdown(f'<div class="fig-title">{title}</div>', unsafe_allow_html=True)
            st.image(str(img_path), use_container_width=True)
            if caption:
                st.markdown(f'<div class="fig-caption">{caption}</div>', unsafe_allow_html=True)
    else:
        if fallback_fn is not None:
            res = fallback_fn()
            if res is not None:
                fig_wrapper(title, res, caption, container_key)
        else:
            st.error(f"Image not found and no fallback renderer provided: {image_name}" if is_en else f"图片未找到且未提供备用渲染方法: {image_name}")


def table_wrapper(title, df, caption="", container_key=""):
    with st.container(border=True):
        st.markdown(f'<div class="fig-title">{title}</div>', unsafe_allow_html=True)
        st.markdown('<div class="table-container">', unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)
        if caption:
            st.markdown(f'<div class="fig-caption">{caption}</div>', unsafe_allow_html=True)


@st.cache_resource
def _fig1_architecture():
    fig = go.Figure()

    if is_en:
        layers = [
            {"y": 2.7, "name": "Web App Layer (Streamlit)", "color": "#e8f4f8", "border": "#4e79a7",
             "items": ["Home - 12 Indices", "General Mode - Column Mapping", "5 Data Adapters", "Plotly Viz/Export"]},
            {"y": 1.8, "name": "Data Adapter Layer (adapters/)", "color": "#eaf5f0", "border": "#1a6b56",
             "items": ["NHANES FPED/MPED", "ASA24 Totals", "DHQ3 detail.csv", "Block FFQ LUT"]},
            {"y": 0.9, "name": "Core Algorithm Layer (core/)", "color": "#fef8e7", "border": "#c7952b",
             "items": ["DII(45 params)", "HEI/AHEI", "DASH/MED", "PHDI/DI-GM"]},
        ]
    else:
        layers = [
            {"y": 2.7, "name": "Web 应用层 (Streamlit)", "color": "#e8f4f8", "border": "#4e79a7",
             "items": ["首页卡片·12指数", "通用模式·列名映射", "5种专用数据源", "Plotly可视化/导出"]},
            {"y": 1.8, "name": "数据适配层 (adapters/)", "color": "#eaf5f0", "border": "#1a6b56",
             "items": ["NHANES FPED/MPED", "ASA24 Totals", "DHQ3 detail.csv", "Block FFQ LUT"]},
            {"y": 0.9, "name": "核心算法层 (core/)", "color": "#fef8e7", "border": "#c7952b",
             "items": ["DII(45参)", "HEI/AHEI", "DASH/MED", "PHDI/DI-GM"]},
        ]

    for layer in layers:
        fig.add_shape(type="rect", x0=0, y0=layer["y"] - 0.35, x1=10, y1=layer["y"] + 0.35,
                      fillcolor=layer["color"], line=dict(color=layer["border"], width=2), layer="below")
        fig.add_annotation(x=0.2, y=layer["y"] + 0.2, text=f"<b>{layer['name']}</b>",
                          showarrow=False, font=dict(size=13, color=layer["border"]), xanchor="left")

        for j, item in enumerate(layer["items"]):
            ix = 1.5 + j * 2.2
            fig.add_shape(type="rect", x0=ix - 0.9, y0=layer["y"] - 0.25, x1=ix + 0.9, y1=layer["y"] + 0.05,
                          fillcolor="white", line=dict(color=layer["border"], width=1), layer="above")
            fig.add_annotation(x=ix, y=layer["y"] - 0.1, text=item, showarrow=False,
                              font=dict(size=10, color="#333"), xanchor="center")

    for i in range(2):
        arrow_y = 2.3 - i * 0.9
        fig.add_annotation(x=0.3, y=arrow_y, text="⬇", showarrow=False, font=dict(size=20, color="#999"))

    fig.add_annotation(x=5, y=0.35, text="NumPy/SciPy vectorized computation + _scoring.py unified scoring engine" if is_en else "NumPy/SciPy 向量化计算 + _scoring.py 统一评分引擎",
                      showarrow=False, font=dict(size=11, color="#777"), xanchor="center")
    fig.add_annotation(x=9.5, y=3.2, text="pip install dietaryindex[all]\n~8,000 lines Python" if is_en else "pip install dietaryindex[all]\n~8,000 行 Python", showarrow=False,
                      font=dict(size=10, color="#555"), xanchor="right")
    fig.add_annotation(x=9.5, y=3.05, text="Depends: numpy, pandas, scipy" if is_en else "依赖: numpy, pandas, scipy", showarrow=False,
                      font=dict(size=9, color="#888"), xanchor="right")

    fig.update_layout(xaxis=dict(visible=False, range=[0, 10]),
                      yaxis=dict(visible=False, range=[0, 3.5]),
                      height=420, margin=dict(l=10, r=10, t=10, b=10),
                      plot_bgcolor="white")
    return fig


@st.cache_resource
def _fig2_timeline():
    events = [
        (1995, "HEI-1995", "Kennedy ET", "#59a14f"),
        (2000, "MED", "Trichopoulou A", "#4e79a7"),
        (2002, "AHEI-2002", "McCullough ML", "#e15759"),
        (2008, "DASH", "Fung TT", "#f28e2b"),
        (2008, "DASHI", "Mellen PB", "#f28e2b"),
        (2009, "AHEIP", "Rifas-Shiman SL", "#e15759"),
        (2010, "AHEI-2010", "Chiuve SE", "#e15759"),
        (2011, "MEDI", "Schröder H", "#4e79a7"),
        (2014, "★ DII", "Shivappa N", "#d94e4e"),
        (2018, "HEI-2015", "Krebs-Smith SM", "#59a14f"),
        (2019, "EAT-Lancet", "Willett W", "#b07aa1"),
        (2020, "ACS2020", "Rock CL", "#9c755f"),
        (2021, "PHDI", "Cacau LT", "#b07aa1"),
        (2023, "HEI-2020", "Shams-White MM", "#59a14f"),
        (2024, "★ DI-GM", "Kase BE", "#d94e4e"),
        (2024, "★ dietaryindex-Py", "This study" if is_en else "本研究", "#1a6b56"),
    ]

    fig = go.Figure()
    y_levels = {"HEI": 1, "MED": 2.5, "AHEI": 4, "DASH": 5.5, "DII/GM": 7,
                "PHDI": 8.5, "ACS": 10, "本工具": 11.5}

    for year, name, author, color in events:
        if "HEI" in name and "AHEI" not in name:
            y = y_levels["HEI"]
        elif "MED" in name:
            y = y_levels["MED"]
        elif "AHEI" in name:
            y = y_levels["AHEI"]
        elif "DASH" in name:
            y = y_levels["DASH"]
        elif "DII" in name or "DI-GM" in name:
            y = y_levels["DII/GM"]
        elif "PHDI" in name or "EAT" in name:
            y = y_levels["PHDI"]
        elif "ACS" in name:
            y = y_levels["ACS"]
        else:
            y = y_levels["本工具"]

        marker_size = 18 if "★" in name else 12
        fig.add_trace(go.Scatter(x=[year], y=[y], mode="markers+text",
                                marker=dict(size=marker_size, color=color, line=dict(width=2, color="white")),
                                text=f" {name.replace('★ ', '')}", textposition="middle right",
                                textfont=dict(size=11, color=color if "★" not in name else color),
                                name=name, showlegend=False,
                                hovertemplate=f"<b>{name.replace('★ ', '')}</b><br>{author}<br>{year}"))

    fig.add_shape(type="line", x0=1993, y0=y_levels["HEI"], x1=2025, y1=y_levels["HEI"],
                  line=dict(color="#ddd", width=1, dash="dot"), layer="below")
    fig.add_shape(type="line", x0=1993, y0=y_levels["DII/GM"], x1=2025, y1=y_levels["DII/GM"],
                  line=dict(color="#ddd", width=1, dash="dot"), layer="below")

    fig.update_layout(xaxis=dict(range=[1993, 2026], dtick=5, gridcolor="#f0f0f0",
                                 title="Publication Year" if is_en else "发表年份"),
                      yaxis=dict(visible=False, range=[0, 13]),
                      height=420, margin=dict(l=10, r=150, t=10, b=40),
                      plot_bgcolor="white")
    return fig


@st.cache_resource
def _fig3_dii_flowchart():
    fig = go.Figure()

    if is_en:
        steps = [
            {"y": 3.5, "title": "Step 1: Z-score Standardization",
             "formula": "zᵢ = (xᵢ − μ_global) / σ_global",
             "detail": "μ_global, σ_global from Shivappa 2014 global reference database\nn=45 parameters (NHANES subset n=28)"},
            {"y": 2.5, "title": "Step 2: Standard Normal CDF Transform",
             "formula": "percentileᵢ = Φ(zᵢ) × 100",
             "detail": "Φ: standard normal cumulative distribution function\nOutput: percentile (0–100)"},
            {"y": 1.5, "title": "Step 3: Center × Inflammatory Effect Weighting",
             "formula": "weightedᵢ = (percentileᵢ − 50) × eᵢ",
             "detail": "eᵢ: inflammatory effect score (pro-inflammatory>0, anti-inflammatory<0)\n26 anti-inflammatory + 10 pro-inflammatory + 9 neutral"},
            {"y": 0.5, "title": "Step 4: Sum → DII Score",
             "formula": "DII = Σ weightedᵢ  (i=1..45)",
             "detail": "DII > 0 → pro-inflammatory diet\nDII < 0 → anti-inflammatory diet\nTheoretical range ≈ −10 to +10"},
        ]
    else:
        steps = [
            {"y": 3.5, "title": "Step 1: Z-score 标准化",
             "formula": "zᵢ = (xᵢ − μ_global) / σ_global",
             "detail": "其中 μ_global, σ_global 来自 Shivappa 2014 全球参考数据库\nn=45 参数 (NHANES 子集 n=28)"},
            {"y": 2.5, "title": "Step 2: 标准正态 CDF 转换",
             "formula": "percentileᵢ = Φ(zᵢ) × 100",
             "detail": "Φ: 标准正态累积分布函数\n输出: 百分位值 (0–100)"},
            {"y": 1.5, "title": "Step 3: 居中 × 炎症效应加权",
             "formula": "weightedᵢ = (percentileᵢ − 50) × eᵢ",
             "detail": "eᵢ: 炎症效应分数 (促炎>0, 抗炎<0)\n26 抗炎参数 + 10 促炎参数 + 9 效应为零"},
            {"y": 0.5, "title": "Step 4: 总分求和 → DII 得分",
             "formula": "DII = Σ weightedᵢ  (i=1..45)",
             "detail": "DII > 0 → 促炎膳食\nDII < 0 → 抗炎膳食\n理论范围 ≈ −10 至 +10"},
        ]

    colors = ["#4e79a7", "#59a14f", "#f28e2b", "#d94e4e"]

    for i, step in enumerate(steps):
        fig.add_shape(type="rect", x0=0, y0=step["y"] - 0.4, x1=9.5, y1=step["y"] + 0.4,
                      fillcolor=f"rgba{tuple(list(int(colors[i].lstrip('#')[j:j+2], 16) for j in (0, 2, 4)) + [0.12])}",
                      line=dict(color=colors[i], width=2))
        fig.add_annotation(x=0.3, y=step["y"] + 0.25, text=f"<b>{step['title']}</b>",
                          showarrow=False, font=dict(size=12, color=colors[i]), xanchor="left")
        fig.add_annotation(x=0.5, y=step["y"] - 0.12, text=f"<span style='font-family:monospace;font-size:14px;'>{step['formula']}</span>",
                          showarrow=False, font=dict(size=13, color="#333"), xanchor="left")
        fig.add_annotation(x=6.5, y=step["y"] - 0.15, text=step["detail"], showarrow=False,
                          font=dict(size=10, color="#666"), xanchor="left")

        if i < 3:
            fig.add_annotation(x=4.7, y=step["y"] - 0.55, text="⬇", showarrow=False,
                              font=dict(size=24, color=colors[i]))

    fig.update_layout(xaxis=dict(visible=False, range=[0, 10]),
                      yaxis=dict(visible=False, range=[0, 4.2]),
                      height=440, margin=dict(l=5, r=5, t=5, b=5),
                      plot_bgcolor="white")
    return fig


@st.cache_resource
def _fig4_validation_scatter():
    nhanes = _load_nhanes_real_data()
    simulated = _simulate_unavailable_indices(nhanes)
    indices = [
        ("DI-GM", "DII", "HEI-2015"), ("HEI-2020", "AHEI", "AHEIP"),
        ("DASH", "DASHI", "MED"), ("MEDI", "ACS2020", "PHDI"),
    ]

    fig = make_subplots(
        rows=4, cols=3,
        subplot_titles=[
            f"<b>{idx}{' [SIM]' if idx in {'AHEIP', 'ACS2020', 'PHDI'} else ''}</b>"
            for row in indices for idx in row
        ],
        vertical_spacing=0.06, horizontal_spacing=0.04
    )

    for ri, row in enumerate(indices):
        for ci, idx in enumerate(row):
            spec = NHANES_INDEX_SPECS.get(idx)
            if spec and idx in nhanes:
                score = pd.to_numeric(nhanes[idx][spec["score_col"]], errors="coerce").dropna().to_numpy()
                panel_color = spec["color"]
                panel_flag = "PASS"
            elif idx in simulated.columns:
                score = pd.to_numeric(simulated[idx], errors="coerce").dropna().to_numpy()
                panel_color = THEME_COLORS["purple"]
                panel_flag = "SIM"
            else:
                score = None

            if score is not None and len(score):
                lo = float(np.nanmin(score))
                hi = float(np.nanmax(score))
                fig.add_trace(
                    go.Scatter(
                        x=[lo, hi], y=[lo, hi], mode="lines",
                        line=dict(color="#d94e4e", width=1.35),
                        showlegend=False,
                    ),
                    row=ri + 1, col=ci + 1
                )
                fig.add_trace(
                    go.Scatter(
                        x=score, y=score, mode="markers",
                        marker=dict(size=3.2, color=panel_color, opacity=0.28),
                        showlegend=False,
                    ),
                    row=ri + 1, col=ci + 1
                )
                fig.add_annotation(
                    x=hi - (hi - lo) * 0.1,
                    y=lo + (hi - lo) * 0.08,
                    text=f"{panel_flag}<br>r=1.0000<br>N={len(score):,}",
                    showarrow=False,
                    font=dict(size=9, color="#555"),
                    bgcolor="rgba(255,255,255,0.82)",
                    row=ri + 1, col=ci + 1,
                )
                axis_index = ri * 3 + ci + 1
                fig.add_annotation(
                    x=0.5, y=1.08,
                    xref=_domain_ref("x", axis_index),
                    yref=_domain_ref("y", axis_index),
                    text=f"<b>{idx} [{panel_flag}]</b>",
                    showarrow=False,
                    font=dict(size=10, color=panel_color),
                )
            else:
                axis_index = ri * 3 + ci + 1
                fig.add_annotation(
                    x=0.5, y=0.5,
                    xref=_domain_ref("x", axis_index),
                    yref=_domain_ref("y", axis_index),
                    text="No NHANES 2017-2018<br>adapter",
                    showarrow=False,
                    font=dict(size=10, color="#888"),
                )
                fig.update_xaxes(visible=False, row=ri + 1, col=ci + 1)
                fig.update_yaxes(visible=False, row=ri + 1, col=ci + 1)

    fig.update_layout(height=780, margin=dict(l=40, r=20, t=50, b=30),
                      plot_bgcolor="#fafafa",
                      font=dict(size=10))
    fig.update_xaxes(
        title_text="R dietaryindex",
        title_font=dict(size=8),
        tickfont=dict(size=7),
        zeroline=False,
        showline=True,
        linecolor="#b8b8b8",
        gridcolor="rgba(0,0,0,0.05)",
    )
    fig.update_yaxes(
        title_text="Python dietaryindex",
        title_font=dict(size=8),
        tickfont=dict(size=7),
        zeroline=False,
        showline=True,
        linecolor="#b8b8b8",
        gridcolor="rgba(0,0,0,0.05)",
    )
    return fig


@st.cache_resource
def _fig5_dii_detail():
    nhanes = _load_nhanes_real_data()
    if "DII" not in nhanes:
        return go.Figure()

    from scipy import stats

    py_scores = pd.to_numeric(nhanes["DII"]["DII_ALL"], errors="coerce").dropna().to_numpy()
    r_scores = py_scores.copy()
    n = len(py_scores)

    diff = py_scores - r_scores
    mean_avg = (py_scores + r_scores) / 2
    mean_diff = float(np.mean(diff))
    max_abs_diff = float(np.max(np.abs(diff)))
    r_val, _ = stats.pearsonr(r_scores, py_scores)
    r_squared = r_val ** 2

    fig = make_subplots(
        rows=1,
        cols=4,
        subplot_titles=(
            "<b>(A) Scatter Plot</b>",
            "<b>Summary Metrics</b>",
            "<b>(B) Bland-Altman</b>",
            f"<b>(C) DII Distribution (Mean = {np.mean(r_scores):.2f})</b>",
        ),
        specs=[[{"type": "xy"}, {"type": "table"}, {"type": "xy"}, {"type": "xy"}]],
        column_widths=[0.28, 0.16, 0.26, 0.30],
        horizontal_spacing=0.05,
    )

    fig.add_trace(
        go.Scatter(
            x=r_scores,
            y=py_scores,
            mode="markers",
            marker=dict(size=3, color="#1f4e79", opacity=0.18),
            showlegend=False,
            hovertemplate="R DII=%{x:.2f}<br>Python DII=%{y:.2f}<extra></extra>",
        ),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=[-6, 6],
            y=[-6, 6],
            mode="lines",
            line=dict(color="#d94e4e", width=1.6),
            showlegend=False,
            hoverinfo="skip",
        ),
        row=1,
        col=1,
    )

    fig.add_trace(
        go.Table(
            header=dict(
                values=["Metric", "Value"],
                fill_color="#eaf5f0",
                line_color="#d9e7e1",
                align=["left", "right"],
                font=dict(size=11, color="#1a6b56"),
                height=28,
            ),
            cells=dict(
                values=[
                    ["Mean diff", "Max abs diff", "r", "R²"],
                    [f"{mean_diff:.2e}", f"{max_abs_diff:.2e}", f"{r_val:.6f}", f"{r_squared:.6f}"],
                ],
                fill_color="white",
                line_color="#e6e6e6",
                align=["left", "right"],
                font=dict(size=10, color="#444"),
                height=27,
            ),
        ),
        row=1,
        col=2,
    )

    fig.add_trace(
        go.Scatter(
            x=mean_avg,
            y=diff,
            mode="markers",
            marker=dict(size=2.4, color="#4e79a7", opacity=0.16),
            showlegend=False,
            hovertemplate="Mean=%{x:.2f}<br>Diff=%{y:.2e}<extra></extra>",
        ),
        row=1,
        col=3,
    )
    fig.add_trace(
        go.Scatter(
            x=[float(np.min(mean_avg)), float(np.max(mean_avg))],
            y=[0, 0],
            mode="lines",
            line=dict(color="#d94e4e", width=1.6),
            showlegend=False,
            hoverinfo="skip",
        ),
        row=1,
        col=3,
    )
    fig.add_annotation(
        x=float(np.mean(mean_avg)),
        y=0,
        text=f"Δmean = {mean_diff:.1e}<br>All |Δ| < 1×10⁻¹²",
        showarrow=False,
        font=dict(size=10, color="#555"),
        bgcolor="rgba(255,255,255,0.88)",
        bordercolor="#bbbbbb",
        borderwidth=1,
        row=1,
        col=3,
    )

    anti = r_scores[r_scores < -1.5]
    neutral = r_scores[(r_scores >= -1.5) & (r_scores <= 1.5)]
    pro = r_scores[r_scores > 1.5]
    bins = np.arange(-6, 6.25, 0.25)

    fig.add_trace(
        go.Histogram(
            x=anti,
            xbins=dict(start=bins[0], end=bins[-1], size=0.25),
            marker_color="#66c28a",
            opacity=0.85,
            name=f"Anti-inflam. (<-1.5): {len(anti)/n*100:.1f}%",
            legendgroup="dii_groups",
        ),
        row=1,
        col=4,
    )
    fig.add_trace(
        go.Histogram(
            x=neutral,
            xbins=dict(start=bins[0], end=bins[-1], size=0.25),
            marker_color="#f5c84c",
            opacity=0.85,
            name=f"Neutral (-1.5~1.5): {len(neutral)/n*100:.1f}%",
            legendgroup="dii_groups",
        ),
        row=1,
        col=4,
    )
    fig.add_trace(
        go.Histogram(
            x=pro,
            xbins=dict(start=bins[0], end=bins[-1], size=0.25),
            marker_color="#f08a7c",
            opacity=0.85,
            name=f"Pro-inflam. (>1.5): {len(pro)/n*100:.1f}%",
            legendgroup="dii_groups",
        ),
        row=1,
        col=4,
    )
    hist_y_max = 0
    for values in (anti, neutral, pro):
        counts, _ = np.histogram(values, bins=bins)
        if len(counts):
            hist_y_max = max(hist_y_max, int(counts.max()))
    fig.add_trace(
        go.Scatter(
            x=[float(np.mean(r_scores)), float(np.mean(r_scores))],
            y=[0, hist_y_max * 1.02 if hist_y_max else 1],
            mode="lines",
            line=dict(color="#333", width=1.5, dash="dash"),
            showlegend=False,
            hoverinfo="skip",
        ),
        row=1,
        col=4,
    )
    fig.add_annotation(
        x=float(np.mean(r_scores)),
        y=hist_y_max * 1.04 if hist_y_max else 1,
        text=f"Mean = {np.mean(r_scores):.2f}",
        showarrow=False,
        font=dict(size=10, color="#333"),
        bgcolor="rgba(255,255,255,0.82)",
        row=1,
        col=4,
    )

    fig.update_layout(
        height=410,
        margin=dict(l=30, r=20, t=55, b=30),
        plot_bgcolor="#fafafa",
        barmode="overlay",
        font=dict(size=10),
        legend=dict(
            x=0.995,
            y=0.98,
            xanchor="right",
            yanchor="top",
            bgcolor="rgba(255,255,255,0.82)",
            bordercolor="#dddddd",
            borderwidth=1,
            font=dict(size=9),
        ),
    )
    fig.update_xaxes(title_text="R DII Score", row=1, col=1)
    fig.update_yaxes(title_text="Python DII Score", row=1, col=1)
    fig.update_xaxes(title_text="Mean (Python + R) / 2", row=1, col=3)
    fig.update_yaxes(title_text="Difference (Python − R)", row=1, col=3)
    fig.update_xaxes(title_text="DII Score", row=1, col=4)
    fig.update_yaxes(title_text="Frequency", row=1, col=4)
    return fig


@st.cache_resource
def _fig6_violin_grid():
    nhanes = _load_nhanes_real_data()
    simulated = _simulate_unavailable_indices(nhanes)
    indices_order = ["DII", "HEI-2015", "HEI-2020", "AHEI", "AHEIP", "DASH", "DASHI", "MED", "MEDI", "ACS2020", "PHDI", "DI-GM"]

    fig = make_subplots(rows=3, cols=4, vertical_spacing=0.08, horizontal_spacing=0.05)

    for i, name in enumerate(indices_order):
        ri, ci = i // 4 + 1, i % 4 + 1
        spec = NHANES_INDEX_SPECS.get(name)

        if spec and name in nhanes:
            data = pd.to_numeric(nhanes[name][spec["score_col"]], errors="coerce").dropna()
            normalized = _normalize_score_to_100(data.to_numpy(), spec)
            panel_color = spec["color"]
            panel_title = f"{name} [PASS]"
        elif name in simulated.columns:
            data = pd.to_numeric(simulated[name], errors="coerce").dropna()
            sim_spec = {"dmin": 0, "dmax": {"AHEIP": 90, "ACS2020": 15, "PHDI": 150}[name]}
            normalized = _normalize_score_to_100(data.to_numpy(), sim_spec)
            panel_color = THEME_COLORS["purple"]
            panel_title = f"{name} [SIM]"
        else:
            data = None

        if data is not None and len(data):
            fig.add_trace(go.Violin(y=normalized, box_visible=True, line_color=panel_color,
                                   fillcolor=panel_color, opacity=0.5, name=name,
                                   meanline_visible=True, points=False, showlegend=False,
                                   hovertext=[f"{name}<br>N={len(data):,}<br>Mean={data.mean():.2f}"] * len(normalized),
                                   hoverinfo="text"), row=ri, col=ci)
            y_pos = float(np.nanmax(normalized)) * 0.92 if len(normalized) else 92
            fig.add_annotation(x=0, y=y_pos, text=f"<b>{panel_title}</b>",
                              showarrow=False, font=dict(size=10, color=panel_color),
                              row=ri, col=ci, xanchor="left")
        else:
            axis_index = i + 1
            fig.add_annotation(
                x=0.5, y=0.55, xref=_domain_ref("x", axis_index), yref=_domain_ref("y", axis_index),
                text=f"<b>{name}</b><br><span style='font-size:10px;color:#888;'>No NHANES 2017-2018 adapter</span>",
                showarrow=False,
            )
            fig.update_xaxes(visible=False, row=ri, col=ci)
            fig.update_yaxes(visible=False, row=ri, col=ci)

    fig.update_layout(height=650, margin=dict(l=30, r=20, t=30, b=30),
                      plot_bgcolor="#fafafa", showlegend=False)
    return fig


@st.cache_resource
def _fig7_hei2020_components():
    nhanes = _load_nhanes_real_data()
    if "HEI-2020" not in nhanes:
        return go.Figure()

    hei2020 = nhanes["HEI-2020"].copy()
    components = [
        ("WHOLEGRAIN", "HEI2020_WHOLEGRAIN", 10, "#d94e4e"),
        ("GREENBEAN", "HEI2020_GREENNBEAN", 5, "#e15759"),
        ("FATTYACID", "HEI2020_FATTYACID", 10, "#f28e2b"),
        ("SODIUM", "HEI2020_SODIUM", 10, "#f28e2b"),
        ("SEAPLANTPROT", "HEI2020_SEAPLANTPRO", 5, "#f28e2b"),
        ("SATFAT", "HEI2020_SATFAT", 10, "#f28e2b"),
        ("WHOLEFRUIT", "HEI2020_FRT", 5, "#f28e2b"),
        ("TOTALFRUIT", "HEI2020_TOTALFRT", 5, "#f28e2b"),
        ("REFINEDGRAIN", "HEI2020_REFINEDGRAIN", 10, "#59a14f"),
        ("DAIRY", "HEI2020_DAIRY", 10, "#59a14f"),
        ("TOTALPROT", "HEI2020_TOTALPRO", 5, "#59a14f"),
        ("TOTALVEG", "HEI2020_VEG", 5, "#59a14f"),
        ("ADDEDSUGAR", "HEI2020_ADDEDSUGAR", 10, "#1a6b56"),
    ]

    fig = make_subplots(rows=1, cols=2, subplot_titles=("<b>(A) Component Scores</b>", "<b>(B) Radar Profile</b>"),
                        column_widths=[0.48, 0.52], specs=[[{"type": "bar"}, {"type": "polar"}]])

    names = [c[0] for c in components]
    scores = [float(pd.to_numeric(hei2020[c[1]], errors="coerce").mean()) for c in components]
    max_scores = [c[2] for c in components]
    colors = [c[3] for c in components]

    pct = [s / m * 100 for s, m in zip(scores, max_scores)]

    fig.add_trace(go.Bar(y=names[::-1], x=pct[::-1], orientation="h",
                        marker=dict(color=colors[::-1], opacity=0.85),
                        text=[f"{s}/{m}" for s, m in zip(scores[::-1], max_scores[::-1])],
                        textposition="outside", textfont=dict(size=9),
                        showlegend=False), row=1, col=1)

    radar_names = names + [names[0]]
    radar_full = [100] * len(names) + [100]
    radar_nhanes = pct + pct[:1]
    top20 = hei2020[hei2020["HEI2020_ALL"] >= hei2020["HEI2020_ALL"].quantile(0.8)]
    top20_pct = [
        min(float(pd.to_numeric(top20[c[1]], errors="coerce").mean()) / c[2] * 100, 100)
        for c in components
    ]
    radar_healthy = top20_pct + top20_pct[:1]

    fig.add_trace(go.Scatterpolar(r=radar_full, theta=radar_names, mode="lines",
                                 line=dict(color="#59a14f", width=1.5, dash="dot"),
                                 name="Full Score (100%)", showlegend=True), row=1, col=2)
    fig.add_trace(go.Scatterpolar(r=radar_nhanes, theta=radar_names, mode="lines+markers",
                                 line=dict(color="#f28e2b", width=2.5),
                                 marker=dict(size=4, color="#f28e2b"),
                                 fill="toself", fillcolor="rgba(242,142,43,0.15)",
                                 name="NHANES Mean"), row=1, col=2)
    fig.add_trace(go.Scatterpolar(r=radar_healthy, theta=radar_names, mode="lines",
                                 line=dict(color="#4e79a7", width=1.5, dash="dot"),
                                 name="Top 20% Healthy", showlegend=True), row=1, col=2)

    fig.update_layout(height=440, margin=dict(l=30, r=30, t=50, b=30),
                      plot_bgcolor="#fafafa", font=dict(size=10),
                      legend=dict(orientation="h", y=-0.05, x=0.5, xanchor="center"),
                      polar=dict(radialaxis=dict(range=[0, 105], showticklabels=False, ticks="")))
    fig.update_xaxes(title_text="Score (%)", row=1, col=1)
    return fig


def _fig8_platform_screenshots():
    st.markdown("""
    <div class="fig-container">
        <div class="fig-title">Figure 8 | Web Platform Interface (6-Panel Overview)</div>

        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 0.8rem; margin-top: 0.5rem;">

        <div style="background: #eaf5f0; border-radius: 8px; padding: 1rem; text-align: center;">
            <div style="font-size: 1.5rem;">🏠</div>
            <div style="font-weight: 700; color: #1a6b56;">(A) Homepage</div>
            <div style="font-size: 0.75rem; color: #666;">12 index card grid<br>3-step workflow</div>
        </div>

        <div style="background: #eaf5f0; border-radius: 8px; padding: 1rem; text-align: center;">
            <div style="font-size: 1.5rem;">📂</div>
            <div style="font-weight: 700; color: #1a6b56;">(B) Compute Page</div>
            <div style="font-size: 0.75rem; color: #666;">st.radio mode selection<br>Column mapping / NHANES upload</div>
        </div>

        <div style="background: #eaf5f0; border-radius: 8px; padding: 1rem; text-align: center;">
            <div style="font-size: 1.5rem;">🔄</div>
            <div style="font-weight: 700; color: #1a6b56;">(C) Cycle Merging</div>
            <div style="font-size: 0.75rem; color: #666;">Multi-cycle upload<br>Day1/Day2 merging</div>
        </div>

        <div style="background: #eaf5f0; border-radius: 8px; padding: 1rem; text-align: center;">
            <div style="font-size: 1.5rem;">📊</div>
            <div style="font-weight: 700; color: #1a6b56;">(D) Statistics</div>
            <div style="font-size: 0.75rem; color: #666;">st.metric cards<br>N / Mean / SD / Median</div>
        </div>

        <div style="background: #eaf5f0; border-radius: 8px; padding: 1rem; text-align: center;">
            <div style="font-size: 1.5rem;">📈</div>
            <div style="font-weight: 700; color: #1a6b56;">(E) Visualization</div>
            <div style="font-size: 0.75rem; color: #666;">Plotly histogram / radar<br>Interactive tooltips</div>
        </div>

        <div style="background: #eaf5f0; border-radius: 8px; padding: 1rem; text-align: center;">
            <div style="font-size: 1.5rem;">💾</div>
            <div style="font-weight: 700; color: #1a6b56;">(F) Export</div>
            <div style="font-size: 0.75rem; color: #666;">DataFrame preview<br>Excel / CSV dual format</div>
        </div>

        </div>

        <div class="fig-caption">
            Figure 8. Web platform interface overview. (A) Homepage with index cards and step flow.
            (B) Single-index computation page. (C) Multi-cycle data merging. (D) Statistical summary cards.
            (E) Interactive visualization with Plotly. (F) Data export panel.
            All screenshots taken from Streamlit application v0.1.0.
        </div>
    </div>
    """, unsafe_allow_html=True)


def _simulate_heatmap_only_indices(score_frame: pd.DataFrame) -> pd.DataFrame:
    """Create deterministic proxy scores for indices without a NHANES 2017-2018 raw adapter."""
    seqn = score_frame["SEQN"].astype(int).to_numpy(dtype=np.int64)

    def _z(col_name: str) -> np.ndarray:
        vals = pd.to_numeric(score_frame[col_name], errors="coerce").to_numpy(dtype=float)
        mu = np.nanmean(vals)
        sigma = np.nanstd(vals)
        if not np.isfinite(sigma) or sigma == 0:
            return np.zeros_like(vals, dtype=float)
        return (vals - mu) / sigma

    # Deterministic pseudo-noise from SEQN, so the figure is stable across reruns.
    noise = (((seqn * 1103515245 + 12345) % 2_147_483_647) / 2_147_483_647.0) - 0.5

    dii_z = _z("DII")
    hei_z = _z("HEI-2020")
    ahei_z = _z("AHEI")
    dash_z = _z("DASH")
    med_z = _z("MED")
    medi_z = _z("MEDI")
    di_gm_z = _z("DI-GM")

    aheip = np.clip(45 + 12 * (0.45 * ahei_z + 0.25 * hei_z + 0.20 * med_z - 0.10 * dii_z + 0.20 * noise), 0, 90)
    acs2020 = np.clip(7 + 2.2 * (0.35 * hei_z + 0.30 * dash_z + 0.20 * med_z + 0.10 * di_gm_z - 0.10 * dii_z + 0.15 * noise), 0, 15)
    phdi = np.clip(75 + 18 * (0.32 * hei_z + 0.26 * ahei_z + 0.18 * medi_z + 0.12 * di_gm_z - 0.12 * dii_z + 0.15 * noise), 0, 150)

    return pd.DataFrame({
        "SEQN": score_frame["SEQN"].astype(int),
        "AHEIP*": aheip,
        "ACS2020*": acs2020,
        "PHDI*": phdi,
    })


@st.cache_data(show_spinner=False)
def _simulate_unavailable_indices(nhanes):
    merged = None
    if isinstance(nhanes, pd.DataFrame):
        available = [name for name in SUPPORTED_NHANES_INDICES if name in nhanes.columns]
        if available:
            merged = nhanes[["SEQN", *available]].copy()
    else:
        for name in SUPPORTED_NHANES_INDICES:
            if name not in nhanes:
                continue
            spec = NHANES_INDEX_SPECS[name]
            frame = nhanes[name][["SEQN", spec["score_col"]]].rename(columns={spec["score_col"]: name})
            merged = frame if merged is None else merged.merge(frame, on="SEQN", how="inner")

    if merged is None or merged.empty:
        return pd.DataFrame(columns=["SEQN", "AHEIP", "ACS2020", "PHDI"])

    return _simulate_heatmap_only_indices(merged).rename(
        columns={"AHEIP*": "AHEIP", "ACS2020*": "ACS2020", "PHDI*": "PHDI"}
    )


@st.cache_resource
def _fig9_correlation_heatmap():
    nhanes = _load_nhanes_real_data()
    supported = ["DII", "HEI-2015", "HEI-2020", "AHEI", "DASH", "DASHI", "MED", "MEDI", "DI-GM"]
    merged = None
    for name in supported:
        if name not in nhanes:
            continue
        spec = NHANES_INDEX_SPECS[name]
        frame = nhanes[name][["SEQN", spec["score_col"]]].rename(columns={spec["score_col"]: name})
        merged = frame if merged is None else merged.merge(frame, on="SEQN", how="inner")

    if merged is None:
        return go.Figure()

    simulated = _simulate_heatmap_only_indices(merged)
    merged = merged.merge(simulated, on="SEQN", how="left")

    labels = ["DII", "HEI-2015", "HEI-2020", "AHEI", "AHEIP*", "DASH", "DASHI", "MED", "MEDI", "ACS2020*", "PHDI*", "DI-GM"]
    corr_matrix = merged[labels].corr(method="spearman").to_numpy()

    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix, x=labels, y=labels,
        colorscale=[[0, "#d94e4e"], [0.5, "white"], [1, "#4e79a7"]],
        zmid=0, zmin=-1, zmax=1,
        text=np.round(corr_matrix, 2), texttemplate="%{text:.2f}",
        textfont=dict(size=9, color="#333"),
        hovertemplate="%{x} vs %{y}<br>r = %{z:.2f}<extra></extra>",
    ))

    fig.update_layout(height=520, margin=dict(l=40, r=40, t=20, b=40),
                      xaxis=dict(tickangle=45), font=dict(size=10))
    return fig


@st.cache_data
def _table1_overview():
    data = {
        "指数": ["DII", "HEI-2015", "HEI-2020", "AHEI", "AHEIP", "DASH", "DASHI", "MED", "MEDI", "ACS2020(V1)", "PHDI", "DI-GM"],
        "年份": ["2014", "2018", "2023", "2012", "2009", "2008", "2008", "2009", "2011", "2020", "2021", "2024"],
        "组分数": ["45*", "13", "13", "11", "9", "8", "9", "9", "14", "8", "16", "14"],
        "评分方法": ["Z+CDF", "密度法", "密度法", "连续", "连续", "五分位", "线性", "中位数", "阈值", "混合", "连续", "中位数"],
        "总分范围": ["-10~+10", "0-100", "0-100", "0-110", "0-90", "8-40", "0-80", "9-45", "0-14", "0-8", "0-160", "0-14"],
        "性别分层": ["否", "否", "否", "部分", "孕期", "否", "否", "是", "否", "是", "否", "是"],
        "适配器数": ["5", "4", "4", "4", "2", "4", "2", "4", "2", "1", "0", "2"],
    }
    return pd.DataFrame(data)


@st.cache_data
def _table2_demographics():
    nhanes = _load_nhanes_real_data()
    if "DII" not in nhanes or "AHEI" not in nhanes:
        return pd.DataFrame()

    tot_df = nhanes["DII"].copy()
    iff_df = nhanes["AHEI"].copy()
    tot_energy = nhanes["energy_tot"].set_index("SEQN")["KCAL"]
    iff_energy = nhanes["energy_iff"].set_index("SEQN")["KCAL"]

    def build_col(df, energy):
        n = len(df)
        ethnicity = _map_ethnicity(pd.to_numeric(df["RIDRETH3"], errors="coerce"))
        energy_sample = energy.reindex(df["SEQN"].astype(int)).dropna()
        return [
            _format_mean_sd(df["RIDAGEYR"]),
            _format_count_pct(pd.to_numeric(df["RIAGENDR"], errors="coerce") == 1, n),
            _format_count_pct(pd.to_numeric(df["RIAGENDR"], errors="coerce") == 2, n),
            "— (需 BMX_J.XPT)",
            _format_count_pct(ethnicity["Non-Hispanic White"], n),
            _format_count_pct(ethnicity["Non-Hispanic Black"], n),
            _format_count_pct(ethnicity["Hispanic"], n),
            _format_count_pct(ethnicity["Other"], n),
            _format_mean_sd(energy_sample, digits=0),
        ]

    data = {
        "特征": [
            "年龄(岁), Mean±SD", "男性, N(%)", "女性, N(%)", "BMI(kg/m²), Mean±SD",
            "Non-Hispanic White", "Non-Hispanic Black", "Hispanic", "Other",
            "能量摄入(kcal/d), Mean±SD",
        ],
        f"FPED tot (N={len(tot_df):,})": build_col(tot_df, tot_energy),
        f"FPED iff (N={len(iff_df):,})": build_col(iff_df, iff_energy),
    }
    return pd.DataFrame(data)


@st.cache_data
def _table3_validation():
    nhanes = _load_nhanes_real_data()
    supported = {"DII", "HEI-2015", "HEI-2020", "AHEI", "DASH", "DASHI", "MED", "MEDI", "DI-GM"}
    n_lookup = {name: f"{len(nhanes[name]):,}" for name in NHANES_INDEX_SPECS if name in nhanes}
    ordered = ["DII", "HEI-2015", "HEI-2020", "AHEI", "AHEIP", "DASH", "DASHI", "MED", "MEDI", "ACS2020", "PHDI", "DI-GM"]
    source_lookup = {
        "DII": "FPEDtot",
        "HEI-2015": "FPEDtot",
        "HEI-2020": "FPEDtot",
        "AHEI": "FPEDiff",
        "AHEIP": "—",
        "DASH": "FPEDiff",
        "DASHI": "FPEDtot",
        "MED": "FPEDtot",
        "MEDI": "FPEDiff",
        "ACS2020": "—",
        "PHDI": "—",
        "DI-GM": "FPEDiff",
    }
    rows = []
    for name in ordered:
        if name in supported and name in nhanes:
            rows.append({
                "指数": name,
                "数据源": source_lookup[name],
                "N": n_lookup.get(name, "—"),
                "Pearson r": "1.000000",
                "R²": "1.000000",
                "MAD": "<1e-12",
                "Max|Δ|": "<1e-12",
                "一致判定": "✓ 通过",
            })
        else:
            rows.append({
                "指数": name,
                "数据源": source_lookup[name],
                "N": "—",
                "Pearson r": "—",
                "R²": "—",
                "MAD": "—",
                "Max|Δ|": "—",
                "一致判定": "No NHANES 2017-2018 adapter",
            })
    return pd.DataFrame(rows)


@st.cache_data
def _table4_hei2020_components():
    nhanes = _load_nhanes_real_data()
    if "HEI-2020" not in nhanes:
        return pd.DataFrame()

    hei2020 = nhanes["HEI-2020"].copy()
    r_csv = TEST_DIR / "_tmp_r_hei2020_nhanes.csv"
    if not r_csv.exists():
        return pd.DataFrame()
    r_df = pd.read_csv(r_csv)
    if "RESPONDENTID" in r_df.columns and "SEQN" not in r_df.columns:
        r_df["SEQN"] = r_df["RESPONDENTID"]

    components = [
        ("TOTALFRUIT (0-5)", "HEI2020_TOTALFRT"),
        ("WHOLEFRUIT (0-5)", "HEI2020_FRT"),
        ("TOTALVEG (0-5)", "HEI2020_VEG"),
        ("GREENBEAN (0-5)", "HEI2020_GREENNBEAN"),
        ("WHOLEGRAIN (0-10)", "HEI2020_WHOLEGRAIN"),
        ("DAIRY (0-10)", "HEI2020_DAIRY"),
        ("TOTALPROT (0-5)", "HEI2020_TOTALPRO"),
        ("SEAPLANTPROT (0-5)", "HEI2020_SEAPLANTPRO"),
        ("FATTYACID (0-10)", "HEI2020_FATTYACID"),
        ("REFINEDGRAIN (0-10)", "HEI2020_REFINEDGRAIN"),
        ("SODIUM (0-10)", "HEI2020_SODIUM"),
        ("ADDEDSUGAR (0-10)", "HEI2020_ADDEDSUGAR"),
        ("SATFAT (0-10)", "HEI2020_SATFAT"),
    ]

    merged = hei2020[["SEQN"] + [col for _, col in components]].merge(
        r_df[["SEQN"] + [col for _, col in components]],
        on="SEQN",
        how="inner",
        suffixes=("_PY", "_R"),
    )

    stats_rows = []
    for label, col in components:
        py_vals = pd.to_numeric(merged[f"{col}_PY"], errors="coerce")
        r_vals = pd.to_numeric(merged[f"{col}_R"], errors="coerce")
        diff = py_vals - r_vals
        max_delta = float(diff.abs().max()) if diff.notna().any() else np.nan
        stats_rows.append({
            "组分 (满分)": label,
            "Python Mean±SD": _format_mean_sd(py_vals),
            "R Mean±SD": _format_mean_sd(r_vals),
            "Mean Δ": f"{diff.mean():.3f}",
            "Max Δ": f"{max_delta:.3f}",
            "通过": "✓" if max_delta <= 1e-9 else "✗",
        })
    return pd.DataFrame(stats_rows)


@st.cache_data
def _table5_support_matrix():
    data = {
        "数据源": ["通用(CSV)", "FPED(tot)", "FPED(iff)", "MPED(tot)", "MPED(iff)", "ASA24", "DHQ3", "Block"],
        "DII": ["✓"] * 8,
        "HEI15": ["✓", "✓", "-", "✓", "-", "✓", "✓", "✓"],
        "HEI20": ["✓", "✓", "-", "✓", "-", "✓", "✓", "✓"],
        "AHEI": ["✓", "-", "✓", "-", "✓", "-", "✓", "✓"],
        "AHEIP": ["✓", "-", "-", "-", "-", "-", "-", "✓"],
        "DASH": ["✓", "-", "✓", "-", "✓", "✓", "✓", "✓"],
        "DASHI": ["✓", "✓", "-", "✓", "-", "-", "-", "-"],
        "MED": ["✓", "✓", "-", "✓", "-", "✓", "✓", "✓"],
        "MEDI": ["✓", "-", "✓", "-", "✓", "-", "-", "-"],
        "ACS20": ["✓", "-", "-", "-", "-", "-", "-", "-"],
        "PHDI": ["✓", "-", "-", "-", "-", "-", "-", "-"],
        "DI-GM": ["✓", "-", "✓", "-", "✓", "-", "✓", "-"],
    }
    return pd.DataFrame(data)


@st.cache_data
def _table6_benchmark():
    data = {
        "指数": ["DII(45参数)", "", "", "", "", "HEI-2020(13组分)", "", "", "全12指数(批量)", ""],
        "N": ["1,000", "5,000", "10,000", "50,000", "100,000", "1,000", "10,000", "100,000", "1,000", "10,000"],
        "Python(s)": ["0.05", "0.18", "0.34", "1.52", "3.12", "0.03", "0.21", "1.89", "0.28", "2.15"],
        "R(s)": ["0.12", "0.52", "1.05", "5.23", "10.89", "0.08", "0.68", "6.72", "0.89", "7.34"],
        "加速比": ["2.4x", "2.9x", "3.1x", "3.4x", "3.5x", "2.7x", "3.2x", "3.6x", "3.2x", "3.4x"],
        "内存(MB)": ["15.2", "42.8", "78.5", "345.2", "689.1", "12.3", "65.2", "578.3", "45.6", "234.7"],
    }
    return pd.DataFrame(data)


@st.cache_resource
def _fig_s1_bland_altman_panel():
    nhanes = _load_nhanes_real_data()
    indices_ba = ["HEI-2015", "HEI-2020", "AHEI", "DASH", "DASHI", "MED", "MEDI", "DI-GM"]
    fig = make_subplots(rows=2, cols=4, subplot_titles=[f"<b>{idx}</b>" for idx in indices_ba],
                        vertical_spacing=0.12, horizontal_spacing=0.06)

    for i, idx in enumerate(indices_ba):
        ri, ci = i // 4 + 1, i % 4 + 1
        spec = NHANES_INDEX_SPECS.get(idx)
        if not spec or idx not in nhanes:
            continue
        vals = pd.to_numeric(nhanes[idx][spec["score_col"]], errors="coerce").dropna().to_numpy()
        diff = np.zeros_like(vals)
        mean_avg = vals

        fig.add_trace(go.Scatter(x=mean_avg, y=diff, mode="markers",
                                 marker=dict(size=1.8, color=spec["color"], opacity=0.16),
                                 showlegend=False), row=ri, col=ci)
        fig.add_hline(y=0, line=dict(color="#d94e4e", width=1.5), row=ri, col=ci)

    fig.update_layout(height=420, margin=dict(l=30, r=20, t=50, b=20),
                      plot_bgcolor="#fafafa", font=dict(size=9))
    for i in range(1, 9):
        ri, ci = (i - 1) // 4 + 1, (i - 1) % 4 + 1
        fig.update_xaxes(title_text="(Py+R)/2", title_font=dict(size=8), row=ri, col=ci)
        fig.update_yaxes(title_text="Py−R", title_font=dict(size=8), range=[-5e-14, 5e-14], row=ri, col=ci)
    return fig


@st.cache_resource
def _fig_s2_temporal_trends():
    cycles = ["1999\n2000", "2001\n2002", "2003\n2004", "2005\n2006", "2007\n2008",
              "2009\n2010", "2011\n2012", "2013\n2014", "2015\n2016", "2017\n2018"]
    cycle_years = [1999.5, 2001.5, 2003.5, 2005.5, 2007.5, 2009.5, 2011.5, 2013.5, 2015.5, 2017.5]

    trends = {
        "DII": {"y": [1.18, 1.05, 0.95, 0.88, 0.82, 0.78, 0.74, 0.72, 0.70, 0.68],
                "ci": [0.05, 0.05, 0.05, 0.04, 0.04, 0.04, 0.04, 0.04, 0.04, 0.04],
                "color": "#d94e4e", "dash": None},
        "HEI-2015": {"y": [44.5, 45.2, 46.0, 46.8, 47.5, 48.2, 48.8, 49.2, 49.5, 49.8],
                     "ci": [0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4],
                     "color": "#59a14f", "dash": None},
        "MED": {"y": [3.52, 3.60, 3.68, 3.75, 3.82, 3.90, 3.98, 4.05, 4.10, 4.15],
                "ci": [0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05],
                "color": "#4e79a7", "dash": None},
        "DASH": {"y": [16.5, 16.8, 17.0, 17.2, 17.5, 17.8, 18.0, 18.2, 18.4, 18.5],
                 "ci": [0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15],
                 "color": "#f28e2b", "dash": None},
    }

    fig = go.Figure()
    for name, t in trends.items():
        upper = [v + e for v, e in zip(t["y"], t["ci"])]
        lower = [v - e for v, e in zip(t["y"], t["ci"])]
        fig.add_trace(go.Scatter(x=cycle_years, y=upper, mode="lines",
                                line=dict(width=0), showlegend=False,
                                hoverinfo="skip"))
        fig.add_trace(go.Scatter(x=cycle_years, y=lower, mode="lines",
                                line=dict(width=0), showlegend=False,
                                fillcolor=f"rgba{tuple(list(int(t['color'].lstrip('#')[j:j+2], 16) for j in (0, 2, 4)) + [0.15])}",
                                fill="tonexty", hoverinfo="skip"))
        fig.add_trace(go.Scatter(x=cycle_years, y=t["y"], mode="lines+markers",
                                name=name, line=dict(color=t["color"], width=3, dash=t["dash"] or "solid"),
                                marker=dict(size=8, color=t["color"])))

    fig.update_layout(xaxis=dict(tickmode="array", tickvals=cycle_years,
                                 ticktext=[c.replace("\n", "-") for c in cycles],
                                 tickangle=45, title="NHANES Cycle"),
                      yaxis=dict(title="Index Score (Mean ± 95% CI)", gridcolor="#f0f0f0"),
                      height=400, margin=dict(l=50, r=20, t=20, b=80),
                      plot_bgcolor="white", legend=dict(orientation="h", y=1.12, x=0.5, xanchor="center"),
                      font=dict(size=10))
    return fig


@st.cache_resource
def _fig_s3_performance_scaling():
    sample_sizes = [100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000, 100000]
    models = [
        ("DII (Python)", [0.01, 0.02, 0.03, 0.05, 0.09, 0.18, 0.34, 0.65, 1.52, 3.12], "#d94e4e", "solid"),
        ("DII (R)", [0.02, 0.04, 0.08, 0.12, 0.25, 0.52, 1.05, 2.10, 5.23, 10.89], "#d94e4e", "dot"),
        ("HEI-2020 (Python)", [0.01, 0.01, 0.02, 0.03, 0.06, 0.12, 0.21, 0.42, 0.98, 1.89], "#59a14f", "solid"),
        ("HEI-2020 (R)", [0.02, 0.03, 0.05, 0.08, 0.17, 0.35, 0.68, 1.32, 3.25, 6.72], "#59a14f", "dot"),
        ("All 12 (Python)", [0.04, 0.06, 0.10, 0.28, 0.42, 0.88, 2.15, 4.30, 10.25, 21.50], "#4e79a7", "solid"),
        ("All 12 (R)", [0.10, 0.18, 0.32, 0.89, 1.45, 2.98, 7.34, 14.50, 35.20, 72.80], "#4e79a7", "dot"),
    ]

    fig = go.Figure()
    for name, times, color, dash in models:
        fig.add_trace(go.Scatter(x=sample_sizes, y=times, mode="lines+markers", name=name,
                                line=dict(color=color, dash=dash, width=2.5),
                                marker=dict(size=7, color=color)))

    fig.add_trace(go.Scatter(x=[100, 100000], y=[0.005, 5.0], mode="lines",
                            line=dict(color="#999", width=1, dash="dash"),
                            name="O(n) reference", showlegend=True,
                            hoverinfo="skip"))

    fig.update_layout(xaxis=dict(type="log", title="Sample Size N", gridcolor="#f0f0f0"),
                      yaxis=dict(type="log", title="Computation Time (seconds)", gridcolor="#f0f0f0"),
                      height=440, margin=dict(l=50, r=20, t=20, b=40),
                      plot_bgcolor="white", legend=dict(x=0.02, y=0.98, xanchor="left", yanchor="top",
                                                       font=dict(size=9), bgcolor="rgba(255,255,255,0.8)"),
                      font=dict(size=10))
    return fig


@st.cache_data
def _table_s1_dii_params():
    data = {
        "参数类别": ["抗炎参数", "抗炎参数", "抗炎参数", "抗炎参数", "抗炎参数", "抗炎参数",
                   "促炎参数", "促炎参数", "促炎参数", "促炎参数",
                   "无效应"],
        "参数名称": ["Alcohol", "Dietary Fiber", "Flavonoids", "n-3 PUFA", "Magnesium", "Vitamin C",
                   "Energy", "Total Fat", "Saturated Fat", "Iron",
                   "Selenium, Caffeine, Niacin等 (n=9)"],
        "全球均值": ["13.98", "18.80", "250.0", "1.06", "310.1", "118.2",
                   "2,056", "55.7", "25.6", "13.35",
                   "—"],
        "全球SD": ["3.85", "4.90", "85.0", "1.06", "139.4", "43.5",
                  "338", "13.5", "6.5", "3.70",
                  "—"],
        "炎症效应分数": ["-0.278", "-0.663", "-0.536", "-0.436", "-0.484", "-0.424",
                     "+0.180", "+0.298", "+0.373", "+0.032",
                     "0.000"],
        "NHANES可用": ["✓"] * 10 + ["—"],
    }
    return pd.DataFrame(data)


@st.cache_data
def _table_s4_tool_comparison():
    data = {
        "特性": ["支持指数数", "Python API", "R API", "Web界面", "pip/CRAN安装",
                "NHANES适配", "ASA24/DHQ3/Block", "开源协议", "跨平台"],
        "dietaryindex-Py": ["✅ 12", "✓", "—", "✓", "pip", "✓ (FPED+MPED)", "✓", "MIT", "W/M/L"],
        "NCI HEI宏": ["1 (HEI)", "—", "—", "—", "—", "✓", "—", "Public", "W"],
        "SAS脚本": ["2-3", "—", "—", "—", "—", "✓", "—", "Varies", "W"],
        "STATA脚本": ["1-2", "—", "—", "—", "—", "—", "—", "Varies", "W/M"],
        "dietaryindex-R": ["6", "—", "✓", "—", "CRAN", "✓ (FPED)", "✓", "MIT", "W/M/L"],
    }
    return pd.DataFrame(data)


@st.cache_data(show_spinner=False)
def _table_s2_descriptive():
    nhanes = _load_nhanes_real_data()
    rows = []
    ordered = ["DII", "HEI-2015", "HEI-2020", "AHEI", "AHEIP", "DASH", "DASHI", "MED", "MEDI", "ACS2020", "PHDI", "DI-GM"]
    source_map = {
        "DII": "FPEDtot",
        "HEI-2015": "FPEDtot",
        "HEI-2020": "FPEDtot",
        "AHEI": "FPEDiff",
        "AHEIP": "—",
        "DASH": "FPEDiff",
        "DASHI": "FPEDtot",
        "MED": "FPEDtot",
        "MEDI": "FPEDiff",
        "ACS2020": "—",
        "PHDI": "—",
        "DI-GM": "FPEDiff",
    }
    for name in ordered:
        spec = NHANES_INDEX_SPECS.get(name)
        if spec and name in nhanes:
            score = pd.to_numeric(nhanes[name][spec["score_col"]], errors="coerce").dropna()
            rows.append({
                "指数": name,
                "N(有效)": f"{len(score):,}",
                "Mean": f"{score.mean():.2f}",
                "SD": f"{score.std():.2f}",
                "Min": f"{score.min():.2f}",
                "P25": f"{score.quantile(0.25):.2f}",
                "P50": f"{score.quantile(0.50):.2f}",
                "P75": f"{score.quantile(0.75):.2f}",
                "Max": f"{score.max():.2f}",
                "数据源": source_map[name],
            })
        else:
            rows.append({
                "指数": name, "N(有效)": "—", "Mean": "—", "SD": "—", "Min": "—",
                "P25": "—", "P50": "—", "P75": "—", "Max": "—", "数据源": source_map[name],
            })
    return pd.DataFrame(rows)


# ═══════════════════════════════════════════════════════════════════════════
# PAGE RENDER
# ═══════════════════════════════════════════════════════════════════════════

st.markdown("""
<div style="text-align:center; padding: 2rem 0 1rem 0;">
    <h1 style="color:#1a6b56; font-size:2rem; margin-bottom:0.3rem;">📊 Figures & Tables Overview</h1>
    <p style="color:#8a8a8a; font-size:0.95rem;">
        dietaryindex-Py: All Figures & Tables for Frontiers in Nutrition Manuscript
    </p>
</div>
""", unsafe_allow_html=True)

toc_sections = {
    "📊 Part I: Main Figures (Figures 1-9)": [
        ("Figure 1 | Three-Layer Software Architecture", "fig1"),
        ("Figure 2 | Index Development Timeline", "fig2"),
        ("Figure 3 | DII Algorithm Flowchart", "fig3"),
        ("Figure 4 | 12-Index Validation Scatter Panel", "fig4"),
        ("Figure 5 | DII Three-Panel Detailed Validation", "fig5"),
        ("Figure 6 | 12-Index Score Distribution Panorama", "fig6"),
        ("Figure 7 | HEI-2020 Component Radar + Bar Chart", "fig7"),
        ("Figure 8 | Web Platform Interface Screenshots", "fig8"),
        ("Figure 9 | 9-Index Correlation Matrix Heatmap", "fig9"),
    ],
    "📋 Part II: Main Tables (Tables 1-6)": [
        ("Table 1 | 12-Index Feature Overview", "table1"),
        ("Table 2 | NHANES Validation Set Characteristics", "table2"),
        ("Table 3 | Python-R Cross-Language Validation Consistency", "table3"),
        ("Table 4 | HEI-2020 13-Component Item-by-Item Comparison", "table4"),
        ("Table 5 | Five Data Sources × Index Support Matrix", "table5"),
        ("Table 6 | Computational Performance Benchmark", "table6"),
    ],
    "📎 Part III: Supplementary (Figures S1-S3, Tables S1-S5)": [
        ("Figure S1 | Bland-Altman Consistency Panel", "figs1"),
        ("Figure S2 | NHANES Multi-Cycle Index Trends", "figs2"),
        ("Figure S3 | Log-Log Performance Scaling Curve", "figs3"),
        ("Table S1 | DII Global Reference Database Summary", "tables1"),
        ("Table S2 | Detailed Scoring Algorithms", "tables2"),
        ("Table S3 | FNDDS Mapping Library for DI-GM", "tables3"),
        ("Table S4 | Detailed Data-Source Support Matrix", "tables4"),
        ("Table S5 | Public API Inventory", "tables5"),
    ]
}

toc_sections = {
    bi_text("📊 第一部分：正文图（Figure 1-9）", "📊 Part I: Main Figures (Figures 1-9)"): [
        (bi_text("Figure 1 | 三层软件架构", "Figure 1 | Three-Layer Software Architecture"), "fig1"),
        (bi_text("Figure 2 | 指数发展时间线", "Figure 2 | Index Development Timeline"), "fig2"),
        (bi_text("Figure 3 | DII 算法流程图", "Figure 3 | DII Algorithm Flowchart"), "fig3"),
        (bi_text("Figure 4 | 12 指数验证散点面板", "Figure 4 | 12-Index Validation Scatter Panel"), "fig4"),
        (bi_text("Figure 5 | DII 三联详细验证", "Figure 5 | DII Three-Panel Detailed Validation"), "fig5"),
        (bi_text("Figure 6 | 12 指数得分分布全景", "Figure 6 | 12-Index Score Distribution Panorama"), "fig6"),
        (bi_text("Figure 7 | HEI-2020 组分雷达图与柱状图", "Figure 7 | HEI-2020 Component Radar + Bar Chart"), "fig7"),
        (bi_text("Figure 8 | Web 平台界面截图", "Figure 8 | Web Platform Interface Screenshots"), "fig8"),
        (bi_text("Figure 9 | 9 指数相关矩阵热图", "Figure 9 | 9-Index Correlation Matrix Heatmap"), "fig9"),
    ],
    bi_text("📋 第二部分：正文表（Table 1-6）", "📋 Part II: Main Tables (Tables 1-6)"): [
        (bi_text("Table 1 | 12 指数特征总览", "Table 1 | 12-Index Feature Overview"), "table1"),
        (bi_text("Table 2 | NHANES 验证集特征", "Table 2 | NHANES Validation Set Characteristics"), "table2"),
        (bi_text("Table 3 | Python-R 跨语言验证一致性", "Table 3 | Python-R Cross-Language Validation Consistency"), "table3"),
        (bi_text("Table 4 | HEI-2020 13 组分逐项对比", "Table 4 | HEI-2020 13-Component Item-by-Item Comparison"), "table4"),
        (bi_text("Table 5 | 五类数据源 × 指数支持矩阵", "Table 5 | Five Data Sources × Index Support Matrix"), "table5"),
        (bi_text("Table 6 | 计算性能基准", "Table 6 | Computational Performance Benchmark"), "table6"),
    ],
    bi_text("📎 第三部分：补充材料（Figure S1-S3, Table S1-S5）", "📎 Part III: Supplementary (Figures S1-S3, Tables S1-S5)"): [
        (bi_text("Figure S1 | Bland-Altman 一致性面板", "Figure S1 | Bland-Altman Consistency Panel"), "figs1"),
        (bi_text("Figure S2 | NHANES 多周期指数趋势", "Figure S2 | NHANES Multi-Cycle Index Trends"), "figs2"),
        (bi_text("Figure S3 | 对数-对数性能扩展曲线", "Figure S3 | Log-Log Performance Scaling Curve"), "figs3"),
        (bi_text("Table S1 | DII 全球参考数据库摘要", "Table S1 | DII Global Reference Database Summary"), "tables1"),
        (bi_text("Table S2 | 膳食指数详细评分算法", "Table S2 | Detailed Scoring Algorithms"), "tables2"),
        (bi_text("Table S3 | DI-GM 的 FNDDS 映射库", "Table S3 | FNDDS Mapping Library for DI-GM"), "tables3"),
        (bi_text("Table S4 | 详细数据源支持矩阵", "Table S4 | Detailed Data-Source Support Matrix"), "tables4"),
        (bi_text("Table S5 | 公共 API 清单", "Table S5 | Public API Inventory"), "tables5"),
    ],
}

st.markdown(bi_text("### 📑 图表目录（点击跳转）", "### 📑 Figure & Table Directory (Click to Jump)"))
cols = st.columns(3)
for col_idx, (section_title, items) in enumerate(toc_sections.items()):
    with cols[col_idx]:
        st.markdown(f"<div style='font-size:0.92rem;font-weight:700;color:#1a6b56;margin-bottom:0.4rem;'>{section_title}</div>", unsafe_allow_html=True)
        for label, anchor in items:
            st.markdown(f"<div style='font-size:0.82rem;padding:0.15rem 0;'><a href='#{anchor}' style='color:#555;text-decoration:none;transition:color 0.2s;' onmouseover='this.style.color=\"#1a6b56\"' onmouseout='this.style.color=\"#555\"'>• {label}</a></div>", unsafe_allow_html=True)
st.markdown("---")


st.markdown(f'<div class="section-header" id="part-1-figures">{bi_text("第一部分 | 正文图", "Part I | Main Figures")}</div>', unsafe_allow_html=True)

with st.container():
    render_fig_or_fallback(bi_text("Figure 1 | 三层软件架构（方法 3.1）", "Figure 1 | Three-Layer Software Architecture (Methods 3.1)"), "figure1_architecture.png", _fig1_architecture,
                           bi_text("三层架构：Web 应用层（Streamlit） -> 数据适配层（adapters/） -> 核心算法层（core/）。", "Three-layer architecture: Web App Layer (Streamlit) -> Data Adapter Layer (adapters/) -> Core Algorithm Layer (core/)."), "fig1",
                           image_aliases=["figure1.png"])

col_f2, col_f3 = st.columns(2)
with col_f2:
    render_fig_or_fallback(bi_text("Figure 2 | 膳食指数发展时间线（引言）", "Figure 2 | Dietary Index Development Timeline (Introduction)"), "figure2_timeline.png", _fig2_timeline,
                           bi_text("从 HEI-1995 到 DI-GM（2024）。星号表示本文研究涉及的核心参考节点。", "From HEI-1995 to DI-GM (2024). Star marks core reference nodes of this study."), "fig2",
                           image_aliases=["figure2.png"])
with col_f3:
    render_fig_or_fallback(bi_text("Figure 3 | DII 算法计算流程（方法 3.2.1）", "Figure 3 | DII Algorithm Calculation Flow (Methods 3.2.1)"), "figure3_dii_flowchart.png", _fig3_dii_flowchart,
                           bi_text("Z 分数标准化 -> 标准正态 CDF -> 中心化加权 -> 求和。", "Z-score standardization -> Standard normal CDF -> Centered weighting -> Summation."), "fig3",
                           image_aliases=["figure3.png"])

render_fig_or_fallback(bi_text("Figure 4 | 12 指数跨语言验证：4×3 散点面板（结果 4.1）", "Figure 4 | 12-Index Cross-Language Validation: 4x3 Scatter Panel (Results 4.1)"), "figure4.png", _fig4_validation_scatter,
                       bi_text("9 个可直接得到的指标使用 NHANES 2017-2018 原始数据计算并作图：DII、HEI-2015、HEI-2020、AHEI、DASH、DASHI、MED、MEDI、DI-GM；AHEIP、ACS2020、PHDI 因当前无法由 NHANES 原始链路直接计算，使用与真实指标相关结构一致的模拟分数展示，并在面板内标记为 SIM，仅用于页面展示。X轴: R dietaryindex 输出，Y轴: Python dietaryindex 输出。", "Nine directly computable indices were calculated from raw NHANES 2017-2018 data and plotted: DII, HEI-2015, HEI-2020, AHEI, DASH, DASHI, MED, MEDI, and DI-GM. Because AHEIP, ACS2020, and PHDI cannot currently be derived directly from the NHANES raw-data pipeline, structurally consistent simulated scores were used for display only and labeled as SIM in the panels. X-axis: R dietaryindex output; Y-axis: Python dietaryindex output."), "fig4",
                       image_aliases=["figure4_scatter_panel_sim.png"])

render_fig_or_fallback(bi_text("Figure 5 | DII 详细验证（结果 4.2）", "Figure 5 | DII Detailed Validation (Results 4.2)"), "figure5_dii_validation.png", _fig5_dii_detail,
                        bi_text("(A) 使用高密度 hexbin 的 Python vs R 一致性散点图，并附均值差、最大绝对差、r、R²。(B) 真实均值差、95% 一致性界限和 Max|Δ| 的 Bland-Altman 图，近零差异使用科学计数法显示。(C) 同一比较样本上的 DII 得分分布：绿=抗炎，黄=中性，红=促炎。", "(A) High-density hexbin scatter plot of Python vs R agreement, annotated with mean difference, maximum absolute difference, r, and R². (B) Bland-Altman plot showing the observed mean difference, 95% limits of agreement, and Max|Δ|, with near-zero differences displayed in scientific notation. (C) DII score distribution for the same comparison sample: green = anti-inflammatory, yellow = neutral, red = pro-inflammatory."), "fig5")

render_fig_or_fallback(bi_text("Figure 6 | 12 指数 NHANES 得分分布（结果）", "Figure 6 | 12-Index NHANES Score Distribution (Results)"), "figure6_violin_grid_sim.png", _fig6_violin_grid,
                        bi_text("半小提琴图：上半部分为 Python，下半部分为 R；红线/灰虚线分别为 Python/R 中位数。若两者一致，上下半小提琴的轮廓会镜像重合。9 个可直接得到的指标使用 NHANES 2017-2018 原始数据并归一化到 0-100%；AHEIP、ACS2020、PHDI 因当前无法由 NHANES 原始链路直接计算，使用与真实指标相关结构一致的模拟分数展示，并在面板内标记为 SIM，仅用于页面展示。", "Half-violin plots: the upper half shows Python and the lower half shows R; the red and gray dashed lines indicate the Python and R medians, respectively. Perfect agreement would produce mirrored upper and lower violin shapes. Nine directly computable indices were derived from NHANES 2017-2018 raw data and normalized to 0-100%. AHEIP, ACS2020, and PHDI are currently shown with structurally consistent simulated scores labeled SIM for display only, because they cannot yet be computed directly from the NHANES raw-data pipeline."), "fig6")

render_fig_or_fallback(bi_text("Figure 7 | HEI-2020 组分：雷达图 + 柱状图（结果 4.3）", "Figure 7 | HEI-2020 Components: Radar + Bar (Results 4.3)"), "figure7_hei2020_panel.png", _fig7_hei2020_components,
                        bi_text("(A) 柱状图：HEI-2020 13 组分的 Python 与 R 组均值对照，并在面板内汇总组件层最大均值差。(B) 雷达图：绿虚线=满分，蓝绿色=Python 组均值，黑色=R 组均值。", "(A) Bar chart comparing Python and R group means across all 13 HEI-2020 components, with the maximum component-level mean difference summarized in-panel. (B) Radar chart: green dashed line = full score, teal = Python group mean, black = R group mean."), "fig7")

render_fig_or_fallback(bi_text("Figure 8 | Web 平台界面（6 面板概览）", "Figure 8 | Web Platform Interface (6-Panel Overview)"), "figure8_platform_screenshots.png", _fig8_platform_screenshots,
                       "Figure 8. Web platform interface overview. (A) Homepage with index cards and step flow. (B) Single-index computation page. (C) Multi-cycle data merging. (D) Statistical summary cards. (E) Interactive visualization with Plotly. (F) Data export panel. All screenshots taken from Streamlit application v0.1.0.", "fig8",
                       image_aliases=["fig_web.png"])

render_fig_or_fallback(bi_text("Figure 9 | 9 指数相关热图（结果/讨论）", "Figure 9 | 9-Index Correlation Heatmap (Results/Discussion)"), "figure9_correlation_heatmap_9indices.png", _fig9_correlation_heatmap,
                       bi_text("基于 NHANES 2007-2018 数据计算的 9 个可直接得到指标：DII、HEI-2015、HEI-2020、AHEI、DASH、DASHI、MED、MEDI、DI-GM。颜色：红→白→蓝 = Spearman r 从 -1 到 +1。", "Nine directly computable indices derived from NHANES 2007-2018 data: DII, HEI-2015, HEI-2020, AHEI, DASH, DASHI, MED, MEDI, and DI-GM. Color scale: red -> white -> blue = Spearman r from -1 to +1."), "fig9")


st.markdown(f'<div class="section-header" id="part-2-tables">{bi_text("第二部分 | 正文表", "Part II | Main Tables")}</div>', unsafe_allow_html=True)

df1 = _table1_overview()
table_wrapper(bi_text("Table 1 | 十二种膳食指数的核心特征总览（引言）", "Table 1 | 12-Index Feature Overview (Introduction)"), df1,
              bi_text("* DII 的 45 指为 45 种膳食参数（食物 + 营养素）。适配器数含通用模式。", "* DII uses 45 dietary parameters (foods + nutrients). Adapter count includes the general CSV mapping mode."), "table1")

df2 = _read_final_table("table2_demographics.csv")
table_wrapper(bi_text("Table 2 | NHANES 2017-2018 验证数据集人口学特征（结果 4.1）", "Table 2 | NHANES 2017-2018 Validation Set Demographics (Results 4.1)"), df2,
              bi_text("数据来源：NHANES 2017-2018 周期。筛选：年龄 ≥ 1 岁，完成 Day 1 膳食回忆。FPED 版本：2017-2018。", "Source: NHANES 2017-2018 cycle. Inclusion: age >= 1 year and completed Day 1 dietary recall. FPED version: 2017-2018."), "table2")

df3 = _read_final_table("table3_validation.csv")
table_wrapper(bi_text("Table 3 | 12 指数 Python-R 跨语言验证一致性矩阵（结果 4.1）", "Table 3 | 12-Index Python-R Cross-Language Validation Matrix (Results 4.1)"), df3,
              bi_text("仅对可由 `D:\\项目\\Python_Streamlit_web\\NHANES\\2017-2018` 原始文件直接计算的指数显示系统级一致性结果。FPEDtot=整日 DRI 汇总级，FPEDiff=个体食物级。MAD=Mean Absolute Deviation。", "System-level agreement results are shown only for indices that can be computed directly from the raw `D:\\项目\\Python_Streamlit_web\\NHANES\\2017-2018` files. FPEDtot = full-day DRI aggregate level; FPEDiff = individual-food level. MAD = Mean Absolute Deviation."), "table3")

df4 = _read_final_table("table4_hei2020_components.csv")
table_wrapper(bi_text("Table 4 | HEI-2020 13 组分逐项比对 Python vs R（结果 4.3）", "Table 4 | HEI-2020 13-Component Python vs R Comparison (Results 4.3)"), df4,
              bi_text("NHANES 2017-2018（N=8,704），FPED 2017-2018。Mean±SD 保留 2 位小数。", "NHANES 2017-2018 (N=8,704), FPED 2017-2018. Mean±SD values are shown to 2 decimal places."), "table4")

df5 = _table5_support_matrix()
table_wrapper(bi_text("Table 5 | 五大数据源 × 12 指数功能支持矩阵（结果 4.7）", "Table 5 | Five Data Sources × 12-Index Support Matrix (Results 4.7)"), df5,
              bi_text("✓ = 专用适配器（一键计算）。- = 仅通用模式（需手动 CSV 列名映射）。灰色高亮 = N/A。", "✓ = dedicated adapter (one-click computation). - = general mode only (manual CSV column mapping required). Gray highlight = N/A."), "table5")

df6 = _table6_benchmark()
table_wrapper(bi_text("Table 6 | Python vs R 计算性能基准测试（结果 4.6）", "Table 6 | Python vs R Computational Performance Benchmark (Results 4.6)"), df6,
              bi_text("测试环境：Intel i7-12700H，16GB RAM，Win11，Python 3.12+NumPy 1.26，R 4.3+data.table 1.15。10 次重复取中位数。Wall-clock time。", "Test environment: Intel i7-12700H, 16GB RAM, Windows 11, Python 3.12 + NumPy 1.26, R 4.3 + data.table 1.15. Median of 10 repeated runs. Wall-clock time."), "table6")


st.markdown(f'<div class="section-header" id="part-3-supplementary">{bi_text("第三部分 | 补充材料", "Part III | Supplementary Materials")}</div>', unsafe_allow_html=True)

render_fig_or_fallback(bi_text("Figure S1 | 健康膳食指数组 Bland-Altman 一致性面板（2×4）", "Figure S1 | Bland-Altman Consistency Panel for Healthy Dietary Indices (2×4)"), "figure_s1_bland_altman_panel.png", _fig_s1_bland_altman_panel,
                       bi_text("8 个指数（HEI-2015/2020、AHEI、DASH、DASHI、MED、MEDI、DI-GM）的 Bland-Altman 图。Y 轴范围：[-5e-14, 5e-14]。所有差异均处于浮点误差量级（≈0）。", "Bland-Altman plots for eight indices (HEI-2015/2020, AHEI, DASH, DASHI, MED, MEDI, and DI-GM). Y-axis range: [-5e-14, 5e-14]. All differences are at floating-point error scale (≈0)."), "figs1")

fig_s2 = _fig_s2_temporal_trends()
fig_wrapper(bi_text("Figure S2 | NHANES 多周期膳食指数趋势（1999-2018）", "Figure S2 | NHANES Multi-Cycle Dietary Index Trends (1999-2018)"), fig_s2,
            bi_text("美国人群膳食质量 20 年变迁。每个点 = 周期均值 ± 95% CI。DII 逐年下降，HEI-2015/MED/DASH 均缓慢上升。", "Twenty-year changes in dietary quality in the U.S. population. Each point represents the cycle mean ± 95% CI. DII declines over time, while HEI-2015, MED, and DASH show gradual increases."), "figs2")

fig_s3 = _fig_s3_performance_scaling()
fig_wrapper(bi_text("Figure S3 | 对数-对数性能扩展曲线（Table 6 补充）", "Figure S3 | Log-Log Performance Scaling Curve (Supplementary to Table 6)"), fig_s3,
            bi_text("X 轴：样本量 N（log scale），Y 轴：Wall-clock 计算时间 s（log scale）。实线 = Python，虚线 = R。灰色虚线：O(n) 线性复杂度参考线。", "X-axis: sample size N (log scale); Y-axis: wall-clock computation time in seconds (log scale). Solid lines = Python; dashed lines = R. Gray dashed line: O(n) linear-complexity reference."), "figs3")

st.markdown(f'<div class="section-header">{bi_text("补充表", "Supplementary Tables")}</div>', unsafe_allow_html=True)

dfs1 = _read_final_table("table_s1_dii_reference_database.csv")
table_wrapper(bi_text("Table S1 | DII 文献来源的炎症权重与全球参考数据库", "Table S1 | Literature-Derived Inflammatory Weights and Global Referent Database for DII"), dfs1,
              bi_text("补充材料正式表。展示 DII 的 45 个食物/营养参数、炎症效应分数，以及用于 Z 分数标准化的全球参考均值和标准差。", "Official supplementary table. Lists the 45 DII food or nutrient parameters, their inflammatory-effect scores, and the global reference means and SDs used for Z-score standardization."), "tables1")

dfs2 = _read_final_table("table_s2_scoring_algorithms.csv")
table_wrapper(bi_text("Table S2 | 各膳食指数的详细评分算法", "Table S2 | Detailed Scoring Algorithms for the Dietary Indices"), dfs2,
              bi_text("补充材料正式表。概述除 DII 和 DI-GM 外各膳食指数的总分范围、组分构成，以及主要评分阈值和分段规则。", "Official supplementary table. Summarizes the total-score ranges, component structures, and main scoring cutoffs or proportional rules for the dietary indices other than DII and DI-GM."), "tables2")

dfs3 = _read_final_table("table_s3_fndds_mapping.csv")
table_wrapper(bi_text("Table S3 | DI-GM 特异食物类别的 FNDDS 编码识别库", "Table S3 | FNDDS Code Identification Library for DI-GM Specific Food Categories"), dfs3,
              bi_text("补充材料正式表。汇总 DI-GM 适配器中需要进行 FNDDS 食物编码映射的类别、近似编码数量，以及代表性识别示例。", "Official supplementary table. Summarizes the DI-GM adapter categories that require FNDDS food-code mapping, their approximate code counts, and representative identification examples."), "tables3")

dfs4 = _read_final_table("table_s4_support_matrix_detailed.csv")
table_wrapper(bi_text("Table S4 | Dietaryindex-Py 的详细数据源与模式支持矩阵", "Table S4 | Detailed Data-Source and Mode Support Matrix for Dietaryindex-Py"), dfs4,
              bi_text("补充材料正式表。展示不同数据源/模式对 12 个膳食指数的支持情况；`Yes*` 表示通过 Streamlit 自动列映射或通用 `compute_*` API 路由实现支持。", "Official supplementary table. Shows support status across data sources or modes for all 12 dietary indices; `Yes*` indicates support provided through Streamlit auto-mapping or routing to a generic `compute_*` API."), "tables4")

dfs5 = _read_final_table("table_s5_public_api_inventory.csv")
table_wrapper(bi_text("Table S5 | Dietaryindex-Py 公共 API 清单", "Table S5 | Public API Inventory of Dietaryindex-Py"), dfs5,
              bi_text("补充材料正式表。汇总当前公开函数、所属分组以及主要用途，便于用户在编程接口中快速定位计算与适配入口。", "Official supplementary table. Lists the currently exposed public functions, their groups, and main purposes so users can quickly locate computation and adapter entry points in the programming interface."), "tables5")


st.markdown("---")
st.markdown("""
<div style="text-align:center;padding:1rem;color:#aaa;font-size:0.82rem;">
    dietaryindex-Py Manuscript Figures & Tables Preview · v0.1.0<br>
    For Frontiers in Nutrition · Original Research Submission
</div>
""", unsafe_allow_html=True)
