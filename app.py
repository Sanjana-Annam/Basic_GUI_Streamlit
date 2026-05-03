import datetime
import streamlit as st
from validation import validate_inputs
from pipeline import run_pipeline
from utils import get_extension

st.set_page_config(page_title="GNSS Processing Panel", page_icon="🛰️", layout="wide")

# ── STYLES ──────────────────────────────────────────────────────────
st.markdown("""
<style>
.stApp {
    background: #111827;
    font-family: 'Inter', sans-serif;
}

/* Header */
.gnss-title {
    font-size: 22px !important;
    color: #f9fafb;
    white-space: nowrap;
}

/* Panels */
.panel {
    background: #1f2937;
    border-radius: 12px;
    padding: 20px;
}

/* Labels */
label {
    color: #d1d5db !important;
    font-size: 12px !important;
    text-transform: uppercase;
}

/* Inputs */
.stTextInput input {
    background: #111827 !important;
    color: #ffffff !important;
    border: 1px solid #4b5563 !important;
}

/* File uploader */
div[data-testid="stFileUploader"] {
    background: #111827 !important;
    border: 1.5px dashed #4b5563 !important;
    border-radius: 10px !important;
    padding: 20px !important;
}

/* Remove duplicate uploader UI */
div[data-testid="stFileUploader"] > div:nth-child(2) {
    display: none !important;
}

/* Button */
.stButton > button {
    background: #2563eb !important;
    color: white !important;
    border-radius: 8px !important;
    padding: 10px;
    font-weight: 600;
}

/* Console */
.console {
    background: #0d1117;
    border-radius: 10px;
    padding: 20px;
    min-height: 250px;
    color: #d1d5db;
    font-family: monospace;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

# ── HEADER ──────────────────────────────────────────────────────────
st.markdown("<h2 class='gnss-title'>🛰️ GNSS Processing Panel</h2>", unsafe_allow_html=True)

# ── LAYOUT ──────────────────────────────────────────────────────────
left, right = st.columns([1, 1.6])

# ── LEFT PANEL ──────────────────────────────────────────────────────
with left:
    st.markdown('<div class="panel">', unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Observation File")

    station_name = st.text_input("Station Identifier", placeholder="e.g. PUNE")
    station_name = station_name.strip().upper() if station_name else ""

    obs_date = st.date_input("Observation Date", value=datetime.date.today())

    file_label = get_extension(uploaded_file.name) if uploaded_file else "—"

    st.write(f"**Station:** {station_name or '—'}")
    st.write(f"**Date:** {obs_date.strftime('%d %b %Y')}")
    st.write(f"**File:** {file_label}")

    run_clicked = st.button("🚀 Run Processing")

    st.markdown('</div>', unsafe_allow_html=True)

# ── RIGHT PANEL ─────────────────────────────────────────────────────
with right:
    st.markdown('<div class="panel">', unsafe_allow_html=True)

    console = st.empty()
    progress_slot = st.empty()
    status_slot = st.empty()
    alert = st.empty()

    st.markdown('</div>', unsafe_allow_html=True)

# ── DEFAULT STATE ───────────────────────────────────────────────────
if not run_clicked:
    console.markdown("""
    <div class="console">
    Awaiting input... Upload file and click Run.
    </div>
    """, unsafe_allow_html=True)

# ── RUN PIPELINE ────────────────────────────────────────────────────
if run_clicked:
    errors = validate_inputs(uploaded_file, station_name, obs_date)

    if errors:
        for e in errors:
            alert.error(e)

    else:
        progress_bar = progress_slot.progress(0)
        status_label = status_slot.empty()

        logs = run_pipeline(
            uploaded_file,
            station_name,
            obs_date,
            progress_bar,
            status_label
        )

        # ── CLEAN SUMMARY OUTPUT ─────────────────────────────
        file_name = uploaded_file.name if uploaded_file else "—"
        station = station_name or "—"
        date_str = obs_date.strftime("%d %b %Y")

        status = "SUCCESS" if any("COMPLETE" in str(l) for l in logs) else "FAILED"

        console.markdown(f"""
        <div class='console'>
        <b>📂 File:</b> {file_name}<br><br>
        <b>📡 Station:</b> {station}<br><br>
        <b>📅 Date:</b> {date_str}<br><br>
        <b>🚀 Status:</b> <span style='color:#34d399'>{status}</span>
        </div>
        """, unsafe_allow_html=True)

        status_label.empty()
        alert.success("✔ Processing completed successfully")