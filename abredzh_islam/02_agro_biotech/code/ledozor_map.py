# -*- coding: utf-8 -*-
"""ЛЕДОЗОР: карта поля и зоны управленческих решений.

Задел проекта. По данным радиометрического обследования строится карта
поля с ячейкой 10 м и зоны решений: разрушение притёртой корки /
наблюдение / норма. Воспроизводит сводку пилота январь — февраль 2026:
три хозяйства северной зоны, 2 400 га обследования.
"""
import random

CELL_M = 10.0          # ячейка карты, м
CRUST_DANGER_CM = 2.0  # порог опасности притёртой корки


def classify_cell(snow_cm: float, ice_cm: float, crust: str) -> str:
    """Классификация ячейки карты."""
    if crust == "притёртая" and ice_cm >= CRUST_DANGER_CM:
        return "РАЗРУШИТЬ"      # кольчато-шпоровые бороны
    if crust in ("притёртая", "висячая"):
        return "НАБЛЮДАТЬ"      # повторный проход через 7–10 дней
    return "НОРМА"


def build_field(ha: float, crust_share: float, seed: int) -> dict:
    """Синтез поля: равномерная сетка, очаги корки по долям."""
    rng = random.Random(seed)
    n = int(ha * 10_000 / CELL_M ** 2)
    side = int(n ** 0.5)
    zones = {"РАЗРУШИТЬ": 0, "НАБЛЮДАТЬ": 0, "НОРМА": 0}
    for _ in range(side * side):
        if rng.random() < crust_share:
            ice = rng.choice([2.0, 2.5, 3.0, 3.5, 4.0])
            crust = rng.choice(["притёртая", "притёртая", "висячая"])
            snow = rng.choice([0, 2, 4])
        else:
            ice, crust = 0.0, "нет"
            snow = rng.choice([6, 8, 10, 12, 15])
        zones[classify_cell(snow, ice, crust)] += 1
    area_cell = CELL_M ** 2 / 10_000.0
    return {k: round(v * area_cell, 1) for k, v in zones.items()}


if __name__ == "__main__":
    # пилотные поля: КФХ «Агро-Север», ООО «Кубанская нива», СПК «Рассвет»
    fields = [
        ("КФХ «Агро-Север»", 900, 0.265, 20260101),
        ("ООО «Кубанская нива»", 820, 0.22, 20260102),
        ("СПК «Рассвет»", 680, 0.135, 20260103),
    ]
    total = {"РАЗРУШИТЬ": 0.0, "НАБЛЮДАТЬ": 0.0, "НОРМА": 0.0}
    surveyed = 0.0
    print("Карта зон решений, пилот январь — февраль 2026")
    for name, ha, share, seed in fields:
        z = build_field(ha, share, seed)
        surveyed += ha
        print(f"{name}: обследовано {ha:.0f} га — "
              f"разрушить {z['РАЗРУШИТЬ']} га, наблюдать {z['НАБЛЮДАТЬ']} га, "
              f"норма {z['НОРМА']} га")
        for k in total:
            total[k] += z[k]
    print(f"ИТОГО обследовано: {surveyed:.0f} га")
    print(f"К разрушению корки: {total['РАЗРУШИТЬ']:.0f} га "
          f"(притёртая ≥ {CRUST_DANGER_CM} см), "
          f"к наблюдению: {total['НАБЛЮДАТЬ']:.0f} га")
