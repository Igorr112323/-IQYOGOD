# -*- coding: utf-8 -*-
"""КАПСУЛА-ЩИТ: контроль активаций капсульной сети и оповещение.

Задел проекта. Каждая активация капсулы приходит радиометкой;
система строит карту статуса и уведомляет оператора и МЧС.
"""
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class ActivationEvent:
    capsule_id: str
    ts: datetime
    x_m: float
    y_m: float


@dataclass
class NetworkState:
    total_capsules: int
    events: list[ActivationEvent] = field(default_factory=list)

    def register(self, ev: ActivationEvent) -> None:
        self.events.append(ev)

    def status_map(self) -> dict:
        activated = {ev.capsule_id for ev in self.events}
        return {
            "всего": self.total_capsules,
            "активировано": len(activated),
            "в строю": self.total_capsules - len(activated),
        }

    def cluster_alerts(self, radius_m: float = 10.0) -> list[list[ActivationEvent]]:
        """Кластеризация активаций: два срабатывания рядом — крупный очаг."""
        clusters: list[list[ActivationEvent]] = []
        for ev in sorted(self.events, key=lambda e: e.ts):
            placed = False
            for cl in clusters:
                base = cl[0]
                if ((ev.x_m - base.x_m) ** 2 + (ev.y_m - base.y_m) ** 2) ** 0.5 <= radius_m:
                    cl.append(ev)
                    placed = True
                    break
            if not placed:
                clusters.append([ev])
        return [cl for cl in clusters if len(cl) >= 2]


def notify(state: NetworkState) -> list[str]:
    """Оповещения: оператор полигона — на каждую активацию, МЧС — на кластер."""
    msgs = [f"Оператору: активация {ev.capsule_id} в ({ev.x_m:.0f},{ev.y_m:.0f})"
            for ev in state.events]
    if state.cluster_alerts():
        msgs.insert(0, "МЧС: кластер активаций — крупный очаг, выезд бригады")
    return msgs
