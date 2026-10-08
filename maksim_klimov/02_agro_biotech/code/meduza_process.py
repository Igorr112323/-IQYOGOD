# -*- coding: utf-8 -*-
"""МЕДУЗА-АГРО: управление циклом переработки комплекса «АЗОВ-М1».

Задел проекта. Цикл: приём биомассы → обезвоживание → кавитационный
гидролиз → концентрирование. Ограничение: старт гидролиза не позже
2 часов с момента сбора (автолиз биомассы).
"""
from dataclasses import dataclass

MAX_LAG_HOURS = 2.0
PRESS_MOISTURE_TARGET = 0.62
HYDROLYSIS_C = 45.0
HYDROLYSIS_HOURS = 6.0
CONCENTRATE_SV = 0.18


@dataclass
class Batch:
    biomass_kg: float
    collected_at_h: float
    press_started_at_h: float


def press_output(batch: Batch) -> float:
    """Масса жидкой фракции после циклон-пресса (−38 % массы)."""
    return batch.biomass_kg * 0.62


def hydrolysis_ready(batch: Batch) -> bool:
    """Гидролиз должен стартовать не позже 2 часов после сбора."""
    return (batch.press_started_at_h - batch.collected_at_h) <= MAX_LAG_HOURS


def concentrate_volume(batch: Batch, yield_l_per_t: float = 114.0) -> float:
    """Выход концентрата, л: расчётная норма 114 л/т биомассы."""
    return batch.biomass_kg / 1000.0 * yield_l_per_t


def daily_capacity(batches: list[Batch]) -> dict:
    """Суточная сводка комплекса."""
    total_kg = sum(b.biomass_kg for b in batches)
    violations = [b for b in batches if not hydrolysis_ready(b)]
    return {
        "биомасса_т": round(total_kg / 1000, 2),
        "концентрат_л": round(sum(concentrate_volume(b) for b in batches), 0),
        "нарушений_тайминга": len(violations),
    }
