import streamlit as st
import os
from datetime import datetime

# 1. STYLE
try:
    with open("style.css", "r") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
except FileNotFoundError:
    st.error("ERREUR : Fichier style.css introuvable.")
except OSError as e:
    st.error(f"ERREUR : Impossible de charger style.css ({e}).")

# 2. GARDE : connexion requise
if not st.session_state.get("logged_in", False):
    st.warning("ACCÈS REFUSÉ — Initialisez votre session depuis le terminal principal.")
    if st.button("⬅️ RETOUR AU TERMINAL"):
        st.switch_page("app.py")
    st.stop()

# 3. TITRE
st.markdown('<h1 class="main-title">PALMARÈS_OPS</h1>', unsafe_allow_html=True)

palmares = st.session_state.get("palmares", [])

# 4. STATS GLOBALES
total_contrats = len(palmares)
total_xp = sum(e.get("xp_gained", 0) for e in palmares)
streak = st.session_state.get("streak", 0)

col_a, col_b, col_c = st.columns(3)
with col_a:
    st.markdown(f'''
        <div class="stat-badge">
            <span class="stat-badge__val">{total_contrats}</span>
            <span class="stat-badge__label">CONTRATS ACCOMPLIS</span>
        </div>
    ''', unsafe_allow_html=True)
with col_b:
    st.markdown(f'''
        <div class="stat-badge">
            <span class="stat-badge__val">{total_xp}</span>
            <span class="stat-badge__label">DONNÉES_XP RÉCOLTÉES</span>
        </div>
    ''', unsafe_allow_html=True)
with col_c:
    streak_color = "#00ff00" if streak >= 3 else "#00f2ff"
    st.markdown(f'''
        <div class="stat-badge" style="border-color: {streak_color};">
            <span class="stat-badge__val" style="color: {streak_color};">{streak}🔥</span>
            <span class="stat-badge__label">SÉRIE ACTIVE</span>
        </div>
    ''', unsafe_allow_html=True)

st.markdown("---")

# 5. BADGES THÉMATIQUES
ZONE_BADGES = {
    "cuisine": ("🍳", "CHEF DE ZONE", "#ff6b35"),
    "sol":     ("🧹", "BALAYEUR_ELITE", "#00f2ff"),
    "sanitaires": ("🚿", "PURIFICATEUR", "#7b2fff"),
    "general": ("⚙️", "OPÉRATEUR", "#ffffff"),
}

if palmares:
    # Compter les badges gagnés par zone
    zones_count = {}
    for entry in palmares:
        z = entry.get("zone", "general")
        zones_count[z] = zones_count.get(z, 0) + 1

    st.markdown("### [ BADGES_TERRAIN ]")
    badge_cols = st.columns(len(ZONE_BADGES))
    for idx, (zone_key, (icon, label, color)) in enumerate(ZONE_BADGES.items()):
        count = zones_count.get(zone_key, 0)
        with badge_cols[idx]:
            opacity = "1" if count > 0 else "0.25"
            st.markdown(f'''
                <div class="trophy-badge" style="opacity:{opacity}; border-color:{color};">
                    <span style="font-size:2rem;">{icon}</span>
                    <p style="color:{color}; font-size:0.7rem; font-family:Orbitron; margin:4px 0 0;">{label}</p>
                    <p style="color:#888; font-size:0.65rem; margin:0;">×{count}</p>
                </div>
            ''', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### [ HISTORIQUE_OPÉRATIONS ]")

    # Trier du plus récent au plus ancien
    sorted_pal = sorted(palmares, key=lambda x: x.get("date", ""), reverse=True)

    for entry in sorted_pal:
        nom = entry.get("nom", "CONTRAT_INCONNU")
        date_str = entry.get("date", "")
        xp = entry.get("xp_gained", 0)
        zone = entry.get("zone", "general")
        icon = ZONE_BADGES.get(zone, ZONE_BADGES["general"])[0]
        color = ZONE_BADGES.get(zone, ZONE_BADGES["general"])[2]

        # Formater la date lisiblement
        try:
            date_obj = datetime.fromisoformat(date_str)
            date_display = date_obj.strftime("%d/%m/%Y — %Hh%M")
        except (ValueError, TypeError):
            date_display = date_str or "DATE_INCONNUE"

        st.markdown(f'''
            <div class="palmares-entry">
                <span class="palmares-entry__icon">{icon}</span>
                <div class="palmares-entry__info">
                    <p class="palmares-entry__name">{nom}</p>
                    <p class="palmares-entry__date">{date_display}</p>
                </div>
                <span class="palmares-entry__xp" style="color:{color}">+{xp} XP</span>
            </div>
        ''', unsafe_allow_html=True)
else:
    st.markdown('''
        <div class="login-frame" style="text-align:center; opacity:0.6;">
            <p style="font-family:Orbitron; color:#00f2ff;">AUCUNE OPÉRATION RÉPERTORIÉE</p>
            <p style="font-size:0.85rem;">Scannez votre première corvée pour écrire l'histoire.</p>
        </div>
    ''', unsafe_allow_html=True)

# 6. NAVIGATION
st.markdown("<br>", unsafe_allow_html=True)
if st.button("⬅️ RETOUR AU TERMINAL"):
    st.switch_page("app.py")
