# -*- coding: utf-8 -*-
"""ПОЛЯРИС-БЕРЕГ: Монте-Карло 3 000 сценариев — выручка и окупаемость.

Случайные величины: число постов в портфеле (муниципалитеты + базы отдыха),
доля годовых контрактов, обслуживание, сезонные факторы.
Калибровка: выручка медиана 14,8 млн руб./год при 18 постах, прибыль
3,9 млн руб./год, окупаемость 5,2 млн руб. — 16,0 месяца.
"""
import random

random.seed(20260813)

N_SCEN = 3000
START_COST = 5_200_000        # руб.: серия 20 постов, оснастка, интеграции ЕДДС

revenues = []
profits = []
payback = []
for _ in range(N_SCEN):
    posts = int(random.triangular(13, 19, 27))
    share_contract = random.betavariate(4, 6)
    sale_rev = posts * (1 - share_contract) * random.triangular(590_000, 620_000, 660_000)
    contract_rev = posts * share_contract * random.triangular(540_000, 600_000, 680_000)
    service_rev = posts * random.triangular(155_000, 170_000, 190_000)
    revenue = sale_rev + contract_rev + service_rev
    cost = posts * random.triangular(440_000, 490_000, 550_000) + 1_620_000
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
