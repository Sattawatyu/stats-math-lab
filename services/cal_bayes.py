"""Bayes' theorem:  P(A|B) = P(B|A) · P(A) / P(B)"""
from services.i18n import tr


def _check_prob(name: str, p: float, lang: str = "en") -> None:
    if not 0 <= p <= 1:
        raise ValueError(tr(lang, "by_err_range", name=name, p=p))


def total_probability(prior: float, likelihood: float, false_rate: float, lang: str = "en") -> float:
    """Evidence by the law of total probability:
    P(B) = P(B|A)·P(A) + P(B|¬A)·P(¬A)
    """
    for name, p in [("P(A)", prior), ("P(B|A)", likelihood), ("P(B|¬A)", false_rate)]:
        _check_prob(name, p, lang)
    return likelihood * prior + false_rate * (1 - prior)


def posterior(prior: float, likelihood: float, evidence: float, lang: str = "en") -> dict:
    """Compute P(A|B) and the pieces needed to explain it."""
    for name, p in [("P(A)", prior), ("P(B|A)", likelihood), ("P(B)", evidence)]:
        _check_prob(name, p, lang)
    if evidence == 0:
        raise ValueError(tr(lang, "by_err_zero"))
    joint = likelihood * prior                      # P(A ∩ B)
    post = joint / evidence
    if post > 1 + 1e-9:
        raise ValueError(tr(lang, "by_err_inconsistent", j=f"{joint:.4f}", e=f"{evidence:.4f}", p=f"{post:.4f}"))
    post = min(post, 1.0)
    return {
        "prior": prior,
        "likelihood": likelihood,
        "evidence": evidence,
        "joint": joint,
        "posterior": post,
        "not_posterior": 1 - post,
        "change": post - prior,
        "ratio": post / prior if prior > 0 else float("inf"),
    }


def interpret(result: dict, lang: str = "en") -> str:
    """Plain-language summary of how the evidence changed our belief."""
    pr, po = result["prior"], result["posterior"]
    if abs(po - pr) < 1e-9:
        verb = tr(lang, "by_same")
    elif po > pr:
        verb = tr(lang, "by_up")
    else:
        verb = tr(lang, "by_down")
    return tr(lang, "by_interp", pr=f"{pr:.2%}", po=f"{po:.2%}", verb=verb)


def frequency_view(result: dict, population: int = 1000) -> dict:
    """Natural-frequency explanation: out of `population` cases, how many are A and B."""
    a = result["prior"] * population
    a_and_b = result["joint"] * population
    b = result["evidence"] * population
    return {
        "population": population,
        "A": a,
        "B": b,
        "A_and_B": a_and_b,
        "notA_and_B": b - a_and_b,
    }


PRESETS = {
    "medical": {
        "title": {"en": "Medical test", "th": "ตรวจโรค"},
        "desc": {
            "en": "A = has the disease, B = test is positive. 1% of people have the disease, "
                  "the test detects 95% of them, and 5% of healthy people also test positive.",
            "th": "A = เป็นโรค, B = ผลตรวจเป็นบวก ประชากร 1% เป็นโรค ชุดตรวจตรวจพบผู้ป่วยได้ 95% "
                  "และคนที่ไม่ป่วยตรวจได้ผลบวก (ผลบวกลวง) 5%",
        },
        "prior": 0.01, "likelihood": 0.95, "false_rate": 0.05,
    },
    "spam": {
        "title": {"en": "Spam filter", "th": "กรองอีเมลสแปม"},
        "desc": {
            "en": "A = email is spam, B = email contains the word 'FREE'. "
                  "40% of email is spam, 60% of spam contains 'FREE', 5% of normal email does.",
            "th": "A = อีเมลเป็นสแปม, B = อีเมลมีคำว่า 'FREE' อีเมล 40% เป็นสแปม "
                  "สแปม 60% มีคำว่า 'FREE' และอีเมลปกติ 5% มีคำนี้",
        },
        "prior": 0.40, "likelihood": 0.60, "false_rate": 0.05,
    },
    "rain": {
        "title": {"en": "Rain forecast", "th": "พยากรณ์ฝน"},
        "desc": {
            "en": "A = it rains today, B = the morning is cloudy. "
                  "It rains on 20% of days, 80% of rainy days start cloudy, 30% of dry days start cloudy.",
            "th": "A = วันนี้ฝนตก, B = ตอนเช้ามีเมฆมาก ฝนตก 20% ของวัน "
                  "วันที่ฝนตก 80% ตอนเช้ามีเมฆมาก และวันที่ฝนไม่ตก 30% ตอนเช้ามีเมฆมาก",
        },
        "prior": 0.20, "likelihood": 0.80, "false_rate": 0.30,
    },
}
