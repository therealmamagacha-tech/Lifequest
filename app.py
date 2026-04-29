import streamlit as st
import google.generativeai as genai
from PIL import Image
import hashlib
import os
import auth  # Ton fichier auth.py doit être présent dans le dossier


def load_dotenv_file(path=".env"):
    """Charge les variables d'environnement depuis un fichier .env local."""
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

# --- CONFIGURATION PAGE ---
st.set_page_config(page_title="CORE-OS", layout="wide")

if not GEMINI_API_KEY:
    st.warning("Clé API absente: ajoute GEMINI_API_KEY dans le fichier .env.")

# Injection du CSS (Grille, Néons, Biseaux)
try:
    with open("style.css", "r") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
except FileNotFoundError:
    st.error("ERREUR : Fichier style.css introuvable.")
except OSError as e:
    st.error(f"ERREUR : Impossible de charger style.css ({e}).")

# --- INITIALISATION SESSION ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

def get_image_hash(img):
    """Crée une empreinte unique pour l'image."""
    return hashlib.md5(img.tobytes()).hexdigest()

def sync_save():
    """Sauvegarde physique des données de l'agent."""
    if st.session_state.logged_in:
        data = {
            "password": st.session_state.password,
            "xp": st.session_state.xp,
            "lvl": st.session_state.lvl,
            "mode": st.session_state.mode,
            "mission_active": st.session_state.mission_active,
            "mission_text": st.session_state.mission_text,
            "history": st.session_state.history
        }
        auth.save_user(st.session_state.username, data)

# --- ÉCRAN D'ACCÈS (REMPLISSAGE DU RECTANGLE NOIR) ---
if not st.session_state.logged_in:
    st.markdown('<h1 class="main-title">CORE_OS</h1>', unsafe_allow_html=True)
    
    # Ton cadre biseauté avec instructions
    st.markdown('''
        <div class="login-frame">
            <h3 style="margin:0; letter-spacing:3px; color:#00f2ff; font-family:Orbitron;">[ STANDBY_MODE ]</h3>
            <p style="margin:15px 0 0 0; font-size:1rem; opacity:0.9; line-height:1.5;">
                Système de gamification CORE_OS détecté.<br>
                Identifiez-vous pour charger votre <b>Neural-Link</b> ou créez un compte agent pour commencer.
            </p>
        </div>
    ''', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div style="max-width:500px; margin:auto; padding:10px;">', unsafe_allow_html=True)
        user_input = st.text_input("🆔 AGENT_ID")
        pass_input = st.text_input("🔑 ACCESS_CODE", type="password")
        can_auth = bool(user_input.strip()) and bool(pass_input)
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("LOG_IN", type="primary", disabled=not can_auth):
                data = auth.load_user(user_input, pass_input)
                if data:
                    st.session_state.update(data)
                    st.session_state.username = user_input
                    st.session_state.logged_in = True
                    st.session_state.waiting_for_proof = False
                    st.rerun()
                else:
                    st.error("ACCÈS REFUSÉ : Identifiants invalides.")

            if st.button("📂 ACCÉDER AUX ARCHIVES", disabled=not st.session_state.get("logged_in", False)):
                st.switch_page("pages/archives.py")

            if st.button("⚔️ LANCER UNE MISSION", disabled=not st.session_state.get("logged_in", False)):
                st.switch_page("missions.py")
        with c2:
            # Correction du bouton SIGN_UP pour une connexion instantanée
            if st.button("SIGN_UP", type="primary", disabled=not can_auth):
                if len(user_input) > 2 and len(pass_input) > 3:
                    if auth.user_exists(user_input):
                        st.warning("AGENT DÉJÀ RÉPERTORIÉ.")
                    else:
                        pwd_h = auth.hash_password(pass_input)
                        new_data = {
                            "password": pwd_h,
                            "xp": 0, "lvl": 1, "mode": None,
                            "mission_active": False, "mission_text": "", "history": []
                        }
                        auth.save_user(user_input, new_data)
                        
                        # Connexion automatique immédiate
                        st.session_state.update(new_data)
                        st.session_state.username = user_input
                        st.session_state.logged_in = True
                        st.rerun()
                else:
                    st.error("IDENTIFIANTS TROP COURTS.")
        st.markdown('</div>', unsafe_allow_html=True)

# --- INTERFACE DE JEU (APRÈS CONNEXION) ---
else:
    # HUD SIDEBAR
    with st.sidebar:
        st.markdown(f'''
            <div class="level-card">
                <small>OPERATOR: {st.session_state.username.upper()}</small><br>
                <span class="level-val">LVL_{st.session_state.lvl}</span>
            </div>
        ''', unsafe_allow_html=True)
        st.write(f"PROGRESSION : {st.session_state.xp}/100 XP")
        st.progress(min(st.session_state.xp / 100, 1.0))
        if st.button("📂 CONSULTER LES ARCHIVES", type="primary"):
            st.switch_page("pages/archives.py")
        st.markdown("---")
        st.caption("Zone critique")
        if st.button("🔌 DISCONNECT", type="secondary"):
            sync_save()
            st.session_state.logged_in = False
            st.rerun()
            
        can_reboot = st.session_state.mode is not None or st.session_state.mission_active or st.session_state.waiting_for_proof
        if st.button("🔄 REBOOT HUB", type="secondary", disabled=not can_reboot):
            st.session_state.mode = None
            st.session_state.mission_active = False
            st.session_state.waiting_for_proof = False
            sync_save()
            st.rerun()

    st.markdown('<h1 class="main-title">CORE_OS</h1>', unsafe_allow_html=True)

    # 1. CHOIX DU MODE
    if st.session_state.mode is None:
        st.markdown('''
            <div class="manual-frame panel-shell">
                <h3>[ MANUAL_OVERRIDE ]</h3>
                <p>Scannez une corvée ou une tâche pour générer une mission.</p>
            </div>
        ''', unsafe_allow_html=True)
        st.markdown('<div class="mobile-cta">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📷 OPTIC SCANNER", type="primary"):
                st.session_state.mode = "camera"
                sync_save(); st.rerun()
        with col2:
            if st.button("📁 DATA FEED", type="primary"):
                st.session_state.mode = "upload"
                sync_save(); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # 2. MISSION ACTIVE
    elif st.session_state.mission_active:
        st.markdown(f'''
            <div class="mission-box panel-shell">
                <h3 style="margin:0; color:#00f2ff; font-family:Orbitron;">> MISSION_DÉCRYPTÉE</h3>
                <p style="color:#fff; margin-top:15px;">{st.session_state.mission_text}</p>
            </div>
        ''', unsafe_allow_html=True)
        
        if not st.session_state.waiting_for_proof:
            if st.button("🛰️ SOUMETTRE PREUVE", type="primary"):
                st.session_state.waiting_for_proof = True
                st.rerun()
        else:
            st.info(f"ANALYSEUR DE PREUVE ACTIVÉ : {st.session_state.mode.upper()}")
            proof = st.camera_input("CAPTURE") if st.session_state.mode == "camera" else st.file_uploader("FICHIER")
            
            if proof:
                img_p = Image.open(proof)
                h_p = get_image_hash(img_p)
                if st.button("⚡ ANALYSER L'INTÉGRITÉ", type="primary", disabled=proof is None):
                    if model is None:
                        st.error("IA indisponible: configure GEMINI_API_KEY dans .env.")
                        st.stop()
                    if h_p in st.session_state.history:
                        st.error("DOUBLON : Image déjà utilisée.")
                    else:
                        try:
                            with st.spinner("VÉRIFICATION IA..."):
                                check_res = model.generate_content([f"La mission est : {st.session_state.mission_text}. Réponds 'VALIDÉ' ou 'REJETÉ'.", img_p])
                                if "VALIDÉ" in check_res.text.upper():
                                    st.session_state.xp += 20
                                    st.session_state.mission_active = False
                                    st.session_state.waiting_for_proof = False
                                    st.session_state.history.append(h_p)
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

    # 3. SCAN DE DÉPART
    else:
        st.markdown(f"### [ ACQUISITION : {st.session_state.mode.upper()} ]")
        source = st.camera_input("SCAN") if st.session_state.mode == "camera" else st.file_uploader("DATA")
        
        if source:
            img = Image.open(source)
            h_i = get_image_hash(img)
            if h_i in st.session_state.history:
                st.warning("ANOMALIE : Donnée déjà traitée.")
            else:
                st.image(img, width=400)
                if st.button("⚡ GÉNÉRER OBJECTIF", type="primary", disabled=source is None):
                    if model is None:
                        st.error("IA indisponible: configure GEMINI_API_KEY dans .env.")
                        st.stop()
                    try:
                        with st.spinner("LIAISON CORE..."):
                            resp = model.generate_content(["Crée une mission RPG ultra courte : NOM, OBJECTIF, +20XP.", img])
                            st.session_state.mission_text = resp.text
                            st.session_state.mission_active = True
                            st.session_state.history.append(h_i)
                            sync_save()
                            st.rerun()
                    except Exception as e:
                        st.error(f"ERREUR : {e}")