# app.py
import datetime
import streamlit as st
from validation import validate_inputs
from pipeline   import run_pipeline
from utils      import get_extension

st.set_page_config(page_title="GNSS Processing Panel", page_icon="🛰️", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=Inter:wght@400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; }

.stApp {
    background: #111827;
    font-family: 'Inter', sans-serif;
}
.block-container {
    padding: 1.6rem 2rem 3rem !important;
    max-width: 1360px !important;
}
.stApp > header, footer { display: none !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #1f2937; }
::-webkit-scrollbar-thumb { background: #374151; border-radius: 4px; }

/* ══════════════════════════
   HEADER
══════════════════════════ */
.gnss-header {
    display: flex; align-items: center; gap: 14px;
    margin-bottom: 1.6rem;
    padding-bottom: 1.2rem;
    border-bottom: 1px solid #1f2937;
}
.gnss-logo {
    width: 44px; height: 44px;
    background: #1d4ed8;
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 22px; flex-shrink: 0;
}
.gnss-title {
    font-size: 20px; font-weight: 600;
    color: #f9fafb; letter-spacing: -0.3px;
}
.gnss-sub {
    font-size: 12px; color: #6b7280;
    font-family: 'IBM Plex Mono', monospace;
    letter-spacing: 0.4px; margin-top: 2px;
}
.gnss-badge {
    margin-left: auto;
    display: flex; align-items: center; gap: 7px;
    background: #064e3b;
    border: 1px solid #065f46;
    border-radius: 20px;
    padding: 6px 14px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px; letter-spacing: 0.6px;
    color: #34d399; flex-shrink: 0;
}
.pulse {
    width: 7px; height: 7px; border-radius: 50%;
    background: #34d399;
    animation: blink 2s ease-in-out infinite;
    flex-shrink: 0;
}
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:.3} }

/* ══════════════════════════
   PANELS
══════════════════════════ */
.panel {
    background: #1f2937;
    border: 1px solid #374151;
    border-radius: 12px;
    padding: 20px 20px 24px;
}
.panel-hd {
    display: flex; align-items: center; gap: 8px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px; font-weight: 600;
    letter-spacing: 1.5px; text-transform: uppercase;
    color: #9ca3af; margin-bottom: 18px;
}
.panel-hd::after {
    content: ''; flex: 1; height: 1px;
    background: #374151;
}
.panel-dot {
    width: 7px; height: 7px; border-radius: 50%;
    background: #3b82f6; flex-shrink: 0;
}

/* ══════════════════════════
   LABELS  — highly visible
══════════════════════════ */
.stTextInput  > label,
.stDateInput  > label,
.stFileUploader > label {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size:   12px  !important;
    font-weight: 600   !important;
    color:       #d1d5db !important;
    letter-spacing: 0.6px !important;
    text-transform: uppercase !important;
    margin-bottom: 6px !important;
    display: block !important;
}

/* ══════════════════════════
   TEXT INPUT
══════════════════════════ */
.stTextInput input {
    background:    #111827 !important;
    color:         #f3f4f6 !important;
    border:        1px solid #4b5563 !important;
    border-radius: 8px !important;
    font-family:   'IBM Plex Mono', monospace !important;
    font-size:     14px !important;
    padding:       10px 14px !important;
    transition:    border-color .15s !important;
    caret-color:   #60a5fa !important;
    box-shadow:    none !important;
    outline:       none !important;
}
.stTextInput input:focus {
    border-color: #3b82f6 !important;
    box-shadow:   0 0 0 2px rgba(59,130,246,0.2) !important;
    outline: none !important;
}
.stTextInput input::placeholder { color: #4b5563 !important; }

/* kill Streamlit's red outline on empty required fields */
.stTextInput input:invalid,
.stTextInput input[aria-invalid] {
    border-color: #4b5563 !important;
    box-shadow: none !important;
}

/* ══════════════════════════
   DATE INPUT
══════════════════════════ */
.stDateInput input {
    background:    #111827 !important;
    color:         #f3f4f6 !important;
    border:        1px solid #4b5563 !important;
    border-radius: 8px !important;
    font-family:   'IBM Plex Mono', monospace !important;
    font-size:     14px !important;
    padding:       10px 14px !important;
    box-shadow:    none !important;
    outline:       none !important;
}
.stDateInput input:focus {
    border-color: #3b82f6 !important;
    box-shadow:   0 0 0 2px rgba(59,130,246,0.2) !important;
    outline: none !important;
}

/* ══════════════════════════
   FILE UPLOADER
══════════════════════════ */
div[data-testid="stFileUploader"] {
    background:    #111827 !important;
    border:        1.5px dashed #4b5563 !important;
    border-radius: 10px !important;
    transition: border-color .2s, background .2s !important;
}
div[data-testid="stFileUploader"]:hover {
    border-color: #3b82f6 !important;
    background:   #161e2e !important;
}
div[data-testid="stFileUploader"] small,
div[data-testid="stFileUploader"] span,
div[data-testid="stFileUploader"] p {
    color: #6b7280 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 12px !important;
}
div[data-testid="stFileUploader"] button {
    background: #1f2937 !important;
    color: #d1d5db !important;
    border: 1px solid #4b5563 !important;
    border-radius: 6px !important;
    font-size: 12px !important;
}
div[data-testid="stFileUploader"] svg { fill: #6b7280 !important; }

/* ══════════════════════════
   RUN BUTTON
══════════════════════════ */
.stButton > button {
    width: 100% !important;
    background:    #1d4ed8 !important;
    color:         #eff6ff !important;
    border:        1px solid #2563eb !important;
    border-radius: 8px !important;
    padding:       12px 20px !important;
    font-family:   'IBM Plex Mono', monospace !important;
    font-size:     12px !important;
    font-weight:   600 !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
    transition:    all .15s !important;
    box-shadow:    none !important;
}
.stButton > button:hover {
    background:   #2563eb !important;
    border-color: #3b82f6 !important;
    transform:    translateY(-1px) !important;
    box-shadow:   0 4px 12px rgba(37,99,235,0.35) !important;
}
.stButton > button:active { transform: translateY(0) !important; }
.stButton > button:focus  { box-shadow: 0 0 0 2px rgba(59,130,246,0.4) !important; outline: none !important; }

/* ══════════════════════════
   PROGRESS BAR
══════════════════════════ */
div[data-testid="stProgressBar"] > div {
    background: #1f2937 !important;
    border-radius: 4px !important;
    height: 6px !important;
}
div[data-testid="stProgressBar"] > div > div {
    background: linear-gradient(90deg, #2563eb, #34d399) !important;
    border-radius: 4px !important;
}

/* ══════════════════════════
   METRIC STRIP
══════════════════════════ */
.metric-strip { display: flex; gap: 8px; margin: 14px 0; }
.m-box {
    flex: 1;
    background: #111827;
    border: 1px solid #374151;
    border-radius: 8px;
    padding: 10px 12px;
}
.m-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 9px; letter-spacing: 1.2px;
    text-transform: uppercase;
    color: #6b7280; margin-bottom: 5px;
}
.m-val {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 14px; font-weight: 600; color: #9ca3af;
}
.m-val.hi { color: #34d399; }

/* ══════════════════════════
   DIVIDER
══════════════════════════ */
.div-line { height: 1px; background: #374151; margin: 14px 0; }

/* ══════════════════════════
   CONSOLE
══════════════════════════ */
.console-wrap {
    background: #0d1117;
    border: 1px solid #21262d;
    border-radius: 10px;
    padding: 14px 16px;
    min-height: 360px; max-height: 440px;
    overflow-y: auto;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 12px; line-height: 1.85;
    letter-spacing: 0.2px;
}
.cl { display: flex; gap: 14px; align-items: baseline; }
.cl-ts   { color: #30363d; min-width: 92px; flex-shrink: 0; }
.cl-sep  { color: #21262d; }
.cl-ok   { color: #3fb950; }
.cl-info { color: #58a6ff; }
.cl-warn { color: #d29922; }
.cl-done { color: #a371f7; }
.cl-mute { color: #30363d; }

/* ══════════════════════════
   STEP STATUS LABEL
══════════════════════════ */
p[style*="color:#2563eb"] {
    color: #60a5fa !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 12px !important;
}
</style>
""", unsafe_allow_html=True)

# ── HEADER ──────────────────────────────────────────────────────────
st.markdown("""
<div class="gnss-header">
    <div class="gnss-logo">🛰️</div>
    <div>
        <div class="gnss-title">GNSS Processing Panel</div>
        <div class="gnss-sub">PPK / RTK / PPP  ·  PIPELINE v2.4.1</div>
    </div>
    <div class="gnss-badge">
        <div class="pulse"></div>SYSTEM READY
    </div>
</div>
""", unsafe_allow_html=True)

# ── LAYOUT ──────────────────────────────────────────────────────────
left, right = st.columns([1, 1.65], gap="large")

# ═══════════════════════════════
# LEFT — INPUT PANEL
# ═══════════════════════════════
with left:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-hd"><div class="panel-dot"></div>Input Configuration</div>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Observation File",
        type=None,
        help="Upload any GNSS observation file (RINEX, UBX, BIN, OBS, NAV, etc.)",
    )

    st.markdown('<div class="div-line"></div>', unsafe_allow_html=True)

    station_name = st.text_input("Station Identifier", placeholder="e.g. PUNE", max_chars=10)
    station_name = station_name.strip().upper() if station_name else ""

    obs_date = st.date_input("Observation Date", value=datetime.date.today(), max_value=datetime.date.today())

    st.markdown('<div class="div-line"></div>', unsafe_allow_html=True)

    # live mini metrics
    file_label = get_extension(uploaded_file.name) if uploaded_file else "—"
    file_cls   = "hi" if uploaded_file else ""

    st.markdown(f"""
    <div class="metric-strip">
        <div class="m-box">
            <div class="m-label">Station</div>
            <div class="m-val {'hi' if station_name else ''}">{station_name or '—'}</div>
        </div>
        <div class="m-box">
            <div class="m-label">Date</div>
            <div class="m-val">{obs_date.strftime('%d %b %Y')}</div>
        </div>
        <div class="m-box">
            <div class="m-label">File</div>
            <div class="m-val {file_cls}">{file_label}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    run_clicked = st.button("▶  Run Processing Pipeline")
    st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════
# RIGHT — OUTPUT PANEL
# ═══════════════════════════════
with right:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-hd"><div class="panel-dot"></div>Processing Console</div>', unsafe_allow_html=True)

    console_slot  = st.empty()
    progress_slot = st.empty()
    status_slot   = st.empty()
    alert_slot    = st.empty()

    st.markdown('</div>', unsafe_allow_html=True)

# ── CONSOLE RENDERER ────────────────────────────────────────────────
def render_console(log_tuples: list):
    rows = []
    for style, ts, msg in log_tuples:
        if style == "sep":
            rows.append(f"<div class='cl'><span class='cl-sep'>{msg}</span></div>")
        else:
            rows.append(
                f"<div class='cl'>"
                f"<span class='cl-ts'>{ts}</span>"
                f"<span class='cl-{style}'>{msg}</span>"
                f"</div>"
            )
    console_slot.markdown(
        "<div class='console-wrap'>" + "".join(rows) + "</div>",
        unsafe_allow_html=True,
    )

# ── IDLE STATE ───────────────────────────────────────────────────────
if not run_clicked:
    console_slot.markdown("""
    <div class='console-wrap'>
        <div class='cl'><span class='cl-ts'>--:--.---</span><span class='cl-mute'>Awaiting input configuration…</span></div>
        <div class='cl'><span class='cl-ts'>--:--.---</span><span class='cl-mute'>Upload a GNSS file and enter a station ID, then click Run.</span></div>
    </div>
    """, unsafe_allow_html=True)

# ── RUN PIPELINE ─────────────────────────────────────────────────────
if run_clicked:
    errors = validate_inputs(uploaded_file, station_name, obs_date)

    if errors:
        for err in errors:
            alert_slot.error(f"⚠  {err}")
        render_console([
            ("warn", "", f"Validation failed ({len(errors)} error{'s' if len(errors) > 1 else ''}) — fix inputs and retry.")
        ])
    else:
        progress_bar = progress_slot.progress(0)
        status_label = status_slot.empty()

        logs = run_pipeline(
            uploaded_file=uploaded_file,
            station_name=station_name,
            obs_date=obs_date,
            progress_bar=progress_bar,
            status_label=status_label,
        )

        render_console(logs)
        status_label.empty()
        alert_slot.success("✔  Pipeline executed successfully — all steps completed.")