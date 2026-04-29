import streamlit as st
import hashlib
import base64  # AJOUTÉ pour lire tes images locales
import os      # AJOUTÉ pour vérifier tes fichiers

# 1. STYLE ET CONFIG
try:
    with open("style.css", "r") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
except FileNotFoundError:
    st.error("ERREUR : Fichier style.css introuvable.")
except OSError as e:
    st.error(f"ERREUR : Impossible de charger style.css ({e}).")

# On récupère le niveau actuel du joueur (app.py l'initialise à 1)
user_lvl = st.session_state.get('lvl', 1)

st.markdown('<h1 class="main-title">ARCHIVES_GÉNÉRATIVES</h1>', unsafe_allow_html=True)

# --- FONCTION POUR CONVERTIR TES IMAGES PERSO EN TEXTE LISIBLE PAR LE HTML ---
def get_base64_image(image_path):
    try:
        if os.path.exists(image_path):
            with open(image_path, "rb") as img_file:
                return f"data:image/png;base64,{base64.b64encode(img_file.read()).decode()}"
        return None
    except OSError:
        return None

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
    
    # Nom automatique
    nom = f"UNIT_NX_{niveau}"
    
    return nom, img_data, puissance

# 3. AFFICHAGE EN GRILLE
st.write(f"### [ NIVEAU D'ACCÈS : {user_lvl} / 50 ]")

# On crée 3 colonnes pour l'affichage
cols = st.columns(3)

for i in range(1, 51):
    nom, img, pwr = generer_agent(i)
    is_unlocked = user_lvl >= i
    
    # On place dans la bonne colonne
    with cols[(i-1) % 3]:
        if is_unlocked:
            # --- AGENT DÉBLOQUÉ (Structure 100% conservée) ---
            st.markdown(f'''
                <div class="mission-box" style="border-top: 2px solid #00f2ff; text-align: center; min-height: 380px; margin-bottom:20px;">
                    <p style="font-size: 0.6rem; color: #00f2ff;">ID: {hashlib.md5(nom.encode()).hexdigest()[:8]}</p>
                    <div style="background: rgba(0,242,255,0.05); padding: 10px; margin: 10px auto; width: 80px; border: 1px solid #00f2ff33; display: flex; align-items: center; justify-content: center;">
                        <img src="{img}" style="width: 60px; height: 60px; image-rendering: pixelated; object-fit: contain;">
                    </div>
                    <h4 style="font-family: Orbitron; font-size: 0.8rem;">{nom}</h4>
                    <p style="color: #00ff00; font-family: 'Share Tech Mono';">PWR: +{pwr}%</p>
                </div>
            ''', unsafe_allow_html=True)
            
            # Bouton pour sélectionner cet agent
            if st.button(f"SYNCHRONISER V{i}", key=f"btn_{i}"):
                st.session_state.active_agent = nom
                st.session_state.active_puissance = pwr
                st.session_state.active_img = img
                st.success(f"Unité {nom} activée !")
                st.rerun()
        else:
            # --- AGENT VERROUILLÉ ---
            st.markdown(f'''
                <div class="mission-box" style="opacity: 0.2; filter: grayscale(1); text-align: center; min-height: 380px; margin-bottom:20px;">
                    <div style="font-size: 2rem; margin-top: 60px;">🔒</div>
                    <p style="font-family: Orbitron; margin-top: 40px; font-size:0.7rem;">REQUIS: LVL {i}</p>
                </div>
            ''', unsafe_allow_html=True)

# 4. NAVIGATION
if st.button("⬅️ TERMINAL"):
    st.switch_page("app.py")