# -*- coding: utf-8 -*-
# НОС-КОД: Монте-Карло 3 000 сценариев — предотвращённые нападения стай собак и эффект.
# Только стандартная библиотека (без numpy/matplotlib).
# Три района: события стай за учебный год, доля охваченных маршрутов, точность обнаружения,
# вероятность нападения без раннего наряда. Эффект — лечение, компенсации, внеплановые работы
# на один случай. Экономика проекта: капзатраты 2,4 млн руб., чистый результат 2,2 млн руб./год
# (выручка 6,3 − расходы 4,1, см. заявку).
import random

random.seed(2026)
N = 3000

prevented_all = []
effects = []
for _ in range(N):
    pack_events = random.triangular(38, 60, 92)        # событий стай за учебный год в районе
    coverage = random.uniform(0.55, 0.85)              # доля охваченных маршрутов
    detect = random.uniform(0.84, 0.92)                # точность обнаружения
    attack_given_pack = random.uniform(0.10, 0.21)     # вероятность нападения без раннего наряда
    prevented = 3 * pack_events * coverage * detect * attack_given_pack
    prevented_all.append(prevented)
    cost_case = random.triangular(0.8, 1.4, 2.4)       # млн руб. на один случай
    effects.append(prevented * cost_case)

prevented_all.sort(); effects.sort()
med = lambda v: v[len(v) // 2]
p = lambda v, q: v[int(len(v) * q)]

NET = 2.2       # млн руб./год, чистый результат проекта
CAPEX = 2.4     # млн руб.
PAYBACK_M = 12 * CAPEX / NET

print("НОС-КОД: Монте-Карло %d сценариев (3 района)" % N)
print("Предотвращённые нападения за учебный год: медиана %.0f (p10 %.0f, p90 %.0f)"
      % (med(prevented_all), p(prevented_all, 0.10), p(prevented_all, 0.90)))
print("Эффект: медиана %.1f млн руб./год" % med(effects))
print("Окупаемость капзатрат 2,4 млн руб. при чистом результате 2,2 млн руб./год: %.1f мес." % PAYBACK_M)
