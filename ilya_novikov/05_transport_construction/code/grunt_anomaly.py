# -*- coding: utf-8 -*-
"""ГРУНТ-ЭХО: пороговая классификация скоростных аномалий.

Задел проекта. Уровни: жёлтый δv/v ≤ −2,5 %, красный ≤ −5 %.
Для участка формируется карта аномалий по 28 виртуальным трассам.
"""
from dataclasses import dataclass

YELLOW = -0.025
RED = -0.050
STABILITY_STD_LIMIT = 0.003   # предельная нестабильность базовой линии


@dataclass
class TraceResult:
    pair: tuple[int, int]
    dv: float
    level: str
    chainage_m: float          # пикетаж середины трассы


def classify(dv: float) -> str:
    if dv <= RED:
        return "красный"
    if dv <= YELLOW:
        return "жёлтый"
    return "норма"


def section_report(traces: list[TraceResult], baseline_std: float) -> dict:
    """Заключение по участку: список аномалий и пригодность базовой линии."""
    anomalies = [t for t in traces if t.level in ("жёлтый", "красный")]
    anomalies.sort(key=lambda t: t.dv)
    return {
        "трасс": len(traces),
        "аномалий": len(anomalies),
        "красных": sum(1 for t in anomalies if t.level == "красный"),
        "базовая_линия": "принята" if baseline_std <= STABILITY_STD_LIMIT else "пересчитать",
        "наряд": bool(any(t.level == "красный" for t in traces)),
        "пикеты": [round(t.chainage_m, 1) for t in anomalies],
    }
