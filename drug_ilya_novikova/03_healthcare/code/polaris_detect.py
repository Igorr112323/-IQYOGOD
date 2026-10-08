# -*- coding: utf-8 -*-
"""ПОЛЯРИС-БЕРЕГ: детекция погружённого объекта и тревога.

Задел проекта. Кандидаты — компактные области в подповерхностном слое
с оценкой глубины по ослаблению яркости; тревога при подтверждении
трекингом (объект не всплывает 3+ секунд).
"""
from dataclasses import dataclass

DEPTH_MIN, DEPTH_MAX = 0.3, 1.8     # м
STILL_SECONDS = 3.0                 # неподвижность для подтверждения


@dataclass
class Detection:
    x_m: float
    y_m: float
    depth_est_m: float
    still_seconds: float


def depth_from_attenuation(brightness: float, surface_brightness: float,
                           k_water: float = 0.55) -> float:
    """Глубина по ослаблению яркости: I = I0 * exp(-k*z)."""
    import math
    ratio = max(brightness / max(surface_brightness, 1e-6), 1e-6)
    return float(min(max(-math.log(ratio) / k_water, 0.0), DEPTH_MAX + 1.0))


def confirm(track: list[Detection]) -> Detection | None:
    """Подтверждение тревоги: объект погружён и не всплывает."""
    if not track:
        return None
    depths = [d.depth_est_m for d in track]
    durations = [d.still_seconds for d in track]
    if depths[-1] >= DEPTH_MIN and durations[-1] >= STILL_SECONDS:
        return track[-1]
    return None


def alert_payload(det: Detection, post_id: str, ts: str) -> dict:
    """Пакет для дежурного ЕДДС: координаты точки и запись."""
    return {
        "post": post_id,
        "time": ts,
        "point_m": [round(det.x_m, 1), round(det.y_m, 1)],
        "depth_m": round(det.depth_est_m, 2),
        "priority": "красный",
    }
