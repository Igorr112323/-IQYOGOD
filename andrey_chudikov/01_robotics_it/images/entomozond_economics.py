# -*- coding: utf-8 -*-
"""ЭНТОМОЗОНД: Монте-Карло 3 000 сценариев — выручка и окупаемость.

Случайные величины: обследованная площадь за сезон, доля подписных
контрактов, площадь плавневых участков с ограниченной проходимостью.
"""
import random

random.seed(20261009)

N_SCEN = 3000
START_COST = 4_600_000        # руб.: два серийных комплекса, датасет, полевой регламент

revenues = []
profits = []
payback = []
for _ in range(N_SCEN):
    area_ha = random.triangular(6000, 8000, 12000)          # га в сезон, два комплекса
    price = random.triangular(880, 905, 940)                # руб./га
    survey_rev = area_ha * price
    season_subs = random.triangular(2.5, 4, 6) * random.triangular(340_000, 380_000, 430_000)
    revenue = survey_rev + season_subs
    cost = area_ha * random.triangular(482, 512, 548) + 2_140_000
    profit = revenue - cost
    revenues.append(revenue)
    profits.append(profit)
    payback.append(START_COST / max(profit / 12, 1))

revenues.sort(); profits.sort(); payback.sort()

def pct(v, p):
    return v[int(len(v) * p)]

print(f"Сценариев: {N_SCEN}")
print(f"Выручка, млн руб/год: медиана {pct(revenues,0.5)/1e6:.2f}; Q75 {pct(revenues,0.75)/1e6:.2f}")
print(f"Прибыль, млн руб/год: медиана {pct(profits,0.5)/1e6:.2f}")
print(f"Окупаемость, мес: медиана {pct(payback,0.5):.1f}; 95-й процентиль {pct(payback,0.95):.1f}")
print(f"Доля сценариев с окупаемостью < 24 мес: {sum(1 for m in payback if m < 24)/N_SCEN:.2f}")
