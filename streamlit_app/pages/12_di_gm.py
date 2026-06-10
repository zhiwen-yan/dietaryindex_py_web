"""DI_GM 德国膳食指数"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import streamlit as st
from config.i18n import get_lang
st.set_page_config(page_title="DI-GM Dietary Index" if get_lang() == "en" else "DI_GM 德国膳食指数", page_icon="🇩🇪", layout="wide")
from render_utils import render_full_index_page
render_full_index_page("DI_GM")

is_en = get_lang() == "en"
st.markdown("---")
if is_en:
    st.markdown("""
    ### 📚 DI-GM References

    1. Kase BE, Liese AD, Zhang J, Murphy EA, Zhao L, Steck SE. The Development and Evaluation
       of a Literature-Based Dietary Index for Gut Microbiota.
       *Nutrients*. 2024;16(7):1045. doi:10.3390/nu16071045
    """)
else:
    st.markdown("""
    ### 📚 DI-GM 参考文献

    1. Kase BE, Liese AD, Zhang J, Murphy EA, Zhao L, Steck SE. The Development and Evaluation
       of a Literature-Based Dietary Index for Gut Microbiota.
       *Nutrients*. 2024;16(7):1045. doi:10.3390/nu16071045
    """)
