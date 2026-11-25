"""Home page - UI only."""
import pandas as pd
import streamlit as st

from services.i18n import tr
from services.ui_helpers import chunks, ensure_main

ensure_main(__file__)  # opened before main.py ran? go through main.py so the normal menu shows
lang = st.session_state.get("lang", "th")
T = lambda key, **kw: tr(lang, key, **kw)  # noqa: E731

st.title(T("home_title"))
st.markdown(f"#### {T('home_tagline')}")

# ---- 1. Project name ------------------------------------------------------------
st.subheader(f"🏷️ {T('home_name_h')}")
with st.container(border=True):
    for label, value in T("home_name_rows"):
        a, b = st.columns([1, 3])
        a.markdown(f"**{label}**")
        b.markdown(value)

# ---- 2. System overview ---------------------------------------------------------
st.subheader(f"🧭 {T('home_overview_h')}")
st.markdown(T("home_overview"))
st.info(T("home_flow"))
m = st.columns(3)
m[0].metric(T("home_m_apps"), 6)
m[1].metric(T("home_m_services"), 6)
m[2].metric(T("home_m_data"), 3)

# ---- 3. Main menu ---------------------------------------------------------------
st.subheader(f"📋 {T('home_menu_h')}")
st.caption(T("home_menu_hint"))
PATHS = ["pages/statistics.py", "pages/bayes.py", "pages/markov.py",
         "pages/display_data.py", "pages/custom_app.py", "pages/members.py"]
apps = T("home_apps")
for path_row, app_row in zip(chunks(PATHS, 3), chunks(apps, 3)):
    cols = st.columns(3)
    for col, path, app in zip(cols, path_row, app_row):
        name, _, _, concept, what = app
        with col.container(border=True, height="stretch"):
            st.markdown(f"#### {name}")
            st.caption(what)
            st.page_link(path, label=T("home_open"), icon="➡️")

# ---- 4. Summary table -----------------------------------------------------------
st.subheader(f"🗒️ {T('home_table_h')}")
st.dataframe(pd.DataFrame(apps, columns=T("home_cols")), hide_index=True, width="stretch")

# ---- 5. Project structure -------------------------------------------------------
with st.expander(f"📁 {T('home_struct_h')}"):
    st.code(
        """sec227C-1-project/
├── main.py              # routing
├── data/                # raw data (.json, images)
│   ├── imgs/
│   ├── raw_data.json
│   ├── students.json
│   └── members.json
├── pages/               # UI only
│   ├── home.py  statistics.py  bayes.py  markov.py
│   └── display_data.py  custom_app.py  members.py
└── services/            # all calculations
    ├── cal_statistics.py  cal_mode.py  cal_bayes.py
    ├── text_prediction.py  data_loader.py
    ├── custom_service.py  ui_helpers.py
    └── i18n.py          # EN / TH text""",
        language="text",
    )
