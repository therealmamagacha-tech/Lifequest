import streamlit as st
import os
from datetime import datetime
from i18n import T, BADGES_DEF
from lucide import icon_html
from ui_preferences import ensure_ui_defaults, inject_ui_overrides

# 1. STYLE
try:
    with open("style.css", "r") as f:
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

# 3. TITRE
st.markdown(
    f'<h1 class="main-title" style="margin-top: 18px; margin-bottom: 28px;">{T("palmares_title")}</h1>',
    unsafe_allow_html=True,
)

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
            <span class="stat-badge__label">{T("stat_contrats")}</span>
        </div>
    ''', unsafe_allow_html=True)
with col_b:
    st.markdown(f'''
        <div class="stat-badge">
            <span class="stat-badge__val">{total_xp}</span>
            <span class="stat-badge__label">{T("stat_xp")}</span>
        </div>
    ''', unsafe_allow_html=True)
with col_c:
    streak_color = "#00ff00" if streak >= 3 else "#00f2ff"
    streak_svg = icon_html("flame", 20, streak_color)
    st.markdown(f'''
        <div class="stat-badge" style="border-color: {streak_color};">
            <span class="stat-badge__val" style="color: {streak_color};">{streak_svg} {streak}</span>
            <span class="stat-badge__label">{T("stat_serie")}</span>
        </div>
    ''', unsafe_allow_html=True)

st.markdown("---")

# 5. BADGES THÉMATIQUES
ZONE_BADGES = {
    "cuisine": ("utensils-crossed", "badge_cuisine", "#ff6b35"),
    "sol":     ("brush", "badge_sol",     "#00f2ff"),
    "sanitaires": ("shower-head", "badge_sanitaires", "#7b2fff"),
    "general": ("settings", "badge_general", "#ffffff"),
}

if palmares:
    # Compter les badges gagnés par zone
    zones_count = {}
    for entry in palmares:
        z = entry.get("zone", "general")
        zones_count[z] = zones_count.get(z, 0) + 1

    st.markdown(f"### {T('badges_terrain_title')}")
    badge_cols = st.columns(len(ZONE_BADGES))
    for idx, (zone_key, (icon_name, label_key, color)) in enumerate(ZONE_BADGES.items()):
        count = zones_count.get(zone_key, 0)
        zone_icon = icon_html(icon_name, 30, color)
        with badge_cols[idx]:
            opacity = "1" if count > 0 else "0.25"
            st.markdown(f'''
                <div class="trophy-badge" style="opacity:{opacity}; border-color:{color};">
                    <span style="display:block; line-height:1;">{zone_icon}</span>
                    <p style="color:{color}; font-size:0.7rem; font-family:Orbitron; margin:4px 0 0;">{T(label_key)}</p>
                    <p style="color:#ffffff; font-size:0.65rem; margin:0;">×{count}</p>
                </div>
            ''', unsafe_allow_html=True)

    st.markdown("---")

    # 5b. SUCCÈS AGENT (achievements)
    st.markdown(f"### {T('achievements_title')}")
    earned_badges = st.session_state.get("badges", [])
    stats = {
        "total": total_contrats,
        "streak": streak,
        "hard": sum(1 for e in palmares if e.get("difficulty") in ("difficile", "hard")),
        "total_xp": total_xp,
    }
    ach_cols = st.columns(3)
    for idx, (badge_id, icon_name, label_key, condition) in enumerate(BADGES_DEF):
        unlocked = badge_id in earned_badges or condition(stats)
        label = T(label_key)
        ach_color = "#ffb700" if unlocked else "#ffffff"
        ach_icon = icon_html(icon_name, 28, ach_color)
        with ach_cols[idx % 3]:
            opacity = "1" if unlocked else "0.2"
            border_color = "#ffb700" if unlocked else "#333"
            glow = "0 0 12px rgba(255,183,0,0.5)" if unlocked else "none"
            st.markdown(f'''
                <div class="achievement-badge" style="opacity:{opacity}; border-color:{border_color}; box-shadow:{glow};">
                    <span style="display:block; line-height:1;">{ach_icon}</span>
                    <p style="font-family:Orbitron; font-size:0.62rem; color:{ach_color}; margin:4px 0 0; letter-spacing:0.5px;">{label}</p>
                </div>
            ''', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f"### {T('historique_title')}")

    # Trier du plus récent au plus ancien
    sorted_pal = sorted(palmares, key=lambda x: x.get("date", ""), reverse=True)

    for entry in sorted_pal:
        nom = entry.get("nom", "CONTRAT_INCONNU")
        date_str = entry.get("date", "")
        xp = entry.get("xp_gained", 0)
        zone = entry.get("zone", "general")
        difficulty = entry.get("difficulty", "moyen")
        icon_name = ZONE_BADGES.get(zone, ZONE_BADGES["general"])[0]
        color = ZONE_BADGES.get(zone, ZONE_BADGES["general"])[2]
        row_icon = icon_html(icon_name, 22, color)

        diff_icons = {
            "facile": icon_html("circle", 12, "#00ff00"),
            "easy": icon_html("circle", 12, "#00ff00"),
            "moyen": icon_html("circle", 12, "#ffb700"),
            "medium": icon_html("circle", 12, "#ffb700"),
            "difficile": icon_html("circle", 12, "#ff4d6d"),
            "hard": icon_html("circle", 12, "#ff4d6d"),
        }
        diff_icon = diff_icons.get(difficulty, icon_html("circle", 12, "#ffb700"))

        # Formater la date lisiblement
        try:
            date_obj = datetime.fromisoformat(date_str)
            date_display = date_obj.strftime("%d/%m/%Y — %Hh%M")
        except (ValueError, TypeError):
            date_display = date_str or "DATE_INCONNUE"

        st.markdown(f'''
            <div class="palmares-entry">
                <span class="palmares-entry__icon">{row_icon}</span>
                <div class="palmares-entry__info">
                    <p class="palmares-entry__name">{nom}</p>
                    <p class="palmares-entry__date">{date_display} {diff_icon}</p>
                </div>
                <span class="palmares-entry__xp" style="color:{color}">+{xp} XP</span>
            </div>
        ''', unsafe_allow_html=True)
else:
    st.markdown(f'''
        <div class="login-frame" style="text-align:center; opacity:0.6;">
            <p style="font-family:Orbitron; color:#00f2ff;">{T("no_ops")}</p>
            <p style="font-size:0.85rem;">{T("no_ops_sub")}</p>
        </div>
    ''', unsafe_allow_html=True)

# 6. NAVIGATION
st.markdown("<br>", unsafe_allow_html=True)
if st.button(T("btn_back_terminal")):
    st.switch_page("app.py")
