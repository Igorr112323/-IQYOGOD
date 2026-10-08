# -*- coding: utf-8 -*-
"""ГАЗ-ДОЗОР: Монте-Карло 3 000 сценариев — выручка и окупаемость.

Потоки: комплекты «ГАЗ-ДОЗОР-Д1» с монтажом на МКД и сервисные контракты
(телеметрия, поверка оптики, журналы инцидентов).
"""
import random

random.seed(20261008)

N_SCEN = 3000
START_COST = 4_100_000        # руб.: серия комплектов, стенд калибровки, оборотный запас

revenues = []
profits = []
payback = []
for _ in range(N_SCEN):
    installs = random.triangular(28, 34, 42)                    # домов за год
    install_rev = installs * random.triangular(230_000, 240_000, 255_000)
    contracts = random.triangular(28, 34, 42)                   # сервисные контракты
    service_rev = contracts * random.triangular(88_000, 96_000, 104_000)
    revenue = install_rev + service_rev
    cost = installs * random.triangular(115_000, 125_000, 135_000)   # себестоимость и монтаж
    cost += contracts * random.triangular(26_000, 30_000, 34_000)    # сервисные выезды, поверка
    cost += random.triangular(2_200_000, 2_400_000, 2_700_000)       # ФОТ и накладные
    net = revenue - cost - revenue * 0.06                       # УСН 6 %
    revenues.append(revenue)
    profits.append(net)
    payback.append(START_COST / max(net / 12, 1))

revenues.sort(); profits.sort(); payback.sort()

def pct(v, p):
    return v[int(len(v) * p)]

print(f"Сценариев: {N_SCEN}")
print(f"Выручка, млн руб/год: медиана {pct(revenues,0.5)/1e6:.2f}; Q75 {pct(revenues,0.75)/1e6:.2f}")
print(f"Прибыль, млн руб/год: медиана {pct(profits,0.5)/1e6:.2f}")
print(f"Окупаемость, мес: медиана {pct(payback,0.5):.1f}; 95-й процентиль {pct(payback,0.95):.1f}")
print(f"Доля сценариев с окупаемостью < 24 мес: {sum(1 for m in payback if m < 24)/N_SCEN:.2f}")
