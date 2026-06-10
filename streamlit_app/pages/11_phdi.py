"""PHDI 地球健康膳食指数"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import streamlit as st
from config.i18n import get_lang
st.set_page_config(page_title="PHDI Planetary Health Diet Index" if get_lang() == "en" else "PHDI 地球健康膳食指数", page_icon="🌍", layout="wide")
from render_utils import render_full_index_page
render_full_index_page("PHDI")

is_en = get_lang() == "en"
st.markdown("---")
if is_en:
    st.markdown("""
    ### 📚 PHDI References

    1. Willett W, Rockström J, Loken B, et al. Food in the Anthropocene: the EAT-Lancet
       Commission on healthy diets from sustainable food systems.
       *Lancet*. 2019;393(10170):447-492. doi:10.1016/S0140-6736(18)31788-4

    2. Cacau LT, De Carli E, de Carvalho AM, et al. Development and Validation of an Index
       Based on EAT-Lancet Recommendations: The Planetary Health Diet Index.
       *Nutrients*. 2021;13(5):1698. doi:10.3390/nu13051698
    """)
else:
    st.markdown("""
    ### 📚 PHDI 参考文献

    1. Willett W, Rockström J, Loken B, et al. Food in the Anthropocene: the EAT-Lancet
       Commission on healthy diets from sustainable food systems.
       *Lancet*. 2019;393(10170):447-492. doi:10.1016/S0140-6736(18)31788-4

    2. Cacau LT, De Carli E, de Carvalho AM, et al. Development and Validation of an Index
       Based on EAT-Lancet Recommendations: The Planetary Health Diet Index.
       *Nutrients*. 2021;13(5):1698. doi:10.3390/nu13051698
    """)
