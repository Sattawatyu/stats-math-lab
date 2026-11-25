"""Descriptive statistics: parsing input, mean, median, variance, standard deviation.

All formulas are written out by hand (no statistics library) so they can be
explained during the presentation.
"""
import math
import re

from services.cal_mode import find_mode
from services.i18n import tr


def parse_numbers(text: str, lang: str = "en") -> list[float]:
    """Turn a string like "-100, 0, 10 20;30" into [-100.0, 0.0, 10.0, 20.0, 30.0].

    Raises ValueError with a readable message if any token is not a number.
    """
    tokens = [t for t in re.split(r"[,\s;]+", text.strip()) if t]
    if not tokens:
        raise ValueError(tr(lang, "err_empty"))
    numbers = []
    for t in tokens:
        try:
            numbers.append(float(t))
        except ValueError:
            raise ValueError(tr(lang, "err_nan", t=t)) from None
    return numbers


def cal_mean(data: list[float]) -> float:
    """x̄ = Σx / n"""
    return sum(data) / len(data)


def cal_median(data: list[float]) -> float:
    """Middle value of the sorted data (average of the two middle values if n is even)."""
    s = sorted(data)
    n = len(s)
    mid = n // 2
    if n % 2 == 1:
        return s[mid]
    return (s[mid - 1] + s[mid]) / 2


def cal_variance(data: list[float], sample: bool = False, lang: str = "en") -> float:
    """Population σ² = Σ(x-μ)² / n,  sample s² = Σ(x-x̄)² / (n-1)."""
    n = len(data)
    if sample and n < 2:
        raise ValueError(tr(lang, "err_sample2"))
    mu = cal_mean(data)
    ss = sum((x - mu) ** 2 for x in data)
    return ss / (n - 1 if sample else n)


def cal_sd(data: list[float], sample: bool = False) -> float:
    """Standard deviation = √variance"""
    return math.sqrt(cal_variance(data, sample))


def deviation_table(data: list[float]) -> list[dict]:
    """Step-by-step table: x, x - mean, (x - mean)²  (used to explain the variance)."""
    mu = cal_mean(data)
    return [
        {"x": x, "x - mean": x - mu, "(x - mean)²": (x - mu) ** 2}
        for x in data
    ]


def summarize(data: list[float], sample: bool = False, lang: str = "en") -> dict:
    """Return every statistic the Statistics page needs, in one dictionary."""
    if not data:
        raise ValueError(tr(lang, "err_empty"))
    variance = cal_variance(data, sample, lang)
    mode_info = find_mode(data)
    return {
        "n": len(data),
        "sum": sum(data),
        "mean": cal_mean(data),
        "median": cal_median(data),
        "mode": mode_info["modes"],
        "mode_count": mode_info["count"],
        "frequency": mode_info["frequency"],
        "variance": variance,
        "sd": variance ** 0.5,
        "min": min(data),
        "max": max(data),
        "range": max(data) - min(data),
        "sorted": sorted(data),
        "deviations": deviation_table(data),
        "sum_sq": sum(d["(x - mean)²"] for d in deviation_table(data)),
        "divisor": len(data) - 1 if sample else len(data),
        "kind": "sample (n-1)" if sample else "population (n)",
    }


def chart_points(data: list[float]) -> list[dict]:
    """Rows for the dot chart: point number (1..n) and value."""
    return [{"index": i, "value": x} for i, x in enumerate(data, start=1)]


def reference_lines(result: dict) -> list[dict]:
    """Vertical lines on the chart: mean, median and mean ± 1 SD."""
    mean, sd = result["mean"], result["sd"]
    return [
        {"stat": "Mean", "value": mean},
        {"stat": "Median", "value": result["median"]},
        {"stat": "Mean − SD", "value": mean - sd},
        {"stat": "Mean + SD", "value": mean + sd},
    ]
