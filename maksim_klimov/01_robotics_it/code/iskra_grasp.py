# -*- coding: utf-8 -*-
"""ИСКРА-СТОП: планирование захвата объекта манипулятором на движущейся ленте.

Задел проекта: расчёт точки перехвата с учётом скорости конвейера и
цикла манипулятора 0,6 с.
"""
from dataclasses import dataclass

BELT_SPEED = 0.8          # м/с
GRASP_CYCLE_S = 0.6       # полный цикл манипулятора
GRASP_ZONE_START = 0.45   # м от детектора до начала зоны захвата
GRASP_ZONE_LEN = 0.9      # м рабочей зоны


@dataclass
class GraspPlan:
    wait_s: float
    reach_m: float
    feasible: bool


def plan_grasp(detector_to_object_m: float) -> GraspPlan:
    """Когда манипулятору стартовать, чтобы встретить предмет в зоне."""
    time_to_zone = max(0.0, (GRASP_ZONE_START - detector_to_object_m) / BELT_SPEED)
    if time_to_zone < GRASP_CYCLE_S:
        return GraspPlan(0.0, 0.0, feasible=False)   # не успеваем — объект на дробилку
    wait = time_to_zone - GRASP_CYCLE_S
    reach = detector_to_object_m + BELT_SPEED * (wait + GRASP_CYCLE_S)
    feasible = GRASP_ZONE_START <= reach <= GRASP_ZONE_START + GRASP_ZONE_LEN
    return GraspPlan(wait_s=round(wait, 3), reach_m=round(reach, 3), feasible=bool(feasible))


def queue_scheduler(events: list[float]) -> list[int]:
    """Из последовательности событий выбирает захватываемые (без конфликтов цикла)."""
    busy_until = 0.0
    taken = []
    for i, t in enumerate(events):
        if t >= busy_until:
            taken.append(i)
            busy_until = t + GRASP_CYCLE_S
    return taken
