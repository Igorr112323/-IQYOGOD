# -*- coding: utf-8 -*-
"""КЕРАТИН-ГЛИК: Монте-Карло 3 000 сценариев — прибыль и окупаемость.

Потоки: продажа приборов, годовая подписка, расходные кассеты анализа.
Случайные величины: число приборов в крае/год, цена, себестоимость,
доля подписки, кассеты на прибор, операционные расходы.
Калибровка: медиана прибыли 4,6 млн руб./год при 20 приборах,
окупаемость стартовых затрат 3,2 млн руб. — 8,3 месяца.
"""
import random

random.seed(20260712)

N_SCEN = 3000
START_COST = 3_200_000      # руб.: серия, сертификация, дистрибуция

profits = []
payback = []
for _ in range(N_SCEN):
    units = int(random.triangular(15, 21, 27))              # приборов в крае/год
    price = random.triangular(330_000, 340_000, 350_000)
    cost = random.triangular(195_000, 205_000, 215_000)
    subs_share = random.betavariate(6, 3)                   # доля оформивших подписку
    cassettes = random.triangular(104_000, 130_000, 158_000)  # расходные кассеты/год
    revenue = units * (price - cost + subs_share * 24_000 + cassettes)
    opex = 750_000 + units * random.triangular(14_000, 17_000, 21_000)
    profit = revenue - opex
    profits.append(profit)
    payback.append(min(START_COST / max(profit / 12, 1), 999.0))

profits.sort()
payback.sort()

def pct(v, p):
    return v[int(len(v) * p)]

print(f"Сценариев: {N_SCEN}")
print(f"Прибыль, млн руб/год: медиана {pct(profits,0.5)/1e6:.2f}; "
      f"Q25 {pct(profits,0.25)/1e6:.2f}; Q75 {pct(profits,0.75)/1e6:.2f}")
print(f"Окупаемость, мес: медиана {pct(payback,0.5):.1f}; 95-й процентиль {pct(payback,0.95):.1f}")
print(f"Доля сценариев с окупаемостью < 24 мес: {sum(1 for m in payback if m < 24)/N_SCEN:.2f}")
