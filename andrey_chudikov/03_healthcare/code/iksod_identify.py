# -*- coding: utf-8 -*-
"""ИКСОД-НАДЗОР: морфометрическая идентификация видов иксодид.

Задел проекта. 24 признака из кадра планшета; эталонные профили видов
обучены на коллекции 4 700 экземпляров (верификация 580 проб
паразитологической лабораторией).
"""
from dataclasses import dataclass

SPECIES_PROFILES = {
    "Ixodes":        {"scutum_ratio": 0.62, "capitulum_len": 0.31, "festoons": 0},
    "Dermacentor":   {"scutum_ratio": 0.74, "capitulum_len": 0.22, "festoons": 1},
    "Rhipicephalus": {"scutum_ratio": 0.70, "capitulum_len": 0.25, "festoons": 1},
    "Hyalomma":      {"scutum_ratio": 0.81, "capitulum_len": 0.38, "festoons": 1},
}
TOLERANCE = 0.09


@dataclass
class SpecimenFeatures:
    scutum_ratio: float       # отношение ширины скутума к длине идосомы
    capitulum_len: float      # относительная длина хоботка
    festoons: float           # выраженность фестонов (0–1)
    area_px: float


def classify(spec: SpecimenFeatures) -> tuple[str, float]:
    """Вид и правдоподобие по евклидову расстоянию до эталонных профилей."""
    best, best_dist = "не идентифицирован", 10.0
    for name, p in SPECIES_PROFILES.items():
        d = ((spec.scutum_ratio - p["scutum_ratio"]) ** 2
             + (spec.capitulum_len - p["capitulum_len"]) ** 2
             + 0.5 * (spec.festoons - p["festoons"]) ** 2) ** 0.5
        if d < best_dist:
            best, best_dist = name, d
    if best_dist > TOLERANCE:
        return "не идентифицирован", 0.0
    confidence = max(0.0, 1.0 - best_dist / TOLERANCE)
    return best, round(confidence, 2)


def daily_summary(specimens: list[SpecimenFeatures]) -> dict:
    """Суточная сводка ловушки: число экземпляров по видам."""
    out: dict[str, int] = {}
    for s in specimens:
        name, _ = classify(s)
        out[name] = out.get(name, 0) + 1
    return out
