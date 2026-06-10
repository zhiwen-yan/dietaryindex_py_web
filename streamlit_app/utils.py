"""
Streamlit 页面通用工具模块
"""

import sys
import os
from io import BytesIO

import streamlit as st
import pandas as pd
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.params import INDEX_PARAMS
from config.i18n import get_lang
from config.templates import generate_generic_template

# 延迟导入：FUNCTION_MAP 仅在 _run_computation 被调用时才需要
_FUNCTION_MAP = None


def _get_function_map():
    global _FUNCTION_MAP
    if _FUNCTION_MAP is None:
        from dietaryindex import (
            compute_dii, compute_hei2015, compute_hei2020, compute_hei2020_v2,
            compute_ahei, compute_aheip, compute_dash, compute_dashi,
            compute_med, compute_medi, compute_medi_v2,
            compute_acs2020_v1, compute_acs2020_v2,
            compute_phdi, compute_phdi_v2, compute_di_gm,
            compute_hei2015_nhanes_fped, compute_hei2020_nhanes_fped,
            compute_med_nhanes_fped, compute_dashi_nhanes_fped,
            compute_dash_nhanes_fped, compute_ahei_nhanes_fped,
            compute_medi_nhanes_fped, compute_di_gm_nhanes_fped,
        )
        _FUNCTION_MAP = {
            "compute_dii": compute_dii,
            "compute_hei2015": compute_hei2015,
            "compute_hei2020": compute_hei2020,
            "compute_hei2020_v2": compute_hei2020_v2,
            "compute_ahei": compute_ahei,
            "compute_aheip": compute_aheip,
            "compute_dash": compute_dash,
            "compute_dashi": compute_dashi,
            "compute_med": compute_med,
            "compute_medi": compute_medi,
            "compute_medi_v2": compute_medi_v2,
            "compute_acs2020_v1": compute_acs2020_v1,
            "compute_acs2020_v2": compute_acs2020_v2,
            "compute_phdi": compute_phdi,
            "compute_phdi_v2": compute_phdi_v2,
            "compute_di_gm": compute_di_gm,
        }
    return _FUNCTION_MAP


FUNCTION_MAP = _get_function_map  # 旧引用兼容，改用函数调用


# NHANES_ADAPTER_MAP 仅在 legacy render_index_page 中使用
_NHANES_ADAPTER_MAP = None

def _get_nhanes_adapter_map():
    global _NHANES_ADAPTER_MAP
    if _NHANES_ADAPTER_MAP is None:
        from dietaryindex import (
            compute_hei2015_nhanes_fped, compute_hei2020_nhanes_fped,
            compute_med_nhanes_fped, compute_dashi_nhanes_fped,
            compute_dash_nhanes_fped, compute_ahei_nhanes_fped,
            compute_medi_nhanes_fped, compute_di_gm_nhanes_fped,
        )
        _NHANES_ADAPTER_MAP = {
            "HEI2015": compute_hei2015_nhanes_fped,
            "HEI2020": compute_hei2020_nhanes_fped,
            "MED": compute_med_nhanes_fped,
            "DASHI": compute_dashi_nhanes_fped,
            "DASH": compute_dash_nhanes_fped,
            "AHEI": compute_ahei_nhanes_fped,
            "MEDI": compute_medi_nhanes_fped,
            "DI_GM": compute_di_gm_nhanes_fped,
        }
    return _NHANES_ADAPTER_MAP


NHANES_ADAPTER_MAP = _get_nhanes_adapter_map  # 旧引用兼容

NHANES_ADAPTER_FILES = {
    "HEI2015": "FPED tot (fped_dr1tot*.sas7bdat) + NUTRIENT tot (DR1TOT*.XPT) + DEMO (*.XPT)",
    "HEI2020": "FPED tot (fped_dr1tot*.sas7bdat) + NUTRIENT tot (DR1TOT*.XPT) + DEMO (*.XPT, RIDAGEYR)",
    "MED": "FPED tot (fpre_dr1tot*.sas7bdat) + NUTRIENT tot (DR1TOT*.XPT) + DEMO (*.XPT)",
    "DASHI": "NUTRIENT tot (DR1TOT*.XPT) + DEMO (*.XPT)",
    "DASH": "FPED iff (fped_dr1iff*.sas7bdat) + NUTRIENT iff (DR1IFF*.XPT) + DEMO (*.XPT)",
    "AHEI": "FPED iff (fped_dr1iff*.sas7bdat) + NUTRIENT iff (DR1IFF*.XPT) + DEMO (*.XPT, RIAGENDR)",
    "MEDI": "FPED iff (fped_dr1iff*.sas7bdat) + NUTRIENT iff (DR1IFF*.XPT) + DEMO (*.XPT)",
    "DI_GM": "FPED iff (fped_dr1iff*.sas7bdat) + NUTRIENT iff (DR1IFF*.XPT) + DEMO (*.XPT, RIAGENDR)",
}


def load_data(uploaded_file):
    """加载上传的数据文件，支持 CSV / Excel / XPT / sas7bdat"""
    fname = uploaded_file.name.lower()

    if fname.endswith(".csv"):
        return pd.read_csv(uploaded_file)
    elif fname.endswith(".xlsx"):
        return pd.read_excel(uploaded_file, engine="openpyxl")
    elif fname.endswith(".xls"):
        return pd.read_excel(uploaded_file, engine="xlrd")
    elif fname.endswith(".xpt"):
        try:
            return pd.read_sas(uploaded_file, format="xport")
        except Exception:
            import pyreadstat
            data_bytes = uploaded_file.read()
            df, _ = pyreadstat.read_xport(BytesIO(data_bytes))
            return df
    elif fname.endswith(".sas7bdat"):
        import pyreadstat
        data_bytes = uploaded_file.read()
        df, _ = pyreadstat.read_sas7bdat(BytesIO(data_bytes))
        return df
    else:
        lang = get_lang()
        st.error(f"Unsupported file format: {uploaded_file.name}" if lang == "en" else f"不支持的文件格式: {uploaded_file.name}")
        return None


def to_excel_download(df, filename="results.xlsx"):
    """将 DataFrame 转为 Excel 下载按钮"""
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Results")
    output.seek(0)
    return output


@st.cache_data
def convert_df_to_excel_bytes(df):
    return to_excel_download(df)


# ── Component column detection ────────────────────────────────────────────

_COMPONENT_EXCLUDE = {
    "RESPONDENTID", "SEQN", "SDDSRVYR", "RIDAGEYR", "RIAGENDR",
}

def _detect_component_cols(result, index_key):
    """Detect component score columns from result DataFrame."""
    prefix_map = {
        "DII": "DII_",
        "HEI2020": "HEI2020_",
        "HEI2015": "HEI2015_",
        "AHEI": "AHEI_",
        "AHEIP": "AHEIP_",
        "DASH": "DASH_",
        "DASHI": "DASHI_",
        "MED": "MED_",
        "MEDI": "MEDI_",
        "MEDI_V1": "MEDI_",
        "MEDI_V2": "MEDI_",
        "ACS2020": "ACS2020_",
        "ACS2020_V1": "ACS2020_",
        "ACS2020_V2": "ACS2020_",
        "PHDI": "PHDI_",
        "DI_GM": "DI_GM_",
    }
    prefix = prefix_map.get(index_key, f"{index_key}_")
    total_suffixes = {"ALL", "NOETOH", "TOTAL", "V1_ALL", "V2_ALL"}
    comps = []
    for col in result.columns:
        if col in _COMPONENT_EXCLUDE:
            continue
        if col.startswith(prefix):
            col_suffix = col[len(prefix):]
            if col_suffix in total_suffixes:
                continue
            comps.append(col)
    return comps


# ── Result Display with Charts ────────────────────────────────────────────

def _show_result(result, cfg, index_key):
    """展示计算结果 — 增强版，含评分报告、柱状图、雷达图"""
    lang = get_lang()
    is_en = lang == "en"

    output_cols = cfg.get("output_cols", [])
    main_col = output_cols[0] if output_cols else None

    # ── Score Report Header ──
    title_display = cfg["title_en"] if is_en else cfg["title"]
    st.markdown(f"""
    <div class="score-report">
        <div class="report-title">📊 {title_display} {"· Report" if is_en else "· 计算报告"}</div>
    """, unsafe_allow_html=True)

    # ── Stat Cards Row ──
    stat_cols = st.columns(4)
    with stat_cols[0]:
        st.metric("📋 N" if is_en else "📋 样本量", f"{len(result):,}")
    with stat_cols[1]:
        if main_col and main_col in result.columns:
            mean_val = result[main_col].mean()
            st.metric("📈 Mean" if is_en else "📈 平均得分", f"{mean_val:.2f}")
    with stat_cols[2]:
        if main_col and main_col in result.columns:
            std_val = result[main_col].std()
            st.metric("📐 SD" if is_en else "📐 标准差", f"{std_val:.2f}")
    with stat_cols[3]:
        if main_col and main_col in result.columns:
            median_val = result[main_col].median()
            st.metric("📍 Median" if is_en else "📍 中位数", f"{median_val:.2f}")

    st.markdown("---")

    # ── Distribution Chart ──
    if main_col and main_col in result.columns:
        col_chart, col_table = st.columns([3, 2])

        with col_chart:
            st.markdown("##### 📊 Score Distribution" if is_en else "##### 📊 得分分布")
            try:
                import plotly.express as px
                fig = px.histogram(
                    result, x=main_col, nbins=30,
                    title=f"{title_display} Distribution" if is_en else f"{title_display} 分布",
                    color_discrete_sequence=["#2d8c6e"],
                    marginal="box",
                )
                fig.update_layout(
                    bargap=0.08,
                    template="plotly_white",
                    margin=dict(l=20, r=20, t=40, b=20),
                    height=320,
                    xaxis_title="Score" if is_en else "得分",
                    yaxis_title="Count" if is_en else "频数",
                )
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
            except Exception:
                st.caption("Chart failed to load. Please check the data table below." if is_en else "图表加载失败，请查看下方数据表")

        with col_table:
            st.markdown("##### 📋 Summary Statistics" if is_en else "##### 📋 描述统计")
            stats = result[main_col].describe().to_frame().T
            stats.index = ["Value" if is_en else "统计值"]
            st.dataframe(stats.style.format("{:.2f}"), use_container_width=True)

    # ── Component Charts ──
    component_cols = _detect_component_cols(result, index_key)

    if len(component_cols) >= 3:
        st.markdown("---")
        tab_bar, tab_radar = st.tabs(["📊 Bar Chart" if is_en else "📊 组分柱状图", "🎯 Radar Chart" if is_en else "🎯 组分雷达图"])

        with tab_bar:
            comp_data = result[component_cols].mean().sort_values(ascending=False).reset_index()
            comp_data.columns = ["Component" if is_en else "组分", "Mean" if is_en else "平均分"]

            try:
                import plotly.express as px
                fig = px.bar(
                    comp_data, x=comp_data.columns[0], y=comp_data.columns[1],
                    title=f"{title_display} Component Means" if is_en else f"{title_display} 各组分平均得分",
                    color_discrete_sequence=["#2d8c6e"],
                    text_auto=".2f",
                )
                fig.update_traces(textposition="outside", textfont_size=11)
                fig.update_layout(
                    template="plotly_white",
                    margin=dict(l=20, r=20, t=40, b=60),
                    height=400,
                    xaxis_tickangle=-30,
                )
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
            except Exception:
                st.caption("Bar chart failed to load." if is_en else "柱状图加载失败")

        with tab_radar:
            if len(component_cols) >= 3:
                try:
                    comp_means = result[component_cols].mean()
                    r_values = list(comp_means.values)
                    r_labels = [c.replace(f"{index_key}_", "") for c in component_cols]
                    r_values.append(r_values[0])
                    r_labels.append(r_labels[0])

                    fig = px.line_polar(
                        r=r_values, theta=r_labels,
                        line_close=True,
                        title=f"{title_display} Radar Chart" if is_en else f"{title_display} 组分雷达图",
                    )
                    fig.update_traces(fill="toself", fillcolor="rgba(45,140,110,0.3)", line=dict(color="#2d8c6e", width=2))
                    fig.update_layout(
                        template="plotly_white",
                        margin=dict(l=40, r=40, t=60, b=40),
                        height=450,
                        polar=dict(
                            radialaxis=dict(visible=True, range=[0, max(r_values) * 1.1]),
                        ),
                    )
                    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
                except Exception:
                    st.caption("Radar chart failed to load." if is_en else "雷达图加载失败")

    # ── Data Table ──
    st.markdown("---")
    st.markdown("##### 📋 Data Table" if is_en else "##### 📋 完整数据表")
    with st.expander("Expand to view data" if is_en else "展开查看完整数据", expanded=False):
        st.dataframe(result, use_container_width=True)

    # ── Export Panel ──
    st.markdown("---")

    exp_col1, exp_col2, exp_col3 = st.columns(3)
    with exp_col1:
        excel_bytes = to_excel_download(result, f"{index_key}_results.xlsx")
        st.download_button(
            "📥 Download Excel (.xlsx)" if is_en else "📥 下载 Excel 结果 (.xlsx)",
            excel_bytes,
            file_name=f"{index_key}_results.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )
    with exp_col2:
        csv_data = result.to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            "📥 Download CSV (.csv)" if is_en else "📥 下载 CSV 结果 (.csv)",
            csv_data,
            file_name=f"{index_key}_results.csv",
            mime="text/csv",
            use_container_width=True,
        )
    with exp_col3:
        st.caption(f"{len(result)} rows × {len(result.columns)} cols" if is_en else f"共 {len(result)} 行 × {len(result.columns)} 列")

    st.markdown("</div>", unsafe_allow_html=True)


# ── Computation ───────────────────────────────────────────────────────────

def _run_computation(index_key, cfg, df, col_mapping):
    """执行计算，返回计算结果 DataFrame"""
    lang = get_lang()
    is_en = lang == "en"
    with st.spinner("Computing..." if is_en else "正在计算中..."):
        try:
            func_name = cfg["function"]
            func = FUNCTION_MAP()[func_name]

            extra_params = cfg.get("extra_params", [])

            respondent_id_val = None
            extra_vals = {}

            for ep in extra_params:
                val = col_mapping.get(ep["name"])
                if ep["name"] == "respondent_id":
                    if val is not None and isinstance(val, str) and val in df.columns:
                        respondent_id_val = df[val].values
                    elif val is None:
                        respondent_id_val = None
                    elif isinstance(val, (int, float)):
                        respondent_id_val = int(val) if val == int(val) else val
                    else:
                        respondent_id_val = val
                else:
                    if val is not None and isinstance(val, str) and val in df.columns:
                        extra_vals[ep["name"]] = df[val].values
                    elif isinstance(val, (int, float, np.ndarray)):
                        extra_vals[ep["name"]] = val
                    else:
                        extra_vals[ep["name"]] = val

            if index_key == "DII":
                kwargs = {"respondent_id": respondent_id_val}
                repeat_num = extra_vals.get("repeat_num", 1)
                kwargs["repeat_num"] = repeat_num
                for group in cfg.get("groups", []):
                    for p in group["params"]:
                        mapped_col = col_mapping.get(p["name"])
                        if mapped_col is not None and mapped_col in df.columns:
                            kwargs[p["name"]] = df[mapped_col].values
                        elif p.get("required"):
                            label = p["label_en"] if is_en else p["label"]
                            st.error(f"Missing required parameter: {label}" if is_en else f"缺少必需参数: {label}")
                            return None
                result = compute_dii(data=df, **kwargs)
            else:
                param_order = _get_param_order(func, index_key)

                args = {}
                for param_name in param_order:
                    if param_name == "data":
                        args["data"] = df
                    elif param_name == "respondent_id":
                        args["respondent_id"] = respondent_id_val if respondent_id_val is not None else np.arange(1, len(df) + 1)
                    elif param_name in extra_vals:
                        args[param_name] = extra_vals[param_name]
                    else:
                        mapped_col = col_mapping.get(param_name)
                        if mapped_col is not None and mapped_col in df.columns:
                            args[param_name] = df[mapped_col].values
                        else:
                            is_required = False
                            for group in cfg.get("groups", []):
                                for p in group["params"]:
                                    if p["name"] == param_name and p.get("required"):
                                        is_required = True
                            if is_required:
                                st.error(f"Missing required parameter: {param_name}" if is_en else f"缺少必需参数: {param_name}")
                                return None

                result = func(**args)

            return result

        except Exception as e:
            st.error(f"Computation error: {type(e).__name__}: {e}" if is_en else f"计算出错: {type(e).__name__}: {e}")
            st.exception(e)
            return None


def _get_param_order(func, index_key):
    """获取函数参数名顺序"""
    import inspect
    sig = inspect.signature(func)
    return list(sig.parameters.keys())


# ── Generic Index Page (legacy, kept for DII page) ────────────────────────

def render_index_page(index_key):
    """渲染指数计算通用页面，支持 NHANES FPED 快速模式 (legacy)"""
    cfg = INDEX_PARAMS[index_key]

    st.title(cfg["title"])
    st.markdown(f"*{cfg['title_en']}*")
    st.markdown(cfg["description"])
    if cfg.get("max_score"):
        st.info(f"总分范围: 0\u2013{cfg['max_score']}")

    nhanes_adapter = NHANES_ADAPTER_MAP().get(index_key)

    if nhanes_adapter is not None:
        st.markdown("---")
        st.subheader("\U0001f4e6 NHANES FPED 快速模式 (2005+)")
        st.caption(f"直接上传 NHANES 原始文件，一步完成计算。所需文件：{NHANES_ADAPTER_FILES.get(index_key, '')}")

        with st.expander("\U0001f504 展开 NHANES FPED 快速上传", expanded=False):
            is_iff = index_key in ["DASH", "AHEI", "MEDI", "DI_GM"]
            if is_iff:
                col1, col2 = st.columns(2)
                with col1:
                    fped_ind_file = st.file_uploader(
                        "Day1 FPED iff 文件 (DR1IFF)", type=["sas7bdat", "xpt"],
                        key=f"nhanes_fped_ind_{index_key}",
                        help="fped_dr1iff_XXXX.sas7bdat"
                    )
                    nut_ind1_file = st.file_uploader(
                        "Day1 营养 iff 文件 (DR1IFF)", type=["xpt", "XPT"],
                        key=f"nhanes_nut_ind1_{index_key}",
                        help="DR1IFF_J.XPT"
                    )
                with col2:
                    fped_ind2_file = st.file_uploader(
                        "Day2 FPED iff 文件 (可选)", type=["sas7bdat", "xpt"],
                        key=f"nhanes_fped_ind2_{index_key}",
                        help="fped_dr2iff_XXXX.sas7bdat (可选)"
                    )
                    nut_ind2_file = st.file_uploader(
                        "Day2 营养 iff 文件 (可选)", type=["xpt", "XPT"],
                        key=f"nhanes_nut_ind2_{index_key}",
                        help="DR2IFF_J.XPT (可选)"
                    )
                demo_file = st.file_uploader(
                    "人口学文件 DEMO", type=["xpt", "XPT"],
                    key=f"nhanes_demo_{index_key}",
                    help="DEMO_J.XPT / demo_d.xpt (AHEI/DI_GM 需要含 RIAGENDR)"
                )
            else:
                col1, col2 = st.columns(2)
                with col1:
                    fped_file = st.file_uploader(
                        "Day1 FPED tot 文件", type=["sas7bdat", "xpt"],
                        key=f"nhanes_fped_{index_key}",
                        help="fped_dr1tot_XXXX.sas7bdat / fpre_dr1tot_XXXX.sas7bdat"
                    )
                    nut1_file = st.file_uploader(
                        "Day1 营养文件 (DR1TOT)", type=["xpt", "XPT"],
                        key=f"nhanes_nut1_{index_key}",
                        help="DR1TOT_J.XPT / dr1tot_d.xpt"
                    )
                with col2:
                    fped2_file = st.file_uploader(
                        "Day2 FPED tot 文件 (可选)", type=["sas7bdat", "xpt"],
                        key=f"nhanes_fped2_{index_key}",
                        help="fped_dr2tot_XXXX.sas7bdat (可选)"
                    )
                    nut2_file = st.file_uploader(
                        "Day2 营养文件 (可选)", type=["xpt", "XPT"],
                        key=f"nhanes_nut2_{index_key}",
                        help="DR2TOT_J.XPT (可选)"
                    )
                demo_file = st.file_uploader(
                    "人口学文件 DEMO", type=["xpt", "XPT"],
                    key=f"nhanes_demo_{index_key}",
                    help="DEMO_J.XPT / demo_d.xpt"
                )

            if st.button("\U0001f680 开始 NHANES FPED 计算", type="primary", use_container_width=True,
                         key=f"nhanes_compute_{index_key}"):
                if is_iff:
                    if nut_ind1_file is None:
                        st.error("请上传 Day1 营养 iff 文件 (DR1IFF)")
                    else:
                        with st.spinner(f"正在计算 {cfg['title']} (NHANES FPED iff)..."):
                            try:
                                result = nhanes_adapter(
                                    fped_ind_path=fped_ind_file or None,
                                    nutrient_ind_path=nut_ind1_file,
                                    fped_ind_path2=fped_ind2_file or None,
                                    nutrient_ind_path2=nut_ind2_file or None,
                                    demo_path=demo_file or None,
                                )
                                _show_result(result, cfg, index_key)
                            except Exception as e:
                                st.error(f"计算出错: {type(e).__name__}: {e}")
                                st.exception(e)
                else:
                    if nut1_file is None:
                        st.error("请上传 Day1 营养文件 (DR1TOT)")
                    else:
                        with st.spinner(f"正在计算 {cfg['title']} (NHANES FPED)..."):
                            try:
                                if index_key == "DASHI":
                                    result = nhanes_adapter(
                                        nutrient_path=nut1_file,
                                        nutrient_path2=nut2_file or None,
                                        demo_path=demo_file or None,
                                    )
                                else:
                                    result = nhanes_adapter(
                                        fped_path=fped_file,
                                        nutrient_path=nut1_file,
                                        demo_path=demo_file or None,
                                        fped_path2=fped2_file or None,
                                        nutrient_path2=nut2_file or None,
                                    )
                                _show_result(result, cfg, index_key)
                            except Exception as e:
                                st.error(f"计算出错: {type(e).__name__}: {e}")
                                st.exception(e)

    st.markdown("---")
    st.subheader("\U0001f4c2 通用上传模式")
    st.caption("上传已预处理好的膳食摄入数据文件（CSV/Excel），手动映射列名后计算。")

    uploaded_file = st.file_uploader(
        "上传数据文件",
        type=["csv", "xlsx", "xls", "xpt", "sas7bdat"],
        key=f"file_{index_key}",
        help="支持 CSV / Excel / SAS XPT / SAS sas7bdat",
    )

    if uploaded_file is not None:
        df = load_data(uploaded_file)
        if df is None:
            st.stop()

        st.success(f"已加载 {len(df)} 行 x {len(df.columns)} 列数据")
        with st.expander("\U0001f4cb 预览数据", expanded=False):
            st.dataframe(df.head(20), use_container_width=True)

        all_columns = ["--- 请选择列 ---"] + list(df.columns)
        col_mapping = {}

        extra_params = cfg.get("extra_params", [])
        if extra_params:
            st.subheader("基本信息参数")
            ep_cols = st.columns(min(len(extra_params), 4))
            for i, ep in enumerate(extra_params):
                with ep_cols[i % 4]:
                    if ep["name"] in ["respondent_id", "gender", "age"]:
                        selected = st.selectbox(
                            ep["label"],
                            all_columns,
                            key=f"ep_{index_key}_{ep['name']}",
                            help=ep.get("label_en", ""),
                        )
                        col_mapping[ep["name"]] = selected if selected != all_columns[0] else None
                    else:
                        col_mapping[ep["name"]] = st.number_input(
                            ep["label"],
                            value=ep.get("default", 1),
                            key=f"ep_{index_key}_{ep['name']}",
                        )

        st.subheader("数据列映射")
        st.caption("将您数据中的列对应到以下参数。未映射的参数将不参与计算。")

        groups = cfg.get("groups", [])
        for gi, group in enumerate(groups):
            with st.expander(f"\U0001f4ce {group['name']} ({group['name_en']})", expanded=(gi == 0)):
                params = group["params"]
                pcols = st.columns(min(len(params), 3))
                for i, p in enumerate(params):
                    with pcols[i % 3]:
                        selected = st.selectbox(
                            f"{p['label']} [{p['name']}]",
                            all_columns,
                            key=f"param_{index_key}_{p['name']}",
                            help=p.get("label_en", ""),
                        )
                        col_mapping[p["name"]] = selected if selected != all_columns[0] else None

        st.markdown("---")

        c1, c2, c3 = st.columns([1, 1, 2])
        with c1:
            compute_clicked = st.button(f"\U0001f680 计算 {cfg['title']}", type="primary", use_container_width=True)
        with c2:
            template_data = _get_template_data(index_key, groups, extra_params)
            st.download_button(
                "\U0001f4e5 下载模板CSV",
                template_data,
                file_name=f"{index_key}_template.csv",
                mime="text/csv",
                use_container_width=True,
            )

        if compute_clicked:
            _run_computation(index_key, cfg, df, col_mapping)


def _get_template_data(index_key, groups, extra_params):
    """获取模板CSV数据"""
    all_params = []
    if extra_params:
        for ep in extra_params:
            all_params.append((ep["name"], ep["label"]))
    for group in groups:
        for p in group["params"]:
            all_params.append((p["name"], p["label"]))
    return generate_generic_template(all_params)


def _run_asa24_for_index(index_key, cfg, df, recall_summarize=True):
    """从 ASA24 Totals.csv 数据计算指定指数，支持回忆合并。"""
    from render_utils import _auto_map_columns

    # 1. 自动映射列名
    auto_mapping = _auto_map_columns(df, index_key, cfg)

    # 2. 回忆合并
    if recall_summarize:
        id_col = None
        for candidate in ["UserName", "username", "USERNAME", "UserName"]:
            if candidate in df.columns:
                id_col = candidate
                break

        if id_col is not None:
            # 找到所有被映射的列
            mapped_cols = [v for k, v in auto_mapping.items() if v is not None and isinstance(v, str) and v in df.columns]
            agg_dict = {}
            for col in mapped_cols:
                if pd.api.types.is_numeric_dtype(df[col]):
                    agg_dict[col] = "mean"
                else:
                    agg_dict[col] = "first"

            resp_col = auto_mapping.get("respondent_id")
            if resp_col and resp_col in df.columns and resp_col != id_col:
                agg_dict[resp_col] = "first"

            df = df.groupby(id_col, as_index=False).agg(agg_dict)
            auto_mapping["respondent_id"] = id_col

    # 3. 运行计算
    col_mapping = {k: v for k, v in auto_mapping.items() if v is not None}
    return _run_computation(index_key, cfg, df, col_mapping)

