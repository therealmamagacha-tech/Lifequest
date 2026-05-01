import streamlit as st
import auth
from i18n import T
from ui_preferences import ensure_ui_defaults, inject_ui_overrides


# 1. STYLE
try:
    with open("style.css", "r", encoding="utf-8") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
except FileNotFoundError:
    st.error("ERREUR : Fichier style.css introuvable.")
except OSError as e:
    st.error(f"ERREUR : Impossible de charger style.css ({e}).")

ensure_ui_defaults(st.session_state)
inject_ui_overrides(st.session_state)


# 2. GARDE : connexion requise
if not st.session_state.get("logged_in", False):
    st.warning(T("guard_login_required"))
    if st.button(T("btn_back_terminal")):
        st.switch_page("app.py")
    st.stop()


st.markdown(f'<h1 class="main-title">{T("settings_title")}</h1>', unsafe_allow_html=True)
st.markdown(
    f"<p style='font-family:monospace; color:#ffffff; text-align:center; margin-top:14px; margin-bottom:22px; line-height:1.5;'>{T('settings_subtitle')}</p>",
    unsafe_allow_html=True,
)


def save_all_user_data():
    username = st.session_state.get("username")
    if not username:
        return

    data = {
        "password": st.session_state.get("password"),
        "xp": st.session_state.get("xp", 0),
        "lvl": st.session_state.get("lvl", 1),
        "mode": st.session_state.get("mode"),
        "mission_active": st.session_state.get("mission_active", False),
        "mission_text": st.session_state.get("mission_text", ""),
        "history": st.session_state.get("history", []),
        "streak": st.session_state.get("streak", 0),
        "last_mission_date": st.session_state.get("last_mission_date"),
        "palmares": st.session_state.get("palmares", []),
        "badges": st.session_state.get("badges", []),
        "lang": st.session_state.get("lang", "fr"),
        "ui_animations": st.session_state.get("ui_animations", True),
        "ui_high_contrast": st.session_state.get("ui_high_contrast", False),
        "ui_sound": st.session_state.get("ui_sound", False),
    }
    auth.save_user(username, data)


col_l, col_r = st.columns([1, 1])

with col_l:
    st.markdown(f"### {T('settings_language')}")
    lang_options = {"fr": T("settings_lang_fr"), "en": T("settings_lang_en")}
    current_lang = st.session_state.get("lang", "fr")
    selected_lang = st.radio(
        T("settings_language_label"),
        options=list(lang_options.keys()),
        format_func=lambda k: lang_options[k],
        index=0 if current_lang == "fr" else 1,
        horizontal=True,
    )

with col_r:
    st.markdown(f"### {T('settings_accessibility')}")
    animations = st.toggle(T("settings_animations"), value=st.session_state.get("ui_animations", True))
    high_contrast = st.toggle(T("settings_contrast"), value=st.session_state.get("ui_high_contrast", False))
    sound = st.toggle(T("settings_sound"), value=st.session_state.get("ui_sound", False))

if st.button(T("settings_apply"), type="primary"):
    st.session_state.lang = selected_lang
    st.session_state.ui_animations = animations
    st.session_state.ui_high_contrast = high_contrast
    st.session_state.ui_sound = sound
    save_all_user_data()
    st.success(T("settings_saved"))
    st.rerun()

st.markdown("---")
if st.button(T("btn_back_terminal")):
    st.switch_page("app.py")
