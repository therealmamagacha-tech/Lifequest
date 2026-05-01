import streamlit as st
import google.generativeai as genai
from PIL import Image
import hashlib
import html
import os
import auth
from i18n import T, DIFFICULTY_MAP, BADGES_DEF, check_badges
from lucide import icon_html
from ui_preferences import ensure_ui_defaults, inject_ui_overrides


def load_dotenv_file(path=".env"):
    if not os.path.exists(path):
        return
    with open(path, "r", encoding="utf-8") as env_file:
        for raw_line in env_file:
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = value

# --- CONFIGURATION IA ---
load_dotenv_file()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
model = None

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-2.5-flash')

if not GEMINI_API_KEY:
    st.warning("Clé API absente: ajoute GEMINI_API_KEY dans le fichier .env.")

# Injection du CSS
try:
    with open("style.css", "r") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
except FileNotFoundError:
    st.error("ERREUR : Fichier style.css introuvable.")
except OSError as e:
    st.error(f"ERREUR : Impossible de charger style.css ({e}).")

ensure_ui_defaults(st.session_state)
inject_ui_overrides(st.session_state)

# --- INITIALISATION SESSION ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

def get_image_hash(img):
    return hashlib.md5(img.tobytes()).hexdigest()

def sync_save():
    if st.session_state.logged_in:
        data = {
            "password": st.session_state.password,
            "xp": st.session_state.xp,
            "lvl": st.session_state.lvl,
            "mode": st.session_state.mode,
            "mission_active": st.session_state.mission_active,
            "mission_text": st.session_state.mission_text,
            "history": st.session_state.history,
            "streak": st.session_state.get("streak", 0),
            "last_mission_date": st.session_state.get("last_mission_date", None),
            "palmares": st.session_state.get("palmares", []),
            "badges": st.session_state.get("badges", []),
            "lang": st.session_state.get("lang", "fr"),
            "ui_animations": st.session_state.get("ui_animations", True),
            "ui_high_contrast": st.session_state.get("ui_high_contrast", False),
            "ui_sound": st.session_state.get("ui_sound", False),
            "mission_difficulty": st.session_state.get("mission_difficulty", {"key": "moyen", "xp": 20}),
        }
        auth.save_user(st.session_state.username, data)

# --- ÉCRAN D'ACCÈS ---
if not st.session_state.logged_in:
    col_lang_r = st.columns([12, 1])
    with col_lang_r[1]:
        if st.button(T("lang_toggle"), key="lang_login"):
            st.session_state.lang = "en" if st.session_state.lang == "fr" else "fr"
            st.rerun()

    st.markdown(f'<h1 class="main-title">{T("page_title")}</h1>', unsafe_allow_html=True)

    st.markdown(f'''
        <div class="login-frame">
            <h3 style="margin:0; letter-spacing:3px; color:#00f2ff; font-family:Orbitron;">{T("standby_mode")}</h3>
            <p style="margin:15px 0 0 0; font-size:1rem; opacity:0.9; line-height:1.5;">
                {T("standby_desc")}
            </p>
        </div>
    ''', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div style="max-width:500px; margin:auto; padding:10px;">', unsafe_allow_html=True)
        user_input = st.text_input(T("label_id"))
        pass_input = st.text_input(T("label_pass"), type="password")
        can_auth = bool(user_input.strip()) and bool(pass_input)

        c1, c2 = st.columns(2)
        with c1:
            if st.button(T("btn_login"), type="primary", disabled=not can_auth):
                data = auth.load_user(user_input, pass_input)
                if data:
                    st.session_state.update(data)
                    st.session_state.username = user_input
                    st.session_state.logged_in = True
                    st.session_state.waiting_for_proof = False
                    if "streak" not in st.session_state:
                        st.session_state.streak = 0
                    if "last_mission_date" not in st.session_state:
                        st.session_state.last_mission_date = None
                    if "palmares" not in st.session_state:
                        st.session_state.palmares = []
                    if "badges" not in st.session_state:
                        st.session_state.badges = []
                    if "mission_difficulty" not in st.session_state:
                        st.session_state.mission_difficulty = {"key": "moyen", "xp": 20}
                    ensure_ui_defaults(st.session_state)
                    st.rerun()
                else:
                    st.error(T("err_wrong_creds"))
        with c2:
            if st.button(T("btn_register"), type="primary", disabled=not can_auth):
                if len(user_input) > 2 and len(pass_input) > 3:
                    if auth.user_exists(user_input):
                        st.warning(T("warn_already_exists"))
                    else:
                        pwd_h = auth.hash_password(pass_input)
                        new_data = {
                            "password": pwd_h,
                            "xp": 0, "lvl": 1, "mode": None,
                            "mission_active": False, "mission_text": "",
                            "history": [], "streak": 0,
                            "last_mission_date": None, "palmares": [], "badges": [],
                            "lang": "fr", "ui_animations": True,
                            "ui_high_contrast": False, "ui_sound": False,
                            "mission_difficulty": {"key": "moyen", "xp": 20},
                        }
                        auth.save_user(user_input, new_data)
                        st.session_state.update(new_data)
                        st.session_state.username = user_input
                        st.session_state.logged_in = True
                        st.rerun()
                else:
                    st.error(T("err_short_creds"))
        st.markdown('</div>', unsafe_allow_html=True)

# --- INTERFACE DE JEU (APRÈS CONNEXION) ---
else:
    with st.sidebar:
        if st.button(T("lang_toggle"), key="lang_sidebar"):
            st.session_state.lang = "en" if st.session_state.lang == "fr" else "fr"
            st.rerun()

        streak = st.session_state.get("streak", 0)
        streak_color = "#00ff00" if streak >= 7 else ("#ffb700" if streak >= 3 else "#00f2ff")
        streak_icon = icon_html("flame", 14, streak_color)
        streak_label = f"{streak_icon} {streak} {T('sidebar_serie')}" if streak > 0 else T('sidebar_no_serie')

        st.markdown(f'''
            <div class="level-card">
                <small>{T('sidebar_operateur')}: {html.escape(st.session_state.username.upper())}</small><br>
                <span class="level-val">{T('sidebar_rang')}{st.session_state.lvl}</span><br>
                <span style="font-size:0.75rem; color:{streak_color}; font-family:monospace;">{streak_label}</span>
            </div>
        ''', unsafe_allow_html=True)

        st.caption(T("sidebar_xp_label"))
        st.progress(min(st.session_state.xp / 100, 1.0))
        st.caption(f"{st.session_state.xp}/100 XP")

        next_unit = st.session_state.lvl + 1
        xp_to_next = max(0, (next_unit * 10) - st.session_state.xp)
        st.caption(f"{T('sidebar_next_unit')} : V{next_unit} — {xp_to_next} {T('sidebar_xp_restants')}")
        progress_to_next = max(0.0, min(1.0, st.session_state.xp / max(next_unit * 10, 1)))
        st.progress(progress_to_next)

        st.markdown("---")
        if st.button(T("btn_disconnect"), type="secondary"):
            sync_save()
            st.session_state.logged_in = False
            st.rerun()

        can_reboot = st.session_state.mode is not None or st.session_state.mission_active or st.session_state.waiting_for_proof
        if st.button(T("btn_reboot"), type="secondary", disabled=not can_reboot):
            st.session_state.mode = None
            st.session_state.mission_active = False
            st.session_state.waiting_for_proof = False
            sync_save()
            st.rerun()

    st.markdown(f'<h1 class="main-title">{T("page_title")}</h1>', unsafe_allow_html=True)

    # TICKER D'ÉTAT DE LA BASE
    palmares_count = len(st.session_state.get("palmares", []))
    last_date = st.session_state.get("last_mission_date", None)
    if last_date:
        try:
            import datetime as _dt
            days_since = (_dt.date.today() - _dt.date.fromisoformat(last_date[:10])).days
            ticker_msg = f"{T('ticker_stable')} {days_since}{T('ticker_stable_j')} {palmares_count} {T('ticker_stable_ops')}"
            ticker_color = "#ff4d6d" if days_since >= 3 else "#00f2ff"
        except (ValueError, TypeError):
            ticker_msg = f"BASE STABLE — {palmares_count} {T('ticker_stable_ops')}"
            ticker_color = "#00f2ff"
    else:
        ticker_msg = T("ticker_no_ops")
        ticker_color = "#ffb700"
    ticker_icon = icon_html("chevron-right", 12, ticker_color)
    st.markdown(f'<p style="font-family:monospace; font-size:0.75rem; color:{ticker_color}; border-left:2px solid {ticker_color}; padding-left:8px; margin-bottom:1rem;">{ticker_icon} {ticker_msg}</p>', unsafe_allow_html=True)

    # 1. CHOIX DU MODE
    if st.session_state.mode is None:
        st.markdown(f'''
            <div class="manual-frame panel-shell">
                <h3>{T('frame_scan_title')}</h3>
                <p>{T('frame_scan_desc')}</p>
            </div>
        ''', unsafe_allow_html=True)

        lang = st.session_state.get("lang", "fr")
        diff_options = list(DIFFICULTY_MAP[lang].keys())
        diff_choice = st.radio(
            T("difficulty_label"),
            diff_options,
            index=1,
            horizontal=True,
            key="diff_radio",
        )
        diff_key, diff_xp, diff_color = DIFFICULTY_MAP[lang][diff_choice]
        st.session_state.mission_difficulty = {"key": diff_key, "xp": diff_xp}
        st.markdown(f'<p style="font-size:0.75rem; font-family:monospace; color:{diff_color};">PROTOCOLE_{diff_key.upper()} | RÉCOMPENSE : +{diff_xp} XP</p>', unsafe_allow_html=True)

        st.markdown('<div class="mobile-cta">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            if st.button(T("btn_camera"), type="primary"):
                st.session_state.mode = "camera"
                sync_save(); st.rerun()
        with col2:
            if st.button(T("btn_upload"), type="primary"):
                st.session_state.mode = "upload"
                sync_save(); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # 2. CONTRAT ACTIF
    elif st.session_state.mission_active:
        diff_info = st.session_state.get("mission_difficulty", {"key": "moyen", "xp": 20})
        diff_color = {"facile": "#00ff00", "easy": "#00ff00", "moyen": "#ffb700", "medium": "#ffb700", "difficile": "#ff4d6d", "hard": "#ff4d6d"}.get(diff_info.get("key", "moyen"), "#ffb700")
        st.markdown(f'''
            <div class="mission-box panel-shell">
                <h3 style="margin:0; color:#00f2ff; font-family:Orbitron;">{T('mission_active_title')}</h3>
                <p style="margin:8px 0 4px 0; color:{diff_color}; font-family:monospace; font-size:0.78rem;">PROTOCOLE_{diff_info['key'].upper()} | +{diff_info['xp']} XP</p>
                <p style="color:#fff; margin-top:15px;">{st.session_state.mission_text}</p>
            </div>
        ''', unsafe_allow_html=True)

        if not st.session_state.waiting_for_proof:
            if st.button(T("btn_send_proof"), type="primary"):
                st.session_state.waiting_for_proof = True
                st.rerun()
        else:
            st.info(f"{T('proof_analyser_label')} : {st.session_state.mode.upper()}")
            proof = st.camera_input("CAPTURE") if st.session_state.mode == "camera" else st.file_uploader("FICHIER")

            if proof:
                img_p = Image.open(proof)
                h_p = get_image_hash(img_p)
                if st.button(T("btn_analyse"), type="primary", disabled=proof is None):
                    if model is None:
                        st.error(T("err_ai_unavail"))
                        st.stop()
                    if h_p in st.session_state.history:
                        st.error(T("err_duplicate"))
                    else:
                        try:
                            with st.spinner(T("spinner_verify")):
                                diff_key = diff_info.get("key", "moyen")
                                if diff_key in ("facile", "easy"):
                                    check_prompt = (
                                        f"Mission à vérifier : {st.session_state.mission_text}. "
                                        "Niveau FACILE: valide si la preuve montre clairement une progression réelle de la tâche, même si ce n'est pas parfait. "
                                        "Réponds d'abord par VALIDÉ ou REJETÉ, puis une justification en une phrase."
                                    )
                                elif diff_key in ("difficile", "hard"):
                                    check_prompt = (
                                        f"Mission à vérifier : {st.session_state.mission_text}. "
                                        "Niveau DIFFICILE: valide uniquement si l'objectif est totalement accompli et si la preuve montre aussi la contrainte/qualité attendue. "
                                        "En cas de doute, REJETÉ. Réponds d'abord par VALIDÉ ou REJETÉ, puis une justification en une phrase."
                                    )
                                else:
                                    check_prompt = (
                                        f"Mission à vérifier : {st.session_state.mission_text}. "
                                        "Niveau MOYEN: valide si l'objectif principal est atteint de façon crédible. "
                                        "Réponds d'abord par VALIDÉ ou REJETÉ, puis une justification en une phrase."
                                    )
                                check_res = model.generate_content([check_prompt, img_p])
                                if "VALIDÉ" in check_res.text.upper():
                                    import datetime as _dt
                                    today_str = _dt.date.today().isoformat()
                                    last = st.session_state.get("last_mission_date", None)
                                    if last == today_str:
                                        pass
                                    elif last and (_dt.date.today() - _dt.date.fromisoformat(last)).days == 1:
                                        st.session_state.streak = st.session_state.get("streak", 0) + 1
                                    else:
                                        st.session_state.streak = 1
                                    st.session_state.last_mission_date = today_str

                                    xp_gain = diff_info["xp"]
                                    st.session_state.xp += xp_gain
                                    st.session_state.mission_active = False
                                    st.session_state.waiting_for_proof = False
                                    st.session_state.history.append(h_p)

                                    if "palmares" not in st.session_state:
                                        st.session_state.palmares = []
                                    st.session_state.palmares.append({
                                        "nom": st.session_state.mission_text[:60],
                                        "date": _dt.datetime.now().isoformat(),
                                        "xp_gained": xp_gain,
                                        "zone": "general",
                                        "difficulty": diff_info["key"],
                                    })

                                    new_badges = check_badges(st.session_state)
                                    for icon_name, label_key in new_badges:
                                        st.toast(f"{T('badge_unlocked')} : {T(label_key)}")

                                    if st.session_state.xp >= 100:
                                        st.session_state.lvl += 1
                                        st.session_state.xp = 0
                                        st.balloons()
                                    sync_save()
                                    st.rerun()
                                else:
                                    st.error(f"REJETÉ : {check_res.text}")
                        except Exception as e:
                            st.error(f"ERREUR : {e}")

    # 3. SCAN DE ZONE
    else:
        diff_info = st.session_state.get("mission_difficulty", {"key": "moyen", "xp": 20})
        st.markdown(f"### [ {T('scan_title')} : {st.session_state.mode.upper()} ]")
        source = st.camera_input("SCAN") if st.session_state.mode == "camera" else st.file_uploader("DATA")

        if source:
            img = Image.open(source)
            h_i = get_image_hash(img)
            if h_i in st.session_state.history:
                st.warning(T("err_img_used"))
            else:
                st.image(img, width=400)
                if st.button(T("btn_generate"), type="primary", disabled=source is None):
                    if model is None:
                        st.error(T("err_ai_unavail"))
                        st.stop()
                    try:
                        with st.spinner(T("spinner_gen")):
                            diff_key = diff_info["key"]
                            diff_xp = diff_info["xp"]
                            if diff_key in ("facile", "easy"):
                                prompt = f"Tu es une IA de gamification cyberpunk. À partir de cette photo de corvée domestique, génère un contrat de mission RPG SIMPLE et rapide : NOM DE MISSION (style cyberpunk), OBJECTIF SIMPLE ET PRÉCIS, RÉCOMPENSE (+{diff_xp} XP). Maximum 3 lignes."
                            elif diff_key in ("difficile", "hard"):
                                prompt = f"Tu es une IA de gamification cyberpunk. À partir de cette photo de corvée domestique, génère un contrat de mission RPG DIFFICILE et exigeant avec un objectif précis et mesurable, une contrainte supplémentaire (temps, qualité, exhaustivité) : NOM DE MISSION (style cyberpunk), OBJECTIF DIFFICILE, CONTRAINTE, RÉCOMPENSE (+{diff_xp} XP). Maximum 4 lignes."
                            else:
                                prompt = f"Tu es une IA de gamification cyberpunk. À partir de cette photo de corvée domestique, génère un contrat de mission RPG ultra court et immersif : NOM DE MISSION (style cyberpunk), OBJECTIF PRÉCIS (ce que l'opérateur doit accomplir), RÉCOMPENSE (+{diff_xp} XP). Maximum 3 lignes."
                            resp = model.generate_content([prompt, img])
                            st.session_state.mission_text = resp.text
                            st.session_state.mission_active = True
                            st.session_state.history.append(h_i)
                            sync_save()
                            st.rerun()
                    except Exception as e:
                        st.error(f"ERREUR : {e}")
