# -*- coding: utf-8 -*-
"""МЕДУЗА-АГРО: Монте-Карло 3 000 сценариев — выручка и окупаемость.

Потоки: продажа концентрата «АЗОВ-БИО» (1 200 руб./л), контрактная
переработка биомассы муниципалитетов (4 500 руб./т), продажа жома
(900 руб./т). Сезон август — октябрь, три комплекса «АЗОВ-М1».
"""
import random

random.seed(20261002)

N_SCEN = 3000
START_COST = 5_900_000        # руб.: три комплекса, ёмкости, оборотный запас

revenues = []
profits = []
payback = []
for _ in range(N_SCEN):
    biomass_t = random.triangular(74, 90, 108)               # т за сезон, три комплекса
    conc_l = biomass_t * random.triangular(104, 114, 124)    # л концентрата
    conc_rev = conc_l * random.triangular(1_150, 1_200, 1_260)
    intake_rev = biomass_t * random.triangular(4_250, 4_500, 4_800)
    pulp_rev = biomass_t * random.triangular(850, 900, 960)
    revenue = conc_rev + intake_rev + pulp_rev
    # сбор, логистика, переработка и сбыт — на литр концентрата,
    # плюс постоянные затраты трёх комплексов
    cost = conc_l * random.triangular(425, 450, 480)
    cost += random.triangular(4_600_000, 4_800_000, 5_000_000)
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
