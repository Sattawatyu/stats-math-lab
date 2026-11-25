"""Small helpers for page layout and access, kept out of pages/ (pages are UI only)."""
import os
from pathlib import Path

import streamlit as st

LOCAL_HOSTS = {"localhost", "127.0.0.1", "[::1]", "::1"}


def editing_allowed(host_header: str | None) -> bool:
    """The text editor is only for the team's own computer.

    On the public site (Streamlit Cloud) anyone could change the text for every
    visitor, so the editor is shown only when the app is opened on localhost.
    Set CS207_ALLOW_EDIT=1 to allow it elsewhere.
    """
    if os.environ.get("CS207_ALLOW_EDIT") == "1":
        return True
    host = (host_header or "").strip().lower()
    if host.startswith("["):  # IPv6 like [::1]:8501
        host = host.split("]")[0] + "]"
    else:
        host = host.split(":")[0]
    return host in LOCAL_HOSTS


def chunks(items: list, size: int) -> list[list]:
    """Split a list into rows of `size` items (for card grids)."""
    return [items[i:i + size] for i in range(0, len(items), size)]


def chart_height(n_rows: int, per_row: int, padding: int = 0) -> int:
    """Height in pixels for a chart with one band per row."""
    return per_row * n_rows + padding


def ensure_main(page_file: str) -> None:
    """Make every page go through main.py.

    Right after the server starts, a link like /members can run pages/members.py
    on its own (Streamlit's old pages/ folder mode), which shows a plain list of
    file names instead of our menu. main.py always sets `lang` first, so if it is
    missing we jump to main.py and let it open the page that was asked for.
    """
    if "lang" not in st.session_state:
        st.session_state.goto_page = Path(page_file).stem
        st.switch_page("main.py")
