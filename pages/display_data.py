"""Raw data viewer - UI only. Reading/summarising: services/data_loader.py"""
import altair as alt
import pandas as pd
import streamlit as st

from services.data_loader import (
    corpus_summary, corpus_table, filter_students, grade_counts, list_data_files, load_members,
    load_raw_data, load_students, numeric_summary, word_frequency,
)
from services.i18n import tr
from services.ui_helpers import ensure_main

ensure_main(__file__)  # opened before main.py ran? go through main.py so the normal menu shows
lang = st.session_state.get("lang", "th")
T = lambda key, **kw: tr(lang, key, **kw)  # noqa: E731

st.title(T("dd_title"))
st.caption(T("dd_caption"))

st.dataframe(pd.DataFrame(list_data_files()), hide_index=True, width="stretch")

tab_text, tab_students, tab_members = st.tabs(["raw_data.json", "students.json", "members.json"])

with tab_text:
    raw = load_raw_data()
    st.markdown(f"_{raw['description']}_")
    st.dataframe(pd.DataFrame(corpus_summary(raw)), hide_index=True, width="stretch")

    key = st.selectbox(T("dd_dataset"), list(raw["datasets"]), format_func=lambda k: raw["datasets"][k]["title"])
    left, right = st.columns([3, 2])
    with left:
        st.dataframe(pd.DataFrame(corpus_table(raw, key)), hide_index=True,
                     width="stretch")
    with right:
        wf = pd.DataFrame(word_frequency(raw, key))
        st.altair_chart(
            alt.Chart(wf).mark_bar(color="#6366F1", cornerRadiusEnd=4).encode(
                x="count:Q", y=alt.Y("word:N", sort="-x", title=None), tooltip=["word", "count"]
            ).properties(title=T("dd_topwords"), height=380),
            width="stretch",
        )
    with st.expander(T("dd_rawjson")):
        st.json(raw, expanded=1)

with tab_students:
    students = load_students()
    st.markdown(T("dd_students", n=len(students)))
    left, right = st.columns([2, 1])
    with left:
        st.dataframe(pd.DataFrame(numeric_summary(students)), hide_index=True, width="stretch")
    with right:
        gc = pd.DataFrame(grade_counts(students))
        st.altair_chart(
            alt.Chart(gc).mark_bar(color="#10B981", cornerRadiusEnd=4).encode(
                x=alt.X("grade:N", sort=None, axis=alt.Axis(labelAngle=0)), y="students:Q",
                tooltip=["grade", "students"],
            ).properties(height=220),
            width="stretch",
        )
    grade_filter = st.multiselect(T("dd_filter"), list("ABCDF"), default=list("ABCDF"))
    st.dataframe(pd.DataFrame(filter_students(students, grade_filter)), hide_index=True,
                 width="stretch", height=320)

with tab_members:
    st.json(load_members())
