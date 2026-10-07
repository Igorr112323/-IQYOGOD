# КУБАНЬ-ХРУСТ: экономика масштабирования
# Запуск: python3 khrust_economics.py -> khrust_economics.png
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(21)
N = 3000
YIELD_RATIO = 8.5                 # кг сырья на кг продукта
RAW = 30.0                        # руб./кг некондиции
energy_cost = 1.9 * 7.5           # кВт·ч/кг × руб./кВт·ч

price = rng.triangular(900, 1050, 1250, N)      # оптово-розничный микс, руб./кг
volume = rng.triangular(120, 155, 170, N) * 1e3  # кг/год

revenue = price * volume / 1e6
cogs = (YIELD_RATIO * RAW + 33 + energy_cost) * volume / 1e6   # сырьё, упаковка+лог, энергия
opex = (6.2 + 3.0)  # ФОТ + прочие, млн/год
profit = revenue - cogs - opex
margin = profit / revenue

plt.rcParams.update({"font.size": 9})
fig, ax = plt.subplots(1, 2, figsize=(10, 4.2))
ax[0].hist(margin * 100, bins=40, color="#c62828", alpha=0.8)
ax[0].axvline(np.median(margin) * 100, color="k", ls="--", lw=1)
ax[0].set_title(f"Маржа, % (медиана {np.median(margin)*100:.0f}%)")
ax[0].set_xlabel("%"); ax[0].set_ylabel("сценарии")

months = np.arange(1, 25)
cum = np.median(profit) / 12 * months - 5.4   # доп. инвестиции 5,4 млн
ax[1].plot(months, cum, color="#2e7d32", lw=2)
ax[1].axhline(0, color="gray", lw=0.8)
ax[1].set_title(f"Окупаемость масштабирования: {5.4/(np.median(profit)/12):.1f} мес")
ax[1].set_xlabel("месяц"); ax[1].set_ylabel("млн руб. накоплено"); ax[1].grid(alpha=0.3)
fig.suptitle("КУБАНЬ-ХРУСТ: год 2, полная загрузка 155 т/год")
fig.tight_layout()
fig.savefig("khrust_economics.png", dpi=150)
print("медиана прибыли %.1f млн руб./год; маржа %.0f%%" % (np.median(profit), np.median(margin)*100))
