"""DASH 控制高血压膳食评分"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import streamlit as st
from config.i18n import get_lang
st.set_page_config(page_title="DASH Diet Score" if get_lang() == "en" else "DASH 控制高血压膳食评分", page_icon="💚", layout="wide")
from render_utils import render_full_index_page
render_full_index_page("DASH")

is_en = get_lang() == "en"
st.markdown("---")
if is_en:
    st.markdown("""
    ### 📚 DASH References

    1. Appel LJ, Moore TJ, Obarzanek E, et al. A clinical trial of the effects of dietary patterns
       on blood pressure. *N Engl J Med*. 1997;336(16):1117-1124. doi:10.1056/NEJM199704173361601

    2. Fung TT, Chiuve SE, McCullough ML, et al. Adherence to a DASH-style diet and risk of
       coronary heart disease and stroke in women.
       *Arch Intern Med*. 2008;168(7):713-720. doi:10.1001/archinte.168.7.713
    """)
else:
    st.markdown("""
    ### 📚 DASH 参考文献

    1. Appel LJ, Moore TJ, Obarzanek E, et al. A clinical trial of the effects of dietary patterns
       on blood pressure. *N Engl J Med*. 1997;336(16):1117-1124. doi:10.1056/NEJM199704173361601

    2. Fung TT, Chiuve SE, McCullough ML, et al. Adherence to a DASH-style diet and risk of
       coronary heart disease and stroke in women.
       *Arch Intern Med*. 2008;168(7):713-720. doi:10.1001/archinte.168.7.713
    """)
