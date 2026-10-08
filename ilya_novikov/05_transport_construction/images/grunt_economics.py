# -*- coding: utf-8 -*-
"""ГРУНТ-ЭХО: Монте-Карло 3 000 сценариев — выручка и окупаемость услуги обследования.

Случайные величины: километраж обследования в год, цена за км,
доля повторных обследований, операционные расходы.
Калибровка: выручка медиана 5,7 млн руб./год при 15 км, прибыль
3,1 млн руб./год, окупаемость 1,9 млн руб. — 7,4 месяца.
"""
import random

random.seed(20260615)

N_SCEN = 3000
START_COST = 1_900_000        # руб.: серия датчиков, контроллеры, поверка
PRICE_PER_KM = 380_000        # руб./км
COST_PER_KM = 115_000         # руб./км обследование + обработка

revenues = []
profits = []
payback = []
for _ in range(N_SCEN):
    km = random.triangular(8, 13.7, 20.5)
    repeat = random.betavariate(3, 7)               # доля повторных контрактов
    km_eff = km * (1 + 0.3 * repeat)
    revenue = km_eff * PRICE_PER_KM
    cost = km_eff * COST_PER_KM + 950_000           # постоянные расходы/год
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
