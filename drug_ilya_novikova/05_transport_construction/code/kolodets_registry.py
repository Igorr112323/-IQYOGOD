# -*- coding: utf-8 -*-
"""КОЛОДЕЦ-ТРАССА: сверка найденных люков с реестрами и нарядная цепочка.

Задел проекта. Люк вне всех реестров получает статус «ничий» и уходит
в публичную карту с назначением ответственного.
"""
from dataclasses import dataclass

MATCH_RADIUS_M = 2.5


@dataclass
class FoundLid:
    coord_m: tuple[float, float]
    condition: str          # "цела" | "смещена" | "разрушена" | "отсутствует"


def match_registry(lid: FoundLid, registry: list[tuple[float, float, str]]) -> str | None:
    """Возвращает владельца из реестра, если люк найден в радиусе."""
    for rx, ry, owner in registry:
        d = ((lid.coord_m[0] - rx) ** 2 + (lid.coord_m[1] - ry) ** 2) ** 0.5
        if d <= MATCH_RADIUS_M:
            return owner
    return None


def build_map(lids: list[FoundLid], registries: list[list[tuple]]) -> dict:
    """Карта района: реестровые, «ничьи» и опасные объекты."""
    registered, orphaned, dangerous = [], [], []
    for lid in lids:
        owner = None
        for reg in registries:
            owner = match_registry(lid, reg)
            if owner:
                break
        if owner:
            registered.append((lid, owner))
        else:
            orphaned.append(lid)
        if lid.condition in ("смещена", "разрушена", "отсутствует"):
            dangerous.append(lid)
    return {"в реестре": len(registered),
            "ничьи": len(orphaned),
            "опасные": [d.coord_m for d in dangerous]}


def dispatch_order(dangerous: FoundLid) -> dict:
    """Наряд коммунальной службе: норматив закрытия — 6 часов."""
    return {"объект": dangerous.coord_m,
            "состояние": dangerous.condition,
            "срок_часов": 6,
            "исполнитель": "коммунальная служба района"}
