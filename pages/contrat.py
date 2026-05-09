import streamlit as st
import random
import time
from lucide import icon_html
from i18n import T
from ui_preferences import ensure_ui_defaults, inject_ui_overrides

# 1. STYLE (On garde ton identité visuelle)
try:
    with open("style.css", "r") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
except FileNotFoundError:
    st.error(T("err_css_not_found"))
except OSError as e:
    st.error(T("err_css_load").format(error=e))

ensure_ui_defaults(st.session_state)
inject_ui_overrides(st.session_state)

# 2. RÉCUPÉRATION DES INFOS DE L'AGENT
# On récupère le perso choisi dans les archives. Si rien, on met des valeurs de base.
agent_nom = st.session_state.get('active_agent')
agent_puissance = st.session_state.get('active_puissance', 10)
agent_img = st.session_state.get('active_img', None)
display_agent_name = agent_nom or T("no_agent")

st.markdown(f'<h1 class="main-title" style="font-size:clamp(1.2rem,5vw,2.5rem); word-break:break-word;">{T("contract_title")}</h1>', unsafe_allow_html=True)

# 3. INTERFACE DE MISSION
col1, col2 = st.columns([1, 1.5])

with col1:
    # Rappel de l'agent actif dans une login-frame
    has_agent = bool(agent_nom)
    agent_visual = f'<img src="{agent_img}" style="width:80px; image-rendering:pixelated;">'\
        if (has_agent and agent_img) else \
        '<div style="width:80px;height:80px;margin:auto;border:2px dashed #00f2ff;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:1.5rem;color:#00f2ff;">?</div>'
    st.markdown(f'''
        <div class="login-frame panel-shell" style="text-align:center;">
            <p style="color:#00f2ff; font-size:0.8rem;">{T("contract_unit_deployed")}</p>
            {agent_visual}
            <h3 style="font-family:Orbitron; font-size:0.9rem;">{display_agent_name}</h3>
            <p style="color:#00ff00; font-family:monospace;">PWR: {agent_puissance}</p>
        </div>
    ''', unsafe_allow_html=True)

with col2:
    # Détails de la mission dans une mission-box
    st.markdown(f'''
        <div class="mission-box panel-shell">
            <h2 style="color:#ff0055; font-size:1.2rem; font-family:Orbitron;">{T("contract_name")}</h2>
            <p style="font-size:0.8rem;">{T("contract_target")} <br>{T("contract_difficulty")} : <b>{T("contract_level")}</b></p>
            <hr style="border:0.5px solid #333;">
            <p style="font-size:0.7rem; color:#ffffff;">{T("contract_power_hint")}</p>
        </div>
    ''', unsafe_allow_html=True)

    # CALCUL DES CHANCES (Exemple: Base 30% + Puissance de l'agent)
    chances_succes = 30 + agent_puissance
    if chances_succes > 98: chances_succes = 98 # Jamais 100% de sécurité !

    st.write(f"{T('contract_success_rate')} : **{chances_succes}%**")
    can_launch = bool(agent_nom)
    
    if st.button(T("contract_activate"), use_container_width=True, type="primary", disabled=not can_launch):
        if can_launch:
            barre = st.progress(0, text=T("contract_progress"))
            for percent_complete in range(100):
                time.sleep(0.02) # Simule le temps de l'action
                barre.progress(percent_complete + 1)
            
            # TIRAGE AU SORT
            resultat = random.randint(1, 100)
            
            if resultat <= chances_succes:
                st.balloons()
                st.success(T("contract_success"))
                st.session_state.lvl = st.session_state.get('lvl', 1) + 1
                st.info(T("contract_rank_up").format(level=st.session_state.lvl))
                st.write(T("contract_go_squad"))
            else:
                st.error(T("contract_rejected"))
    if not can_launch:
        st.caption(T("contract_need_agent"))

# Bouton de navigation
st.markdown("<br>", unsafe_allow_html=True)
col_nav1, col_nav2 = st.columns(2)
with col_nav1:
    st.markdown(f'<p style="margin:0 0 8px 0;">{icon_html("arrow-left", 14, "#00f2ff")}</p>', unsafe_allow_html=True)
    if st.button(T("btn_back_terminal")):
        st.switch_page("pages/hub.py")
with col_nav2:
    st.markdown(f'<p style="margin:0 0 8px 0;">{icon_html("users", 14, "#00f2ff")}</p>', unsafe_allow_html=True)
    if st.button(T("btn_escouade")):
        st.switch_page("pages/escouade.py")