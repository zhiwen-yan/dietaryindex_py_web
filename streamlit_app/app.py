"""
膳食指数计算平台 — 首页
Dietary Index Calculation Platform
"""

import streamlit as st

from sidebar_utils import render_sidebar
from config.i18n import get_lang

lang = get_lang()

st.set_page_config(
    page_title="Dietary Index Calculation Platform" if lang == "en" else "膳食指数计算平台",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded",
)

render_sidebar("home")

# ═══════════════════════════════════════════════════════════════════════════════
# 缓存数据与 HTML 生成器 — 纯函数，lang → HTML string
# ═══════════════════════════════════════════════════════════════════════════════

_HERO_EN = (
    '<div class="hero-banner">'
    '<h1>🥗 Dietary Index Calculation Platform</h1>'
    '<div class="hero-subtitle">Dietary Index Calculation Platform</div>'
    '<div class="hero-tagline" style="white-space:normal;">'
    '<p style="margin:0;font-size:0.92rem;color:rgba(255,255,255,0.85);">'
    'Built on the <b>dietaryindex</b> Python package, supporting 12 internationally recognized dietary quality indices '
    'across NHANES, ASA24, DHQ3, and BLOCK FFQ data sources — all computation runs entirely in the browser.</p>'
    '</div></div>'
)

_HERO_ZH = (
    '<div class="hero-banner">'
    '<h1>🥗 膳食指数计算平台</h1>'
    '<div class="hero-subtitle">Dietary Index Calculation Platform</div>'
    '<div class="hero-tagline" style="white-space:normal;">'
    '<p style="margin:0;font-size:0.92rem;color:rgba(255,255,255,0.85);">'
    '基于 <b>dietaryindex</b> Python 包开发，支持 12 个国际通用膳食质量评估指数，'
    '兼容 NHANES、ASA24、DHQ3、BLOCK FFQ 数据源 — 所有计算均在浏览器中完成。</p>'
    '</div></div>'
)

_FEATURED_INDICES = (
    ("🔥", "DII", "膳食炎症指数", "Dietary Inflammatory Index", "≈ −10 to +10",
     "基于 45 种食物/营养素的全球参考数据库，Z-score 标准化评估膳食炎症潜力",
     "Z-score standardized assessment of dietary inflammatory potential using global reference database of 45 foods/nutrients",
     "pages/01_dii.py"),
    ("📊", "HEI-2020", "健康饮食指数 2020", "Healthy Eating Index 2020", "0–100",
     "USDA 最新膳食质量评价标准，13 个组分密度法评分，含幼儿版",
     "USDA newest dietary quality standard, 13-component density-based scoring, includes toddler version",
     "pages/02_hei2020.py"),
    ("🫀", "AHEI", "替代健康饮食指数", "Alternative Healthy Eating Index", "0–110",
     "哈佛大学开发，11 组分关注慢性病预防，含性别差异处理",
     "Harvard-developed, 11 components focused on chronic disease prevention, includes gender-specific handling",
     "pages/04_ahei.py"),
    ("💚", "DASH", "DASH 饮食评分", "DASH Diet Score", "8–40",
     "8 个食物组分五分位数排名，评估降血压膳食模式依从性",
     "8 food component quintile ranking, assesses adherence to blood-pressure-lowering dietary pattern",
     "pages/06_dash.py"),
)

_ALL_INDICES = (
    ("🔥", "DII", "膳食炎症指数", "Dietary Inflammatory Index", "≈ −10 to +10",
     "Z-score 标准化，评估膳食炎症潜力",
     "Z-score standardized, assesses dietary inflammatory potential",
     "pages/01_dii.py"),
    ("📊", "HEI-2020", "健康饮食指数 2020", "Healthy Eating Index 2020", "0–100",
     "USDA 13 组分密度法，含幼儿版",
     "USDA 13-component density method, includes toddler version",
     "pages/02_hei2020.py"),
    ("📊", "HEI-2015", "健康饮食指数 2015", "Healthy Eating Index 2015", "0–100",
     "USDA 13 组分密度法",
     "USDA 13-component density method",
     "pages/03_hei2015.py"),
    ("🫀", "AHEI", "替代健康饮食指数", "AHEI", "0–110",
     "哈佛 11 组分，慢性病预防",
     "Harvard 11-component, chronic disease prevention",
     "pages/04_ahei.py"),
    ("🤰", "AHEIP", "AHEI 孕期版", "AHEI-P", "0–90",
     "孕期专用 9 组分替代健康指数",
     "Pregnancy-specific 9-component index",
     "pages/05_aheip.py"),
    ("💚", "DASH", "DASH 饮食评分", "DASH Score", "8–40",
     "8 组分五分位排名",
     "8-component quintile ranking",
     "pages/06_dash.py"),
    ("❤️", "DASHI", "DASH 营养密度版", "DASHI", "0–9",
     "9 营养素线性评分",
     "9-nutrient linear scoring",
     "pages/07_dashi.py"),
    ("🫒", "MED", "地中海饮食指数", "MED", "0–9",
     "9 组分中位数排名",
     "9-component median-based ranking",
     "pages/08_med.py"),
    ("🐟", "MEDI", "MEDI PREDIMED", "MEDI", "0–11",
     "11 组分绝对阈值二值评分",
     "11-component absolute threshold binary scoring",
     "pages/09_medi.py"),
    ("🎗️", "ACS2020", "ACS 膳食指数", "ACS2020", "0–15",
     "ACS 指南 8 组分性别分层",
     "ACS guideline 8-component gender-stratified",
     "pages/10_acs2020.py"),
    ("🌍", "PHDI", "行星健康饮食指数", "PHDI", "0–150",
     "EAT-Lancet 16 组分",
     "EAT-Lancet 16 components",
     "pages/11_phdi.py"),
    ("🦠", "DI-GM", "肠道微生物膳食指数", "DI-GM", "0–14",
     "14 组分性别分层中位数",
     "14-component gender-stratified median",
     "pages/12_di_gm.py"),
)

_step_zh = '<div class="step-flow"><div class="step-item"><div class="step-number">1</div><div class="step-text">📂 选择指数<br><small>从侧边栏选择膳食指数</small></div></div><div class="step-arrow">→</div><div class="step-item"><div class="step-number">2</div><div class="step-text">📤 上传数据<br><small>选择数据源模式并上传文件</small></div></div><div class="step-arrow">→</div><div class="step-item"><div class="step-number">3</div><div class="step-text">📊 计算 & 导出<br><small>映射列名后计算，查看图表并导出</small></div></div></div>'
_step_en = '<div class="step-flow"><div class="step-item"><div class="step-number">1</div><div class="step-text">📂 Select Index<br><small>Choose a dietary index from the sidebar</small></div></div><div class="step-arrow">→</div><div class="step-item"><div class="step-number">2</div><div class="step-text">📤 Upload Data<br><small>Select data source mode and upload files</small></div></div><div class="step-arrow">→</div><div class="step-item"><div class="step-number">3</div><div class="step-text">📊 Compute & Export<br><small>Map columns, compute, view charts and export</small></div></div></div>'


def _all_page_html(is_en: bool) -> str:
    """一次性生成首页全部 HTML，避免逐个 Streamlit 元素导致的渲染延迟"""
    
    # ── Featured Indices ──
    ft_title = "🌟 Featured Indices" if is_en else "🌟 核心指数"
    ft_cards = []
    for icon, name, cn, en_name, score_en, cn_desc, en_desc, page_path in _FEATURED_INDICES:
        dn = en_name if is_en else cn
        ds = f"Score {score_en}" if is_en else f"总分 {score_en}"
        dd = en_desc if is_en else cn_desc
        label = f"Compute {name} →" if is_en else f"进入 {name} 计算 →"
        href = page_path.replace(".py", "").replace("pages/", "")
        # Strip numeric prefix from filename (e.g. "01_dii" → "dii", "12_di_gm" → "di_gm")
        if "_" in href and href.split("_")[0].isdigit():
            href = href.split("_", 1)[1]
        ft_cards.append(
            f'<div class="index-card-wrapper">'
            f'<div class="index-card featured"><div class="card-icon">{icon}</div><div class="card-name">{name}</div>'
            f'<div class="card-eng">{dn}</div><div style="text-align:center;margin:0.3rem 0;"><span class="card-score">{ds}</span></div>'
            f'<div class="card-desc">{dd}</div></div>'
            f'<div class="card-button-wrapper"><a class="idx-btn" href="{href}">{label}</a></div>'
            f'</div>'
        )
    ft_html = f'<div class="section-card"><div class="section-title">{ft_title}</div><div class="idx-grid-4">{"".join(ft_cards)}</div></div>'

    # ── Step Flow ──
    step = _step_en if is_en else _step_zh

    # ── All 12 Indices ──
    all_title = "📋 All 12 Indices" if is_en else "📋 全部 12 个指数"
    all_cards = []
    for icon, name, cn, en_name, score_en, cn_desc, en_desc, page_path in _ALL_INDICES:
        dn = en_name if is_en else cn
        ds = f"Score {score_en}" if is_en else f"总分 {score_en}"
        dd = en_desc if is_en else cn_desc
        label = "Compute →" if is_en else "进入计算 →"
        href = page_path.replace(".py", "").replace("pages/", "")
        # Strip numeric prefix from filename (e.g. "01_dii" → "dii", "12_di_gm" → "di_gm")
        if "_" in href and href.split("_")[0].isdigit():
            href = href.split("_", 1)[1]
        all_cards.append(
            f'<div class="index-card-wrapper">'
            f'<div class="index-card-h"><div class="card-h-row"><div class="card-h-icon">{icon}</div>'
            f'<div class="card-h-info"><div class="card-h-name">{name}</div><div class="card-h-meta">{dn} · {ds}</div></div></div>'
            f'<div class="card-h-desc">{dd}</div></div>'
            f'<div class="card-button-wrapper"><a class="idx-btn" href="{href}">{label}</a></div>'
            f'</div>'
        )
    all_html = f'<div class="section-card"><div class="section-title">{all_title}</div><div class="idx-grid-3">{"".join(all_cards)}</div></div>'

    # ── Upload Modes ──
    if is_en:
        modes = [("🗂️", "General", "CSV / Excel<br>Manual column mapping"),
                 ("🏥", "NHANES FPED", "Post-2005<br>.sas7bdat + .XPT"),
                 ("🏥", "NHANES MPED", "1999–2004<br>equiv.txt + .XPT"),
                 ("📱", "ASA24", "Totals.csv<br>Auto aggregation"),
                 ("📋", "DHQ3 / BLOCK", "FFQ raw data<br>One-step computation")]
        up_title = "📂 Supported Data Upload Modes"
    else:
        modes = [("🗂️", "通用版", "CSV / Excel<br>列名手动映射"),
                 ("🏥", "NHANES FPED", "2005年后<br>.sas7bdat + .XPT"),
                 ("🏥", "NHANES MPED", "1999–2004<br>equiv.txt + .XPT"),
                 ("📱", "ASA24", "Totals.csv<br>系统自动汇总"),
                 ("📋", "DHQ3 / BLOCK", "FFQ 原始数据<br>一步式计算")]
        up_title = "📂 支持的数据上传模式"
    up_cards = ''.join(
        f'<div style="flex:1;min-width:180px;background:var(--green-bg);border-radius:12px;padding:1rem;text-align:center;">'
        f'<div style="font-size:1.8rem;">{icon}</div><div style="font-weight:700;color:var(--green-deep);">{name}</div>'
        f'<div style="font-size:0.78rem;color:var(--text-secondary);">{desc}</div></div>'
        for icon, name, desc in modes
    )
    up_html = f'<div class="section-card"><div class="section-title">{up_title}</div><div style="display:flex;gap:1rem;flex-wrap:wrap;margin-top:0.5rem;">{up_cards}</div></div>'

    # ── Footer ──
    zh = "dietaryindex v0.1.0 &nbsp;|&nbsp; 纯 Python 实现，无需 R 环境，所有计算在浏览器本地完成 &nbsp;|&nbsp; 支持 Windows / macOS / Linux"
    en = "dietaryindex v0.1.0 &nbsp;|&nbsp; Pure Python — serverless, all computation runs locally in the browser &nbsp;|&nbsp; Windows / macOS / Linux"
    ft_html2 = f'<div class="app-footer">{en if is_en else zh}</div>'

    return ft_html + step + all_html + up_html + ft_html2


# ═══════════════════════════════════════════════════════════════════════════════
# 页面渲染 — 一次 st.markdown 输出全部 HTML
# ═══════════════════════════════════════════════════════════════════════════════

is_en = lang == "en"
st.markdown(_HERO_EN if is_en else _HERO_ZH, unsafe_allow_html=True)
st.markdown(_all_page_html(is_en), unsafe_allow_html=True)
