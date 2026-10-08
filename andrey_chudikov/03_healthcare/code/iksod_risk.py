# -*- coding: utf-8 -*-
"""ИКСОД-НАДЗОР: расчёт риск-индекса территории.

Задел проекта. Индекс — взвешенная плотность экземпляров на
ловушко-сутки; превышение порога формирует оповещение.
"""

SPECIES_WEIGHTS = {
    "Ixodes": 1.0,
    "Dermacentor": 1.2,
    "Rhipicephalus": 1.2,
    "Hyalomma": 2.5,
    "не идентифицирован": 0.6,
}
ALERT_THRESHOLD = 3.0
WARN_THRESHOLD = 1.5


def risk_index(daily_counts: list[dict], traps: int) -> float:
    """Σ (экземпляры × вес вида) / ловушко-сутки за период."""
    if not daily_counts or traps <= 0:
        return 0.0
    total = 0.0
    for day in daily_counts:
        for species, count in day.items():
            total += count * SPECIES_WEIGHTS.get(species, 0.6)
    return total / (len(daily_counts) * traps)


def status(index: float) -> str:
    if index >= ALERT_THRESHOLD:
        return "оповещение: внеочередная обработка"
    if index >= WARN_THRESHOLD:
        return "наблюдение: повторная оценка через 48 часов"
    return "фоновый режим"


def hyalomma_flag(daily_counts: list[dict]) -> bool:
    """Отдельный флаг: присутствие переносчика КГЛ."""
    return any(day.get("Hyalomma", 0) > 0 for day in daily_counts)
