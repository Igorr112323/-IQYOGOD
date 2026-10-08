# -*- coding: utf-8 -*-
"""РИТМ-КАДРЫ: Монте-Карло 3 000 сценариев — выручка и окупаемость.

Потоки: годовые лицензии на организации (до 3 киосков),
закупка киосков, обслуживание.
"""
import random

random.seed(20261001)

N_SCEN = 3000
START_COST = 4_200_000        # руб.: серия 60 киосков, ПО, пилоты

revenues = []
profits = []
payback = []
for _ in range(N_SCEN):
    licenses = random.triangular(24, 34, 52)
    lic_rev = licenses * random.triangular(240_000, 260_000, 290_000)
    kiosks = random.triangular(30, 55, 85) * random.triangular(90_000, 96_000, 108_000)
    revenue = lic_rev + kiosks
    cost = licenses * random.triangular(58_000, 70_000, 84_000) + 2_400_000
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
