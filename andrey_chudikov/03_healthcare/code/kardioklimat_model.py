# КАРДИОКЛИМАТ-КУБАНЬ: фрагмент обучения и валидации модели (задел)
# Полная модель — градиентный бустинг; здесь воспроизводимая логистическая
# регрессия с теми же признаками (интерпретируемая копия, этап 2).

import numpy as np

def make_demo_dataset(n=5479, seed=2026):
    """Демонстрационный датасет с той же структурой признаков, что и рабочий.
    В реальной работе используется датасет «метеоряды — сводки ССЗ» 2023–2025."""
    rng = np.random.default_rng(seed)
    tmax = rng.normal(28, 6, n)
    series33 = np.clip((tmax - 30) / 2 + rng.normal(0, 1, n), 0, 14)
    grad48 = rng.normal(0, 1.5, n)
    share65 = rng.uniform(0.14, 0.26, n)
    logit = -4.2 + 0.11 * (tmax - 33) + 0.34 * series33 + 0.22 * grad48 + 6.1 * (share65 - 0.18)
    y = (rng.random(n) < 1 / (1 + np.exp(-logit))).astype(int)
    X = np.c_[tmax, series33, grad48, share65]
    return X, y

def train_logreg(X, y, lr=0.05, epochs=800):
    n, d = X.shape
    w = np.zeros(d); b = 0.0
    for _ in range(epochs):
        z = X @ w + b
        p = 1 / (1 + np.exp(-np.clip(z, -30, 30)))
        g = (p - y) / n
        w -= lr * (X.T @ g)
        b -= lr * g.sum()
    return w, b

def roc_auc(y, score):
    order = np.argsort(score)[::-1]
    y_sorted = y[order]
    tp = np.cumsum(y_sorted); fp = np.cumsum(1 - y_sorted)
    tpr = tp / max(y.sum(), 1); fpr = fp / max((1 - y).sum(), 1)
    return float(np.trapz(np.r_[0, tpr], np.r_[0, fpr]))

if __name__ == "__main__":
    X, y = make_demo_dataset()
    cut = int(len(y) * 0.7)
    w, b = train_logreg(X[:cut], y[:cut])
    score = X[cut:] @ w + b
    print(f"демо-валидация: ROC-AUC = {roc_auc(y[cut:], score):.3f}")
    print("признаки (веса): Tmax %.2f, серия>33°.2f, градиент48 %.2f, доля65+ %.2f" % (*w,))
