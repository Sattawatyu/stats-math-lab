"""Main entry point - routing, language and theme switch only.

Run:  streamlit run main.py
"""
import pandas as pd
import streamlit as st

from services.data_loader import members_table, save_members
from services.i18n import LANGS, page_text_items, reset_overrides, save_overrides, tr
from services.ui_helpers import editing_allowed

st.set_page_config(page_title="CS207 Group 1 | Stats & Math Lab", page_icon="📐", layout="wide")

# ---- Language (EN / TH) ----------------------------------------------------------
# Kept in session_state; also read from ?lang= so it survives the theme-switch reload.
if "lang" not in st.session_state:
    st.session_state.lang = st.query_params.get("lang", "th")
lang = st.session_state.lang
T = lambda key, **kw: tr(lang, key, **kw)  # noqa: E731

PAGES = {
    T("sec_overview"): [
        st.Page("pages/home.py", title=T("nav_home"), icon="🏠", url_path="home", default=True),
    ],
    T("sec_calc"): [
        st.Page("pages/statistics.py", title=T("nav_stats"), icon="📊", url_path="statistics"),
        st.Page("pages/bayes.py", title=T("nav_bayes"), icon="🎲", url_path="bayes"),
        st.Page("pages/markov.py", title=T("nav_markov"), icon="🔗", url_path="markov"),
    ],
    T("sec_data"): [
        st.Page("pages/display_data.py", title=T("nav_data"), icon="🗂️", url_path="display_data"),
        st.Page("pages/custom_app.py", title=T("nav_custom"), icon="🎓", url_path="custom_app"),
    ],
    T("sec_team"): [
        st.Page("pages/members.py", title=T("nav_members"), icon="👥", url_path="members"),
    ],
}

# ---- Dark / light mode toggle -------------------------------------------------------
# Both themes are defined in .streamlit/config.toml ([theme.light] / [theme.dark]).
# The browser remembers the chosen theme in localStorage; the button writes the
# new choice there and reloads the page so Streamlit applies it.
is_dark = st.context.theme.type == "dark"

if target := st.session_state.pop("theme_target", None):
    paths = ["/"] + [f"/{p.url_path}" for group in PAGES.values() for p in group]
    st.html(
        f"""<script>
        const paths = new Set({paths!r}.concat([window.location.pathname]));
        paths.forEach(p => localStorage.setItem(`stActiveTheme-${{p}}-v2`, '"{target}"'));
        const url = new URL(window.location.href);
        url.searchParams.set("lang", "{lang}");
        window.location.replace(url.toString());
        </script>""",
        unsafe_allow_javascript=True,
    )


def toggle_theme() -> None:
    st.session_state.theme_target = "Light" if is_dark else "Dark"


def change_lang() -> None:
    if st.session_state.lang_choice is None:  # clicked the already-selected language: keep it selected
        st.session_state.lang_choice = st.session_state.lang
    st.session_state.lang = st.session_state.lang_choice


nav = st.navigation(PAGES)

# a page that was opened before main.py ran (see services/ui_helpers.ensure_main):
# main.py has now switched the server to our menu, so reload that same page
if goto := st.session_state.pop("goto_page", None):
    # the default page (Home) lives at "/", not "/home": "/home" would show "Page not found"
    goto = "" if goto == "home" else goto
    st.html(
        f"""<script>
        const url = new URL(window.location.href);
        url.pathname = url.pathname.replace(/[^/]*$/, "{goto}");
        window.location.replace(url.toString());
        </script>""",
        unsafe_allow_javascript=True,
    )
    st.stop()

current_page = nav.url_path or "home"


# ---- Text editor (edit every page's text from the browser) -------------------------
def _text_fields(items: list[dict], prefix: str) -> dict:
    """Render one input per text item; returns {key: new value}."""
    values = {}
    for it in items:
        label = it["key"] + (f"  ✏️ {T('ed_edited')}" if it["edited"] else "")
        if it["kind"] == "table":
            st.markdown(f"<small>{label}</small>", unsafe_allow_html=True)
            df = pd.DataFrame(it["current"])
            edited = st.data_editor(df, key=f"{prefix}_{it['key']}", hide_index=True, width="stretch",
                                    num_rows="fixed")
            values[it["key"]] = edited.astype(str).values.tolist()
        elif it["long"]:
            values[it["key"]] = st.text_area(label, it["current"], key=f"{prefix}_{it['key']}",
                                             height=max(80, min(220, 24 * (len(it["current"]) // 90 + 2))),
                                             help=str(it["default"]))
        else:
            values[it["key"]] = st.text_input(label, it["current"], key=f"{prefix}_{it['key']}",
                                              help=str(it["default"]))
    return values


@st.dialog(T("ed_title"), width="large")
def text_editor(page: str) -> None:
    st.caption(T("ed_intro", language=LANGS[lang]))
    tabs = [T("ed_tab_page"), T("ed_tab_nav")] + ([T("ed_tab_members")] if page == "members" else [])
    tab_objs = st.tabs(tabs)

    for tab, group in zip(tab_objs[:2], [page, "nav"]):
        with tab:
            with st.form(f"form_{group}", border=False):
                values = _text_fields(page_text_items(group, lang), group)
                if st.form_submit_button(T("ed_save"), type="primary", icon=":material/save:"):
                    result = save_overrides(lang, values)
                    if result["errors"]:
                        for e in result["errors"]:
                            st.error(e)
                    else:
                        st.session_state.editor_msg = T("ed_saved", n=result["saved"]) if result["saved"] else T("ed_nochange")
                        st.rerun()
            if st.button(T("ed_reset"), key=f"reset_{group}", icon=":material/restart_alt:"):
                n = reset_overrides(lang, group)
                st.session_state.editor_msg = T("ed_saved", n=n)
                st.rerun()

    if page == "members":
        with tab_objs[2]:
            df = pd.DataFrame(members_table(lang), columns=T("ed_mem_cols"))
            edited = st.data_editor(df, hide_index=True, width="stretch", num_rows="fixed", key="members_editor",
                                    column_config={T("ed_mem_cols")[3]: st.column_config.TextColumn(width="large")})
            if st.button(T("ed_mem_save"), type="primary", icon=":material/save:"):
                n = save_members(edited.astype(str).values.tolist(), lang)
                st.session_state.editor_msg = T("ed_saved", n=n) if n else T("ed_nochange")
                st.rerun()


if msg := st.session_state.pop("editor_msg", None):
    st.toast(msg, icon="✅")

with st.sidebar:
    left, right = st.columns([1, 1], vertical_alignment="center")
    left.segmented_control(
        T("lang_label"), list(LANGS), format_func=LANGS.get, default=lang,
        key="lang_choice", on_change=change_lang, label_visibility="collapsed",
    )
    right.button(
        "", icon=":material/light_mode:" if is_dark else ":material/dark_mode:",
        on_click=toggle_theme, help=T("theme_light") if is_dark else T("theme_dark"),
        width="stretch",
    )
    # Only on the team's own computer: on the public site anyone could change the text for everyone
    if editing_allowed(st.context.headers.get("Host")) and st.button(T("ed_button"), icon=":material/edit:", width="stretch"):
        text_editor(current_page)
    st.caption(T("footer"))

nav.run()
