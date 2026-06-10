"""MEDI 地中海膳食指数（包含二值化 V1 与 连续 V2 双版本）"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import streamlit as st
from config.i18n import get_lang
st.set_page_config(page_title="MEDI PREDIMED-based" if get_lang() == "en" else "MEDI 地中海膳食指数", page_icon="🥗", layout="wide")
from render_utils import render_full_index_page
render_full_index_page("MEDI")

is_en = get_lang() == "en"
st.markdown("---")
if is_en:
    st.markdown("""
    ### 📚 MEDI References

    1. Schröder H, Fitó M, Estruch R, et al. A short screener is valid for assessing Mediterranean
       diet adherence among older Spanish men and women.
       *J Nutr*. 2011;141(6):1140-1145. doi:10.3945/jn.110.135566

    2. Estruch R, Ros E, Salas-Salvadó J, et al. Primary prevention of cardiovascular disease
       with a Mediterranean diet supplemented with extra-virgin olive oil or nuts.
       *N Engl J Med*. 2018;378(25):e34. doi:10.1056/NEJMoa1800389
    """)
else:
    st.markdown("""
    ### 📚 MEDI 参考文献

    1. Schröder H, Fitó M, Estruch R, et al. A short screener is valid for assessing Mediterranean
       diet adherence among older Spanish men and women.
       *J Nutr*. 2011;141(6):1140-1145. doi:10.3945/jn.110.135566

    2. Estruch R, Ros E, Salas-Salvadó J, et al. Primary prevention of cardiovascular disease
       with a Mediterranean diet supplemented with extra-virgin olive oil or nuts.
       *N Engl J Med*. 2018;378(25):e34. doi:10.1056/NEJMoa1800389
    """)
