import streamlit as st
import random
import time
from lucide import icon_html

# 1. STYLE (On garde ton identité visuelle)
try:
    with open("style.css", "r") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
except FileNotFoundError:
    st.error("ERREUR : Fichier style.css introuvable.")
except OSError as e:
    st.error(f"ERREUR : Impossible de charger style.css ({e}).")

# 2. RÉCUPÉRATION DES INFOS DE L'AGENT
# On récupère le perso choisi dans les archives. Si rien, on met des valeurs de base.
agent_nom = st.session_state.get('active_agent', "AUCUN_AGENT")
agent_puissance = st.session_state.get('active_puissance', 10)
agent_img = st.session_state.get('active_img', "https://i.ibb.co/L8p61mX/samurai-sprite.png")

st.markdown('<h1 class="main-title">CENTRE_D_OPÉRATIONS</h1>', unsafe_allow_html=True)

# 3. INTERFACE DE MISSION
col1, col2 = st.columns([1, 1.5])

with col1:
    # Rappel de l'agent actif dans une login-frame
    st.markdown(f'''
        <div class="login-frame panel-shell" style="text-align:center;">
            <p style="color:#00f2ff; font-size:0.8rem;">UNITÉ_EN_LIGNE</p>
            <img src="{agent_img}" style="width:80px; image-rendering:pixelated;">
            <h3 style="font-family:Orbitron; font-size:0.9rem;">{agent_nom}</h3>
            <p style="color:#00ff00; font-family:monospace;">PWR: {agent_puissance}</p>
        </div>
    ''', unsafe_allow_html=True)

with col2:
    # Détails de la mission dans une mission-box
    st.markdown('''
        <div class="mission-box panel-shell">
            <h2 style="color:#ff0055; font-size:1.2rem; font-family:Orbitron;">SABOTAGE_RESEAU</h2>
            <p style="font-size:0.8rem;">Cible : Serveurs Arasaka. <br>Difficulté : <b>Niveau 40</b></p>
            <hr style="border:0.5px solid #333;">
            <p style="font-size:0.7rem; color:#ffffff;">Plus votre puissance est élevée, plus le succès est garanti.</p>
        </div>
    ''', unsafe_allow_html=True)

    # CALCUL DES CHANCES (Exemple: Base 30% + Puissance de l'agent)
    chances_succes = 30 + agent_puissance
    if chances_succes > 98: chances_succes = 98 # Jamais 100% de sécurité !

    st.write(f"PROBABILITÉ DE RÉUSSITE : **{chances_succes}%**")
    can_launch = agent_nom != "AUCUN_AGENT"
    
    if st.button("LANCER L'INFILTRATION", use_container_width=True, type="primary", disabled=not can_launch):
        if can_launch:
            barre = st.progress(0, text="Piratage en cours...")
            for percent_complete in range(100):
                time.sleep(0.02) # Simule le temps de l'action
                barre.progress(percent_complete + 1)
            
            # TIRAGE AU SORT
            resultat = random.randint(1, 100)
            
            if resultat <= chances_succes:
                st.balloons()
                st.success("MISSION RÉUSSIE ! Données extraites.")
                # ON AUGMENTE LE NIVEAU DU JOUEUR !
                st.session_state.lvl = st.session_state.get('lvl', 1) + 1
                st.info(f"NIVEAU AUGMENTÉ : Vous êtes maintenant **Niveau {st.session_state.lvl}**")
                st.write("Allez dans les ARCHIVES pour voir votre nouveau personnage !")
            else:
                st.error("ÉCHEC. L'agent a dû battre en retraite. Puissance insuffisante.")
    if not can_launch:
        st.caption("Sélectionne un agent dans les archives pour activer le lancement.")

# Bouton de navigation
st.markdown("<br>", unsafe_allow_html=True)
st.markdown(f'<p style="margin:0 0 8px 0;">{icon_html("arrow-left", 14, "#00f2ff")}</p>', unsafe_allow_html=True)
if st.button("RETOUR AU HUB"):
    st.switch_page("app.py")