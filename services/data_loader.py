"""Reading files from data/ and preparing them for display."""
import io
import json
from collections import Counter
from pathlib import Path

from PIL import Image, ImageOps

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
IMG_DIR = DATA_DIR / "imgs"


def _read_json(name: str) -> dict:
    with open(DATA_DIR / name, encoding="utf-8") as f:
        return json.load(f)


def load_raw_data() -> dict:
    return _read_json("raw_data.json")


def load_members() -> dict:
    return _read_json("members.json")


def load_students() -> list[dict]:
    return _read_json("students.json")["students"]


def members_table(lang: str) -> list[list[str]]:
    """Members as editable rows: name, id, role, responsibilities (newline-separated) in `lang`."""
    sfx = "_th" if lang == "th" else ""
    return [[m["name"], m.get("student_id", ""), m.get("role" + sfx, m["role"]),
             "\n".join(m.get("responsibilities" + sfx, m["responsibilities"]))]
            for m in load_members()["members"]]


def save_members(rows: list[list[str]], lang: str) -> int:
    """Write edited member rows back to members.json (same order as members_table). Returns rows changed."""
    sfx = "_th" if lang == "th" else ""
    data = load_members()
    changed = 0
    for m, (name, sid, role, resp) in zip(data["members"], rows):
        new = {"name": str(name).strip(), "role" + sfx: str(role).strip(),
               "responsibilities" + sfx: [r.strip() for r in str(resp).splitlines() if r.strip()]}
        if str(sid).strip():   # student ID is optional (left out of the public repo)
            new["student_id"] = str(sid).strip()
        if any(m.get(k) != v for k, v in new.items()):
            m.update(new)
            changed += 1
    if changed:
        with open(DATA_DIR / "members.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    return changed


def list_data_files() -> list[dict]:
    """Every file in data/ with its size, for the data viewer."""
    rows = []
    for p in sorted(DATA_DIR.rglob("*")):
        if p.is_file():
            rows.append({
                "file": str(p.relative_to(DATA_DIR)).replace("\\", "/"),
                "type": p.suffix.lstrip(".").upper(),
                "size (KB)": round(p.stat().st_size / 1024, 1),
            })
    return rows


def member_image_path(filename: str) -> str | None:
    p = IMG_DIR / filename
    return str(p) if p.exists() else None


PHOTO_SIZE = 400  # every member photo is stored as a 400 x 400 JPEG (shown at 150 px)


def save_member_photo(filename: str, data: bytes) -> bytes:
    """Save an uploaded photo as data/imgs/<filename>, locked to PHOTO_SIZE x PHOTO_SIZE.

    Any size or shape is accepted: the photo is turned upright (phone EXIF),
    centre-cropped to a square and resized, so every member card looks the same.
    """
    with Image.open(io.BytesIO(data)) as im:
        im = ImageOps.exif_transpose(im).convert("RGB")
        im = ImageOps.fit(im, (PHOTO_SIZE, PHOTO_SIZE), Image.Resampling.LANCZOS)
        out = io.BytesIO()
        im.save(out, "JPEG", quality=90)
    (IMG_DIR / filename).write_bytes(out.getvalue())
    return out.getvalue()


def corpus_table(raw: dict, only_key: str | None = None) -> list[dict]:
    """One row per sentence: dataset, sentence, word count.
    With `only_key`, only that dataset and no dataset column (it would be the same on every row)."""
    rows = []
    for key, ds in raw["datasets"].items():
        if only_key and key != only_key:
            continue
        for s in ds["sentences"]:
            row = {"sentence": s, "words": len(s.split())}
            rows.append(row if only_key else {"dataset": ds["title"], **row})
    return rows


def corpus_summary(raw: dict) -> list[dict]:
    """One row per dataset: sentences, words, unique words."""
    rows = []
    for ds in raw["datasets"].values():
        words = " ".join(ds["sentences"]).split()
        rows.append({
            "dataset": ds["title"],
            "sentences": len(ds["sentences"]),
            "words": len(words),
            "unique words": len(set(words)),
        })
    return rows


def word_frequency(raw: dict, dataset_key: str, top: int = 15) -> list[dict]:
    words = " ".join(raw["datasets"][dataset_key]["sentences"]).split()
    return [{"word": w, "count": c} for w, c in Counter(words).most_common(top)]


def filter_students(students: list[dict], grades: list[str]) -> list[dict]:
    return [s for s in students if s["grade"] in grades]


def grade_counts(students: list[dict]) -> list[dict]:
    c = Counter(s["grade"] for s in students)
    return [{"grade": g, "students": c.get(g, 0)} for g in "ABCDF"]


def numeric_summary(students: list[dict]) -> list[dict]:
    """Mean / min / max for each numeric column of the student dataset."""
    cols = ["study_hours", "attendance", "sleep_hours", "assignments_done", "exam_score"]
    out = []
    for c in cols:
        vals = [s[c] for s in students]
        out.append({
            "column": c,
            "mean": round(sum(vals) / len(vals), 2),
            "min": min(vals),
            "max": max(vals),
        })
    return out
