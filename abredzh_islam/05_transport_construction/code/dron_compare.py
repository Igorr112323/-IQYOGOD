# -*- coding: utf-8 -*-
"""ПРИЁМКА-ДРОН: сверка фактического исполнения с проектной документацией.

Задел проекта. Контролируемые параметры: тип кровельного покрытия,
границы отремонтированных участков, водоотводящие элементы.
"""
from dataclasses import dataclass


@dataclass
class ProjectSpec:
    roof_material: str
    roof_area_m2: float
    gutters_count: int
    work_zones: list[tuple[float, float]]   # полигоны границ работ


@dataclass
class FactModel:
    roof_material: str
    roof_area_m2: float
    gutters_count: int
    work_zones: list[tuple[float, float]]


@dataclass
class Discrepancy:
    parameter: str
    project_value: str
    fact_value: str
    severity: str          # "устранить" | "замечание" | "удержание"


def zone_coverage(project: ProjectSpec, fact: FactModel) -> float:
    """Доля проектных границ работ, покрытая фактом (упрощённо)."""
    if not project.work_zones:
        return 1.0
    matched = sum(1 for z in project.work_zones if z in fact.work_zones)
    return matched / len(project.work_zones)


def compare(project: ProjectSpec, fact: FactModel) -> list[Discrepancy]:
    out: list[Discrepancy] = []
    if fact.roof_material != project.roof_material:
        out.append(Discrepancy("тип покрытия", project.roof_material,
                               fact.roof_material, "удержание"))
    area_dev = abs(fact.roof_area_m2 - project.roof_area_m2) / project.roof_area_m2
    if area_dev > 0.05:
        out.append(Discrepancy("площадь работ", f"{project.roof_area_m2:.0f} м²",
                               f"{fact.roof_area_m2:.0f} м²", "устранить"))
    if fact.gutters_count < project.gutters_count:
        out.append(Discrepancy("водоотведение", str(project.gutters_count),
                               str(fact.gutters_count), "устранить"))
    coverage = zone_coverage(project, fact)
    if coverage < 1.0:
        sev = "устранить" if coverage < 0.8 else "замечание"
        out.append(Discrepancy("границы работ", "100 % проектных зон",
                               f"{coverage:.0%}", sev))
    return out


def acceptance_protocol(discrepancies: list[Discrepancy], house_id: str) -> dict:
    """Протокол для приобщения к акту приёмки."""
    return {
        "дом": house_id,
        "расхождений": len(discrepancies),
        "к_устранению": [d.parameter for d in discrepancies if d.severity == "устранить"],
        "к_удержанию": [d.parameter for d in discrepancies if d.severity == "удержание"],
        "статус_приёмки": "условная" if discrepancies else "подтверждена",
    }
