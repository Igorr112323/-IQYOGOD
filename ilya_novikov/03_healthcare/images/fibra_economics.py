# -*- coding: utf-8 -*-
"""ФИБРА-СТОПА: Монте-Карло 3 000 сценариев — выручка и окупаемость.

Модель: интеррогаторы (разовая продажа) + стельки (расходник, замена
каждые 6 месяцев). Случайные величины: число оснащённых кабинетов,
пациентов на кабинет, доля вовремя заменяемых стелек.
Калибровка: выручка медиана 11,6 млн руб./год при 12 кабинетах,
прибыль 3,3 млн руб./год, окупаемость 2,4 млн руб. — 8,7 месяца.
"""
import random

random.seed(20260428)

N_SCEN = 3000
START_COST = 2_400_000          # руб.: серия стелек, интеррогатор, досье
INTERROGATOR = 68_000           # руб./шт
INSOLE = 12_000                 # руб./пара, замена 2 раза в год

revenues = []
profits = []
payback = []
for _ in range(N_SCEN):
    cabinets = int(random.triangular(8, 12, 16))
    patients = int(random.triangular(32, 50, 74))           # пациентов на кабинет/год
    replace_rate = random.betavariate(8, 2)                 # своевременная замена
    device_rev = cabinets * INTERROGATOR
    insole_rev = cabinets * patients * 2 * INSOLE * replace_rate
    revenue = device_rev + insole_rev
    cost = revenue * random.triangular(0.65, 0.715, 0.78)   # себестоимость + сопровождение
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
