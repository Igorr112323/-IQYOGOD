# -*- coding: utf-8 -*-
"""ЭФИР-ДОЖДЬ: перевод затухания сотового канала в интенсивность осадков.

Задел проекта: степенная модель R = a * k^b, калибровка по муниципальным
данным муниципальных дождемеров (модельная калибровочная кампания: июнь-август, 14 станций).
"""
import numpy as np

# калибровочные коэффициенты модели (западный округ Краснодара, синтетическая кампания)
A, B = 0.0042, 1.62
DRY_ATT_DB = 0.35          # базовое затухание сухой атмосферы, дБ


def link_attenuation(rx_level_dbm: float, tx_level_dbm: float,
                     baseline_db: float) -> float:
    """Избыточное затухание линии сверх базового уровня."""
    atten = (tx_level_dbm - rx_level_dbm) - baseline_db
    return max(atten - DRY_ATT_DB, 0.0)


def rain_intensity(attenuation_db: float) -> float:
    """Интенсивность осадков, мм/ч, по степенной модели."""
    if attenuation_db <= 0:
        return 0.0
    return float(A * attenuation_db ** B * 10.0)   # эмпирический масштаб модели


def calibrate(observed_db: list[float], gauge_mm_h: list[float]) -> tuple[float, float]:
    """Подбор (a, b) по парам затухание/доздемер методом наименьших квадратов."""
    x = np.log(np.asarray(observed_db) + 1e-6)
    y = np.log(np.asarray(gauge_mm_h) + 1e-6)
    b, log_a = np.polyfit(x, y, 1)
    return float(np.exp(log_a)), float(b)
