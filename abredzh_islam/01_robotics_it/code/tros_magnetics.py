# -*- coding: utf-8 -*-
"""ТРОС-ВЕКС: расчёт потери сечения и обрывов проволок по магнитному потоку.

Задел проекта. Прогон каната через кольцо; базовый поток соответствует
полному сечению, дефицит потока — потере металла (LF), локальные
всплески — обрывам проволок (LMA).
"""
import numpy as np

WIRE_BREAK_SPIKE = 0.045      # относительный всплеск на обрыв проволоки
LF_LIMIT_PCT = 8.0            # предел потери сечения по регламенту


def loss_of_section(flux_series: np.ndarray, baseline_flux: float) -> float:
    """LF, %: средний дефицит потока относительно базового сечения."""
    if baseline_flux <= 0:
        return 0.0
    deficit = 1.0 - float(np.median(flux_series)) / baseline_flux
    return round(max(deficit, 0.0) * 100, 2)


def count_wire_breaks(flux_series: np.ndarray, baseline_flux: float) -> int:
    """LMA: число локальных всплесков выше порога."""
    rel = np.abs(flux_series - baseline_flux) / baseline_flux
    peaks = 0
    above = False
    for v in rel:
        if v >= WIRE_BREAK_SPIKE and not above:
            peaks += 1
            above = True
        elif v < WIRE_BREAK_SPIKE * 0.6:
            above = False
    return peaks


def section_status(lf_pct: float, lma: int) -> str:
    """Статус каната по тренду для телеметрии."""
    if lf_pct >= LF_LIMIT_PCT * 0.8 or lma >= 6:
        return "критический: планировать замену"
    if lf_pct >= LF_LIMIT_PCT * 0.5 or lma >= 3:
        return "наблюдение: внеочередной осмотр"
    return "в ресурсе"
