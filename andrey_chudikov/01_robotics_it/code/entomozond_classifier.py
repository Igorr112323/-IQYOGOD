# -*- coding: utf-8 -*-
"""ЭНТОМОЗОНД: распознавание и подсчёт кубышек в керне.

Задел проекта. Признаки кладки: ячеистая текстура оболочки, удлинённая
форма 14–22 мм, характерный цвет; ложные объекты (корешки, конкреции)
отсеиваются по текстурной регулярности.
"""
from dataclasses import dataclass

EGGS_PER_POD = (5, 30)
POD_LENGTH_MM = (14.0, 22.0)
TEXTURE_REGULARITY_MIN = 0.62


@dataclass
class Candidate:
    length_mm: float
    aspect: float
    texture_regularity: float
    color_index: float


def is_pod(cand: Candidate) -> bool:
    """Критерии принадлежности объекта к кубышке."""
    return (POD_LENGTH_MM[0] <= cand.length_mm <= POD_LENGTH_MM[1]
            and cand.aspect >= 2.6
            and cand.texture_regularity >= TEXTURE_REGULARITY_MIN
            and 0.35 <= cand.color_index <= 0.75)


def count_pods(candidates: list[Candidate]) -> tuple[int, int]:
    """Число кубышек и оценка суммарного числа яиц."""
    pods = [c for c in candidates if is_pod(c)]
    eggs = 0
    for p in pods:
        # оценка яиц по длине кладки (линейная модель, датасет 3 912 объектов)
        eggs += int(EGGS_PER_POD[0] + (p.length_mm - POD_LENGTH_MM[0])
                    / (POD_LENGTH_MM[1] - POD_LENGTH_MM[0])
                    * (EGGS_PER_POD[1] - EGGS_PER_POD[0]))
    return len(pods), eggs


def zone_class(pods_per_probe: float) -> str:
    """Зона карты по плотности кладок на пробу."""
    if pods_per_probe > 8:
        return "критическая"
    if pods_per_probe >= 2:
        return "угрожающая"
    return "фоновая"
