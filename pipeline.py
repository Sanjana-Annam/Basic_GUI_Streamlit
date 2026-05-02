# pipeline.py
# -----------
# Simulates a GNSS Precise Point Positioning (PPP) pipeline.
# Each step updates the UI progress bar and adds lines to the log.
#
# To connect to a real GNSS engine later, replace each step's
# time.sleep() block with actual computation calls.

import time
import random
import datetime

from utils import current_timestamp, format_file_size


def run_pipeline(uploaded_file, station_name: str, obs_date: datetime.date,
                 progress_bar, status_label) -> list:
    """
    Run the 10-step simulated pipeline.

    Parameters
    ----------
    uploaded_file : Streamlit UploadedFile object
    station_name  : str  — e.g. "PUNE"
    obs_date      : datetime.date
    progress_bar  : st.progress widget  — updated at each step
    status_label  : st.empty widget     — shows the current step name

    Returns
    -------
    List of (style, timestamp, message) tuples for the log console.
    style values: "ok" | "info" | "warn" | "done" | "sep"
    """

    logs = []
    STEPS = 10  # total number of steps (used for % calculation)

    def step(number: int, label: str):
        """Advance the progress bar and update the status text."""
        progress_bar.progress(int(number / STEPS * 100))
        status_label.markdown(
            f'<p style="font-size:13px; color:#2563eb; margin:6px 0 0 0;">'
            f'⟳ &nbsp; Step {number}/{STEPS} — {label}</p>',
            unsafe_allow_html=True,
        )

    def log(style: str, message: str):
        """Append a single log line with the current timestamp."""
        logs.append((style, current_timestamp(), message))

    # ── Step 1 : Load file ──────────────────────────────────────────────
    step(1, "Loading file")
    time.sleep(0.5)

    file_size = format_file_size(uploaded_file.size)
    log("sep",  "─" * 52)
    log("info", "GNSS PROCESSING PIPELINE   v2.4.1")
    log("sep",  "─" * 52)
    log("ok",   f"[FILE]          {uploaded_file.name}  ({file_size})")
    log("info", f"[STATION]       {station_name.upper()}")
    log("info", f"[DATE]          {obs_date.strftime('%d %b %Y')}")

    # ── Step 2 : Validate ───────────────────────────────────────────────
    step(2, "Validating inputs")
    time.sleep(0.4)
    log("ok", "[VALIDATE]      All inputs passed — OK")

    # ── Step 3 : Parse file header ──────────────────────────────────────
    step(3, "Parsing file header")
    time.sleep(0.5)

    rinex_version = random.choice(["3.03", "3.04", "2.11"])
    receiver      = random.choice(["TRIMBLE NETR9", "LEICA GR50", "JAVAD TRE-G3T"])
    antenna       = random.choice(["TRM59900.00", "LEIAR25.R4", "JAV_RINGANT_G3T"])
    log("ok", f"[HEADER]        RINEX v{rinex_version}  |  Rcvr: {receiver}")
    log("ok", f"[ANTENNA]       {antenna}")

    # ── Step 4 : Detect satellites ──────────────────────────────────────
    step(4, "Detecting visible satellites")
    time.sleep(0.7)

    gps = random.randint(8, 12)
    glo = random.randint(5, 9)
    gal = random.randint(6, 10)
    bds = random.randint(4, 8)
    log("ok", f"[SATELLITES]    Total: {gps+glo+gal+bds}  |  GPS:{gps}  GLO:{glo}  GAL:{gal}  BDS:{bds}")

    # ── Step 5 : Apply corrections ──────────────────────────────────────
    step(5, "Applying corrections")
    time.sleep(0.8)
    log("info", "[CORRECTIONS]   Cycle slip detection … done")
    log("info", "[CORRECTIONS]   Multipath mitigation … done")
    log("info", "[CORRECTIONS]   Troposphere model (VMF3) applied")
    log("info", "[CORRECTIONS]   Ionosphere delay estimated (IONEX)")

    # ── Step 6 : Load orbit & clock products ────────────────────────────
    step(6, "Loading orbit & clock products")
    time.sleep(0.6)

    source = random.choice(["IGS Final", "IGS Rapid", "CODE Final", "JPL Final"])
    log("ok", f"[ORBIT/CLOCK]   Source: {source} — interpolated OK")

    # ── Step 7 : Estimate position ──────────────────────────────────────
    step(7, "Estimating position (PPP)")
    time.sleep(1.0)

    lat  = round(random.uniform(18.0, 28.0), 6)
    lon  = round(random.uniform(73.0, 85.0), 6)
    alt  = round(random.uniform(450.0, 800.0), 3)
    pdop = round(random.uniform(1.2, 2.8), 2)
    log("ok", f"[POSITION]      Lat: {lat}°N   Lon: {lon}°E   Alt: {alt} m")
    log("ok", f"[DOP]           PDOP: {pdop}   HDOP: {round(pdop*0.7,2)}   VDOP: {round(pdop*0.9,2)}")

    # ── Step 8 : Quality control ─────────────────────────────────────────
    step(8, "Quality control")
    time.sleep(0.6)

    obs_count  = random.randint(8_400, 14_400)
    rejected   = round(random.uniform(0.5, 3.5), 1)
    rms_h      = round(random.uniform(2.1, 9.8), 1)
    rms_v      = round(random.uniform(4.2, 14.5), 1)
    log("ok", f"[QC]            Observations: {obs_count:,}   Rejected: {rejected}%")
    log("ok", f"[ACCURACY]      RMS Horizontal: {rms_h} mm   RMS Vertical: {rms_v} mm")

    # ── Step 9 : Export results ──────────────────────────────────────────
    step(9, "Exporting results")
    time.sleep(0.5)
    log("info", "[EXPORT]        Summary report … OK")
    log("info", "[EXPORT]        Coordinate time-series … OK")
    log("info", "[EXPORT]        Residuals plot … OK")

    # ── Step 10 : Done ────────────────────────────────────────────────────
    step(10, "Done")
    time.sleep(0.3)

    elapsed = round(random.uniform(4.8, 7.2), 2)
    log("sep",  "─" * 52)
    log("done", f"[COMPLETE]      Finished in {elapsed}s  —  status: SUCCESS")
    log("sep",  "─" * 52)

    return logs
