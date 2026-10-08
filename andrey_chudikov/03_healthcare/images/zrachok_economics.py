# -*- coding: utf-8 -*-
"""ЗРАЧОК-ВЕКС: Монте-Карло 3 000 сценариев — подписная модель и окупаемость.

Плательщик — учреждения здравоохранения и социального обслуживания.
Случайные величины: число платящих учреждений, доля отказов в первый год,
средняя цена подписки, операционные расходы на учреждение.
"""
import random

random.seed(20260903)

N_SCEN = 3000
START_COST = 1_600_000        # руб.: серийная насадка, доработка модели, досье
BASE_PRICE = 46_000           # руб./мес подписка
TARGET_UNITS = 62             # целевой портфель к концу 3-го года

profits = []
revenues = []
payback = []
for _ in range(N_SCEN):
    units = int(random.triangular(38, 62, 74))          # портфель 12 мес
    churn = random.betavariate(2, 18)                   # доля отказов
    units_eff = units * (1 - churn)
    price = random.triangular(41_000, 46_000, 49_000)
    revenue = units_eff * price * 12
    opex = units_eff * random.triangular(280_000, 340_000, 410_000) + 3_200_000
    profit = revenue - opex
    profits.append(profit)
    revenues.append(revenue)
    payback.append(START_COST / max(profit / 12, 1))

profits.sort()
revenues.sort()
payback.sort()

def pct(v, p):
    return v[int(len(v) * p)]

print(f"Сценариев: {N_SCEN}")
print(f"Выручка медиана: {pct(revenues,0.5)/1e6:.1f} млн руб/год")
print(f"Прибыль медиана: {pct(profits,0.5)/1e6:.1f} млн руб/год; "
      f"Q25 {pct(profits,0.25)/1e6:.1f}; Q75 {pct(profits,0.75)/1e6:.1f}")
print(f"Окупаемость, мес: медиана {pct(payback,0.5):.1f}; 95-й процентиль {pct(payback,0.95):.1f}")
print(f"Доля сценариев с окупаемостью < 24 мес: {sum(1 for m in payback if m < 24)/N_SCEN:.2f}")
