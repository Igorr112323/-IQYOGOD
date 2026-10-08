# -*- coding: utf-8 -*-
"""КАПСУЛА-ЩИТ: Монте-Карло 3 000 сценариев — выручка и окупаемость.

Случайные величины: число оснащённых карт в год, цена сети,
обслуживание контрольной сети, пилотные оснащения.
"""
import random

random.seed(20260906)

N_SCEN = 3000
START_COST = 4_400_000        # руб.: серия 2 000 капсул, оснастка, испытания

revenues = []
profits = []
payback = []
for _ in range(N_SCEN):
    cards = random.triangular(1.5, 2, 4)                  # карт в год
    price = random.triangular(2_700_000, 2_900_000, 3_200_000)
    service = cards * random.triangular(340_000, 380_000, 430_000)
    pilot = random.triangular(0, 1_200_000, 2_000_000)    # пилотные оснащения
    revenue = cards * price + service + pilot
    cost = cards * random.triangular(1_750_000, 1_950_000, 2_200_000) + 1_600_000
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
