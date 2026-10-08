# -*- coding: utf-8 -*-
"""ГРУНТ-ЭХО: взаимная корреляция шумовых записей и оценка δv/v.

Задел проекта. Восстановление функции Грина между парой геотелефонов
по шумовому полю трафика; относительное изменение скорости — методом
растяжения кодовой последовательности (stretching).
"""
import numpy as np

FS = 250                 # Гц
WINDOW_S = 3600          # окно корреляции, с
F_BAND = (5.0, 40.0)     # полоса моды Лява, Гц


def cross_correlate(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Нормированная взаимная корреляция записи пары датчиков."""
    a = a - a.mean()
    b = b - b.mean()
    cc = np.correlate(a, b, mode="full") / (len(a) * a.std() * b.std() + 1e-12)
    return cc


def band_filter(cc: np.ndarray, fs: int, band: tuple[float, float]) -> np.ndarray:
    """Полосовая фильтрация коррелограммы (упрощённо, для задела)."""
    n = len(cc)
    freq = np.fft.rfftfreq(n, d=1.0 / fs)
    spec = np.fft.rfft(cc)
    spec[(freq < band[0]) | (freq > band[1])] = 0.0
    return np.fft.irfft(spec, n)


def stretching_dv(cc_now: np.ndarray, cc_ref: np.ndarray,
                  max_eps: float = 0.08, steps: int = 81) -> float:
    """δv/v: растяжение кодовой последовательности до максимума корреляции.

    Отрицательное значение — снижение скорости (вымывание, полость).
    """
    eps_grid = np.linspace(-max_eps, max_eps, steps)
    n = len(cc_ref)
    t = np.arange(n) - n // 2
    best = (float("inf"), 0.0)
    for eps in eps_grid:
        t_stretch = t * (1.0 + eps)
        idx = np.clip((t_stretch + n // 2).astype(int), 0, n - 1)
        score = float(np.sum((cc_now[idx] - cc_ref) ** 2))
        if score < best[0]:
            best = (score, eps)
    return -best[1]    # δv/v ≈ −ε
