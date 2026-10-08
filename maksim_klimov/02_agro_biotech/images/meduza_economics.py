# -*- coding: utf-8 -*-
"""МЕДУЗА-АГРО: Монте-Карло 3 000 сценариев — выручка и окупаемость.

Потоки: продажа концентрата «АЗОВ-БИО», контрактная переработка
биомассы муниципалитетов, продажа жома.
"""
import random

random.seed(20261002)

N_SCEN = 3000
START_COST = 5_900_000        # руб.: три комплекса, ёмкости, оборотный запас

revenues = []
profits = []
payback = []
for _ in range(N_SCEN):
    biomass_t = random.triangular(260, 360, 520)             # т за сезон, три комплекса
    conc_l = biomass_t * random.triangular(100, 114, 126)    # л концентрата
    conc_rev = conc_l * random.triangular(1_120, 1_200, 1_300)
    intake_rev = biomass_t * random.triangular(4_100, 4_500, 5_000)
    pulp_rev = biomass_t * random.triangular(820, 900, 1_000)
    revenue = conc_rev + intake_rev + pulp_rev
    cost = biomass_t * random.triangular(2_300, 2_650, 3_050) + 2_400_000
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
