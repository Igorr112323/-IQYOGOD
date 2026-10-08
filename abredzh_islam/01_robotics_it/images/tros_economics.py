# -*- coding: utf-8 -*-
"""ТРОС-ВЕКС: Монте-Карло 3 000 сценариев — выручка и окупаемость.

Потоки: продажа комплектов (4 кольца на лифт) по 44-ФЗ/223-ФЗ,
годовые контракты телеметрии.
"""
import random

random.seed(20261013)

N_SCEN = 3000
START_COST = 4_800_000        # руб.: серия 60 комплектов, платформа, интеграции

revenues = []
profits = []
payback = []
for _ in range(N_SCEN):
    lifts = random.triangular(42, 60, 88)                  # лифтов в первый год
    kit_rev = lifts * random.triangular(170_000, 180_000, 196_000)
    telemetry_rev = lifts * random.triangular(44_000, 48_000, 54_000)
    revenue = kit_rev + telemetry_rev
    cost = lifts * random.triangular(72_000, 84_000, 98_000) + 2_500_000
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
