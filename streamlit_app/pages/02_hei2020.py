"""HEI2020 健康膳食指数 2020（包含 V1 与 V2 双版本选择）"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import streamlit as st
from config.i18n import get_lang
st.set_page_config(page_title="HEI2020 Healthy Eating Index" if get_lang() == "en" else "HEI2020 健康膳食指数", page_icon="🍽️", layout="wide")
from render_utils import render_full_index_page
render_full_index_page("HEI2020")

is_en = get_lang() == "en"
st.markdown("---")
if is_en:
    st.markdown("""
    ### 📚 HEI-2020 References

    1. Kennedy ET, Ohls J, Carlson S, Fleming K. The Healthy Eating Index: design and applications.
       *J Am Diet Assoc*. 1995;95(10):1103-1108. doi:10.1016/S0002-8223(95)00300-2

    2. Shams-White MM, Pannucci TE, Lerman JL, et al. Healthy Eating Index-2020: Review and Update
       Process to Reflect the Dietary Guidelines for Americans, 2020-2025.
       *J Acad Nutr Diet*. 2023;123(9):1280-1288. doi:10.1016/j.jand.2023.05.015
    """)
else:
    st.markdown("""
    ### 📚 HEI-2020 参考文献

    1. Kennedy ET, Ohls J, Carlson S, Fleming K. The Healthy Eating Index: design and applications.
       *J Am Diet Assoc*. 1995;95(10):1103-1108. doi:10.1016/S0002-8223(95)00300-2

    2. Shams-White MM, Pannucci TE, Lerman JL, et al. Healthy Eating Index-2020: Review and Update
       Process to Reflect the Dietary Guidelines for Americans, 2020-2025.
       *J Acad Nutr Diet*. 2023;123(9):1280-1288. doi:10.1016/j.jand.2023.05.015
    """)
