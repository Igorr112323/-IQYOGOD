# БОРА-5: кривая мощности модели и окупаемость головной Б-5
# Запуск: python3 bora_economics.py -> bora_economics.png
import numpy as np
import matplotlib.pyplot as plt

v = np.linspace(0, 26, 105)
# Аппроксимация измеренной характеристики Б-01, перенесённая на Б-5 (×8,4 по площади)
p5 = np.clip(0.5 * 1.225 * 4.7 * 0.31 * v ** 3 / 1000, 0, 5.0)
p5[v < 2.8] = 0.0
p5[v > 25] = np.interp(25, v, np.clip(0.5 * 1.225 * 4.7 * 0.31 * v ** 3 / 1000, 0, 5.0))

# Вейбулл площадки Новороссийска: k=2.3, c=7.6
k, c = 2.3, 7.6
weib = (k / c) * (v / c) ** (k - 1) * np.exp(-((v / c) ** k))
hours_v = 8760 * weib * (v[1] - v[0])
energy_kwh = np.sum(p5 * hours_v)

capex, opex, price = 490e3, 12e3, 7.2
annual = energy_kwh * price + 1.8 * 2500   # + тепло балласта, руб
payback = capex / (annual - opex)

plt.rcParams.update({"font.size": 9})
fig, ax = plt.subplots(1, 2, figsize=(10, 4.2))
ax[0].plot(v, p5, lw=2, color="#0d47a1", label="Б-5, расчёт по заделу")
ax[0].plot(v, 100 * weib / weib.max() * 0.1, color="gray", label="распределение ветра (масштаб)")
ax[0].set_xlabel("м/с"); ax[0].set_ylabel("кВт")
ax[0].set_title(f"Характеристика мощности; выработка {energy_kwh/1000:.1f} МВт·ч/год")
ax[0].grid(alpha=0.3); ax[0].legend(fontsize=8)

years = np.arange(0, 15.1, 0.5)
cum = (annual - opex) * years - capex
ax[1].plot(years, cum / 1e3, color="#2e7d32", lw=2)
ax[1].axhline(0, color="gray", lw=0.8)
ax[1].set_title(f"Окупаемость {payback:.1f} года")
ax[1].set_xlabel("лет"); ax[1].set_ylabel("тыс. руб. накоплено"); ax[1].grid(alpha=0.3)
fig.suptitle("БОРА-5: площадка Новороссийска, Вейбулл k=2,3 c=7,6")
fig.tight_layout()
fig.savefig("bora_economics.png", dpi=150)
print(f"выработка {energy_kwh:.0f} кВт·ч/год; окупаемость {payback:.1f} года")
