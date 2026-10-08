# -*- coding: utf-8 -*-
"""ТРОС-ВЕКС: Монте-Карло 3 000 сценариев — выручка и окупаемость.

Потоки: продажа комплектов (4 кольца на лифт, 180 тыс. руб.) по
44-ФЗ/223-ФЗ, годовые контракты телеметрии (48 тыс. руб./лифт).
"""
import random

random.seed(20261013)

N_SCEN = 3000
START_COST = 4_800_000        # руб.: серия 60 комплектов, платформа, интеграции

revenues = []
profits = []
payback = []
for _ in range(N_SCEN):
    lifts = random.triangular(44, 58.5, 79)                # лифтов в первый год
    kit_rev = lifts * random.triangular(174_000, 180_000, 190_000)
    telemetry_rev = lifts * random.triangular(46_500, 48_500, 51_500)
    revenue = kit_rev + telemetry_rev
    # производство комплектов (кольца, магниты, датчики Холла, корпуса),
    # монтаж, пусконаладка и интеграция с диспетчерскими
    cost = lifts * random.triangular(124_000, 132_000, 142_000)
    cost += random.triangular(2_350_000, 2_450_000, 2_600_000)
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
