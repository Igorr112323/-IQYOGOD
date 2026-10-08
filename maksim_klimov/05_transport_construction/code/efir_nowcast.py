# -*- coding: utf-8 -*-
"""ЭФИР-ДОЖДЬ: детектирование ячеек ливня и очередь нарядов.

Задел проекта: события выделяются по росту производной интенсивности
на кластере линий; наряды ранжируются по близости к критическим
коллекторам открытой схемы сетей водоотведения.
"""
from dataclasses import dataclass

ALERT_MM_H = 18.0          # порог интенсивности для события
DERIV_MM_H2 = 6.0          # рост, мм/ч за минуту
LEAD_MIN = 17              # типовой запас времени до пика подтопления


@dataclass
class RainCell:
    cell_id: str
    intensity_mm_h: float
    derivative: float
    minutes_to_peak: int


@dataclass
class CrewTask:
    cell_id: str
    target: str            # насос / решётка / бригада
    address: str
    lead_min: int


def detect_cells(cell_history: dict[str, list[float]]) -> list[RainCell]:
    """Ячейки ливня из истории интенсивностей по кластерам линий."""
    events = []
    for cid, series in cell_history.items():
        if len(series) < 3:
            continue
        now, prev = series[-1], series[-2]
        deriv = now - prev
        if now >= ALERT_MM_H and deriv >= DERIV_MM_H2:
            events.append(RainCell(cid, round(now, 1), round(deriv, 1), LEAD_MIN))
    return sorted(events, key=lambda c: c.intensity_mm_h, reverse=True)


def build_queue(cells: list[RainCell], critical_assets: dict[str, list[str]]) -> list[CrewTask]:
    """Наряды: на каждую ячейку — ближайшие критические объекты."""
    queue = []
    for cell in cells:
        assets = critical_assets.get(cell.cell_id, [])
        for addr in assets[:2]:
            queue.append(CrewTask(cell.cell_id, "насос/решётка", addr, cell.minutes_to_peak))
    return queue
