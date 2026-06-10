"""AHEIP 孕期替代健康膳食指数"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import streamlit as st
from config.i18n import get_lang
st.set_page_config(page_title="AHEIP AHEI Pregnancy" if get_lang() == "en" else "AHEIP 孕期替代健康膳食指数", page_icon="🤰", layout="wide")
from render_utils import render_full_index_page
render_full_index_page("AHEIP")

is_en = get_lang() == "en"
st.markdown("---")
if is_en:
    st.markdown("""
    ### 📚 AHEIP References

    1. Rifas-Shiman SL, Rich-Edwards JW, Kleinman KP, Oken E, Gillman MW. Dietary quality during
       pregnancy varies by maternal characteristics in Project Viva: a US cohort.
       *J Am Diet Assoc*. 2009;109(6):1004-1011. doi:10.1016/j.jada.2009.03.001
    """)
else:
    st.markdown("""
    ### 📚 AHEIP 参考文献

    1. Rifas-Shiman SL, Rich-Edwards JW, Kleinman KP, Oken E, Gillman MW. Dietary quality during
       pregnancy varies by maternal characteristics in Project Viva: a US cohort.
       *J Am Diet Assoc*. 2009;109(6):1004-1011. doi:10.1016/j.jada.2009.03.001
    """)
