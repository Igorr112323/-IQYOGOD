# -*- coding: utf-8 -*-
# КАРБОКУБАНЬ: экономика модуля пиролиза 300 кг/ч, Монте-Карло 3 000 сценариев.
# Только стандартная библиотека (без numpy/matplotlib).
# Двойная монетизация: биоуголь-мелиорант + углеродные единицы (1,74 т CO2-экв./т).
# Исходные данные из заявки (п. 11): сырьё — лузга 1 200 руб./т × 4 900 т = 5,9 млн руб./год;
# полная стоимость модуля 12,4 млн руб. (остаточный CAPEX после макета — 1,8 млн руб.);
# базовые цены 9 500 руб./т биоугля и 700 руб./т углеродной единицы.
import random

random.seed(11)
N = 3000
OUTPUT = 1600.0         # т биоугля/год
RAW_COST = 1200.0 * 4900.0      # руб./год, лузга
OPEX_OTHER = 4.6e6      # руб./год: энергия пиролиза, персонал, логистика, ТО
CO2_PER_T = 1.74        # т CO2-экв./т биоугля
CAPEX_FULL = 12.4       # млн руб. полная стоимость модуля

margins = []
paybacks = []
for _ in range(N):
    price_char = random.triangular(8500, 9500, 11000)   # мелиорант, руб./т
    price_co2 = random.triangular(500, 700, 1000)       # руб./т CO2-экв.
    revenue = OUTPUT * price_char + OUTPUT * CO2_PER_T * price_co2
    margin = (revenue - RAW_COST - OPEX_OTHER) / 1e6    # млн руб./год
    margins.append(margin)
    paybacks.append(CAPEX_FULL / margin)

margins.sort(); paybacks.sort()
med = lambda v: v[len(v) // 2]

print("КАРБОКУБАНЬ: Монте-Карло %d сценариев (модуль 300 кг/ч, %d т биоугля/год)" % (N, int(OUTPUT)))
print("Маржа модуля: медиана %.1f млн руб./год" % med(margins))
print("Окупаемость полной стоимости модуля 12,4 млн руб.: медиана %.2f года" % med(paybacks))
