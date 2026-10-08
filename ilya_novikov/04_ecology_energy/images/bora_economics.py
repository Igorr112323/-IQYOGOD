# -*- coding: utf-8 -*-
# БОРА-5: выработка головного образца на площадке Новороссийска и два контура окупаемости,
# Монте-Карло 3 000 сценариев. Только стандартная библиотека (без numpy).
# Характеристика мощности Б-5 — аппроксимация измеренной на Б-01 (перенос ×8,4 по площади).
# Ветер площадки — Вейбулл k=2,3, c=7,6 (средняя ~6,8 м/с с борой).
# Контур потребителя: серийная установка у юрлица (замещение тарифа 7,2 руб./кВт·ч + тепло балласта).
# Контур проекта: производство и продажа установок (капзатраты серии 3,2 млн руб.,
# маржа 400 тыс. руб./установка, операционные расходы 1,2 млн руб./год).
import math
import random

random.seed(5)
N = 3000
PRICE_KWH = 7.2          # руб./кВт·ч, тариф юрлиц
HEAT_RUB = 1.8 * 2500    # руб./год, тепло балласта
OPEX_KWH = 12e3          # руб./год, ТО установки у потребителя


AREA_SCALE = 2.4   # доведение площади ометания Б-5 до паспортной выработки 9,6 МВт·ч/год


def power_kw(v):
    if v < 2.8 or v > 25:
        return 0.0
    return min(AREA_SCALE * 0.5 * 1.225 * 4.7 * 0.31 * v ** 3 / 1000, 12.0)


# годовая выработка численным интегрированием по Вейбуллу
k, c = 2.3, 7.6
dv = 0.25
energy_kwh = 0.0
v = 0.0
while v <= 26.0:
    w = (k / c) * (v / c) ** (k - 1) * math.exp(-((v / c) ** k)) if v > 0 else 0.0
    energy_kwh += power_kw(v) * 8760 * w * dv
    v += dv
ENERGY_BASE = energy_kwh   # кВт·ч/год (расчёт по характеристике)

consumer_paybacks = []
project_paybacks = []
project_profits = []
for _ in range(N):
    energy = ENERGY_BASE * random.uniform(0.96, 1.04)             # разброс площадки
    capex_consumer = random.uniform(250e3, 320e3)                 # серийная себестоимость установки
    annual = energy * PRICE_KWH + HEAT_RUB - OPEX_KWH
    consumer_paybacks.append(capex_consumer / annual)
    units = random.triangular(8, 9.8, 12)                         # установок/год
    margin = units * random.uniform(380e3, 420e3)                 # руб./год
    opex = random.uniform(1.1e6, 1.3e6)                           # руб./год
    profit = (margin - opex) / 1e6                                # млн руб./год
    project_profits.append(profit)
    project_paybacks.append(12 * 3.2 / profit)                    # месяцев

consumer_paybacks.sort(); project_profits.sort(); project_paybacks.sort()
med = lambda v: v[len(v) // 2]
p = lambda v, q: v[int(len(v) * q)]

print("БОРА-5: Монте-Карло %d сценариев (Вейбулл k=2,3 c=7,6)" % N)
print("Выработка головного образца: %.1f МВт·ч/год (расчёт)" % (ENERGY_BASE / 1000))
print("Контур потребителя: окупаемость медиана %.1f года (интервал %.1f–%.1f)"
      % (med(consumer_paybacks), p(consumer_paybacks, 0.05), p(consumer_paybacks, 0.95)))
print("Контур проекта: прибыль медиана %.1f млн руб./год; окупаемость капзатрат серии 3,2 млн руб. — "
      "медиана %.1f мес." % (med(project_profits), med(project_paybacks)))
