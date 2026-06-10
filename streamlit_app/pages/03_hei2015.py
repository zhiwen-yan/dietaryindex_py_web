"""HEI2015 健康膳食指数 2015"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import streamlit as st
from config.i18n import get_lang
st.set_page_config(page_title="HEI2015 Healthy Eating Index" if get_lang() == "en" else "HEI2015 健康膳食指数", page_icon="🍽️", layout="wide")
from render_utils import render_full_index_page
render_full_index_page("HEI2015")

is_en = get_lang() == "en"
st.markdown("---")
if is_en:
    st.markdown("""
    ### 📚 HEI-2015 References

    1. Kennedy ET, Ohls J, Carlson S, Fleming K. The Healthy Eating Index: design and applications.
       *J Am Diet Assoc*. 1995;95(10):1103-1108. doi:10.1016/S0002-8223(95)00300-2

    2. Krebs-Smith SM, Pannucci TE, Subar AF, et al. Update of the Healthy Eating Index: HEI-2015.
       *J Acad Nutr Diet*. 2018;118(9):1591-1602. doi:10.1016/j.jand.2018.05.021
    """)
else:
    st.markdown("""
    ### 📚 HEI-2015 参考文献

    1. Kennedy ET, Ohls J, Carlson S, Fleming K. The Healthy Eating Index: design and applications.
       *J Am Diet Assoc*. 1995;95(10):1103-1108. doi:10.1016/S0002-8223(95)00300-2

    2. Krebs-Smith SM, Pannucci TE, Subar AF, et al. Update of the Healthy Eating Index: HEI-2015.
       *J Acad Nutr Diet*. 2018;118(9):1591-1602. doi:10.1016/j.jand.2018.05.021
    """)
