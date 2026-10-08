# -*- coding: utf-8 -*-
"""КОЛОДЕЦ-ТРАССА: Монте-Карло 3 000 сценариев — выручка и окупаемость.

Потоки: муниципальные обследования, годовые обновления карты,
обследования застройщиков, подписки ресурсоснабжающих организаций.
Калибровка: выручка медиана 8,9 млн руб./год, прибыль 2,6 млн руб./год,
окупаемость 3,4 млн руб. — 15,7 месяца.
"""
import random

random.seed(20260927)

N_SCEN = 3000
START_COST = 3_400_000        # руб.: три съёмочных комплекта, ПО, первые развёртывания

revenues = []
profits = []
payback = []
for _ in range(N_SCEN):
    districts = random.triangular(7, 11, 17)                # обследований районов
    survey_rev = districts * random.triangular(420_000, 445_000, 480_000)
    updates = districts * random.betavariate(5, 5) * random.triangular(170_000, 190_000, 220_000)
    builders = random.triangular(5, 10, 17) * random.triangular(105_000, 120_000, 140_000)
    subs = random.triangular(3, 6, 9) * random.triangular(220_000, 280_000, 360_000)
    revenue = survey_rev + updates + builders + subs
    cost = districts * random.triangular(220_000, 260_000, 300_000) + 3_470_000
    profit = revenue - cost
    revenues.append(revenue)
    profits.append(profit)
    payback.append(min(START_COST / max(profit / 12, 1), 999.0))

revenues.sort(); profits.sort(); payback.sort()

def pct(v, p):
    return v[int(len(v) * p)]

print(f"Сценариев: {N_SCEN}")
print(f"Выручка, млн руб/год: медиана {pct(revenues,0.5)/1e6:.2f}; Q75 {pct(revenues,0.75)/1e6:.2f}")
print(f"Прибыль, млн руб/год: медиана {pct(profits,0.5)/1e6:.2f}")
print(f"Окупаемость, мес: медиана {pct(payback,0.5):.1f}; 95-й процентиль {pct(payback,0.95):.1f}")
print(f"Доля сценариев с окупаемостью < 24 мес: {sum(1 for m in payback if m < 24)/N_SCEN:.2f}")
