# -*- coding: utf-8 -*-
"""МЕДУЗА-АГРО: контроль партий концентрата «АЗОВ-БИО».

Задел проекта. Партия проходит, если сухие вещества, микробиология
и солёность в допуске; солёность критична — морское сырьё.
"""

SV_RANGE = (0.16, 0.20)
SALT_MAX_G_L = 6.0
CFU_MAX = 1_000           # КОЕ/мл, небактериальная норма до разбавления
PH_RANGE = (5.8, 7.2)


def pass_batch(sv: float, salt_g_l: float, cfu: float, ph: float) -> tuple[bool, list[str]]:
    """Возвращает решение по партии и список отклонений."""
    issues = []
    if not (SV_RANGE[0] <= sv <= SV_RANGE[1]):
        issues.append(f"СВ {sv:.2f} вне допуска {SV_RANGE}")
    if salt_g_l > SALT_MAX_G_L:
        issues.append(f"солёность {salt_g_l:.1f} г/л выше {SALT_MAX_G_L}")
    if cfu > CFU_MAX:
        issues.append(f"микробиология {cfu:.0f} КОЕ/мл выше нормы")
    if not (PH_RANGE[0] <= ph <= PH_RANGE[1]):
        issues.append(f"pH {ph:.1f} вне допуска {PH_RANGE}")
    return len(issues) == 0, issues


def dilution_recipe(concentrate_l: float, ratio: int = 500) -> dict:
    """Рабочий раствор для листовой подкормки 1:500."""
    return {
        "концентрат_л": concentrate_l,
        "вода_л": concentrate_l * (ratio - 1),
        "раствор_л": concentrate_l * ratio,
        "норма": "2 л концентрата на гектар за обработку",
    }
