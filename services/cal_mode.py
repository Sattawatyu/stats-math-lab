"""Mode (most frequent value) and frequency table."""


def frequency_table(data: list[float]) -> dict[float, int]:
    """Count how many times each value appears, keys sorted ascending."""
    counts: dict[float, int] = {}
    for x in data:
        counts[x] = counts.get(x, 0) + 1
    return dict(sorted(counts.items()))


def find_mode(data: list[float]) -> dict:
    """Return all modes (data can be multimodal).

    If every value appears exactly once there is no mode -> modes = [].
    """
    freq = frequency_table(data)
    top = max(freq.values())
    if top == 1 and len(freq) > 1:
        modes = []
    else:
        modes = [x for x, c in freq.items() if c == top]
    return {"modes": modes, "count": top, "frequency": freq}
