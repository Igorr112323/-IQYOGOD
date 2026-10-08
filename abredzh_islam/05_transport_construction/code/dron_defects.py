# -*- coding: utf-8 -*-
"""ПРИЁМКА-ДРОН: классификация дефектов по библиотеке типовых признаков.

Задел проекта. Признаки дефекта извлекаются из ортофотоплана;
библиотека наполняется по пилотам.
"""
from dataclasses import dataclass


@dataclass
class DefectCandidate:
    texture_contrast: float    # контраст участка к покрытию
    edge_irregularity: float   # неровность границы участка
    moisture_index: float      # индекс влагонасыщения участка
    area_m2: float


LIBRARY = [
    ("недоукреплённое примыкание", "высокая неровность границы у парапета"),
    ("вздутие кровельного ковра", "тёмные пятна с высоким индексом влаги"),
    ("отсутствующий элемент водоотведения", "разрыв линии желоба на развёртке"),
    ("тип покрытия не соответствует проекту", "текстурный класс вне заявленного"),
]


def classify(candidate: DefectCandidate) -> str:
    """Возвращает тип дефекта или 'норма' по правилам библиотеки."""
    if candidate.moisture_index > 0.6 and candidate.area_m2 > 0.5:
        return "вздутие кровельного ковра"
    if candidate.edge_irregularity > 0.45 and candidate.area_m2 < 2.0:
        return "недоукреплённое примыкание"
    if candidate.texture_contrast > 0.7 and candidate.area_m2 > 5.0:
        return "тип покрытия не соответствует проекту"
    return "норма"


def defect_report(candidates: list[DefectCandidate]) -> dict:
    found = [classify(c) for c in candidates if classify(c) != "норма"]
    return {"дефектов": len(found),
            "типы": sorted(set(found)),
            "рекомендация": "включить в протокол расхождений" if found else "замечаний нет"}
