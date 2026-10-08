# -*- coding: utf-8 -*-
"""ЭНТОМОЗОНД: цикл отбора пробы и привязка координат.

Задел проекта. Шнековый пробоотборник берёт керн 0–12 см, выкладывает
его в лоток, кадр уходит классификатору; результат пишется с ГЛОНАСС-
координатой в массив маршрута.
"""
from dataclasses import dataclass

CORE_DEPTH_CM = 12
CORE_DIAM_MM = 60
GRID_STEP_FOCUS_M = 25
GRID_STEP_PERIM_M = 100


@dataclass
class ProbeResult:
    lat: float
    lon: float
    pod_count: int
    egg_estimate: int
    depth_cm: float


def grid_points(field_polygon_m: list[tuple[float, float]],
                in_focus_zone: bool) -> list[tuple[float, float]]:
    """Сетка маршрута: шаг 25 м в очаге, 100 м на периферии."""
    step = GRID_STEP_FOCUS_M if in_focus_zone else GRID_STEP_PERIM_M
    xs = [x for x, _ in field_polygon_m]
    ys = [y for _, y in field_polygon_m]
    points = []
    x, y = min(xs), min(ys)
    while y <= max(ys):
        while x <= max(xs):
            points.append((x, y))
            x += step
        x = min(xs)
        y += step
    return points


def probe_cycle(coord: tuple[float, float], classify_frame) -> ProbeResult:
    """Один цикл: бурение → выкладка → съёмка → классификация."""
    frame = acquire_frame()                       # заглушка захвата кадра лотка
    pods, eggs = classify_frame(frame)
    return ProbeResult(lat=coord[0], lon=coord[1],
                       pod_count=pods, egg_estimate=eggs, depth_cm=CORE_DEPTH_CM)


def acquire_frame():
    """Плейсхолдер: кадр камеры лотка (в бортовом исполнении — V4L2)."""
    return None
