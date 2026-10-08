# -*- coding: utf-8 -*-
"""ЗАМОР-СТОП: тревожная логика и оповещение.

Задел проекта. При превышении порога пост за 60 секунд рассылает
оповещения владельцу водоёма, дежурному ЕДДС и рыбоохране
и прикладывает видеозапись эпизода.
"""
from dataclasses import dataclass, field
from datetime import datetime

ALERT_DEADLINE_SEC = 60


@dataclass
class Alert:
    pond_id: str
    ts: datetime
    rate_per_window: float
    threshold: float
    video_ref: str
    receivers: list[str] = field(default_factory=list)


def should_alert(rate: float, threshold: float) -> bool:
    return rate >= threshold


def build_alert(pond_id: str, ts: datetime, rate: float, threshold: float,
                video_ref: str) -> Alert:
    """Пакет тревоги: получатели по регламенту водоёма."""
    return Alert(
        pond_id=pond_id, ts=ts, rate_per_window=rate, threshold=threshold,
        video_ref=video_ref,
        receivers=["владелец_водоёма", "дежурный_ЕДДС", "рыбоохрана"],
    )


def response_measures(pond_type: str) -> list[str]:
    """Регламент мер по типу водоёма."""
    if pond_type == "платный":
        return ["включить аэраторы", "перевести садки на проток", "замерить кислород"]
    if pond_type == "городской":
        return ["выезд бригады ЕДДС", "отбор проб воды", "оповещение парка"]
    return ["наблюдение с воды", "замер кислорода", "доклад рыбоохране"]
