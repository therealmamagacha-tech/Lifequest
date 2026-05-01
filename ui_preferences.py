import streamlit as st


UI_DEFAULTS = {
    "lang": "fr",
    "ui_animations": True,
    "ui_high_contrast": False,
    "ui_sound": False,
}


def ensure_ui_defaults(session_state):
    for key, value in UI_DEFAULTS.items():
        if key not in session_state:
            session_state[key] = value


def inject_ui_overrides(session_state):
    rules = []

    if not session_state.get("ui_animations", True):
        rules.append(
            """
            *, *::before, *::after {
                animation: none !important;
                transition: none !important;
                scroll-behavior: auto !important;
            }
            """
        )

    if session_state.get("ui_high_contrast", False):
        rules.append(
            """
            .stApp,
            .stApp * {
                text-shadow: none !important;
            }

            .stApp,
            [data-testid='stSidebar'],
            .login-frame,
            .manual-frame,
            .mission-box,
            .archive-card,
            .palmares-entry,
            .trophy-badge,
            .achievement-badge {
                border-color: #ffffff !important;
                color: #ffffff !important;
            }

            div.stButton > button {
                border-color: #ffffff !important;
                color: #ffffff !important;
                box-shadow: none !important;
            }
            """
        )

    if rules:
        st.markdown(f"<style>{''.join(rules)}</style>", unsafe_allow_html=True)
