# -*- coding: utf-8 -*-
"""ВОДА-РАДАР: Монте-Карло 3 000 сценариев — выручка и окупаемость.

Контрактная модель: кластерные контракты до 300 км трасс от 640 тыс. руб./год
(44-ФЗ/223-ФЗ), регламентные отчёты, пилоты.
"""
import random

random.seed(20261008)

N_SCEN = 3000
START_COST = 4_900_000        # руб.: платформа, конвейер, пилотные кластеры

revenues = []
profits = []
payback = []
for _ in range(N_SCEN):
    clusters = random.triangular(8, 12, 18)
    price = random.triangular(600_000, 640_000, 760_000)
    reports = clusters * random.triangular(90_000, 120_000, 160_000)
    pilots = random.triangular(0, 1_000_000, 1_800_000)
    revenue = clusters * price + reports + pilots
    cost = clusters * random.triangular(260_000, 310_000, 380_000) + 2_500_000
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
