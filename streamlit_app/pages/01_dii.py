"""
DII 膳食炎症指数
Dietary Inflammatory Index (DII)
"""

import sys
import os
import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.i18n import get_lang, t

st.set_page_config(
    page_title="DII Dietary Inflammatory Index" if get_lang() == "en" else "DII 膳食炎症指数",
    page_icon="🔥",
    layout="wide",
)

from render_utils import render_full_index_page

# 渲染 DII 的完整页面 UI
render_full_index_page("DII")

# 渲染底部的 DII 参考文献
st.markdown("---")
st.markdown(f"""
### {t("ref.title.dii")}

1. Shivappa N, Steck SE, Hurley TG, Hussey JR, Hebert JR. Designing and developing
   a literature-derived, population-based dietary inflammatory index.
   *Public Health Nutrition*, 2014; 17(8): 1689-1696.

2. Shivappa N, Hebert JR, Rietzschel ER, et al. Associations between dietary
   inflammatory index and inflammatory markers in the Asklepios Study.
   *British Journal of Nutrition*, 2015; 113(4): 665-671.
""")
