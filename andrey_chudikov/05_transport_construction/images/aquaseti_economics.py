# -*- coding: utf-8 -*-
# АКУСТИК-СЕТИ: экономика обнаружения утечек, Монте-Карло 3 000 сценариев.
# Только стандартная библиотека (без numpy/matplotlib).
# 200 км магистралей Новороссийска, 900 акустических узлов (7 200 руб./узел) + 1,4 млн руб.
# сервер и внедрение; тариф 47 руб./м3.
import math
import random

random.seed(3)
N = 3000
TARIFF = 47.0                       # руб./м3, Новороссийск
NODES = 900
CAPEX = (NODES * 7200 + 1.4e6) / 1e6   # млн руб. = 7,88


def poisson(lam):
    # выборка Пуассона методом обратного преобразования (Кнут)
    limit = math.exp(-lam)
    k, prob = 0, 1.0
    while True:
        prob *= random.random()
        if prob <= limit:
            return k
        k += 1


totals = []
paybacks = []
for _ in range(N):
    leaks_year = min(100, max(30, int(random.gauss(62, 10))))      # скрытых утечек/год
    q_m3h = random.triangular(0.8, 2.4, 4.0)                        # средний дебит утечки, м3/ч
    months_hidden = random.triangular(1.5, 4.0, 8.0)                # месяцев без системы
    saved_m3 = leaks_year * q_m3h * 24 * 30.4 * months_hidden
    water_money = saved_m3 * TARIFF / 1e6                           # млн руб./год
    avaria = poisson(10) * random.triangular(300, 400, 600) * 1e3 / 1e6  # избегание аварий
    total = water_money + avaria
    totals.append(total)
    paybacks.append(CAPEX / total)

totals.sort(); paybacks.sort()
med = lambda v: v[len(v) // 2]

print("АКУСТИК-СЕТИ: Монте-Карло %d сценариев (200 км, %d узлов, капзатраты %.2f млн руб.)"
      % (N, NODES, CAPEX))
print("Эффект: медиана %.1f млн руб./год" % med(totals))
print("Окупаемость: медиана %.2f года (%.0f мес.)" % (med(paybacks), med(paybacks) * 12))
