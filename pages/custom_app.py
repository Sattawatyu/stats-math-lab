"""StudyCast custom app - UI only. All math lives in services/custom_service.py"""
import altair as alt
import pandas as pd
import streamlit as st

from services import custom_service as cs
from services.cal_statistics import parse_numbers
from services.i18n import tr
from services.ui_helpers import ensure_main

ensure_main(__file__)  # opened before main.py ran? go through main.py so the normal menu shows
lang = st.session_state.get("lang", "th")
T = lambda key, **kw: tr(lang, key, **kw)  # noqa: E731
GRADE_COLORS = ["#10B981", "#22C55E", "#EAB308", "#F97316", "#EF4444"]
ACCENT = "#6366F1"

st.title(T("ca_title"))
st.markdown(T("ca_intro"))
st.markdown(
    ":violet-badge[Matrices · Z = XW + b] :blue-badge[Softmax] :green-badge[Sigmoid] "
    ":orange-badge[Derivatives · gradient descent] :red-badge[Chain rule] :gray-badge[Inverse sigmoid (logit)]"
)

with st.expander(T("ca_train")):
    t1, t2, t3 = st.columns(3)
    lr = t1.select_slider("Learning rate α", [0.01, 0.05, 0.1, 0.3, 0.5, 1.0], value=0.5)
    epochs = t2.select_slider("Epochs", [50, 100, 200, 400, 600, 1000, 2000], value=600)
    lam = t3.select_slider("L2 regularisation λ", [0.0, 0.0001, 0.001, 0.01, 0.1], value=0.001)

model = cs.train(lr, epochs, lam)

st.subheader(T("ca_habits"))
i1, i2, i3, i4 = st.columns(4)
study = i1.slider(T("lbl_study_hours"), 0.0, 25.0, 8.0, 0.5)
attend = i2.slider(T("lbl_attendance"), 30, 100, 85)
sleep = i3.slider(T("lbl_sleep_hours"), 3.5, 10.0, 7.0, 0.5)
hw = i4.slider(T("lbl_assignments_done"), 0, 10, 8)
args = (study, attend, sleep, hw)

pred = cs.predict(model, *args)
levers = cs.rank_levers(cs.sensitivity(model, *args))

tab_pred, tab_whatif, tab_how = st.tabs([T("ca_tab1"), T("ca_tab2"), T("ca_tab3")])

# ------------------------------------------------------------------ prediction
with tab_pred:
    m = st.columns(3)
    m[0].metric(T("ca_best"), pred["best_grade"], T("ca_conf", p=f"{pred['probs'][pred['best_grade']]:.0%}"),
                delta_color="off")
    m[1].metric(T("ca_ppass"), f"{pred['p_pass']:.1%}", help=T("ca_ppass_help"))
    m[2].metric(T("ca_gpa"), f"{pred['expected_gpa']:.2f}", help=T("ca_gpa_help"))

    left, right = st.columns([3, 2])
    with left:
        df = pd.DataFrame({"grade": list(pred["probs"]), "probability": list(pred["probs"].values())})
        st.altair_chart(
            alt.Chart(df).mark_bar(cornerRadiusEnd=6).encode(
                x=alt.X("grade:N", sort=None, title=T("ax_grade"), axis=alt.Axis(labelAngle=0)),
                y=alt.Y("probability:Q", axis=alt.Axis(format="%"), scale=alt.Scale(domain=[0, 1]), title=T("ax_prob")),
                color=alt.Color("grade:N", sort=None, legend=None, scale=alt.Scale(range=GRADE_COLORS)),
                tooltip=["grade", alt.Tooltip("probability:Q", format=".1%")],
            ).properties(title=T("ca_softmax_title"), height=300),
            width="stretch",
        )
    with right:
        st.markdown(T("ca_need"))
        target = st.slider(T("ca_target"), 0.50, 0.99, 0.90, 0.01)
        need = cs.hours_needed(model, target, attend, sleep, hw)
        if need["reason"] == "ok":
            st.success(T("ca_need_ok", h=f"{need['hours']:.1f}", s=f"{study:.1f}"))
        elif need["reason"] == "no_effect":
            st.warning(T("ca_need_none"))
        elif need["reason"] == "already":
            st.info(T("ca_need_already"))
        else:
            st.info(T("ca_need_out", h=f"{need['hours']:.1f}", hi=f"{need['limit']:.0f}"))
        st.latex(r"h = \mu + \sigma\cdot\frac{\ln\frac{p}{1-p} - c}{w_{study}}")

        st.markdown(T("ca_lever_head"))
        top = levers[0]
        st.markdown(T("ca_lever_top", c=T("u_" + top["input"]), p=f"{top['ΔP(pass)']:+.1%}"))
        for lv in levers[1:]:
            st.caption(f"{T('u_' + lv['input'])}: {lv['ΔP(pass)']:+.2%}")

# ------------------------------------------------------------------ what-if
with tab_whatif:
    vary = st.radio(T("ca_vary"), list(cs.FEATURE_LIMITS), format_func=lambda k: T("lbl_" + k), horizontal=True)
    curve = pd.DataFrame(cs.what_if_curve(model, vary, *args)["rows"])
    tan = cs.tangent_line(model, vary, *args)
    tan_df = pd.DataFrame(tan["rows"])
    point = pd.DataFrame([{vary: tan["x0"], "P(pass)": tan["p0"]}])
    x_title = T("lbl_" + vary)

    base = alt.Chart(curve).mark_line(strokeWidth=3, color=ACCENT).encode(
        x=alt.X(f"{vary}:Q", title=x_title),
        y=alt.Y("P(pass):Q", title=T("ax_ppass"), axis=alt.Axis(format="%"), scale=alt.Scale(domain=[0, 1])),
        tooltip=[alt.Tooltip(f"{vary}:Q", format=".1f"), alt.Tooltip("P(pass):Q", format=".1%")],
    )
    tangent = alt.Chart(tan_df).mark_line(strokeDash=[6, 4], color="#EF4444", strokeWidth=2).encode(
        x=f"{vary}:Q", y="tangent:Q")
    dot = alt.Chart(point).mark_circle(size=160, color="#EF4444").encode(x=f"{vary}:Q", y="P(pass):Q")
    st.altair_chart((base + tangent + dot).properties(height=320, title=T("ca_curve_title")), width="stretch")
    st.latex(r"\frac{dP}{dx} = \sigma(z)\,(1-\sigma(z))\cdot\frac{\partial z}{\partial x} = %.4f" % tan["slope"])
    st.caption(T("ca_slope", s=f"{tan['slope']:.4f}", p=f"{tan['slope']:+.2%}"))

    grade_cols = cs.GRADE_PROB_COLS
    st.altair_chart(
        alt.Chart(curve).transform_fold(grade_cols, as_=["grade", "P"]).mark_area().encode(
            x=alt.X(f"{vary}:Q", title=x_title),
            y=alt.Y("P:Q", stack="normalize", axis=alt.Axis(format="%"), title=T("ax_softmax")),
            color=alt.Color("grade:N", sort=grade_cols, scale=alt.Scale(domain=grade_cols, range=GRADE_COLORS)),
            order=alt.Order("grade:N"),
            tooltip=["grade:N", alt.Tooltip("P:Q", format=".1%")],
        ).properties(height=260, title=T("ca_shift_title")),
        width="stretch",
    )

    st.markdown(T("ca_deriv_head"))
    change_labels = {k: T("u_" + k) for k in cs.FEATURE_LIMITS}
    table = pd.DataFrame(cs.levers_table(levers, change_labels, T("col_change")))
    st.dataframe(
        table, hide_index=True, width="stretch",
        column_config={
            "ΔP(pass)": st.column_config.NumberColumn(format="%.5f"),
            "numeric check": st.column_config.NumberColumn(format="%.5f"),
            "ΔGPA": st.column_config.NumberColumn(format="%.4f"),
        },
    )
    st.caption(T("ca_deriv_caption"))

# ------------------------------------------------------------------ how it works
with tab_how:
    cells = cs.matrix_cells(model)
    k = st.columns(4)
    k[0].metric(T("ca_acc"), f"{model['accuracy']:.0%}", T("ca_baseline", p=f"{model['baseline']:.0%}"),
                delta_color="off")
    k[1].metric(T("ca_within"), f"{model['within_one']:.0%}")
    k[2].metric(T("ca_passacc"), f"{model['pass_accuracy']:.0%}")
    k[3].metric(T("ca_split"), f"{model['n_train']} / {model['n_test']}")

    st.markdown(T("ca_h1"))
    st.latex(r"Z_{(n\times5)} = X_{(n\times5)}\,W_{(5\times5)} + b \qquad P = \text{softmax}(Z),\;\; "
             r"\text{softmax}(z)_k = \frac{e^{z_k}}{\sum_j e^{z_j}}")
    st.markdown(T("ca_h2"))
    st.latex(r"L = -\frac{1}{n}\sum_i\sum_k Y_{ik}\ln P_{ik} + \frac{\lambda}{2}\lVert W\rVert^2 \qquad "
             r"\frac{\partial L}{\partial W} = \frac{1}{n}X^\top(P - Y) + \lambda W \qquad "
             r"W \leftarrow W - \alpha\,\frac{\partial L}{\partial W}")

    a, b = st.columns(2)
    with a:
        st.altair_chart(
            alt.Chart(pd.DataFrame(cells["loss"])).mark_line(strokeWidth=2).encode(
                x="epoch:Q", y=alt.Y("loss:Q", title="Cross-entropy loss"), color="model:N",
            ).properties(title=T("ca_loss_title"), height=280),
            width="stretch",
        )
    with b:
        conf = pd.DataFrame(cells["confusion"])
        enc = dict(x=alt.X("predicted:N", sort=cs.GRADES, axis=alt.Axis(labelAngle=0)),
                   y=alt.Y("actual:N", sort=cs.GRADES))
        heat = alt.Chart(conf).mark_rect().encode(
            color=alt.Color("students:Q", scale=alt.Scale(scheme="greens"), legend=None), **enc)
        txt = alt.Chart(conf).mark_text(fontSize=13).encode(text="students:Q", **enc)
        st.altair_chart((heat + txt).properties(title=T("ca_conf_title"), height=280), width="stretch")

    st.markdown(T("ca_h3"))
    a, b = st.columns([3, 2])
    with a:
        W = pd.DataFrame(cells["W"])
        enc = dict(x=alt.X("grade:N", sort=cs.GRADES, axis=alt.Axis(labelAngle=0)),
                   y=alt.Y("feature:N", sort=cs.FEATURES, title=None))
        heat = alt.Chart(W).mark_rect().encode(
            color=alt.Color("weight:Q", scale=alt.Scale(scheme="redblue", domainMid=0)),
            tooltip=["feature", "grade", alt.Tooltip("weight:Q", format=".3f")], **enc)
        txt = alt.Chart(W).mark_text(fontSize=11).encode(text=alt.Text("weight:Q", format=".2f"), **enc)
        st.altair_chart((heat + txt).properties(title=T("ca_W_title"), height=260), width="stretch")
    with b:
        st.altair_chart(
            alt.Chart(pd.DataFrame(cells["w"])).mark_bar(cornerRadiusEnd=4).encode(
                x=alt.X("weight:Q"), y=alt.Y("feature:N", sort=cs.FEATURES, title=None),
                color=alt.condition(alt.datum.weight > 0, alt.value("#10B981"), alt.value("#EF4444")),
            ).properties(title=T("ca_w_title"), height=260),
            width="stretch",
        )
    st.caption(T("ca_std_caption"))

    st.markdown(T("ca_h4"))
    s1, s2 = st.columns([2, 1])
    logits_text = s1.text_input(T("ca_logits"), "2.0, 1.0, 0.1")
    temp = s2.slider("Temperature T", 0.1, 5.0, 1.0, 0.1)
    try:
        logits = parse_numbers(logits_text, lang)
        sm = pd.DataFrame(cs.softmax_demo_rows(logits, temp))
        st.altair_chart(
            alt.Chart(sm).mark_bar(color=ACCENT, cornerRadiusEnd=4).encode(
                x=alt.X("class:N", sort=None, title=None, axis=alt.Axis(labelAngle=0)),
                y=alt.Y("probability:Q", axis=alt.Axis(format="%"), scale=alt.Scale(domain=[0, 1]), title=T("ax_prob")),
                tooltip=[alt.Tooltip("probability:Q", format=".2%")],
            ).properties(height=220),
            width="stretch",
        )
        st.caption(T("ca_temp_caption"))
    except ValueError as e:
        st.error(str(e))
