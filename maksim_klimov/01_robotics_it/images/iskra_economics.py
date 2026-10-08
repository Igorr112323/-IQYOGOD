# -*- coding: utf-8 -*-
"""ИСКРА-СТОП: Монте-Карло 3 000 сценариев — эффект у оператора МСК и окупаемость.

Случайные величины: число инцидентов с возгоранием/остановкой в год,
стоимость дня простоя линии, выручка от передачи источников тока утилизатору.
"""
import random

random.seed(20260814)

N_SCEN = 3000
MODULE_PRICE = 5_300_000     # руб.
SERVICE = 640_000            # руб./год обслуживание

effects = []
payback = []
for _ in range(N_SCEN):
    incidents = random.choices([0, 1, 2, 3], weights=[0.35, 0.38, 0.20, 0.07])[0]
    downtime_cost = random.triangular(0.8e6, 1.0e6, 1.2e6)   # руб./день простоя
    days = random.triangular(1, 3, 8)                        # дней остановки на инцидент
    recycling = random.triangular(240_000, 330_000, 420_000) # выручка утилизатору
    effect = incidents * downtime_cost * days + recycling
    effects.append(effect)
    payback.append(MODULE_PRICE / max((effect - SERVICE) / 12, 1))

effects.sort()
payback.sort()

def pct(v, p):
    return v[int(len(v) * p)]

print(f"Сценариев: {N_SCEN}")
print(f"Эффект у оператора, млн руб/год: медиана {pct(effects,0.5)/1e6:.2f}; "
      f"Q25 {pct(effects,0.25)/1e6:.2f}; Q75 {pct(effects,0.75)/1e6:.2f}")
print(f"Окупаемость, мес: медиана {pct(payback,0.5):.1f}; 95-й процентиль {pct(payback,0.95):.1f}")
print(f"Доля сценариев с окупаемостью < 24 мес: {sum(1 for m in payback if m < 24)/N_SCEN:.2f}")
