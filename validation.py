# validation.py
# -------------
# All input validation logic lives here.
# Returns plain error strings — no UI code in this file.

import datetime


def validate_inputs(uploaded_file, station_name: str, obs_date: datetime.date) -> list:
    """
    Check all three user inputs.

    Returns a list of error messages.
    If the list is empty, all inputs are valid and processing can start.

    Rules
    -----
    1. A file must be uploaded.
    2. Station name must not be blank.
    3. Observation date must not be in the future.
    """
    errors = []

    # Rule 1 — file required
    if uploaded_file is None:
        errors.append("No file uploaded. Please select a GNSS data file.")

    # Rule 2 — station name required
    if not station_name or station_name.strip() == "":
        errors.append("Station name is empty. Please enter a station name (e.g. PUNE).")

    # Rule 3 — date must not be in the future
    if obs_date > datetime.date.today():
        errors.append(
            f"Date '{obs_date}' is in the future. Please choose today or an earlier date."
        )

    return errors
