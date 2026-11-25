"""Markov chain text prediction - UI only. Calculations: services/text_prediction.py"""
import altair as alt
import pandas as pd
import streamlit as st

from services.data_loader import load_raw_data
from services.i18n import tr
from services.text_prediction import (
    build_model, combine_corpus, generate, label_predictions, predict_next, sentence_starters, transition_matrix,
)
from services.ui_helpers import chart_height, ensure_main

ensure_main(__file__)  # opened before main.py ran? go through main.py so the normal menu shows
lang = st.session_state.get("lang", "th")
T = lambda key, **kw: tr(lang, key, **kw)  # noqa: E731

st.title(T("mk_title"))
st.latex(r"P(w_{t+1}=j \mid w_t=i) = \frac{\text{count}(i \to j)}{\sum_k \text{count}(i \to k)}")

raw = load_raw_data()
datasets = raw["datasets"]

c1, c2 = st.columns([2, 1])
key = c1.selectbox(T("mk_data"), list(datasets),
                   format_func=lambda k: datasets[k]["title"])
order = c2.radio(T("mk_order"), [1, 2], horizontal=True, help=T("mk_order_help"))

use_own = st.toggle(T("mk_own"))
extra = ""
if use_own:
    extra = st.text_area(T("mk_own_area"), "i go to the gym after class\nthe gym is busy in the evening")
sentences = combine_corpus(datasets[key]["sentences"], extra)

with st.expander(T("mk_show", n=len(sentences))):
    st.write("\n".join(f"- {s}" for s in sentences))

model = build_model(sentences, order)

st.divider()
st.subheader(T("mk_s1"))
starters = sentence_starters(sentences)
quick = st.pills(T("mk_quick"), starters[:8])
text = st.text_input(T("mk_input"), value=quick or starters[0])
top_k = st.slider(T("mk_top"), 1, 10, 5)
res = predict_next(model, text, order, top_k)

if not res["predictions"]:
    st.warning(T("mk_unseen", s=" ".join(res["state"])))
else:
    if res["backoff"]:
        st.info(T("mk_backoff", s=" ".join(res["state"]), w=res["used_state"][0]))
    best = res["predictions"][0]
    shown = best["word"] if best["word"] != "</s>" else T("mk_end")
    st.markdown(T("mk_best", w=shown, p=f"{best['probability']:.0%}"))
    df = pd.DataFrame(label_predictions(res["predictions"], T("mk_end")))
    bar = alt.Chart(df).mark_bar(cornerRadiusEnd=6, color="#6366F1").encode(
        x=alt.X("probability:Q", axis=alt.Axis(format="%"), title=T("ax_prob")),
        y=alt.Y("word:N", sort="-x", title=None),
        tooltip=["word", alt.Tooltip("probability:Q", format=".1%")],
    ).properties(height=chart_height(len(df), 40, 20))
    st.altair_chart(bar, width="stretch")

st.divider()
st.subheader(T("mk_s2"))
g1, g2, g3 = st.columns(3)
mode = g1.radio(T("mk_method"), ["greedy", "random"], format_func=lambda m: T(f"mk_{m}"))
length = g2.slider(T("mk_len"), 3, 25, 12)
seed = g3.number_input(T("mk_seed"), 0, 9999, 42, disabled=mode == "greedy")
out = generate(model, text, order, length, mode, int(seed))
st.markdown(f"> {out['text']}")
if out["steps"]:
    st.caption(T("mk_seqprob", p=f"{out['sequence_probability']:.4g}"))
    st.dataframe(pd.DataFrame(out["steps"]), hide_index=True, width="stretch")

st.divider()
st.subheader(T("mk_s3"))
n_words = st.slider(T("mk_nwords"), 5, 20, 10)
tm = transition_matrix(sentences, n_words)
long = pd.DataFrame(tm["cells"])
heat = alt.Chart(long).mark_rect().encode(
    x=alt.X("next word:N", sort=tm["labels"], axis=alt.Axis(labelAngle=-40)),
    y=alt.Y("current word:N", sort=tm["labels"]),
    color=alt.Color("P:Q", scale=alt.Scale(scheme="purples"), legend=alt.Legend(format="%")),
    tooltip=["current word", "next word", alt.Tooltip("P:Q", format=".2f")],
).properties(height=chart_height(len(tm["labels"]), 32, 40))
labels = alt.Chart(long).transform_filter(alt.datum.P > 0).mark_text(fontSize=11).encode(
    x=alt.X("next word:N", sort=tm["labels"], axis=alt.Axis(labelAngle=-40)),
    y=alt.Y("current word:N", sort=tm["labels"]),
    text=alt.Text("P:Q", format=".2f"),
    color=alt.condition(alt.datum.P > 0.5, alt.value("white"), alt.value("black")),
)
st.altair_chart(heat + labels, width="stretch")
st.caption(T("mk_caption", n=tm["states"]))
