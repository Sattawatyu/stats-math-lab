"""Descriptive statistics - UI only. Calculations: services/cal_statistics.py, services/cal_mode.py"""
import altair as alt
import pandas as pd
import streamlit as st

from services.cal_statistics import chart_points, parse_numbers, reference_lines, summarize
from services.i18n import tr
from services.ui_helpers import ensure_main

ensure_main(__file__)  # opened before main.py ran? go through main.py so the normal menu shows
lang = st.session_state.get("lang", "th")
T = lambda key, **kw: tr(lang, key, **kw)  # noqa: E731

st.title(T("st_title"))
st.caption(T("st_caption"))

EXAMPLES = {
    "ex_teacher": "-100, 0, 10, 20, 30, 100",
    "ex_scores": "55, 62, 68, 70, 70, 74, 78, 81, 85, 92",
    "ex_bimodal": "1, 2, 2, 3, 4, 4, 5",
}
choice = st.pills(T("st_examples"), list(EXAMPLES), default="ex_teacher", format_func=T)
text = st.text_area(T("st_data"), value=EXAMPLES.get(choice, ""), height=90)
sample = st.radio(T("st_kind"), [False, True], horizontal=True,
                  format_func=lambda s: T("st_sample") if s else T("st_pop"))

try:
    data = parse_numbers(text, lang)
    r = summarize(data, sample=sample, lang=lang)
except ValueError as e:
    st.error(str(e))
    st.stop()

fmt = lambda v: f"{v:,.4f}".rstrip("0").rstrip(".")  # noqa: E731

c = st.columns(5)
c[0].metric(T("m_mean"), fmt(r["mean"]))
c[1].metric(T("m_median"), fmt(r["median"]))
c[2].metric(T("m_mode"), ", ".join(fmt(m) for m in r["mode"]) if r["mode"] else T("m_nomode"),
            help=T("m_nomode_help"))
c[3].metric(T("m_sd"), fmt(r["sd"]))
c[4].metric(T("m_var"), fmt(r["variance"]))

c = st.columns(5)
c[0].metric(T("m_n"), r["n"])
c[1].metric(T("m_sum"), fmt(r["sum"]))
c[2].metric(T("m_min"), fmt(r["min"]))
c[3].metric(T("m_max"), fmt(r["max"]))
c[4].metric(T("m_range"), fmt(r["range"]))

tab_chart, tab_steps, tab_freq = st.tabs([T("tab_chart"), T("tab_steps"), T("tab_freq")])

with tab_chart:
    df = pd.DataFrame(chart_points(data))
    points = alt.Chart(df).mark_circle(size=120, color="#6366F1").encode(
        x=alt.X("value:Q", title=T("ax_value")),
        y=alt.Y("index:O", title=T("ax_point")),
        tooltip=["value"],
    )
    lines = pd.DataFrame(reference_lines(r))
    rules = alt.Chart(lines).mark_rule(strokeWidth=2).encode(
        x="value:Q",
        color=alt.Color("stat:N", scale=alt.Scale(range=["#EF4444", "#10B981", "#9CA3AF", "#9CA3AF"])),
        strokeDash=alt.condition(alt.datum.stat == "Mean", alt.value([1, 0]), alt.value([5, 4])),
        tooltip=["stat", "value"],
    )
    st.altair_chart(points + rules, width="stretch")

with tab_steps:
    n_div = "n − 1" if sample else "n"
    st.latex(r"\bar{x} = \frac{\sum x}{n} = \frac{%s}{%d} = %s" % (fmt(r["sum"]), r["n"], fmt(r["mean"])))
    st.dataframe(pd.DataFrame(r["deviations"]), hide_index=True, width="stretch")
    st.latex(r"\text{Variance} = \frac{\sum (x-\bar{x})^2}{%s} = \frac{%s}{%s} = %s"
             % (n_div, fmt(r["sum_sq"]), r["divisor"], fmt(r["variance"])))
    st.latex(r"SD = \sqrt{\text{Variance}} = %s" % fmt(r["sd"]))
    st.markdown(T("st_sorted", d=", ".join(fmt(x) for x in r["sorted"]), m=fmt(r["median"])))

with tab_freq:
    freq = pd.DataFrame({T("col_value"): list(r["frequency"].keys()),
                         T("col_count"): list(r["frequency"].values())})
    st.dataframe(freq, hide_index=True, width="stretch")
