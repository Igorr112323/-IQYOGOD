# -*- coding: utf-8 -*-
"""КАПСУЛА-ЩИТ: расстановка капсул по карте терморазогрева тела полигона.

Задел проекта. Сетка с шагом 6 м; зоны с расчётным разогревом
уплотняются до шага 3 м.
"""
from dataclasses import dataclass

STEP_BASE_M = 6.0
STEP_DENSE_M = 3.0
HOTSPOT_C = 60.0          # расчётная температура риска


@dataclass
class Capsule:
    x_m: float
    y_m: float
    zone: str


def heatmap_cell(x: float, y: float, hotspots: list[tuple[float, float, float]]) -> float:
    """Упрощённая оценка разогрева: обратное расстояние до очагов риска."""
    t = 35.0
    for hx, hy, power in hotspots:
        d = max(((x - hx) ** 2 + (y - hy) ** 2) ** 0.5, 1.0)
        t += power / d
    return t


def plan_grid(length_m: float, width_m: float,
              hotspots: list[tuple[float, float, float]]) -> list[Capsule]:
    """План расстановки для карты полигона."""
    capsules: list[Capsule] = []
    y = 0.0
    while y <= width_m:
        x = 0.0
        while x <= length_m:
            t = heatmap_cell(x, y, hotspots)
            dense = t >= HOTSPOT_C
            capsules.append(Capsule(x, y, "плотная" if dense else "базовая"))
            x += STEP_DENSE_M if dense else STEP_BASE_M
        y += STEP_BASE_M
    return capsules
