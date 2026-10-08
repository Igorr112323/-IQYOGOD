# -*- coding: utf-8 -*-
"""ФИТОПУЛЬС: карта сроков полива и уборки по данным опорных точек.

Задел проекта. Сервис раз в 3 суток объединяет стресс-индексы точек,
прогноз погоды и режим мелиоративной системы.
"""
from dataclasses import dataclass


@dataclass
class Point:
    point_id: str
    f_v_f_m: float
    norm: float
    moisture_fc: float        # влажность почвы, доля НВ


def irrigation_call(p: Point, forecast_days_dry: int) -> tuple[bool, str]:
    """Решение по поливу для опорной точки."""
    if p.f_v_f_m < p.norm - 0.06 or p.moisture_fc < 0.55:
        return True, "полив в ближайшие 48 часов"
    if p.f_v_f_m < p.norm - 0.03 and forecast_days_dry >= 4:
        return True, "полив планово, до суховея"
    return False, "без полива"


def harvest_window(p: Point, days_since_stress: int) -> bool:
    """Окно уборки: поле вышло из стрессового коридора."""
    return p.f_v_f_m < p.norm - 0.02 and days_since_stress >= 10


def schedule_map(points: list[Point], forecast_days_dry: int) -> dict:
    schedule = {}
    for p in points:
        call, reason = irrigation_call(p, forecast_days_dry)
        schedule[p.point_id] = {"полив": call, "основание": reason}
    return schedule
