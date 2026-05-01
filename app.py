import streamlit as st
from i18n import TRANSLATIONS

# --- CONFIGURATION PAGE (doit rester ici, point d'entrée unique) ---
st.set_page_config(page_title="LIFEQUEST", layout="wide")

# Init langue avant la navigation pour que les labels soient corrects dès le départ
if 'lang' not in st.session_state:
    st.session_state.lang = 'fr'

lang = st.session_state.lang
_T = lambda key: TRANSLATIONS.get(lang, TRANSLATIONS["fr"]).get(key, key)

# Navigation avec labels traduits dynamiquement
pg = st.navigation([
    st.Page("pages/hub.py",        title=_T("nav_hub")),
    st.Page("pages/contrat.py",    title=_T("nav_contrat")),
    st.Page("pages/escouade.py",   title=_T("nav_escouade")),
    st.Page("pages/palmares.py",   title=_T("nav_palmares")),
    st.Page("pages/parametres.py", title=_T("nav_parametres")),
])
pg.run()
