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

    if session_state.get("ui_sound", False):
        inject_sound_effects()


def inject_sound_effects():
    """Inject cyberpunk-style sounds on all interactive elements via Web Audio API."""
    st.markdown(
        """
        <script>
        (function() {
            if (window._cyberpunkSoundReady) return;
            window._cyberpunkSoundReady = true;

            var _ctx = null;
            function getCtx() {
                if (!_ctx) _ctx = new (window.AudioContext || window.webkitAudioContext)();
                if (_ctx.state === 'suspended') _ctx.resume();
                return _ctx;
            }

            // --- BUTTON / generic click ---
            function playCyberpunkClick() {
                try {
                    var ctx = getCtx(); var t = ctx.currentTime;
                    var o1 = ctx.createOscillator(), g1 = ctx.createGain();
                    o1.type = 'sawtooth';
                    o1.frequency.setValueAtTime(1200, t);
                    o1.frequency.exponentialRampToValueAtTime(200, t + 0.08);
                    g1.gain.setValueAtTime(0.18, t);
                    g1.gain.exponentialRampToValueAtTime(0.001, t + 0.09);
                    o1.connect(g1); g1.connect(ctx.destination);
                    o1.start(t); o1.stop(t + 0.09);

                    var o2 = ctx.createOscillator(), g2 = ctx.createGain();
                    o2.type = 'square';
                    o2.frequency.setValueAtTime(3200, t);
                    o2.frequency.exponentialRampToValueAtTime(800, t + 0.03);
                    g2.gain.setValueAtTime(0.08, t);
                    g2.gain.exponentialRampToValueAtTime(0.001, t + 0.03);
                    o2.connect(g2); g2.connect(ctx.destination);
                    o2.start(t); o2.stop(t + 0.03);

                    var o3 = ctx.createOscillator(), g3 = ctx.createGain();
                    o3.type = 'sine';
                    o3.frequency.setValueAtTime(80, t);
                    o3.frequency.exponentialRampToValueAtTime(40, t + 0.06);
                    g3.gain.setValueAtTime(0.25, t);
                    g3.gain.exponentialRampToValueAtTime(0.001, t + 0.06);
                    o3.connect(g3); g3.connect(ctx.destination);
                    o3.start(t); o3.stop(t + 0.06);
                } catch(e) {}
            }

            // --- NAV link ---
            function playCyberpunkNav() {
                try {
                    var ctx = getCtx(); var t = ctx.currentTime;
                    var o1 = ctx.createOscillator(), g1 = ctx.createGain();
                    o1.type = 'sine';
                    o1.frequency.setValueAtTime(300, t);
                    o1.frequency.exponentialRampToValueAtTime(900, t + 0.12);
                    g1.gain.setValueAtTime(0.14, t);
                    g1.gain.exponentialRampToValueAtTime(0.001, t + 0.18);
                    o1.connect(g1); g1.connect(ctx.destination);
                    o1.start(t); o1.stop(t + 0.18);

                    var o2 = ctx.createOscillator(), g2 = ctx.createGain();
                    o2.type = 'sawtooth';
                    o2.frequency.setValueAtTime(1800, t + 0.05);
                    o2.frequency.exponentialRampToValueAtTime(600, t + 0.14);
                    g2.gain.setValueAtTime(0.0, t);
                    g2.gain.setValueAtTime(0.09, t + 0.05);
                    g2.gain.exponentialRampToValueAtTime(0.001, t + 0.15);
                    o2.connect(g2); g2.connect(ctx.destination);
                    o2.start(t); o2.stop(t + 0.16);

                    var o3 = ctx.createOscillator(), g3 = ctx.createGain();
                    o3.type = 'sine';
                    o3.frequency.setValueAtTime(60, t);
                    o3.frequency.exponentialRampToValueAtTime(30, t + 0.1);
                    g3.gain.setValueAtTime(0.3, t);
                    g3.gain.exponentialRampToValueAtTime(0.001, t + 0.1);
                    o3.connect(g3); g3.connect(ctx.destination);
                    o3.start(t); o3.stop(t + 0.1);
                } catch(e) {}
            }

            // --- TOGGLE / CHECKBOX : soft binary beep ---
            function playCyberpunkToggle() {
                try {
                    var ctx = getCtx(); var t = ctx.currentTime;
                    var o1 = ctx.createOscillator(), g1 = ctx.createGain();
                    o1.type = 'square';
                    o1.frequency.setValueAtTime(900, t);
                    o1.frequency.setValueAtTime(1400, t + 0.04);
                    g1.gain.setValueAtTime(0.1, t);
                    g1.gain.exponentialRampToValueAtTime(0.001, t + 0.1);
                    o1.connect(g1); g1.connect(ctx.destination);
                    o1.start(t); o1.stop(t + 0.1);
                } catch(e) {}
            }

            // --- SELECT / RADIO : soft sweep tick ---
            function playCyberpunkSelect() {
                try {
                    var ctx = getCtx(); var t = ctx.currentTime;
                    var o1 = ctx.createOscillator(), g1 = ctx.createGain();
                    o1.type = 'triangle';
                    o1.frequency.setValueAtTime(600, t);
                    o1.frequency.exponentialRampToValueAtTime(1000, t + 0.07);
                    g1.gain.setValueAtTime(0.12, t);
                    g1.gain.exponentialRampToValueAtTime(0.001, t + 0.1);
                    o1.connect(g1); g1.connect(ctx.destination);
                    o1.start(t); o1.stop(t + 0.1);
                } catch(e) {}
            }

            // --- SLIDER : tiny tick on input ---
            function playCyberpunkSlider() {
                try {
                    var ctx = getCtx(); var t = ctx.currentTime;
                    var o1 = ctx.createOscillator(), g1 = ctx.createGain();
                    o1.type = 'sine';
                    o1.frequency.setValueAtTime(2000, t);
                    o1.frequency.exponentialRampToValueAtTime(1200, t + 0.03);
                    g1.gain.setValueAtTime(0.07, t);
                    g1.gain.exponentialRampToValueAtTime(0.001, t + 0.04);
                    o1.connect(g1); g1.connect(ctx.destination);
                    o1.start(t); o1.stop(t + 0.04);
                } catch(e) {}
            }

            // --- TEXT INPUT : subtle keystroke hiss ---
            function playCyberpunkKey() {
                try {
                    var ctx = getCtx(); var t = ctx.currentTime;
                    var buf = ctx.createBuffer(1, ctx.sampleRate * 0.03, ctx.sampleRate);
                    var data = buf.getChannelData(0);
                    for (var i = 0; i < data.length; i++) data[i] = (Math.random() * 2 - 1);
                    var src = ctx.createBufferSource();
                    src.buffer = buf;
                    var filt = ctx.createBiquadFilter();
                    filt.type = 'bandpass';
                    filt.frequency.value = 4000;
                    filt.Q.value = 0.8;
                    var g = ctx.createGain();
                    g.gain.setValueAtTime(0.06, t);
                    g.gain.exponentialRampToValueAtTime(0.001, t + 0.03);
                    src.connect(filt); filt.connect(g); g.connect(ctx.destination);
                    src.start(t); src.stop(t + 0.03);
                } catch(e) {}
            }

            // ---- Selectors for each element type ----
            var BTN_SEL      = 'button';
            var NAV_SEL      = '[data-testid="stSidebarNavLink"] a, [data-testid="stSidebarNav"] a, nav a';
            var TOGGLE_SEL   = '[data-testid="stToggle"] input, [data-testid="stCheckbox"] input, [role="switch"]';
            var SELECT_SEL   = '[data-testid="stSelectbox"] *, [data-testid="stRadio"] input, [data-testid="stMultiSelect"] *';
            var SLIDER_SEL   = '[data-testid="stSlider"] input[type="range"]';
            var INPUT_SEL    = 'input[type="text"], input[type="password"], input[type="number"], textarea';

            function bindOne(el, flag, evtType, fn) {
                if (el[flag]) return;
                el[flag] = true;
                el.addEventListener(evtType, fn, { capture: true, passive: true });
            }

            function attachAll(root) {
                root.querySelectorAll(BTN_SEL).forEach(function(el)    { bindOne(el, '_cpBtn',    'click',    playCyberpunkClick);   });
                root.querySelectorAll(NAV_SEL).forEach(function(el)    { bindOne(el, '_cpNav',    'click',    playCyberpunkNav);     });
                root.querySelectorAll(TOGGLE_SEL).forEach(function(el) { bindOne(el, '_cpToggle', 'change',   playCyberpunkToggle);  });
                root.querySelectorAll(SELECT_SEL).forEach(function(el) { bindOne(el, '_cpSelect', 'mousedown',playCyberpunkSelect);  });
                root.querySelectorAll(SLIDER_SEL).forEach(function(el) { bindOne(el, '_cpSlider', 'input',    playCyberpunkSlider);  });
                root.querySelectorAll(INPUT_SEL).forEach(function(el)  { bindOne(el, '_cpKey',    'focus',    playCyberpunkKey);     });
            }

            attachAll(document);

            var observer = new MutationObserver(function(mutations) {
                mutations.forEach(function(m) {
                    m.addedNodes.forEach(function(node) {
                        if (node.nodeType !== 1) return;
                        // Check the node itself
                        if (node.matches && node.matches(BTN_SEL))    { bindOne(node, '_cpBtn',    'click',     playCyberpunkClick);  }
                        if (node.matches && node.matches(NAV_SEL))    { bindOne(node, '_cpNav',    'click',     playCyberpunkNav);    }
                        if (node.matches && node.matches(TOGGLE_SEL)) { bindOne(node, '_cpToggle', 'change',    playCyberpunkToggle); }
                        if (node.matches && node.matches(SLIDER_SEL)) { bindOne(node, '_cpSlider', 'input',     playCyberpunkSlider); }
                        if (node.matches && node.matches(INPUT_SEL))  { bindOne(node, '_cpKey',    'focus',     playCyberpunkKey);    }
                        // Check descendants
                        attachAll(node);
                    });
                });
            });
            observer.observe(document.body, { childList: true, subtree: true });
        })();
        </script>
        """,
        unsafe_allow_html=True,
    )
