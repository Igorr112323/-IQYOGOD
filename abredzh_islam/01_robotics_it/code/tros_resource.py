# -*- coding: utf-8 -*-
"""ТРОС-ВЕКС: ресурсная модель каната и прогноз остаточного ресурса.

Задел проекта. Тренд потери сечения экстраполируется с поправкой
на интенсивность использования лифта (поездки в сутки).
"""

DESIGN_LIFE_YEARS = 18.0
LF_LIMIT_PCT = 8.0
TRIPS_PER_DAY_NORM = 900.0


def remaining_life_years(lf_pct: float, lf_rate_pct_year: float,
                         trips_per_day: float) -> float:
    """Остаточный ресурс, лет: линейная экстраполяция тренда."""
    if lf_rate_pct_year <= 0:
        return DESIGN_LIFE_YEARS
    load_factor = trips_per_day / TRIPS_PER_DAY_NORM
    rate = lf_rate_pct_year * max(load_factor, 0.5)
    return max((LF_LIMIT_PCT - lf_pct) / rate, 0.0)


def yearly_report(monthly_lf_pct: list[float], trips_per_day: float) -> dict:
    """Годовой отчёт для управляющей организации и регоператора."""
    if len(monthly_lf_pct) < 2:
        return {"статус": "нет данных для тренда"}
    rate = (monthly_lf_pct[-1] - monthly_lf_pct[0]) / (len(monthly_lf_pct) - 1) * 12
    remaining = remaining_life_years(monthly_lf_pct[-1], rate, trips_per_day)
    return {
        "текущая_потеря_сечения_пц": round(monthly_lf_pct[-1], 2),
        "скорость_износа_пц_год": round(rate, 2),
        "остаточный_ресурс_лет": round(remaining, 1),
        "рекомендация": ("плановая замена в горизонте 3 лет"
                          if remaining < 3 else "эксплуатация по тренду"),
    }
