# -*- coding: utf-8 -*-
"""ЛОЗА-ФУРАЖ: Монте-Карло 3 000 сценариев — прибыль линии 5 000 т/сезон.

Случайные величины: объём выжимки в сезоне, цена продажи добавки,
себестоимость (закваска, логистика контейнеров, работа, амортизация).
"""
import random

random.seed(20260930)

N_SCEN = 3000
CAPEX = 4_100_000            # руб.: контейнеры, пресс, автоматика

profits = []
payback = []
for _ in range(N_SCEN):
    volume = random.triangular(3_800, 5_000, 5_600)     # т/сезон
    price = random.triangular(2_600, 2_900, 3_200)      # руб/т продажа
    cost = random.triangular(1_600, 1_750, 1_950)       # руб/т себестоимость
    profit = volume * (price - cost) - 1_100_000        # постоянные расходы/год
    profits.append(profit)
    payback.append(CAPEX / max(profit / 12, 1))

profits.sort()
payback.sort()

def pct(v, p):
    return v[int(len(v) * p)]

print(f"Сценариев: {N_SCEN}")
print(f"Прибыль, млн руб/год: медиана {pct(profits,0.5)/1e6:.2f}; "
      f"Q25 {pct(profits,0.25)/1e6:.2f}; Q75 {pct(profits,0.75)/1e6:.2f}")
print(f"Окупаемость, мес: медиана {pct(payback,0.5):.1f}; 95-й процентиль {pct(payback,0.95):.1f}")
print(f"Доля сценариев с окупаемостью < 24 мес: {sum(1 for m in payback if m < 24)/N_SCEN:.2f}")
