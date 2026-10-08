# -*- coding: utf-8 -*-
"""ЗАМОР-СТОП: Монте-Карло 3 000 сценариев — выручка и окупаемость.

Потоки: продажа постов с установкой, ежемесячные подписки
на сервис оповещения, сезонные контракты на лиманы.
"""
import random

random.seed(20260924)

N_SCEN = 3000
START_COST = 3_700_000        # руб.: серия 24 поста, датасет, развёртывание

revenues = []
profits = []
payback = []
for _ in range(N_SCEN):
    posts = random.triangular(16, 24, 34)
    post_rev = posts * random.triangular(320_000, 340_000, 370_000)
    sub_rev = posts * random.triangular(17, 19, 22) * 1000 * random.uniform(0.75, 0.95)
    seasonal = random.triangular(1, 2, 4) * random.triangular(420_000, 520_000, 640_000)
    revenue = post_rev + sub_rev + seasonal
    cost = posts * random.triangular(185_000, 210_000, 240_000) + 2_100_000
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
