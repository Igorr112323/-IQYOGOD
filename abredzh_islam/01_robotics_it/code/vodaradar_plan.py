# -*- coding: utf-8 -*-
"""ВОДА-РАДАР: приоритизация участков для производственных программ.

Задел проекта. Ранжирование аномальных участков по скорости оседания
и аварийной истории; вывод — обоснование переноса средств
с аварийного ремонта на плановый.
"""
from dataclasses import dataclass


@dataclass
class Segment:
    route_km: float
    vel_mm_year: float
    accidents_5y: int
    pipe_diameter_mm: int


def risk_score(seg: Segment) -> float:
    """Скорость оседания + история аварий + диаметр трубы."""
    return seg.vel_mm_year * (1 + 0.4 * seg.accidents_5y) + seg.pipe_diameter_mm / 500.0


def prioritize(segments: list[Segment], budget_rub: float,
               repair_cost_per_km_rub: float = 6_500_000) -> dict:
    ranked = sorted(segments, key=risk_score, reverse=True)
    chosen, spent = [], 0.0
    for seg in ranked:
        cost = repair_cost_per_km_rub
        if spent + cost <= budget_rub:
            chosen.append(seg)
            spent += cost
    return {
        "приоритетные_участки": [s.route_km for s in chosen],
        "освоение_бюджета": spent,
        "остаток": budget_rub - spent,
    }


def kpi_report(segments: list[Segment]) -> dict:
    """КПЭ для годового регламентного отчёта контракта."""
    anomalies = [s for s in segments if s.vel_mm_year >= 8.0]
    return {
        "участков_в_мониторинге": len(segments),
        "аномалий": len(anomalies),
        "доля_с_историей_аварий": (
            sum(1 for s in anomalies if s.accidents_5y > 0) / max(len(anomalies), 1)
        ),
    }
