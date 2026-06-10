"""
使用指南
"""

import sys
import os
import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sidebar_utils import render_sidebar
from config.i18n import get_lang

lang = get_lang()
is_en = lang == "en"

st.set_page_config(page_title="User Guide" if is_en else "使用指南", page_icon="📖", layout="wide")
render_sidebar("guide")

st.title("📖 User Guide" if is_en else "📖 使用指南")

if is_en:
    st.markdown("""
    <div class="info-box">
        <p>This platform is built on the <b>dietaryindex</b> Python package. With a serverless architecture, all computation runs entirely in the browser, addressing a critical ethical consideration in dietary research: no dietary intake data is ever transmitted to or stored on a remote server. The platform satisfies data governance requirements of Institutional Review Boards that may impose restrictions on cloud computing for sensitive health data. For studies involving sensitive health data, the platform can also be deployed on local or institutional servers to meet data governance and privacy protection needs. The dietaryindex Python package was developed with reference to the dietaryindex R package.</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    tab1, tab2, tab3, tab4 = st.tabs(["🚀 Quick Start", "📋 Index Overview", "📂 Data Modes", "📚 References"])
    with tab1:
        st.markdown("""
        ### Three Steps to Compute

        <div class="step-flow">
            <div class="step-item">
                <div class="step-number">1</div>
                <div class="step-text">📂 Select Index<br><small>Choose a dietary index from the sidebar</small></div>
            </div>
            <div class="step-arrow">→</div>
            <div class="step-item">
                <div class="step-number">2</div>
                <div class="step-text">📤 Upload Data<br><small>Select data source mode and upload files</small></div>
            </div>
            <div class="step-arrow">→</div>
            <div class="step-item">
                <div class="step-number">3</div>
                <div class="step-text">📊 Compute & Export<br><small>Map columns, compute, view charts and export</small></div>
            </div>
        </div>

        ### Detailed Steps

        **1. Select Index** — Choose the dietary index you need from the sidebar. The homepage shows all 12 indices with descriptions, click to jump directly.

        **2. Prepare Data** — Data should be tabular (CSV / Excel / SAS), one row per participant, one column per food/nutrient variable.

        **3. Choose Upload Mode** — After entering an index page, select based on data source:
        - **General**: Pre-processed CSV/Excel, manual column mapping
        - **NHANES FPED**: NHANES 2005+ raw files
        - **NHANES MPED**: NHANES 1999–2004 raw files
        - **ASA24**: ASA24 Totals.csv
        - **DHQ3 / BLOCK**: FFQ raw data

        **4. Map Columns** (General mode) — Map your data columns to system parameters. Unneeded parameters can be skipped.

        **5. Compute & View Report** — After clicking compute, you'll get:
        - Score distribution histogram + box plot
        - Component bar chart + radar chart
        - Full data table + Excel/CSV download
        """, unsafe_allow_html=True)
    with tab2:
        st.markdown("""
        ### All 12 Dietary Indices

        | Index | Name | Components | Score | Method |
        |------|------|:---:|:----:|---------|
        | 🔥 DII | Dietary Inflammatory Index | 45 | No limit | Z-score × Inflammatory Score |
        | 📊 HEI-2020 | Healthy Eating Index 2020 | 13 | 0–100 | Density method (per 1000 kcal) |
        | 📊 HEI-2015 | Healthy Eating Index 2015 | 13 | 0–100 | Density method |
        | 🫀 AHEI | Alternative HEI | 11 | 0–110 | Gender-specific continuous |
        | 🤰 AHEIP | AHEI Pregnancy | 9 | 0–90 | Pregnancy-specific |
        | 💚 DASH | DASH Diet Score | 8 | 8–40 | Quintile ranking |
        | ❤️ DASHI | DASH Nutrient Density | 9 | 0–9 | Nutrient linear scoring |
        | 🫒 MED | Mediterranean Diet | 9 | 0–9 | Median ranking |
        | 🐟 MEDI | MEDI (PREDIMED) | 11 | 0–11 | Absolute threshold binary |
        | 🎗️ ACS2020 | ACS Cancer Prevention | 8 | 0–15 | Gender-stratified quartile |
        | 🌍 PHDI | Planetary Health Diet | 16 | 0–150 | EAT-Lancet scoring |
        | 🦠 DI-GM | Gut Microbiome Diet | 14 | 0–14 | Gender-stratified median |

        ### Data Requirements

        | Index | Special Requirements |
        |------|---------|
        | DII | No strict required parameters; more is better (≥28 recommended) |
        | HEI-2020 | Requires age and total energy; supports toddler version (1-2 yrs) |
        | AHEI | Requires gender parameter (sex-specific handling) |
        | ACS2020 | Requires gender parameter (gender-stratified quartiles) |
        | PHDI | Requires gender and total energy |
        | DI-GM | Requires gender parameter (gender-stratified median) |
        """)
    with tab3:
        st.markdown("""
        ### Five Data Upload Modes

        <div style="display: flex; gap: 1rem; flex-wrap: wrap; margin: 1rem 0;">
            <div style="flex:1; min-width:180px; background:#eaf5f0; border-radius:12px; padding:1rem; text-align:center;">
                <div style="font-size:1.8rem;">🗂️</div>
                <div style="font-weight:700; color:#1a6b56;">General</div>
                <div style="font-size:0.78rem; color:#5a5a5a;">CSV / Excel<br>Manual mapping</div>
            </div>
            <div style="flex:1; min-width:180px; background:#eaf5f0; border-radius:12px; padding:1rem; text-align:center;">
                <div style="font-size:1.8rem;">🏥</div>
                <div style="font-weight:700; color:#1a6b56;">NHANES FPED</div>
                <div style="font-size:0.78rem; color:#5a5a5a;">Post-2005<br>.sas7bdat + .XPT</div>
            </div>
            <div style="flex:1; min-width:180px; background:#eaf5f0; border-radius:12px; padding:1rem; text-align:center;">
                <div style="font-size:1.8rem;">🏥</div>
                <div style="font-weight:700; color:#1a6b56;">NHANES MPED</div>
                <div style="font-size:0.78rem; color:#5a5a5a;">1999–2004<br>equiv.txt + .XPT</div>
            </div>
            <div style="flex:1; min-width:180px; background:#eaf5f0; border-radius:12px; padding:1rem; text-align:center;">
                <div style="font-size:1.8rem;">📱</div>
                <div style="font-weight:700; color:#1a6b56;">ASA24</div>
                <div style="font-size:0.78rem; color:#5a5a5a;">Totals.csv<br>Auto aggregation</div>
            </div>
            <div style="flex:1; min-width:180px; background:#eaf5f0; border-radius:12px; padding:1rem; text-align:center;">
                <div style="font-size:1.8rem;">📋</div>
                <div style="font-weight:700; color:#1a6b56;">DHQ3 / BLOCK</div>
                <div style="font-size:0.78rem; color:#5a5a5a;">FFQ raw data<br>One-step computation</div>
            </div>
        </div>

        ### Mode Compatibility

        | Mode | Data Source | File Format | Mapping Needed |
        |------|---------|---------|:---:|
        | General | Any pre-processed data | CSV / Excel | ✅ |
        | NHANES FPED | NHANES 2005+ cycles | .sas7bdat + .XPT | ❌ Auto |
        | NHANES MPED | NHANES 1999–2004 | equiv.txt + .XPT | ❌ Auto |
        | ASA24 | ASA24 export | Totals.csv | ❌ Auto |
        | DHQ3 / BLOCK | FFQ raw data | detail.csv / .csv | ❌ Auto |
        """, unsafe_allow_html=True)
    with tab4:
        st.markdown("""
        ### References

        1. Shivappa N, Steck SE, Hurley TG, Hussey JR, Hebert JR. Designing and developing a literature-derived, population-based dietary inflammatory index. *Public Health Nutr*. 2014;17(8):1689-1696. doi:10.1017/S1368980013002115

        2. Krebs-Smith SM, Pannucci TE, Subar AF, et al. Update of the Healthy Eating Index: HEI-2015. *J Acad Nutr Diet*. 2018;118(9):1591-1602. doi:10.1016/j.jand.2018.05.021

        3. Shams-White MM, Pannucci TE, Lerman JL, et al. Healthy Eating Index-2020: Review and Update Process to Reflect the Dietary Guidelines for Americans, 2020-2025. *J Acad Nutr Diet*. 2023;123(9):1280-1288. doi:10.1016/j.jand.2023.05.015

        4. Chiuve SE, Fung TT, Rimm EB, et al. Alternative dietary indices both strongly predict risk of chronic disease. *J Nutr*. 2012;142(6):1009-1018. doi:10.3945/jn.111.157222

        5. Rifas-Shiman SL, Rich-Edwards JW, Willett WC, Kleinman KP, Oken E, Gillman MW. Changes in dietary intake from the first to the second trimester of pregnancy. *Paediatr Perinat Epidemiol*. 2006;20(1):35-42. doi:10.1111/j.1365-3016.2006.00691.x

        6. Fung TT, Chiuve SE, McCullough ML, Rexrode KM, Logroscino G, Hu FB. Adherence to a DASH-style diet and risk of coronary heart disease and stroke in women. *Arch Intern Med*. 2008;168(7):713-720. doi:10.1001/archinte.168.7.713

        7. Mellen PB, Gao SK, Vitolins MZ, Goff DC Jr. Deteriorating dietary habits among adults with hypertension: DASH dietary accordance, NHANES 1988-1994 and 1999-2004. *Arch Intern Med*. 2008;168(3):308-314. doi:10.1001/archinternmed.2007.119

        8. Trichopoulou A, Costacou T, Bamia C, Trichopoulos D. Adherence to a Mediterranean diet and survival in a Greek population. *N Engl J Med*. 2003;348(26):2599-2608. doi:10.1056/NEJMoa025039

        9. Schröder H, Fitó M, Estruch R, et al. A short screener is valid for assessing Mediterranean diet adherence among older Spanish men and women. *J Nutr*. 2011;141(6):1140-1145. doi:10.3945/jn.110.135566

        10. McCullough ML, Patel AV, Kushi LH, et al. American Cancer Society guideline for diet and physical activity for cancer prevention. *CA Cancer J Clin*. 2020;70(4):245-271. doi:10.3322/caac.21591

        11. Cacau LT, De Carli E, de Carvalho AM, et al. Development and Validation of an Index Based on EAT-Lancet Recommendations: The Planetary Health Diet Index. *Nutrients*. 2021;13(5):1698. doi:10.3390/nu13051698

        12. Kase BE, Liese AD, Zhang J, et al. The development and evaluation of a dietary index assessing diet-gut microbiome interactions. *J Nutr*. 2024;154(2):742-753. doi:10.1016/j.tjnut.2023.12.033

        ---

        **Software Reference**

        13. Zhan JJZ. dietaryindex: Dietary Index Calculation. R package version 0.1.0. 2024. Available at: https://github.com/jamesjiadazhan/dietaryindex
        """)
    st.markdown("""
    <div class="app-footer">
        For questions or suggestions, please contact the platform administrator.
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="info-box">
        <p>本平台基于 <b>dietaryindex</b> Python 包开发，采用无服务器架构，所有计算均在浏览器中完成。没有任何膳食摄入数据被传输至或存储在远程服务器上，解决了膳食研究中的数据隐私伦理考量。dietaryindex Python 包的开发参考了 dietaryindex R 包。</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    tab1, tab2, tab3, tab4 = st.tabs(["🚀 快速开始", "📋 指数一览", "📂 数据模式", "📚 参考文献"])
    with tab1:
        st.markdown("""
        ### 三步完成计算

        <div class="step-flow">
            <div class="step-item">
                <div class="step-number">1</div>
                <div class="step-text">📂 选择指数<br><small>从侧边栏选择要计算的指数</small></div>
            </div>
            <div class="step-arrow">→</div>
            <div class="step-item">
                <div class="step-number">2</div>
                <div class="step-text">📤 上传数据<br><small>选择数据源模式，上传文件</small></div>
            </div>
            <div class="step-arrow">→</div>
            <div class="step-item">
                <div class="step-number">3</div>
                <div class="step-text">📊 计算 & 导出<br><small>映射列名后计算，查看图表并导出</small></div>
            </div>
        </div>

        ### 详细步骤

        **1. 选择指数** — 从左侧边栏选择您需要计算的膳食指数。首页展示了全部 12 个指数的简介，可直接点击跳转。

        **2. 准备数据** — 数据应为表格格式（CSV / Excel / SAS），每行为一个参与者，每列为一个食物/营养素变量。

        **3. 选择上传模式** — 进入指数页面后，根据数据来源选择：
        - **通用版**：已整理好的 CSV/Excel，手动映射列名
        - **NHANES FPED**：NHANES 2005+ 原始文件
        - **NHANES MPED**：NHANES 1999–2004 原始文件
        - **ASA24**：ASA24 Totals.csv
        - **DHQ3 / BLOCK**：FFQ 原始数据

        **4. 映射列名**（通用版）— 将您数据中的列对应系统参数，不需要的参数可跳过。

        **5. 计算并查看报告** — 点击计算按钮后获得：
        - 得分分布直方图 + 箱线图
        - 各组分柱状图 + 雷达图
        - 完整数据表 + Excel/CSV 下载
        """, unsafe_allow_html=True)
    with tab2:
        st.markdown("""
        ### 全部 12 个膳食指数

        | 指数 | 英文名 | 组分 | 总分 | 评分方法 |
        |------|--------|:---:|:----:|---------|
        | 🔥 DII | Dietary Inflammatory Index | 45 | 无上限 | Z-score 标准化 × 炎症效应 |
        | 📊 HEI-2020 | Healthy Eating Index 2020 | 13 | 0–100 | 密度法 (per 1000 kcal) |
        | 📊 HEI-2015 | Healthy Eating Index 2015 | 13 | 0–100 | 密度法（饱和脂肪/糖输入不同） |
        | 🫀 AHEI | Alternative HEI | 11 | 0–110 | 含性别差异的连续评分 |
        | 🤰 AHEIP | AHEI Pregnancy | 9 | 0–90 | 孕期专属组分设定 |
        | 💚 DASH | DASH Diet Score | 8 | 8–40 | 五分位数排名 |
        | ❤️ DASHI | DASH Nutrient Density | 9 | 0–9 | 营养素线性评分 |
        | 🫒 MED | Mediterranean Diet | 9 | 0–9 | 中位数排名 |
        | 🐟 MEDI | MEDI (PREDIMED) | 11 | 0–11 | 绝对阈值二值评分 |
        | 🎗️ ACS2020 | ACS Cancer Prevention | 8 | 0–15 | 性别分层四等分 |
        | 🌍 PHDI | Planetary Health Diet | 16 | 0–150 | EAT-Lancet 评分 |
        | 🦠 DI-GM | Gut Microbiome Diet | 14 | 0–14 | 性别分层中位数 |

        ### 数据要求参考

        | 指数 | 特殊要求 |
        |------|---------|
        | DII | 无严格必需参数，提供越多越完整（建议 ≥28 个） |
        | HEI-2020 | 需要年龄和总能量，支持 1-2 岁幼儿版 |
        | AHEI | 需要性别参数（男女分开处理） |
        | ACS2020 | 需要性别参数（性别分层四等分） |
        | PHDI | 需要性别和总能量 |
        | DI-GM | 需要性别参数（性别分层中位数） |
        """)
    with tab3:
        st.markdown("""
        ### 五种数据上传模式

        <div style="display: flex; gap: 1rem; flex-wrap: wrap; margin: 1rem 0;">
            <div style="flex:1; min-width:180px; background:#eaf5f0; border-radius:12px; padding:1rem; text-align:center;">
                <div style="font-size:1.8rem;">🗂️</div>
                <div style="font-weight:700; color:#1a6b56;">通用版</div>
                <div style="font-size:0.78rem; color:#5a5a5a;">CSV / Excel<br>手动映射列名</div>
            </div>
            <div style="flex:1; min-width:180px; background:#eaf5f0; border-radius:12px; padding:1rem; text-align:center;">
                <div style="font-size:1.8rem;">🏥</div>
                <div style="font-weight:700; color:#1a6b56;">NHANES FPED</div>
                <div style="font-size:0.78rem; color:#5a5a5a;">2005年后<br>.sas7bdat + .XPT</div>
            </div>
            <div style="flex:1; min-width:180px; background:#eaf5f0; border-radius:12px; padding:1rem; text-align:center;">
                <div style="font-size:1.8rem;">🏥</div>
                <div style="font-weight:700; color:#1a6b56;">NHANES MPED</div>
                <div style="font-size:0.78rem; color:#5a5a5a;">1999–2004<br>equiv.txt + .XPT</div>
            </div>
            <div style="flex:1; min-width:180px; background:#eaf5f0; border-radius:12px; padding:1rem; text-align:center;">
                <div style="font-size:1.8rem;">📱</div>
                <div style="font-weight:700; color:#1a6b56;">ASA24</div>
                <div style="font-size:0.78rem; color:#5a5a5a;">Totals.csv<br>自动汇总</div>
            </div>
            <div style="flex:1; min-width:180px; background:#eaf5f0; border-radius:12px; padding:1rem; text-align:center;">
                <div style="font-size:1.8rem;">📋</div>
                <div style="font-weight:700; color:#1a6b56;">DHQ3 / BLOCK</div>
                <div style="font-size:0.78rem; color:#5a5a5a;">FFQ 原始数据<br>一步式计算</div>
            </div>
        </div>

        ### 各模式的适用情况

        | 模式 | 数据来源 | 文件格式 | 需要映射 |
        |------|---------|---------|:---:|
        | 通用版 | 任何已整理数据 | CSV / Excel | ✅ |
        | NHANES FPED | NHANES 2005+ 周期 | .sas7bdat + .XPT | ❌ 自动 |
        | NHANES MPED | NHANES 1999–2004 | equiv.txt + .XPT | ❌ 自动 |
        | ASA24 | ASA24 系统导出 | Totals.csv | ❌ 自动 |
        | DHQ3 / BLOCK | FFQ 原始数据 | detail.csv / .csv | ❌ 自动 |
        """, unsafe_allow_html=True)
    with tab4:
        st.markdown("""
        ### 参考文献

        1. Shivappa N, Steck SE, Hurley TG, Hussey JR, Hebert JR. Designing and developing a literature-derived, population-based dietary inflammatory index. *Public Health Nutr*. 2014;17(8):1689-1696. doi:10.1017/S1368980013002115

        2. Krebs-Smith SM, Pannucci TE, Subar AF, et al. Update of the Healthy Eating Index: HEI-2015. *J Acad Nutr Diet*. 2018;118(9):1591-1602. doi:10.1016/j.jand.2018.05.021

        3. Shams-White MM, Pannucci TE, Lerman JL, et al. Healthy Eating Index-2020: Review and Update Process to Reflect the Dietary Guidelines for Americans, 2020-2025. *J Acad Nutr Diet*. 2023;123(9):1280-1288. doi:10.1016/j.jand.2023.05.015

        4. Chiuve SE, Fung TT, Rimm EB, et al. Alternative dietary indices both strongly predict risk of chronic disease. *J Nutr*. 2012;142(6):1009-1018. doi:10.3945/jn.111.157222

        5. Rifas-Shiman SL, Rich-Edwards JW, Willett WC, Kleinman KP, Oken E, Gillman MW. Changes in dietary intake from the first to the second trimester of pregnancy. *Paediatr Perinat Epidemiol*. 2006;20(1):35-42. doi:10.1111/j.1365-3016.2006.00691.x

        6. Fung TT, Chiuve SE, McCullough ML, Rexrode KM, Logroscino G, Hu FB. Adherence to a DASH-style diet and risk of coronary heart disease and stroke in women. *Arch Intern Med*. 2008;168(7):713-720. doi:10.1001/archinte.168.7.713

        7. Mellen PB, Gao SK, Vitolins MZ, Goff DC Jr. Deteriorating dietary habits among adults with hypertension: DASH dietary accordance, NHANES 1988-1994 and 1999-2004. *Arch Intern Med*. 2008;168(3):308-314. doi:10.1001/archinternmed.2007.119

        8. Trichopoulou A, Costacou T, Bamia C, Trichopoulos D. Adherence to a Mediterranean diet and survival in a Greek population. *N Engl J Med*. 2003;348(26):2599-2608. doi:10.1056/NEJMoa025039

        9. Schröder H, Fitó M, Estruch R, et al. A short screener is valid for assessing Mediterranean diet adherence among older Spanish men and women. *J Nutr*. 2011;141(6):1140-1145. doi:10.3945/jn.110.135566

        10. McCullough ML, Patel AV, Kushi LH, et al. American Cancer Society guideline for diet and physical activity for cancer prevention. *CA Cancer J Clin*. 2020;70(4):245-271. doi:10.3322/caac.21591

        11. Cacau LT, De Carli E, de Carvalho AM, et al. Development and Validation of an Index Based on EAT-Lancet Recommendations: The Planetary Health Diet Index. *Nutrients*. 2021;13(5):1698. doi:10.3390/nu13051698

        12. Kase BE, Liese AD, Zhang J, et al. The development and evaluation of a dietary index assessing diet-gut microbiome interactions. *J Nutr*. 2024;154(2):742-753. doi:10.1016/j.tjnut.2023.12.033

        ---

        **软件参考**

        13. Zhan JJZ. dietaryindex: Dietary Index Calculation. R package version 0.1.0. 2024. Available at: https://github.com/jamesjiadazhan/dietaryindex
        """)
    st.markdown("""
    <div class="app-footer">
        如有问题或建议，请联系平台管理员
    </div>
    """, unsafe_allow_html=True)
