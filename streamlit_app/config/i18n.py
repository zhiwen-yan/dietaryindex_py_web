"""
国际化翻译模块
支持中文 (zh) 和英文 (en) 切换
"""

import streamlit as st


TRANSLATIONS = {
    # ── 侧边栏 ──
    "sidebar.brand": {
        "zh": "DietaryIndex",
        "en": "DietaryIndex",
    },
    "sidebar.subtitle": {
        "zh": "膳食指数计算平台",
        "en": "Dietary Index Platform",
    },
    "sidebar.home": {
        "zh": "首页",
        "en": "Home",
    },
    "sidebar.figures": {
        "zh": "论文图表",
        "en": "Figures & Tables",
    },
    "sidebar.guide": {
        "zh": "使用指南",
        "en": "User Guide",
    },
    "sidebar.version": {
        "zh": "dietaryindex v0.1.0",
        "en": "dietaryindex v0.1.0",
    },
    "sidebar.language": {
        "zh": "🌐 语言 / Language",
        "en": "🌐 Language",
    },

    # ── 侧边栏分类 ──
    "nav.inflammatory": {
        "zh": "炎症指标",
        "en": "Inflammatory Index",
    },
    "nav.hei_series": {
        "zh": "HEI 系列",
        "en": "HEI Series",
    },
    "nav.alternative_healthy": {
        "zh": "替代健康指数",
        "en": "Alternative Healthy",
    },
    "nav.disease_prevention": {
        "zh": "疾病预防指数",
        "en": "Disease Prevention",
    },
    "nav.dietary_pattern": {
        "zh": "膳食模式指数",
        "en": "Dietary Pattern",
    },
    "nav.emerging": {
        "zh": "新兴指数",
        "en": "Emerging Indices",
    },

    # ── 首页 ──
    "home.page_title": {
        "zh": "膳食指数计算平台",
        "en": "Dietary Index Calculation Platform",
    },
    "home.hero_title": {
        "zh": "🥗 膳食指数计算平台",
        "en": "🥗 Dietary Index Calculation Platform",
    },
    "home.hero_subtitle": {
        "zh": "Dietary Index Calculation Platform",
        "en": "Dietary Index Calculation Platform",
    },
    "home.hero_tagline": {
        "zh": "基于 dietaryindex R 包 (James Zhan) 的 Python 全功能复现 &nbsp;|&nbsp; "
              "12 个国际通用膳食质量评估指数 &nbsp;|&nbsp; "
              "支持 NHANES · ASA24 · DHQ3 · BLOCK FFQ 数据源",
        "en": "Full Python reimplementation of dietaryindex R package (James Zhan) &nbsp;|&nbsp; "
             "12 internationally recognized dietary quality indices &nbsp;|&nbsp; "
             "NHANES · ASA24 · DHQ3 · BLOCK FFQ compatible",
    },
    "home.featured_title": {
        "zh": "🌟 核心指数",
        "en": "🌟 Featured Indices",
    },
    "home.all_indices_title": {
        "zh": "📋 全部 12 个指数",
        "en": "📋 All 12 Indices",
    },
    "home.data_modes_title": {
        "zh": "📂 支持的数据上传模式",
        "en": "📂 Supported Data Upload Modes",
    },
    "home.footer": {
        "zh": "dietaryindex v0.1.0 &nbsp;|&nbsp; "
             "基于 dietaryindex R 包 (James J. Zhan) &nbsp;|&nbsp; "
             "纯 Python 实现，无需 R 环境 &nbsp;|&nbsp; "
             "支持 Windows / macOS / Linux",
        "en": "dietaryindex v0.1.0 &nbsp;|&nbsp; "
             "Based on dietaryindex R package (James J. Zhan) &nbsp;|&nbsp; "
             "Pure Python implementation, no R required &nbsp;|&nbsp; "
             "Windows / macOS / Linux",
    },

    # ── 首页步骤 ──
    "home.step1": {
        "zh": "📂 选择指数",
        "en": "📂 Select Index",
    },
    "home.step2": {
        "zh": "📤 上传数据",
        "en": "📤 Upload Data",
    },
    "home.step3": {
        "zh": "📊 计算 & 导出",
        "en": "📊 Compute & Export",
    },

    # ── 首页数据模式卡片 ──
    "home.mode_general": {
        "zh": "通用版",
        "en": "General",
    },
    "home.mode_general_desc": {
        "zh": "CSV / Excel<br>列名手动映射",
        "en": "CSV / Excel<br>Manual column mapping",
    },
    "home.mode_nhanes_fped": {
        "zh": "NHANES FPED",
        "en": "NHANES FPED",
    },
    "home.mode_nhanes_fped_desc": {
        "zh": "2005年后<br>.sas7bdat + .XPT",
        "en": "Post-2005<br>.sas7bdat + .XPT",
    },
    "home.mode_nhanes_mped": {
        "zh": "NHANES MPED",
        "en": "NHANES MPED",
    },
    "home.mode_nhanes_mped_desc": {
        "zh": "1999–2004<br>equiv.txt + .XPT",
        "en": "1999–2004<br>equiv.txt + .XPT",
    },
    "home.mode_asa24": {
        "zh": "ASA24",
        "en": "ASA24",
    },
    "home.mode_asa24_desc": {
        "zh": "Totals.csv<br>系统自动汇总",
        "en": "Totals.csv<br>Auto aggregation",
    },
    "home.mode_dhq3_block": {
        "zh": "DHQ3 / BLOCK",
        "en": "DHQ3 / BLOCK",
    },
    "home.mode_dhq3_block_desc": {
        "zh": "FFQ 原始数据<br>一步式计算",
        "en": "FFQ raw data<br>One-step computation",
    },

    # ── 指数卡片（首页） ──
    "card.enter_compute": {
        "zh": "进入 {name} 计算 →",
        "en": "Compute {name} →",
    },
    "card.enter_compute_all": {
        "zh": "进入计算 →",
        "en": "Compute →",
    },

    # ── 指数名称 ──
    "index.dii": {"zh": "膳食炎症指数", "en": "Dietary Inflammatory Index"},
    "index.hei2020": {"zh": "健康饮食指数 2020", "en": "Healthy Eating Index 2020"},
    "index.hei2015": {"zh": "健康饮食指数 2015", "en": "Healthy Eating Index 2015"},
    "index.ahei": {"zh": "替代健康饮食指数", "en": "Alternative Healthy Eating Index"},
    "index.aheip": {"zh": "AHEI 孕期版", "en": "AHEI Pregnancy"},
    "index.dash": {"zh": "DASH 饮食评分", "en": "DASH Diet Score"},
    "index.dashi": {"zh": "DASH 营养密度版", "en": "DASH Nutrient Index"},
    "index.med": {"zh": "地中海饮食指数", "en": "Mediterranean Diet Score"},
    "index.medi": {"zh": "MEDI PREDIMED", "en": "MEDI PREDIMED"},
    "index.acs2020": {"zh": "ACS 膳食指数", "en": "ACS Dietary Index"},
    "index.phdi": {"zh": "行星健康饮食指数", "en": "Planetary Health Diet Index"},
    "index.di_gm": {"zh": "肠道微生物膳食指数", "en": "Dietary Index for Gut Microbiota"},

    # ── 页面标题 ──
    "page.title.dii": {"zh": "DII 膳食炎症指数", "en": "DII — Dietary Inflammatory Index"},
    "page.title.hei2020": {"zh": "HEI2020 健康膳食指数", "en": "HEI2020 — Healthy Eating Index 2020"},
    "page.title.hei2015": {"zh": "HEI2015 健康膳食指数", "en": "HEI2015 — Healthy Eating Index 2015"},
    "page.title.ahei": {"zh": "AHEI 替代健康膳食指数", "en": "AHEI — Alternative Healthy Eating Index"},
    "page.title.aheip": {"zh": "AHEIP 孕期替代健康膳食指数", "en": "AHEIP — AHEI Pregnancy"},
    "page.title.dash": {"zh": "DASH 高血压防治膳食评分", "en": "DASH — Dietary Approaches to Stop Hypertension"},
    "page.title.dashi": {"zh": "DASHI 高血压防治营养密度指数", "en": "DASHI — DASH Nutrient Index"},
    "page.title.med": {"zh": "MED 地中海膳食评分", "en": "MED — Mediterranean Diet Score"},
    "page.title.medi": {"zh": "MEDI 地中海膳食指数（改进版）", "en": "MEDI — Mediterranean Diet Index (PREDIMED)"},
    "page.title.acs2020": {"zh": "ACS2020 癌症协会膳食指数", "en": "ACS2020 — Cancer Society Dietary Index"},
    "page.title.phdi": {"zh": "PHDI 行星健康膳食指数", "en": "PHDI — Planetary Health Diet Index"},
    "page.title.di_gm": {"zh": "DI-GM 肠道微生物膳食指数", "en": "DI-GM — Dietary Index for Gut Microbiota"},
    "page.title.guide": {"zh": "使用指南", "en": "User Guide"},
    "page.title.figures": {"zh": "论文图表与表格", "en": "Figures & Tables"},

    # ── 通用 UI ──
    "ui.select_mode": {
        "zh": "📂 选择数据上传模式",
        "en": "📂 Select Data Upload Mode",
    },
    "ui.select_mode_prompt": {
        "zh": "请根据您的数据来源选择对应的上传模式：",
        "en": "Please select the upload mode based on your data source:",
    },
    "ui.quick_experience": {
        "zh": "快速体验",
        "en": "Quick Experience",
    },
    "ui.demo_sample": {
        "zh": "演示版样本",
        "en": "Demo Sample",
    },
    "ui.consistency_sample": {
        "zh": "一致性测试版样本",
        "en": "Consistency Test Sample",
    },
    "ui.one_click_analyze_demo": {
        "zh": "⚡ 一键分析演示版（50条）",
        "en": "⚡ Analyze Demo (50 rows)",
    },
    "ui.one_click_analyze_consistency": {
        "zh": "🧪 一键分析一致性测试版（50条）",
        "en": "🧪 Analyze Consistency Test (50 rows)",
    },
    "ui.download_demo_csv": {
        "zh": "📥 下载演示版示例 CSV（50条）",
        "en": "📥 Download Demo CSV (50 rows)",
    },
    "ui.download_consistency_csv": {
        "zh": "📥 下载一致性测试版 CSV（50条）",
        "en": "📥 Download Consistency Test CSV (50 rows)",
    },
    "ui.preview_demo_data": {
        "zh": "📋 预览演示版示例数据",
        "en": "📋 Preview Demo Data",
    },
    "ui.preview_consistency_data": {
        "zh": "📋 预览一致性测试版示例数据",
        "en": "📋 Preview Consistency Test Data",
    },
    "ui.upload_file": {
        "zh": "上传数据文件",
        "en": "Upload Data File",
    },
    "ui.loaded_data": {
        "zh": "已加载 {rows} 行 x {cols} 列数据",
        "en": "Loaded {rows} rows x {cols} columns",
    },
    "ui.preview_data": {
        "zh": "📋 预览数据",
        "en": "📋 Preview Data",
    },
    "ui.basic_params": {
        "zh": "基本信息参数",
        "en": "Basic Parameters",
    },
    "ui.column_mapping": {
        "zh": "数据列映射",
        "en": "Column Mapping",
    },
    "ui.compute_button": {
        "zh": "🚀 计算 {title}",
        "en": "🚀 Compute {title}",
    },
    "ui.download_template": {
        "zh": "📄 下载空白模板CSV",
        "en": "📄 Download Blank Template CSV",
    },
    "ui.file_format_info": {
        "zh": "📋 文件格式说明",
        "en": "📋 File Format Info",
    },
    "ui.upload_files": {
        "zh": "📤 上传文件",
        "en": "📤 Upload Files",
    },
    "ui.day1_required": {
        "zh": "第1天（Day 1）— 必需",
        "en": "Day 1 — Required",
    },
    "ui.day2_optional": {
        "zh": "第2天（Day 2）— 可选",
        "en": "Day 2 — Optional",
    },
    "ui.compute_success": {
        "zh": "🎉 {title} 计算成功！结果图表和数据已在下方生成。",
        "en": "🎉 {title} computed! Results are shown below.",
    },
    "ui.compute_complete": {
        "zh": "{title} 计算完成",
        "en": "{title} Computation Complete",
    },
    "ui.result_generated": {
        "zh": "结果图表和数据已在下方生成",
        "en": "Results are generated below",
    },
    "ui.jump_to_result": {
        "zh": "👇 跳转",
        "en": "👇 Jump",
    },

    # ── DII 特殊 ──
    "dii.template_hint": {
        "zh": "下方 Excel 为参考模板，用于查看标准列名和参数说明；50 条示例数据请使用下方的演示版或一致性测试版入口。",
        "en": "The Excel files below are reference templates for column names and parameter descriptions. "
              "For 50-row sample data, use the Demo or Consistency Test entry below.",
    },
    "dii.download_cn": {
        "zh": "📄 下载参考模板 (中文版 .xlsx)",
        "en": "📄 Download Reference Template (Chinese .xlsx)",
    },
    "dii.download_en": {
        "zh": "📄 Download Reference Template (English .xlsx)",
        "en": "📄 Download Reference Template (English .xlsx)",
    },

    # ── 评分报告 ──
    "score.total_score": {
        "zh": "总分",
        "en": "Total Score",
    },
    "score.component_scores": {
        "zh": "组分得分详情",
        "en": "Component Score Details",
    },
    "score.distribution": {
        "zh": "分数分布",
        "en": "Score Distribution",
    },
    "score.download_results": {
        "zh": "📥 下载计算结果 (CSV)",
        "en": "📥 Download Results (CSV)",
    },

    # ── 版本选择 ──
    "version.select.acs2020": {
        "zh": "选择计算版本：",
        "en": "Select computation version:",
    },
    "version.select.phdi": {
        "zh": "选择计算版本：",
        "en": "Select computation version:",
    },
    "version.select.hei2020": {
        "zh": "选择计算版本：",
        "en": "Select computation version:",
    },
    "version.select.medi": {
        "zh": "选择计算版本：",
        "en": "Select computation version:",
    },

    # ── 参考文献 ──
    "ref.title.dii": {
        "zh": "📚 DII 参考文献",
        "en": "📚 DII References",
    },
    "ref.title.hei2020": {
        "zh": "📚 参考文献",
        "en": "📚 References",
    },

    # ── 错误/提示 ──
    "error.no_data": {
        "zh": "请先上传数据文件或选择示例数据。",
        "en": "Please upload a data file or select sample data first.",
    },
    "error.column_not_found": {
        "zh": "未找到列: {cols}",
        "en": "Columns not found: {cols}",
    },
}

# ── 辅助函数 ──

def get_lang():
    """获取当前语言，默认中文"""
    if "lang" not in st.session_state:
        st.session_state.lang = "en"
    return st.session_state.lang


def t(key, **kwargs):
    """
    获取翻译文本
    用法: t("sidebar.home") -> "首页" 或 "Home"
          t("ui.loaded_data", rows=50, cols=10) -> "已加载 50 行 x 10 列数据"
    """
    lang = get_lang()
    entry = TRANSLATIONS.get(key)
    if entry is None:
        return key
    text = entry.get(lang, entry.get("zh", key))
    if kwargs:
        return text.format(**kwargs)
    return text


def set_lang(lang):
    """设置语言"""
    st.session_state.lang = lang
