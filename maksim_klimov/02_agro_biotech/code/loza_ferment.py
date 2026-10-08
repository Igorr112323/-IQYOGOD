# -*- coding: utf-8 -*-
"""ЛОЗА-ФУРАЖ: трекер ферментации партии выжимки.

Контроль рН и температуры контейнера; решение о готовности партии.
Задел проекта, исполнялся на контейнерах-прототипах (сезон-2026).
"""
from dataclasses import dataclass, field
from datetime import datetime

PH_READY_MAX = 4.2
PH_READY_MIN = 3.8
TEMP_MAX_C = 32.0
MIN_DAYS = 21


@dataclass
class Batch:
    batch_id: str
    winery: str
    filled_at: datetime
    ph_log: list[float] = field(default_factory=list)
    temp_log: list[float] = field(default_factory=list)


class FermentTracker:
    def __init__(self) -> None:
        self.batches: dict[str, Batch] = {}

    def register(self, batch: Batch) -> None:
        self.batches[batch.batch_id] = batch

    def push(self, batch_id: str, ph: float, temp_c: float) -> None:
        b = self.batches[batch_id]
        b.ph_log.append(ph)
        b.temp_log.append(temp_c)

    def status(self, batch_id: str, now: datetime) -> str:
        b = self.batches[batch_id]
        days = (now - b.filled_at).days
        if not b.ph_log:
            return "нет данных"
        if max(b.temp_log[-24:], default=0.0) > TEMP_MAX_C:
            return "ТРЕВОГА: перегрев"
        if days >= MIN_DAYS and PH_READY_MIN <= b.ph_log[-1] <= PH_READY_MAX:
            return "ГОТОВА К ОТГРУЗКЕ"
        if days >= MIN_DAYS and b.ph_log[-1] > PH_READY_MAX:
            return "доферментировать"
        return f"ферментация, день {days}"
