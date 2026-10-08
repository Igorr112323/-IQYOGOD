# -*- coding: utf-8 -*-
"""ФИТОПУЛЬС: Монте-Карло 3 000 сценариев — выручка и окупаемость.

Потоки: продажа опорных точек с установкой, сезонные подписки
на сервис «карта сроков».
"""
import random

random.seed(20260918)

N_SCEN = 3000
START_COST = 5_100_000        # руб.: серия 150 флуориметров, платформа, пилоты

revenues = []
profits = []
payback = []
for _ in range(N_SCEN):
    points = random.triangular(80, 110, 160)
    point_rev = points * random.triangular(320_000, 340_000, 370_000)
    sub_rev = points * random.triangular(38_000, 42_000, 48_000)
    revenue = point_rev + sub_rev
    cost = points * random.triangular(66_000, 74_000, 84_000) + 2_900_000
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
