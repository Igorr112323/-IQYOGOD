# -*- coding: utf-8 -*-
"""ВОДА-РАДАР: конвейер интерферометрической обработки вдоль трассы.

Задел проекта. Ряды скоростей оседания по оси водовода:
аномалия — устойчивое превышение фонового темпа.
"""
import numpy as np

BACKGROUND_MM_YEAR = 4.0
ANOMALY_MM_YEAR = 8.0


def velocity_series(displacements_mm: np.ndarray, dates_days: np.ndarray) -> float:
    """Скорость оседания, мм/год: линейная регрессия по датам."""
    if len(displacements_mm) < 6:
        return 0.0
    slope = np.polyfit(dates_days, displacements_mm, 1)[0]
    return float(slope * 365.25)


def classify_segment(vel_mm_year: float) -> str:
    if vel_mm_year >= ANOMALY_MM_YEAR:
        return "приоритет ремонта"
    if vel_mm_year >= 5.0:
        return "наблюдение"
    return "фон"


def process_route(node_disp_mm: list[np.ndarray], node_dates: np.ndarray,
                  node_km: list[float]) -> list[dict]:
    """Пасс по узлам оси водовода: скорость и класс для каждого участка."""
    results = []
    for km, series in zip(node_km, node_disp_mm):
        vel = velocity_series(series, node_dates)
        results.append({
            "км_трассы": round(km, 2),
            "скорость_мм_год": round(vel, 1),
            "класс": classify_segment(vel),
        })
    return results


def anomalies_above_background(route: list[dict]) -> list[dict]:
    return [seg for seg in route if seg["скорость_мм_год"] >= ANOMALY_MM_YEAR]
