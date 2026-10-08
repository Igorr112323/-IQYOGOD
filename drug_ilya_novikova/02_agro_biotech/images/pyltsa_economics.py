# -*- coding: utf-8 -*-
"""ПЫЛЬЦА-ВЕКС: Монте-Карло 3 000 сценариев — выручка и окупаемость.

Случайные величины: число датчиков в портфеле, доля активных подписок,
страховые партнёрские платежи, себестоимость датчика.
"""
import random

random.seed(20260704)

N_SCEN = 3000
START_COST = 3_600_000          # руб.: серия 100 датчиков, оснастка, дообучение модели

revenues = []
profits = []
payback = []
for _ in range(N_SCEN):
    units = int(random.triangular(120, 180, 260))
    device_rev = units * random.triangular(44_000, 47_000, 51_000)
    sub_share = random.betavariate(8, 2)
    sub_rev = units * sub_share * 3_900 * 12
    insurance = units * random.triangular(2_000, 3_500, 5_000)   # платежи страховых/год
    revenue = device_rev + sub_rev + insurance
    cost = units * random.triangular(26_000, 29_000, 33_000) + 2_400_000
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
