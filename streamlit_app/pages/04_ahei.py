"""AHEI 替代健康膳食指数"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import streamlit as st
from config.i18n import get_lang
st.set_page_config(page_title="AHEI Alternative Healthy Eating Index" if get_lang() == "en" else "AHEI 替代健康膳食指数", page_icon="🫀", layout="wide")
from render_utils import render_full_index_page
render_full_index_page("AHEI")

is_en = get_lang() == "en"
st.markdown("---")
if is_en:
    st.markdown("""
    ### 📚 AHEI References

    1. McCullough ML, Feskanich D, Stampfer MJ, et al. Diet quality and major chronic disease risk
       in men and women: moving toward improved dietary guidance.
       *Am J Clin Nutr*. 2002;76(6):1261-1271. doi:10.1093/ajcn/76.6.1261

    2. Chiuve SE, Fung TT, Rimm EB, et al. Alternative dietary indices both strongly predict risk
       of chronic disease. *J Nutr*. 2012;142(6):1009-1018. doi:10.3945/jn.111.157222
    """)
else:
    st.markdown("""
    ### 📚 AHEI 参考文献

    1. McCullough ML, Feskanich D, Stampfer MJ, et al. Diet quality and major chronic disease risk
       in men and women: moving toward improved dietary guidance.
       *Am J Clin Nutr*. 2002;76(6):1261-1271. doi:10.1093/ajcn/76.6.1261

    2. Chiuve SE, Fung TT, Rimm EB, et al. Alternative dietary indices both strongly predict risk
       of chronic disease. *J Nutr*. 2012;142(6):1009-1018. doi:10.3945/jn.111.157222
    """)
