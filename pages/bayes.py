"""Bayes' theorem - UI only. Calculations: services/cal_bayes.py"""
import altair as alt
import pandas as pd
import streamlit as st

from services.cal_bayes import PRESETS, frequency_view, interpret, posterior, total_probability
from services.i18n import tr
from services.ui_helpers import ensure_main

ensure_main(__file__)  # opened before main.py ran? go through main.py so the normal menu shows
lang = st.session_state.get("lang", "th")
T = lambda key, **kw: tr(lang, key, **kw)  # noqa: E731

st.title(T("by_title"))
st.latex(r"P(A\mid B) = \frac{P(B\mid A)\,P(A)}{P(B)}")

preset = st.selectbox(T("by_scenario"), ["custom"] + list(PRESETS),
                      format_func=lambda k: T("by_custom") if k == "custom" else PRESETS[k]["title"][lang])
if preset == "custom":
    p = {"prior": 0.30, "likelihood": 0.70, "false_rate": 0.20}
    st.info(T("by_custom_desc"))
else:
    p = PRESETS[preset]
    st.info(p["desc"][lang])

direct = st.radio(T("by_mode"), [False, True], horizontal=True,
                  format_func=lambda d: T("by_direct") if d else T("by_total"))

c1, c2, c3 = st.columns(3)
prior = c1.number_input(T("by_prior"), 0.0, 1.0, p["prior"], 0.01, format="%.4f", key=f"prior_{preset}")
likelihood = c2.number_input(T("by_lik"), 0.0, 1.0, p["likelihood"], 0.01, format="%.4f", key=f"lik_{preset}")

try:
    if direct:
        default_e = total_probability(p["prior"], p["likelihood"], p["false_rate"], lang)
        evidence = c3.number_input(T("by_ev"), 0.0, 1.0, default_e, 0.01, format="%.4f", key=f"ev_{preset}")
    else:
        false_rate = c3.number_input(T("by_false"), 0.0, 1.0, p["false_rate"], 0.01, format="%.4f", key=f"fr_{preset}")
        evidence = total_probability(prior, likelihood, false_rate, lang)
        st.latex(r"P(B) = P(B\mid A)P(A) + P(B\mid\neg A)P(\neg A) = %.4f" % evidence)
    r = posterior(prior, likelihood, evidence, lang)
except ValueError as e:
    st.error(str(e))
    st.stop()

st.divider()
m = st.columns(3)
m[0].metric(T("by_post"), f"{r['posterior']:.2%}", T("by_vs", d=f"{r['change']:+.2%}"))
m[1].metric(T("by_joint"), f"{r['joint']:.4f}")
m[2].metric("P(¬A|B)", f"{r['not_posterior']:.2%}")

st.latex(r"P(A\mid B) = \frac{%.4f \times %.4f}{%.4f} = %.4f" % (r["likelihood"], r["prior"], r["evidence"], r["posterior"]))
st.success(interpret(r, lang))

left, right = st.columns(2)
with left:
    st.markdown(T("by_chart"))
    df = pd.DataFrame({
        "belief": ["Prior P(A)", "Posterior P(A|B)"],
        "probability": [r["prior"], r["posterior"]],
    })
    chart = alt.Chart(df).mark_bar(cornerRadiusEnd=6).encode(
        x=alt.X("probability:Q", scale=alt.Scale(domain=[0, 1]), axis=alt.Axis(format="%"), title=T("ax_prob")),
        y=alt.Y("belief:N", title=None, sort=None),
        color=alt.Color("belief:N", scale=alt.Scale(range=["#9CA3AF", "#6366F1"]), legend=None),
        tooltip=[alt.Tooltip("probability:Q", format=".2%")],
    ).properties(height=160)
    st.altair_chart(chart, width="stretch")

with right:
    f = frequency_view(r)
    st.markdown(T("by_out_of", n=f"{f['population']:,}"))
    st.markdown(T("by_freq", b=f"{f['B']:.0f}", ab=f"{f['A_and_B']:.0f}", nab=f"{f['notA_and_B']:.0f}",
                  p=f"{r['posterior']:.2%}"))
