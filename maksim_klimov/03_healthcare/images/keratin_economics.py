# -*- coding: utf-8 -*-
"""КЕРАТИН-ГЛИК: Монте-Карло 3 000 сценариев — прибыль и окупаемость.

Случайные величины: число проданных приборов в крае, цена прибора,
доля оформивших подписку, себестоимость, операционные расходы.
"""
import random

random.seed(20260712)

N_SCEN = 3000
START_COST = 3_200_000      # руб.: серия, сертификация, дистрибуция

profits = []
payback = []
for _ in range(N_SCEN):
    units = int(random.triangular(12, 20, 28))             # приборов в крае/год
    price = random.triangular(320_000, 340_000, 360_000)
    cost = random.triangular(195_000, 210_000, 230_000)
    subs_share = random.betavariate(6, 3)
    revenue = units * (price - cost) + units * subs_share * 24_000
    opex = 1_400_000 + units * random.triangular(18_000, 24_000, 32_000)
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
