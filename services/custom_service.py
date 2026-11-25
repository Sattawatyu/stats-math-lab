"""StudyCast - exam-result predictor built from scratch with NumPy.

Course topics used
------------------
* Matrices / Linear algebra : the model is Z = X·W + b  (X: n×d, W: d×K)
* Softmax                   : turns the K scores of each student into grade probabilities
* Sigmoid                   : a second (binary) model gives P(grade C or better)
* Derivatives               : gradient descent training (∂Loss/∂W = Xᵀ(P−Y)/n),
                              sensitivity "how much does 1 more study hour help?"
                              (chain rule + softmax Jacobian), checked numerically
* Inverse sigmoid (logit)   : minimum study hours needed to reach a target probability
"""
from functools import lru_cache

import numpy as np

from services.data_loader import load_students

GRADES = ["A", "B", "C", "D", "F"]
GRADE_PROB_COLS = [f"P({g})" for g in GRADES]  # column names in what_if_curve rows
GRADE_POINTS = np.array([4.0, 3.0, 2.0, 1.0, 0.0])
RAW_FEATURES = ["study_hours", "attendance", "sleep_hours", "assignments_done"]
# engineered features: sleep² lets a linear model learn "too little OR too much sleep is bad"
FEATURES = ["study_hours", "attendance", "sleep_hours", "sleep_hours²", "assignments_done"]
FEATURE_LIMITS = {
    "study_hours": (0.0, 25.0),
    "attendance": (30.0, 100.0),
    "sleep_hours": (3.5, 10.0),
    "assignments_done": (0, 10),
}
PASS_GRADES = {"A", "B", "C"}


# ----------------------------------------------------------------- math helpers
def sigmoid(z):
    """σ(z) = 1 / (1 + e^(−z))"""
    return 1.0 / (1.0 + np.exp(-z))


def sigmoid_derivative(z):
    """σ'(z) = σ(z)·(1 − σ(z))"""
    s = sigmoid(z)
    return s * (1 - s)


def softmax(Z):
    """softmax(z)_k = e^(z_k) / Σ_j e^(z_j), row by row (max subtracted for stability)."""
    Z = np.atleast_2d(Z)
    e = np.exp(Z - Z.max(axis=1, keepdims=True))
    return e / e.sum(axis=1, keepdims=True)


def logit(p):
    """Inverse of the sigmoid: σ⁻¹(p) = ln(p / (1 − p))"""
    return np.log(p / (1 - p))


# ------------------------------------------------------------ data preparation
def _engineer(raw: np.ndarray) -> np.ndarray:
    """raw columns = RAW_FEATURES -> engineered columns = FEATURES."""
    raw = np.atleast_2d(raw).astype(float)
    study, attend, sleep, hw = raw.T
    return np.column_stack([study, attend, sleep, sleep ** 2, hw])


def _dataset():
    students = load_students()
    raw = np.array([[s[f] for f in RAW_FEATURES] for s in students], dtype=float)
    y = np.array([GRADES.index(s["grade"]) for s in students])
    return raw, y


def _split(n: int, test_ratio: float = 0.2, seed: int = 7):
    idx = np.random.default_rng(seed).permutation(n)
    cut = int(n * (1 - test_ratio))
    return idx[:cut], idx[cut:]


# --------------------------------------------------------------------- training
def _train_softmax(X, Y_onehot, lr, epochs, lam):
    """Batch gradient descent on cross-entropy loss with L2 regularisation.

    Loss  L = −(1/n) Σ_i Σ_k Y_ik·ln P_ik  +  (λ/2)·‖W‖²
    Grad  ∂L/∂W = Xᵀ(P − Y)/n + λW ,   ∂L/∂b = mean(P − Y)
    """
    n, d = X.shape
    K = Y_onehot.shape[1]
    W = np.zeros((d, K))
    b = np.zeros(K)
    history = []
    for _ in range(epochs):
        P = softmax(X @ W + b)
        loss = -np.mean(np.sum(Y_onehot * np.log(P + 1e-12), axis=1)) + lam / 2 * np.sum(W ** 2)
        history.append(loss)
        G = (P - Y_onehot) / n
        W -= lr * (X.T @ G + lam * W)
        b -= lr * G.sum(axis=0)
    return W, b, history


def _train_sigmoid(X, y01, lr, epochs, lam):
    """Logistic regression: P = σ(Xw + b), binary cross-entropy, gradient Xᵀ(P − y)/n."""
    n, d = X.shape
    w = np.zeros(d)
    b = 0.0
    history = []
    for _ in range(epochs):
        p = sigmoid(X @ w + b)
        loss = -np.mean(y01 * np.log(p + 1e-12) + (1 - y01) * np.log(1 - p + 1e-12)) + lam / 2 * np.sum(w ** 2)
        history.append(loss)
        g = (p - y01) / n
        w -= lr * (X.T @ g + lam * w)
        b -= lr * g.sum()
    return w, b, history


@lru_cache(maxsize=16)
def train(lr: float = 0.5, epochs: int = 600, lam: float = 0.001) -> dict:
    """Train both models and evaluate them on a held-out 20% test set."""
    raw, y = _dataset()
    F = _engineer(raw)
    tr, te = _split(len(y))
    mu, sd = F[tr].mean(axis=0), F[tr].std(axis=0)
    X = (F - mu) / sd                                   # standardise (z-score)
    Y = np.eye(len(GRADES))[y]                          # one-hot matrix n×K
    y_pass = np.isin(y, [GRADES.index(g) for g in PASS_GRADES]).astype(float)

    W, b, hist_soft = _train_softmax(X[tr], Y[tr], lr, epochs, lam)
    w, b2, hist_sig = _train_sigmoid(X[tr], y_pass[tr], lr, epochs, lam)

    pred = softmax(X[te] @ W + b).argmax(axis=1)
    acc = float((pred == y[te]).mean())
    within_one = float((np.abs(pred - y[te]) <= 1).mean())
    conf = np.zeros((len(GRADES), len(GRADES)), dtype=int)
    for t, p in zip(y[te], pred):
        conf[t, p] += 1
    pass_pred = (sigmoid(X[te] @ w + b2) >= 0.5).astype(float)
    pass_acc = float((pass_pred == y_pass[te]).mean())

    return {
        "mu": mu, "sd": sd, "W": W, "b": b, "w": w, "b2": b2,
        "loss_softmax": hist_soft, "loss_sigmoid": hist_sig,
        "accuracy": acc, "within_one": within_one, "pass_accuracy": pass_acc,
        "confusion": conf, "n_train": len(tr), "n_test": len(te),
        "baseline": float(np.bincount(y[tr]).max() / len(tr)),
    }


# ------------------------------------------------------------------- prediction
def _x(model, raw_row):
    return (_engineer(raw_row) - model["mu"]) / model["sd"]


def _dz_dstudy(model):
    """∂(standardised features)/∂(study hours) — only the study column depends on it."""
    g = np.zeros(len(FEATURES))
    g[0] = 1.0 / model["sd"][0]
    return g


def _dz_dsleep(model, sleep):
    """Chain rule: features sleep and sleep² both change, d(sleep²)/d(sleep) = 2·sleep."""
    g = np.zeros(len(FEATURES))
    g[2] = 1.0 / model["sd"][2]
    g[3] = 2.0 * sleep / model["sd"][3]
    return g


def predict(model: dict, study, attendance, sleep, assignments) -> dict:
    raw = np.array([[study, attendance, sleep, assignments]], dtype=float)
    x = _x(model, raw)[0]
    z_soft = x @ model["W"] + model["b"]
    probs = softmax(z_soft)[0]
    z_soft = np.atleast_2d(z_soft)
    z_pass = float(x @ model["w"] + model["b2"])
    p_pass = float(sigmoid(z_pass))
    gpa = float(probs @ GRADE_POINTS)
    return {
        "probs": {g: float(p) for g, p in zip(GRADES, probs)},
        "logits": {g: float(z) for g, z in zip(GRADES, z_soft[0])},
        "best_grade": GRADES[int(probs.argmax())],
        "p_pass": p_pass, "z_pass": z_pass,
        "expected_gpa": gpa,
    }


def sensitivity(model: dict, study, attendance, sleep, assignments) -> dict:
    """Derivatives at the current point (per 1 raw unit).

    Sigmoid model : dP/dx   = σ'(z) · (w · dx_std/dx)
    Softmax model : dE/dx   = Σ_k g_k · p_k · (a_k − ā)   where a_k = ∂z_k/∂x, ā = Σ_j p_j a_j
                    (this is E = Σ g_k p_k differentiated through the softmax Jacobian)
    The analytic answer is compared with a central finite difference
    [f(x+h) − f(x−h)] / 2h to show they match.
    """
    base = predict(model, study, attendance, sleep, assignments)
    p = np.array(list(base["probs"].values()))
    out = {}
    feats = {
        "study_hours": _dz_dstudy(model),
        "attendance": np.eye(len(FEATURES))[1] / model["sd"][1],
        "sleep_hours": _dz_dsleep(model, sleep),
        "assignments_done": np.eye(len(FEATURES))[4] / model["sd"][4],
    }
    args = {"study_hours": study, "attendance": attendance, "sleep_hours": sleep, "assignments_done": assignments}
    h = 1e-4
    for name, dx in feats.items():
        dP = float(sigmoid_derivative(base["z_pass"])) * float(model["w"] @ dx)
        a = dx @ model["W"]                     # ∂z_k/∂x for every grade k
        a_bar = float(p @ a)
        dE = float(np.sum(GRADE_POINTS * p * (a - a_bar)))
        plus, minus = dict(args), dict(args)
        plus[name] += h
        minus[name] -= h
        num_dP = (predict(model, *plus.values())["p_pass"] - predict(model, *minus.values())["p_pass"]) / (2 * h)
        out[name] = {"dP_pass": dP, "dGPA": dE, "numeric_dP_pass": num_dP}
    return out


def what_if_curve(model: dict, vary: str, study, attendance, sleep, assignments, points: int = 60) -> dict:
    """Vary one input over its range, keep the others fixed."""
    lo, hi = FEATURE_LIMITS[vary]
    xs = np.linspace(lo, hi, points)
    rows = []
    for v in xs:
        args = {"study_hours": study, "attendance": attendance, "sleep_hours": sleep, "assignments_done": assignments}
        args[vary] = float(v)
        r = predict(model, *args.values())
        row = {vary: float(v), "P(pass)": r["p_pass"], "Expected GPA": r["expected_gpa"]}
        row.update({f"P({g})": r["probs"][g] for g in GRADES})
        rows.append(row)
    return {"x": vary, "rows": rows}


def tangent_line(model: dict, vary: str, study, attendance, sleep, assignments) -> dict:
    """Tangent of P(pass) at the current point: y = P0 + P'(x0)·(x − x0), drawn over ±3 units."""
    args = {"study_hours": study, "attendance": attendance, "sleep_hours": sleep, "assignments_done": assignments}
    x0 = args[vary]
    p0 = predict(model, *args.values())["p_pass"]
    slope = sensitivity(model, *args.values())[vary]["dP_pass"]
    lo, hi = FEATURE_LIMITS[vary]
    span = (hi - lo) * 0.12
    xs = np.linspace(max(lo, x0 - span), min(hi, x0 + span), 10)
    return {"x0": x0, "p0": p0, "slope": slope,
            "rows": [{vary: float(x), "tangent": float(p0 + slope * (x - x0))} for x in xs]}


def hours_needed(model: dict, target: float, attendance, sleep, assignments) -> dict:
    """Solve σ(z(h)) = target for study hours h using the logit:
    z(h) = c + w_study·(h − μ)/σ   ⇒   h = μ + σ·(logit(target) − c) / w_study
    """
    if not 0 < target < 1:
        raise ValueError("Target must be between 0 and 1.")
    w_s = model["w"][0]
    x0 = _x(model, np.array([[model["mu"][0], attendance, sleep, assignments]]))[0]
    c = float(x0 @ model["w"] + model["b2"])           # z when study = mean (its std value = 0)
    if w_s <= 0:
        return {"hours": None, "reason": "no_effect"}
    h = model["mu"][0] + model["sd"][0] * (float(logit(target)) - c) / w_s
    lo, hi = FEATURE_LIMITS["study_hours"]
    if h <= lo:
        return {"hours": 0.0, "reason": "already"}
    if h > hi:
        return {"hours": float(h), "reason": "out_of_range", "limit": hi}
    return {"hours": float(h), "reason": "ok"}


def weight_table(model: dict) -> dict:
    """Matrix W (features × grades) and vector w (pass model), for visualisation."""
    return {
        "features": FEATURES,
        "grades": GRADES,
        "W": model["W"].tolist(),
        "w": model["w"].tolist(),
    }


UNITS = {
    "study_hours": "1 more study hour / week",
    "attendance": "1% more attendance",
    "sleep_hours": "1 more hour of sleep / night",
    "assignments_done": "1 more assignment done",
}


def rank_levers(sens: dict) -> list[dict]:
    """Sort inputs by how much one extra unit raises P(pass) right now (largest first)."""
    rows = [{"input": k, "change": UNITS[k], "ΔP(pass)": v["dP_pass"], "ΔGPA": v["dGPA"],
             "numeric check": v["numeric_dP_pass"]} for k, v in sens.items()]
    return sorted(rows, key=lambda r: -r["ΔP(pass)"])


def matrix_cells(model: dict) -> dict:
    """Long-format cells for heatmaps: weight matrix W and confusion matrix."""
    W = [{"feature": f, "grade": g, "weight": float(model["W"][i, j])}
         for i, f in enumerate(FEATURES) for j, g in enumerate(GRADES)]
    w = [{"feature": f, "weight": float(model["w"][i])} for i, f in enumerate(FEATURES)]
    conf = [{"actual": a, "predicted": p, "students": int(model["confusion"][i, j])}
            for i, a in enumerate(GRADES) for j, p in enumerate(GRADES)]
    loss = [{"epoch": i + 1, "model": "Softmax (grade)", "loss": float(v)} for i, v in enumerate(model["loss_softmax"])]
    loss += [{"epoch": i + 1, "model": "Sigmoid (pass)", "loss": float(v)} for i, v in enumerate(model["loss_sigmoid"])]
    return {"W": W, "w": w, "confusion": conf, "loss": loss}


def softmax_demo(logits: list[float], temperature: float = 1.0) -> list[float]:
    """Softmax with temperature T: lower T -> sharper, higher T -> flatter."""
    z = np.array(logits, dtype=float) / temperature
    return softmax(z)[0].tolist()


def levers_table(levers: list[dict], change_labels: dict[str, str], change_col: str) -> list[dict]:
    """Derivative table for the page: translated "change" label first, then the numbers."""
    return [{change_col: change_labels[lv["input"]], "ΔP(pass)": lv["ΔP(pass)"], "ΔGPA": lv["ΔGPA"],
             "numeric check": lv["numeric check"]} for lv in levers]


def softmax_demo_rows(logits: list[float], temperature: float = 1.0) -> list[dict]:
    """Chart rows for the softmax demo: label z1 = 2.0 ... and its probability."""
    probs = softmax_demo(logits, temperature)
    return [{"class": f"z{i} = {z:g}", "probability": p} for i, (z, p) in enumerate(zip(logits, probs), start=1)]
