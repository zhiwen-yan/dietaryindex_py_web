"""DASHI 控制高血压膳食指数（营养素版）"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import streamlit as st
from config.i18n import get_lang
st.set_page_config(page_title="DASHI DASH Nutrient Index" if get_lang() == "en" else "DASHI 控制高血压膳食指数", page_icon="💛", layout="wide")
from render_utils import render_full_index_page
render_full_index_page("DASHI")

is_en = get_lang() == "en"
st.markdown("---")
if is_en:
    st.markdown("""
    ### 📚 DASHI References

    1. Appel LJ, Moore TJ, Obarzanek E, et al. A clinical trial of the effects of dietary patterns
       on blood pressure. *N Engl J Med*. 1997;336(16):1117-1124. doi:10.1056/NEJM199704173361601

    2. Mellen PB, Gao SK, Vitolins MZ, Goff DC Jr. Deteriorating dietary habits among adults with
       hypertension: DASH dietary accordance, NHANES 1988-1994 and 1999-2004.
       *Arch Intern Med*. 2008;168(3):308-314. doi:10.1001/archinternmed.2007.119
    """)
else:
    st.markdown("""
    ### 📚 DASHI 参考文献

    1. Appel LJ, Moore TJ, Obarzanek E, et al. A clinical trial of the effects of dietary patterns
       on blood pressure. *N Engl J Med*. 1997;336(16):1117-1124. doi:10.1056/NEJM199704173361601

    2. Mellen PB, Gao SK, Vitolins MZ, Goff DC Jr. Deteriorating dietary habits among adults with
       hypertension: DASH dietary accordance, NHANES 1988-1994 and 1999-2004.
       *Arch Intern Med*. 2008;168(3):308-314. doi:10.1001/archinternmed.2007.119
    """)
