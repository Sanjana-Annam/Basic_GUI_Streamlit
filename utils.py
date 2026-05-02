# utils.py
# --------
# Small helper functions used across the app.
# No Streamlit imports here — pure Python only.

import datetime


def format_file_size(size_bytes: int) -> str:
    """
    Convert a byte count into a readable string.
    Examples: 512 → "512 B",  2048 → "2.0 KB",  1500000 → "1.43 MB"
    """
    if size_bytes < 1_024:
        return f"{size_bytes} B"
    elif size_bytes < 1_024 ** 2:
        return f"{size_bytes / 1_024:.1f} KB"
    else:
        return f"{size_bytes / 1_024 ** 2:.2f} MB"


def get_extension(filename: str) -> str:
    """
    Return the uppercase file extension.
    Example: "data.rnx" → "RNX"
    """
    if "." in filename:
        return filename.rsplit(".", 1)[-1].upper()
    return "UNKNOWN"


def current_timestamp() -> str:
    """
    Return the current time as a log-friendly string.
    Example: "14:35:22.413"
    """
    return datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
