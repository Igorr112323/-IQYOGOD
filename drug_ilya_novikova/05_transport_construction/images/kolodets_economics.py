# -*- coding: utf-8 -*-
"""КОЛОДЕЦ-ТРАССА: Монте-Карло 3 000 сценариев — выручка и окупаемость.

Потоки: муниципальные обследования, годовые обновления карты,
обследования застройщиков, подписки ресурсоснабжающих организаций.
"""
import random

random.seed(20260927)

N_SCEN = 3000
START_COST = 3_400_000        # руб.: три съёмочных комплекта, ПО, пилоты

revenues = []
profits = []
payback = []
for _ in range(N_SCEN):
    districts = random.triangular(6, 10, 16)               # обследований районов
    survey_rev = districts * random.triangular(390_000, 420_000, 460_000)
    updates = districts * random.betavariate(5, 5) * random.triangular(170_000, 190_000, 220_000)
    builders = random.triangular(4, 9, 16) * random.triangular(105_000, 120_000, 140_000)
    subs = random.triangular(2, 4, 7) * random.triangular(220_000, 280_000, 360_000)
    revenue = survey_rev + updates + builders + subs
    cost = districts * random.triangular(150_000, 180_000, 210_000) + 2_300_000
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
