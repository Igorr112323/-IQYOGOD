# -*- coding: utf-8 -*-
"""ЛЕДОЗОР: Монте-Карло 3 000 сценариев — выручка и окупаемость зимней кампании.

Потоки: радиометрическое обследование полей озимых (руб./га),
инструментальные акты для страховых компаний, сводки для штаба зимовки.
"""
import random

random.seed(20261008)

N_SCEN = 3000
START_COST = 4_500_000        # руб.: два серийных комплекса, калибровка, оборотный запас

revenues = []
profits = []
payback = []
for _ in range(N_SCEN):
    area_ha = random.triangular(45_000, 60_000, 72_000)        # га за кампанию январь — февраль
    survey_rev = area_ha * random.triangular(150, 160, 175)    # руб./га
    acts = random.triangular(150, 200, 260)                    # актов для страховых
    acts_rev = acts * random.triangular(8_500, 9_000, 9_800)
    summary_rev = random.triangular(400_000, 550_000, 750_000) # сводки министерству
    revenue = survey_rev + acts_rev + summary_rev
    cost = area_ha * random.triangular(55, 62, 70)             # ГСМ, износ, логистика
    cost += random.triangular(2_500_000, 2_700_000, 3_000_000) # ФОТ: 2 оператора + агрометеоролог
    cost += random.triangular(800_000, 950_000, 1_150_000)     # калибровка, поверка, командировки
    cost += random.triangular(300_000, 450_000, 600_000)       # прочие
    net = revenue - cost - revenue * 0.06                      # УСН 6 %
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
