# -*- coding: utf-8 -*-
"""РИТМ-КАДРЫ: Монте-Карло 3 000 сценариев — выручка и окупаемость.

Потоки: годовые лицензии на организации (до 3 киосков), закупка киосков,
годовое сопровождение лицензий.
Калибровка: выручка медиана 9,8 млн руб./год при 34 лицензиях,
прибыль 2,9 млн руб./год, окупаемость 4,2 млн руб. — 17,4 месяца.
"""
import random

random.seed(20261001)

N_SCEN = 3000
START_COST = 4_200_000        # руб.: серия 60 киосков, ПО, развёртывание

revenues = []
profits = []
payback = []
for _ in range(N_SCEN):
    licenses = random.triangular(24, 34, 52)
    lic_rev = licenses * random.triangular(225_000, 245_000, 270_000)
    kiosks = random.triangular(2, 5, 8) * random.triangular(90_000, 96_000, 108_000)
    support = licenses * random.triangular(14_000, 18_000, 24_000)  # сопровождение
    revenue = lic_rev + kiosks + support
    cost = licenses * random.triangular(90_000, 105_000, 125_000) + 3_180_000
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
