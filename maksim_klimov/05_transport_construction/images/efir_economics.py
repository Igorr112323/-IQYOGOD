# -*- coding: utf-8 -*-
"""ЭФИР-ДОЖДЬ: Монте-Карло 3 000 сценариев — прибыль и окупаемость.

Потоки: районные подписки (890 тыс. руб./год), пилотное партнёрство
оператора ливневых сетей, региональная агрегирующая подписка данных
для дорожных и коммунальных служб.
Калибровка: медиана прибыли 7,4 млн руб./год при 3 районных подписках,
окупаемость стартовых затрат 4,8 млн руб. — 7,8 месяца.
"""
import random

random.seed(20260821)

N_SCEN = 3000
START_COST = 4_800_000      # руб.: кластер, доработка, интеграции, полевой персонал

profits = []
payback = []
for _ in range(N_SCEN):
    districts = int(random.triangular(2, 3, 5))             # районные подписки
    price = random.triangular(800_000, 890_000, 980_000)
    operator_pilot = random.triangular(2_300_000, 3_400_000, 4_500_000)
    data_subscription = random.triangular(2_700_000, 3_600_000, 4_500_000)
    revenue = districts * price + operator_pilot + data_subscription
    opex = 1_300_000 + districts * random.triangular(160_000, 200_000, 260_000)
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
