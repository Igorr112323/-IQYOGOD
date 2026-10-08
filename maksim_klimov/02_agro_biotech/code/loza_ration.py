# -*- coding: utf-8 -*-
"""ЛОЗА-ФУРАЖ: расчёт ввода кормовой добавки из выжимки в рацион стада.

Ввод 8–12 % сухого вещества (СВ) рациона; расчёт потребности партии
и ожидаемого экономического эффекта по продуктивности.
"""
from dataclasses import dataclass

SHARE_MIN, SHARE_MAX = 0.08, 0.12
DM_ADDITIVE = 0.32          # доля сухого вещества в добавке
PRICE_PER_T = 2_900         # руб/т


@dataclass
class Herd:
    cows: int
    avg_milk_kg: float      # кг/день
    dm_intake_kg: float     # потребление СВ, кг/день на голову


def daily_additive_kg(herd: Herd, share: float = SHARE_MIN) -> float:
    share = min(max(share, SHARE_MIN), SHARE_MAX)
    dm_need = herd.cows * herd.dm_intake_kg * share
    return dm_need / DM_ADDITIVE


def seasonal_demand_t(herd: Herd, days: int = 210, share: float = SHARE_MIN) -> float:
    return daily_additive_kg(herd, share) * days / 1000.0


def monthly_spend_t(herd: Herd, share: float = SHARE_MIN) -> float:
    return daily_additive_kg(herd, share) * 30.0 / 1000.0 * PRICE_PER_T


def effect_forecast(herd: Herd) -> dict:
    """Ожидаемый эффект по протоколу: +4,2 % надоя, −11 % затрат на корма."""
    return {
        "milk_gain_kg_day": round(herd.avg_milk_kg * 0.042, 2),
        "feed_cost_change_pct": -11.0,
    }
