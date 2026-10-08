# -*- coding: utf-8 -*-
"""КОЛОДЕЦ-ТРАССА: детектирование магнитных аномалий люков.

Задел проекта. Квантовый магнитометр на штанге внедорожника;
аномалия люка — симметричный пик 200–3000 нТл, арматура плит
отсеивается по форме сигнала.
"""
import numpy as np

PEAK_MIN_NT = 200.0
PEAK_MAX_NT = 3000.0
BASELINE_WIN = 40            # точек скользящего базового уровня


def detrend(trace_nt: np.ndarray) -> np.ndarray:
    """Убираем медленный дрейф поля Земли скользящей медианой."""
    out = np.empty_like(trace_nt)
    half = BASELINE_WIN // 2
    for i in range(len(trace_nt)):
        lo, hi = max(0, i - half), min(len(trace_nt), i + half)
        out[i] = trace_nt[i] - np.median(trace_nt[lo:hi])
    return out


def classify_peak(segment_nt: np.ndarray) -> str:
    """Форма пика: люк — симметричный; арматура — асимметрия/плато."""
    seg = segment_nt - segment_nt.min()
    if seg.max() < PEAK_MIN_NT or seg.max() > PEAK_MAX_NT:
        return "шум"
    peak = int(np.argmax(seg))
    left, right = seg[:peak], seg[peak + 1:]
    if left.size < 3 or right.size < 3:
        return "шум"
    symmetry = abs(left.mean() - right.mean()) / max(seg.mean(), 1e-6)
    plateau = (seg > 0.8 * seg.max()).mean()
    if symmetry < 0.25 and plateau < 0.35:
        return "люк"
    return "арматура"


def scan_route(trace_nt: np.ndarray, coords_m: np.ndarray,
               sample_step_m: float = 0.5) -> list[dict]:
    """Проход по трассе: список найденных люков с координатами."""
    detrended = detrend(trace_nt)
    found = []
    i = 0
    while i < len(detrended):
        if abs(detrended[i]) >= PEAK_MIN_NT:
            j = i
            while j < len(detrended) and abs(detrended[j]) >= PEAK_MIN_NT * 0.5:
                j += 1
            kind = classify_peak(detrended[max(0, i - 5):j + 5])
            if kind == "люк":
                mid = (i + j) // 2
                found.append({"coord_m": coords_m[mid],
                              "peak_nt": float(detrended[i:j + 1].max())})
            i = j
        else:
            i += 1
    return found
