"""
Lightweight sidebar rendering utilities shared by non-computation pages.
"""

from pathlib import Path

import streamlit as st

from config.i18n import get_lang, set_lang, t


INDEX_NAV = [
    ("🔥 DII", "pages/01_dii.py"),
    ("📊 HEI-2020", "pages/02_hei2020.py"),
    ("📊 HEI-2015", "pages/03_hei2015.py"),
    ("🫀 AHEI", "pages/04_ahei.py"),
    ("🤰 AHEIP", "pages/05_aheip.py"),
    ("💚 DASH", "pages/06_dash.py"),
    ("❤️ DASHI", "pages/07_dashi.py"),
    ("🫒 MED", "pages/08_med.py"),
    ("🐟 MEDI", "pages/09_medi.py"),
    ("🎗️ ACS2020", "pages/10_acs2020.py"),
    ("🌍 PHDI", "pages/11_phdi.py"),
    ("🦠 DI-GM", "pages/12_di_gm.py"),
]

NAV_CATEGORIES = [
    ("nav.inflammatory", ["🔥 DII"]),
    ("nav.hei_series", ["📊 HEI-2020", "📊 HEI-2015"]),
    ("nav.alternative_healthy", ["🫀 AHEI", "🤰 AHEIP"]),
    ("nav.disease_prevention", ["💚 DASH", "❤️ DASHI", "🎗️ ACS2020"]),
    ("nav.dietary_pattern", ["🫒 MED", "🐟 MEDI"]),
    ("nav.emerging", ["🌍 PHDI", "🦠 DI-GM"]),
]

NAV_MAP = dict(INDEX_NAV)
_CSS_CACHE_KEY = "_cached_css"


def _inject_sidebar_css():
    css_path = Path(__file__).resolve().parent / "assets" / "style.css"
    if css_path.exists():
        if _CSS_CACHE_KEY not in st.session_state:
            st.session_state[_CSS_CACHE_KEY] = css_path.read_text(encoding="utf-8")
        st.html(f"<style>{st.session_state[_CSS_CACHE_KEY]}</style>")


def render_sidebar(current_page_key=None, pre_render_callback=None):
    """Render the shared sidebar without importing heavy computation helpers."""
    _inject_sidebar_css()

    if pre_render_callback is not None and current_page_key is not None:
        pre_render_callback(current_page_key)

    with st.sidebar:
        st.markdown(
            """
            <div class="sidebar-brand">
                <span class="brand-icon">🥗</span>
                <span class="brand-text">DietaryIndex</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="sidebar-subtitle">{t("sidebar.subtitle")}</div>',
            unsafe_allow_html=True,
        )

        current_lang = get_lang()
        lang_options = {"zh": "中文", "en": "English"}
        selected_lang = st.selectbox(
            t("sidebar.language"),
            options=list(lang_options.keys()),
            format_func=lambda x: lang_options[x],
            index=list(lang_options.keys()).index(current_lang),
            key="lang_selector",
            label_visibility="visible",
        )
        if selected_lang != current_lang:
            set_lang(selected_lang)
            st.rerun()

        st.markdown("---")
        st.page_link("app.py", label=t("sidebar.home"), icon="🏠")

        for category_key, category_items in NAV_CATEGORIES:
            st.markdown(
                f"<div class='sidebar-cat-label'>{t(category_key)}</div>",
                unsafe_allow_html=True,
            )
            for label in category_items:
                st.page_link(NAV_MAP[label], label=label)

        st.markdown("---")
        st.page_link("pages/guide.py", label=t("sidebar.guide"), icon="📖")
        st.markdown(
            f'<div class="sidebar-version">{t("sidebar.version")}</div>',
            unsafe_allow_html=True,
        )
