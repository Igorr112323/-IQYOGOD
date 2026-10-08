# -*- coding: utf-8 -*-
"""ПРИЁМКА-ДРОН: Монте-Карло 3 000 сценариев — выручка и окупаемость.

Потоки: приёмка домов по 95 тыс. руб., повторные облёты через год,
муниципальные заказы.
"""
import random

random.seed(20261006)

N_SCEN = 3000
START_COST = 3_900_000        # руб.: два БПЛА, станция, фотограмметрия, пилоты

revenues = []
profits = []
payback = []
for _ in range(N_SCEN):
    houses = random.triangular(70, 95, 140)
    accept_rev = houses * random.triangular(90_000, 95_000, 104_000)
    recheck = houses * random.betavariate(3, 7) * random.triangular(32_000, 35_000, 40_000)
    municipal = random.triangular(0, 1_100_000, 2_000_000)
    revenue = accept_rev + recheck + municipal
    cost = houses * random.triangular(30_000, 36_000, 44_000) + 2_300_000
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
