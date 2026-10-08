# -*- coding: utf-8 -*-
# АГРОВОЛЬТАИКА-КУБАНЬ: экономика проекта и клиента-винодельни, Монте-Карло 3 000 сценариев.
# Только стандартная библиотека (без numpy/matplotlib).
# Проект: продажа 6 секций/год по 7,9 млн руб., маржа секции ~2,1 млн руб., капзатраты 8,6 млн руб.
# Клиент: секция 50 кВт даёт ~60 МВт·ч/год (экономия ~570 тыс. руб. по тарифу 9,5 руб./кВт·ч)
# + защита лозы, заменяющая противоградовую сетку; при покупке клиент избегает аренды
# 890 тыс. руб./год; индексация тарифов ~12 %/год (задокументированный рост 2025–2026 гг.).
import random

random.seed(23)
N = 3000

client_paybacks = []
client_benefits = []
nets = []
for _ in range(N):
    # --- клиент: секция 50 кВт на 0,7 га виноградника ---
    kwh_year = random.triangular(56, 60, 64) * 1e3      # кВт·ч/год
    price_grid = random.triangular(8.8, 9.5, 10.4)      # руб./кВт·ч для юрлиц
    energy_saving = kwh_year * price_grid               # руб./год
    shield = random.triangular(0.28, 0.45, 0.68) * 1e6  # эквивалент противоградовой сетки
    avoided_rent = 0.89e6                               # аренда, которой избегает покупатель
    tariff_growth = random.uniform(0.12, 0.16)          # индексация тарифа, в год
    benefit0 = energy_saving + shield + avoided_rent    # эффект первого года, руб.
    # окупаемость покупки 7,9 млн руб. нарастающим эффектом
    cum, payback_years = 0.0, None
    for year in range(1, 21):
        cum += benefit0 * (1 + tariff_growth) ** (year - 1)
        if cum >= 7.9e6:
            payback_years = year - 1 + (7.9e6 - (cum - benefit0 * (1 + tariff_growth) ** (year - 1))) / (benefit0 * (1 + tariff_growth) ** (year - 1))
            break
    client_paybacks.append(payback_years if payback_years else 20.0)
    client_benefits.append(benefit0 / 1e6)
    # --- проект: первый полный год, 6 секций ---
    margin_section = random.triangular(1.9, 2.1, 2.3) * 1e6
    revenue = 6 * 7.9e6
    opex = revenue - 6 * margin_section + 7.2e6         # себестоимость + постоянные расходы (итого 42,0 млн)
    nets.append((revenue - opex) / 1e6)

client_paybacks.sort(); client_benefits.sort(); nets.sort()
med = lambda v: v[len(v) // 2]
net = med(nets)
payback_project = 8.6 / net
share_lt5 = sum(1 for x in client_paybacks if x < 5.0) / N

print("АГРОВОЛЬТАИКА-КУБАНЬ: Монте-Карло %d сценариев" % N)
print("Клиент: эффект первого года медиана %.1f млн руб./год; окупаемость секции при покупке "
      "медиана %.1f года (доля сценариев < 5 лет: %.0f %%)"
      % (med(client_benefits), med(client_paybacks), share_lt5 * 100))
print("Проект: чистый результат %.1f млн руб./год при 6 секциях; окупаемость капзатрат 8,6 млн руб. — %.2f года"
      % (net, payback_project))
