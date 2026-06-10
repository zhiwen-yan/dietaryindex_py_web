"""ACS2020 美国癌症学会 2020 生活方式指数"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import streamlit as st
from config.i18n import get_lang
st.set_page_config(page_title="ACS2020 Cancer Society Index" if get_lang() == "en" else "ACS2020 美国癌症学会指数", page_icon="🎗️", layout="wide")
from render_utils import render_full_index_page
render_full_index_page("ACS2020")

is_en = get_lang() == "en"
st.markdown("---")
if is_en:
    st.markdown("""
    ### 📚 ACS2020 References

    1. Rock CL, Thomson C, Gansler T, et al. American Cancer Society guideline for diet and
       physical activity for cancer prevention.
       *CA Cancer J Clin*. 2020;70(4):245-271. doi:10.3322/caac.21591

    2. McCullough ML, Chantaprasopsuk S, Islami F, et al. Association of Socioeconomic and
       Geographic Factors With Diet Quality in US Adults.
       *JAMA Netw Open*. 2022;5(5):e2211618. doi:10.1001/jamanetworkopen.2022.11618
    """)
else:
    st.markdown("""
    ### 📚 ACS2020 参考文献

    1. Rock CL, Thomson C, Gansler T, et al. American Cancer Society guideline for diet and
       physical activity for cancer prevention.
       *CA Cancer J Clin*. 2020;70(4):245-271. doi:10.3322/caac.21591

    2. McCullough ML, Chantaprasopsuk S, Islami F, et al. Association of Socioeconomic and
       Geographic Factors With Diet Quality in US Adults.
       *JAMA Netw Open*. 2022;5(5):e2211618. doi:10.1001/jamanetworkopen.2022.11618
    """)
