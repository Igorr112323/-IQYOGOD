# -*- coding: utf-8 -*-
"""ИКСОД-НАДЗОР: Монте-Карло 3 000 сценариев — выручка и окупаемость.

Потоки: продажа сетей (4 ловушки) с установкой, годовое обслуживание,
сезонные контракты на надзор территорий.
"""
import random

random.seed(20261011)

N_SCEN = 3000
START_COST = 5_400_000        # руб.: серия 40 ловушек, датасет, интеграции

revenues = []
profits = []
payback = []
for _ in range(N_SCEN):
    nets = random.triangular(28, 40, 58)                     # сетей в первый год
    sale_rev = nets * random.triangular(360_000, 380_000, 410_000)
    service_rev = nets * random.triangular(175_000, 190_000, 215_000)
    seasonal = random.triangular(2, 4, 7) * random.triangular(280_000, 340_000, 420_000)
    revenue = sale_rev + service_rev + seasonal
    cost = nets * random.triangular(145_000, 165_000, 190_000) + 2_600_000
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
