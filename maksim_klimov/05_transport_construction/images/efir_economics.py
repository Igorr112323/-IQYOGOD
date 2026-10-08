# -*- coding: utf-8 -*-
"""ЭФИР-ДОЖДЬ: Монте-Карло 3 000 сценариев — прибыль и окупаемость.

Случайные величины: число районов на подписке, цена подписки,
доля пилотных районов оператора, операционные расходы.
"""
import random

random.seed(20260821)

N_SCEN = 3000
START_COST = 4_800_000      # руб.: кластер, доработка, интеграции, полевой персонал

profits = []
payback = []
for _ in range(N_SCEN):
    districts = int(random.triangular(2, 3, 6))              # районные подписки
    price = random.triangular(800_000, 890_000, 980_000)
    operator_pilot = random.triangular(900_000, 1_400_000, 1_900_000)  # партнёрство с оператором
    revenue = districts * price + operator_pilot
    opex = 2_100_000 + districts * random.triangular(180_000, 260_000, 340_000)
    profit = revenue - opex
    profits.append(profit)
    payback.append(START_COST / max(profit / 12, 1))

profits.sort()
payback.sort()

def pct(v, p):
    return v[int(len(v) * p)]

print(f"Сценариев: {N_SCEN}")
print(f"Прибыль, млн руб/год: медиана {pct(profits,0.5)/1e6:.2f}; "
      f"Q25 {pct(profits,0.25)/1e6:.2f}; Q75 {pct(profits,0.75)/1e6:.2f}")
print(f"Окупаемость, мес: медиана {pct(payback,0.5):.1f}; 95-й процентиль {pct(payback,0.95):.1f}")
print(f"Доля сценариев с окупаемостью < 24 мес: {sum(1 for m in payback if m < 24)/N_SCEN:.2f}")
