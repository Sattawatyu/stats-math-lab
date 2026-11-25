"""Keep uploaded member photos after the online app restarts.

Streamlit Community Cloud forgets files written while the app runs, so each
uploaded photo is also committed to the GitHub repo (data/imgs/<file>).
That needs a token in the app's secrets:

    GITHUB_TOKEN = "github_pat_..."    # fine-grained, this repo only, Contents: read and write

Optional: GITHUB_REPO (default Sattawatyu/stats-math-lab), GITHUB_BRANCH (default main).
Streamlit Cloud exposes top-level secrets as environment variables, so no Streamlit import is needed.
"""
import base64
import os

import requests

API = "https://api.github.com/repos/{repo}/contents/data/imgs/{name}"


def persistence_enabled() -> bool:
    return bool(os.environ.get("GITHUB_TOKEN"))


def commit_photo(filename: str, data: bytes) -> bool:
    """Create or replace data/imgs/<filename> in the repo. Returns True on success, False if not configured."""
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        return False
    repo = os.environ.get("GITHUB_REPO", "Sattawatyu/stats-math-lab")
    branch = os.environ.get("GITHUB_BRANCH", "main")
    url = API.format(repo=repo, name=filename)
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"}

    # replacing a file needs its current sha
    r = requests.get(url, headers=headers, params={"ref": branch}, timeout=15)
    sha = r.json().get("sha") if r.status_code == 200 else None

    body = {"message": f"Update member photo {filename} (uploaded from the app)",
            "content": base64.b64encode(data).decode(), "branch": branch}
    if sha:
        body["sha"] = sha
    r = requests.put(url, headers=headers, json=body, timeout=30)
    r.raise_for_status()
    return True
