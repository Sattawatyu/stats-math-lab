"""Markov Chain next-word prediction.

A Markov chain assumes the next word depends only on the current state
(the last `order` words):  P(w_{t+1} | w_1 ... w_t) ≈ P(w_{t+1} | state_t).

Transition probability:
    P(next = j | state = i) = count(i -> j) / Σ_k count(i -> k)
"""
import random
from collections import defaultdict

START = "<s>"
END = "</s>"


def tokenize(sentence: str) -> list[str]:
    cleaned = "".join(ch.lower() if ch.isalnum() or ch.isspace() or ch == "'" else " " for ch in sentence)
    return cleaned.split()


def build_counts(sentences: list[str], order: int = 1) -> dict[tuple, dict[str, int]]:
    """Count transitions state -> next word. A state is a tuple of `order` words.
    Each sentence is padded with <s> at the start and </s> at the end.
    """
    counts: dict[tuple, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for s in sentences:
        words = [START] * order + tokenize(s) + [END]
        for i in range(order, len(words)):
            state = tuple(words[i - order:i])
            counts[state][words[i]] += 1
    return {k: dict(v) for k, v in counts.items()}


def build_model(sentences: list[str], order: int = 1) -> dict[tuple, dict[str, float]]:
    """Normalise counts into transition probabilities (each row sums to 1)."""
    counts = build_counts(sentences, order)
    model = {}
    for state, nxt in counts.items():
        total = sum(nxt.values())
        model[state] = {w: c / total for w, c in sorted(nxt.items(), key=lambda kv: -kv[1])}
    return model


def transition_matrix(sentences: list[str], max_words: int = 12) -> dict:
    """First-order transition matrix restricted to the most frequent words
    (so it fits on screen). Returns labels and a 2-D list of probabilities
    computed over ALL transitions, so a row may sum to < 1 when it leads to
    words outside the shown subset.
    """
    model = build_model(sentences, order=1)
    freq: dict[str, int] = defaultdict(int)
    for s in sentences:
        for w in tokenize(s):
            freq[w] += 1
    labels = [w for w, _ in sorted(freq.items(), key=lambda kv: (-kv[1], kv[0]))[:max_words]]
    matrix = [[model.get((a,), {}).get(b, 0.0) for b in labels] for a in labels]
    cells = [{"current word": a, "next word": b, "P": matrix[i][j]}
             for i, a in enumerate(labels) for j, b in enumerate(labels)]
    return {"labels": labels, "matrix": matrix, "cells": cells, "states": len(model)}


def combine_corpus(base: list[str], extra_text: str = "") -> list[str]:
    """Base sentences plus the user's own sentences (one per non-empty line)."""
    return list(base) + [s.strip() for s in extra_text.splitlines() if s.strip()]


def current_state(text: str, order: int) -> tuple:
    words = tokenize(text)
    padded = [START] * order + words
    return tuple(padded[-order:])


def predict_next(model: dict, text: str, order: int = 1, top_k: int = 5) -> dict:
    """Top-k next words after `text`. Falls back to a shorter context if the
    exact state was never seen (back-off) and reports which state was used.
    """
    state = current_state(text, order)
    used = state
    if state not in model and order > 1:
        # back-off: keep only the last word, look for any state ending with it
        last = state[-1]
        merged: dict[str, float] = defaultdict(float)
        for st, nxt in model.items():
            if st[-1] == last:
                for w, p in nxt.items():
                    merged[w] += p
        if merged:
            total = sum(merged.values())
            preds = sorted(((w, p / total) for w, p in merged.items()), key=lambda x: -x[1])
            return {"state": state, "used_state": (last,), "backoff": True,
                    "predictions": [{"word": w, "probability": p} for w, p in preds[:top_k]]}
    if used not in model:
        return {"state": state, "used_state": used, "backoff": False, "predictions": []}
    preds = list(model[used].items())[:top_k]
    return {"state": state, "used_state": used, "backoff": False,
            "predictions": [{"word": w, "probability": p} for w, p in preds]}


def generate(model: dict, seed_text: str = "", order: int = 1, max_words: int = 15,
             mode: str = "greedy", random_seed: int | None = None) -> dict:
    """Continue `seed_text` word by word.
    mode = "greedy": always take the most probable next word.
    mode = "random": sample the next word using the transition probabilities.
    Returns the generated words and the probability of each step.
    """
    rng = random.Random(random_seed)
    words = tokenize(seed_text)
    steps = []
    for _ in range(max_words):
        state = tuple(([START] * order + words)[-order:])
        nxt = model.get(state)
        if not nxt:
            break
        if mode == "greedy":
            w, p = next(iter(nxt.items()))
        else:
            options, probs = zip(*nxt.items())
            w = rng.choices(options, weights=probs, k=1)[0]
            p = nxt[w]
        if w == END:
            break
        steps.append({"state": " ".join(state).replace(START, "<s>"), "next word": w, "P": p})
        words.append(w)
        if mode == "greedy" and len(steps) >= 3 and words[-3:] == words[-6:-3]:
            break  # greedy decoding can loop forever; stop on a repeated 3-word cycle
    prob = 1.0
    for s in steps:
        prob *= s["P"]
    return {"text": " ".join(words), "steps": steps, "sequence_probability": prob}


def sentence_starters(sentences: list[str]) -> list[str]:
    """Distinct first words, used as quick seeds in the UI."""
    seen = []
    for s in sentences:
        t = tokenize(s)
        if t and t[0] not in seen:
            seen.append(t[0])
    return seen


def label_predictions(predictions: list[dict], end_label: str) -> list[dict]:
    """Replace the end-of-sentence token </s> with a readable label for the chart."""
    return [{**p, "word": end_label if p["word"] == "</s>" else p["word"]} for p in predictions]
