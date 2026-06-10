"""MED 地中海膳食评分"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import streamlit as st
from config.i18n import get_lang
st.set_page_config(page_title="MED Mediterranean Diet Score" if get_lang() == "en" else "MED 地中海膳食评分", page_icon="🫒", layout="wide")
from render_utils import render_full_index_page
render_full_index_page("MED")

is_en = get_lang() == "en"
st.markdown("---")
if is_en:
    st.markdown("""
    ### 📚 MED References

    1. Trichopoulou A, Kouris-Blazos A, Wahlqvist ML, et al. Diet and overall survival in elderly
       people. *BMJ*. 1995;311(7018):1457-1460. doi:10.1136/bmj.311.7018.1457

    2. Fung TT, Rexrode KM, Mantzoros CS, et al. Mediterranean diet and incidence of and mortality
       from coronary heart disease and stroke in women.
       *Circulation*. 2009;119(8):1093-1100. doi:10.1161/CIRCULATIONAHA.108.816736
    """)
else:
    st.markdown("""
    ### 📚 MED 参考文献

    1. Trichopoulou A, Kouris-Blazos A, Wahlqvist ML, et al. Diet and overall survival in elderly
       people. *BMJ*. 1995;311(7018):1457-1460. doi:10.1136/bmj.311.7018.1457

    2. Fung TT, Rexrode KM, Mantzoros CS, et al. Mediterranean diet and incidence of and mortality
       from coronary heart disease and stroke in women.
       *Circulation*. 2009;119(8):1093-1100. doi:10.1161/CIRCULATIONAHA.108.816736
    """)
