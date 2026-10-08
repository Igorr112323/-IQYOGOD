# -*- coding: utf-8 -*-
"""ФИТОПУЛЬС: стресс-индекс опорной точки по кривой индукции флуоресценции.

Задел проекта. Эффект Каутского: при водном стрессе падает
коэффициент переменной флуоресценции Fv/Fm.
"""
import numpy as np


def f_v_over_f_m(induction_curve: np.ndarray) -> float:
    """Fv/Fm = (Fm - F0) / Fm по кривой индукции."""
    f0 = float(np.percentile(induction_curve, 5))
    fm = float(induction_curve.max())
    if fm <= f0:
        return 0.0
    return (fm - f0) / fm


def stress_index(fvfm: float, norm_fvfm: float, phase_tol: float = 0.03) -> str:
    """Класс состояния относительно нормы культуры и фазы."""
    if fvfm < norm_fvfm - 2 * phase_tol:
        return "стресс"
    if fvfm < norm_fvfm - phase_tol:
        return "предстресс"
    return "норма"


def early_alert(series_fvfm: list[float], norm: float, window: int = 6) -> bool:
    """Ранняя тревога: устойчивое падение за 3–6 суток до видимых признаков."""
    if len(series_fvfm) < window:
        return False
    recent = np.array(series_fvfm[-window:])
    return bool(recent.mean() < norm - 0.03 and recent[-1] < recent[0] - 0.02)
