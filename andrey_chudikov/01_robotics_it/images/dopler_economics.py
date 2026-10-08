# -*- coding: utf-8 -*-
"""ДОПЛЕР-СТАДО: Монте-Карло 3 000 сценариев — предотвращённый ущерб и окупаемость.

Стадо 600 коров. Случайные величины:
  - доля коров с эпизодом субклинической хромоты за год (бета-распределение);
  - длительность субклинической фазы в сутках;
  - потеря надоя, кг/сут;
  - цена молока, руб/кг.
Выход: распределение годового эффекта и срока окупаемости системы 1,24 млн руб.
"""
import random

random.seed(20261008)

N_SCEN = 3000
N_COWS = 600
SYSTEM_COST = 1_240_000  # руб.

payback_months = []
effects = []
for _ in range(N_SCEN):
    share_sick = random.betavariate(3.2, 9.8)          # медиана ~0,24
    n_sick = int(N_COWS * share_sick)
    duration = random.triangular(10, 21, 34)            # суток субклиники
    milk_loss = random.triangular(1.5, 2.4, 3.0)        # кг/сут
    price = random.triangular(33, 41, 48)               # руб/кг
    # система обнаруживает раньше: предотвращаем 65 % потери фазы (консервативно)
    saved_days = duration * 0.65
    effect = n_sick * saved_days * milk_loss * price
    effects.append(effect)
    payback_months.append(SYSTEM_COST / (effect / 12.0))

effects.sort()
payback_months.sort()

def pct(v, p):
    return v[int(len(v) * p)]

print(f"Сценариев: {N_SCEN}")
print(f"Эффект, млн руб/год: медиана {pct(effects,0.5)/1e6:.2f}; "
      f"Q25 {pct(effects,0.25)/1e6:.2f}; Q75 {pct(effects,0.75)/1e6:.2f}")
print(f"Окупаемость, мес: медиана {pct(payback_months,0.5):.1f}; "
      f"95-й процентиль {pct(payback_months,0.95):.1f}")
print(f"Доля сценариев с окупаемостью < 24 мес: "
      f"{sum(1 for m in payback_months if m < 24)/N_SCEN:.2f}")
