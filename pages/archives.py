import streamlit as st
import hashlib
import base64  # AJOUTÉ pour lire tes images locales
import os      # AJOUTÉ pour vérifier tes fichiers
from i18n import T
from lucide import icon_html
from ui_preferences import ensure_ui_defaults, inject_ui_overrides

# 1. STYLE ET CONFIG
try:
    with open("style.css", "r") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
except FileNotFoundError:
    st.error(T("err_css_not_found"))
except OSError as e:
    st.error(T("err_css_load").format(error=e))

ensure_ui_defaults(st.session_state)
inject_ui_overrides(st.session_state)

# On récupère le niveau actuel du joueur (app.py l'initialise à 1)
user_lvl = st.session_state.get('lvl', 1)

st.markdown(f'<h1 class="main-title">{T("archives_title")}</h1>', unsafe_allow_html=True)

# --- FONCTION POUR CONVERTIR TES IMAGES PERSO EN TEXTE LISIBLE PAR LE HTML ---
def get_base64_image(image_path):
    try:
        if os.path.exists(image_path):
            with open(image_path, "rb") as img_file:
                return f"data:image/png;base64,{base64.b64encode(img_file.read()).decode()}"
        return None
    except OSError:
        return None

NOMS_AGENTS = [
    "Kenji", "Akira", "Rei", "Hiroshi", "Tetsuo", "Kusanagi", "Yuki", "Hanzo",
    "Miko", "SaitoSterling", "Valerius", "Sloane", "Maximilian", "Eleanor",
    "Kozlov", "Halloway", "Vanderbilt", "Saburo", "ArisProxy", "Glitch",
    "Data", "Cipher", "Null", "Static", "Vector", "Bit", "Link", "Buffer",
]

# 2. FONCTION DU GÉNÉRATEUR (Modifiée pour tes images locales)
def generer_agent(niveau):
    # TA LIGNE D'IMAGE : cherche "Perso 1.png", "Perso 2.png", etc. dans le dossier assets
    chemin_local = f"assets/Perso {niveau}.png"
    
    img_data = get_base64_image(chemin_local)
    
    # Si l'image n'est pas trouvée sur ton PC, on met une image de secours vide
    if not img_data:
        img_data = "https://via.placeholder.com/60/000000/00f2ff?text=NOT_FOUND"
    
    # Calcul de la puissance (10 de base + 2 par niveau)
    puissance = 10 + (niveau * 2)
    
    # Nom du personnage depuis la liste, cycle si niveau > nb de noms
    nom = NOMS_AGENTS[(niveau - 1) % len(NOMS_AGENTS)]
    
    return nom, img_data, puissance

# 3. AFFICHAGE EN GRILLE
st.write(f"### [ {T('archives_level')} : {user_lvl} / 50 ]")

def render_agent_card(i, col_slot):
    nom, img, pwr = generer_agent(i)
    is_unlocked = user_lvl >= i
    tilt_class = "archive-card--tilt-right" if i % 2 else "archive-card--tilt-left"

    with col_slot:
        if is_unlocked:
            # --- AGENT DÉBLOQUÉ ---
            st.markdown(f'''
                <div class="archive-card archive-card--unlocked {tilt_class}">
                    <div class="archive-card__portrait">
                        <img src="{img}" style="width: 124px; height: 124px; image-rendering: pixelated; object-fit: contain;">
                    </div>
                    <h4 class="archive-card__name">{nom}</h4>
                    <p class="archive-card__power">PWR: +{pwr}%</p>
                </div>
            ''', unsafe_allow_html=True)

            # Bouton pour sélectionner cet agent
            if st.button(f"{T('btn_sync')}{i}", key=f"btn_{i}", type="primary"):
                st.session_state.active_agent = nom
                st.session_state.active_puissance = pwr
                st.session_state.active_img = img
                st.success(T("archives_unit_activated").format(name=nom))
                st.rerun()
        else:
            # --- AGENT VERROUILLÉ ---
            lock_icon = icon_html("lock", 36, "#8aa3b8")
            st.markdown(f'''
                <div class="archive-card archive-card--locked {tilt_class}">
                    <div class="archive-card__lock">{lock_icon}</div>
                    <p class="archive-card__locked-text">{T("archives_required_lvl").format(level=i)}</p>
                </div>
            ''', unsafe_allow_html=True)
            st.button(f"{T('btn_locked_txt')}{i}", key=f"btn_locked_{i}", disabled=True)


# Affiche d'abord les 5 premières cartes
top_cols = st.columns(3)
for idx, i in enumerate(range(1, 6)):
    render_agent_card(i, top_cols[idx % 3])

# Les cartes restantes sont pliées dans "Voir plus"
with st.expander(T("archives_voir_plus")):
    more_cols = st.columns(3)
    for idx, i in enumerate(range(6, 51)):
        render_agent_card(i, more_cols[idx % 3])

# 4. NAVIGATION
if st.button(T("archives_nav")):
    st.switch_page("pages/hub.py")