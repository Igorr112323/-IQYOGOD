# -*- coding: utf-8 -*-
"""ПЫЛЬЦА-ВЕКС: тревожная логика и формирование протокола-доказательства.

Задел проекта. Тревога — при превышении доли стрессовых пролётов за час;
протокол фиксирует дату, время, геолокацию и сводку спектров.
"""
from dataclasses import dataclass, field
from datetime import datetime

WATCH_SHARE = 0.08          # «внимание»
ALERT_SHARE = 0.18          # «тревога»


@dataclass
class HourSummary:
    hour_start: datetime
    passes_total: int
    passes_stress: int

    @property
    def stress_share(self) -> float:
        return self.passes_stress / max(self.passes_total, 1)


@dataclass
class ApiaryAlert:
    apiary_id: str
    hive_id: str
    raised_at: datetime
    lat: float
    lon: float
    stress_share: float
    spectra_digest: list[float] = field(default_factory=list)


def evaluate_hour(apiary_id: str, hive_id: str, summary: HourSummary,
                  lat: float, lon: float, digest: list[float]) -> str | ApiaryAlert:
    share = summary.stress_share
    if share >= ALERT_SHARE:
        return ApiaryAlert(apiary_id, hive_id, summary.hour_start, lat, lon,
                           round(share, 3), digest[:8])
    if share >= WATCH_SHARE:
        return "внимание"
    return "фон чист"


def alert_registry(alerts: list[ApiaryAlert]) -> dict:
    """Реестр тревожных эпизодов: для минсельхоза и страховых."""
    by_apiary: dict[str, int] = {}
    for a in alerts:
        by_apiary[a.apiary_id] = by_apiary.get(a.apiary_id, 0) + 1
    return {"эпизодов": len(alerts), "пасек": len(by_apiary), "по_пасекам": by_apiary}
