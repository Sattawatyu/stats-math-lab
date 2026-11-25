"""Team members - UI only. Data: data/members.json + data/imgs/ via services/data_loader.py"""
import streamlit as st

from services.data_loader import load_members, member_image_path, save_member_photo
from services.i18n import tr
from services.photo_store import commit_photo, persistence_enabled
from services.ui_helpers import editing_allowed, ensure_main

ensure_main(__file__)  # opened before main.py ran? go through main.py so the normal menu shows
lang = st.session_state.get("lang", "th")
T = lambda key, **kw: tr(lang, key, **kw)  # noqa: E731
sfx = "_th" if lang == "th" else ""

info = load_members()
# photo upload: on the team's own computer, or online once photos are kept in GitHub (GITHUB_TOKEN secret)
can_edit = editing_allowed(st.context.headers.get("Host")) or persistence_enabled()
st.title(T("mb_title"))
st.caption(T("footer"))


def on_photo_upload(filename: str, up_key: str, ver_key: str) -> None:
    """Runs once when a file is chosen: save it, then switch to a fresh (empty) uploader."""
    up = st.session_state.get(up_key)
    if up is None:
        return
    try:
        jpeg = save_member_photo(filename, up.getvalue())
    except Exception:
        st.session_state.photo_msg = ("⚠️", T("mb_photo_error"))
    else:
        try:
            kept = commit_photo(filename, jpeg)
            st.session_state.photo_msg = ("✅", T("mb_photo_kept") if kept else T("mb_photo_saved"))
        except Exception:
            st.session_state.photo_msg = ("⚠️", T("mb_photo_github_error"))
    st.session_state[ver_key] = st.session_state.get(ver_key, 0) + 1


if msg := st.session_state.pop("photo_msg", None):
    st.toast(msg[1], icon=msg[0])

for m in info["members"]:
    # one row: photo (fixed 150 px) right next to the details, no stretched empty column
    with st.container(border=True, horizontal=True, vertical_alignment="center", gap="medium"):
        img = member_image_path(m["image"])
        with st.container(width=150, gap="small"):
            if img:
                st.image(img, width=150)
            else:
                st.markdown("🧑‍🎓")
            # upload a new photo
            if can_edit:
                with st.popover(T("mb_photo_btn"), icon=":material/photo_camera:", width="stretch"):
                    # a new key after each upload gives an empty uploader, so the file is saved only once
                    ver_key = f"photo_ver_{m['image']}"
                    up_key = f"photo_{m['image']}_{st.session_state.get(ver_key, 0)}"
                    st.file_uploader(T("mb_photo_btn"), type=["jpg", "jpeg", "png", "webp"],
                                     key=up_key, label_visibility="collapsed",
                                     on_change=on_photo_upload, args=(m["image"], up_key, ver_key))
                    st.caption(T("mb_photo_help"))
        with st.container():
            st.markdown(f"### {m['name']}")
            id_line = f"**{T('mb_id')}:** `{m['student_id']}`  \n" if m.get("student_id") else ""
            st.markdown(f"{id_line}**{T('mb_role')}:** {m.get('role' + sfx, m['role'])}")
            st.markdown("\n".join(f"- {r}" for r in m.get("responsibilities" + sfx, m["responsibilities"])))
