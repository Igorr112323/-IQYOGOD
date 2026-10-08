# КАРБОКУБАНЬ: экономика модуля 300 кг/ч, Монте-Карло 2000 сценариев
# Запуск: python3 carbonkuban_economics.py -> carbonkuban_economics.png
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(11)
N = 2000
OUTPUT = 1600.0        # т биоугля/год
CHAR_COST = 4600.0     # себестоимость, руб./т
price_char = rng.triangular(8500, 9500, 11000, N)   # мелиорант, руб./т
price_co2 = rng.triangular(500, 700, 1000, N)       # руб./т CO2-экв.
co2_per_t = 1.74

revenue = OUTPUT * price_char + OUTPUT * co2_per_t * price_co2
costs = OUTPUT * CHAR_COST + 5.9e6  # сырьё + постоянные
margin = (revenue - costs) / 1e6    # млн руб./год
capex = 1.8  # остаточный CAPEX, млн руб.
payback = capex / margin

plt.rcParams.update({"font.size": 9})
fig, ax = plt.subplots(1, 2, figsize=(10, 4.2))
ax[0].hist(margin, bins=40, color="#2e7d32", alpha=0.85)
ax[0].axvline(np.median(margin), color="k", ls="--", lw=1)
ax[0].set_title(f"Маржа модуля, млн руб./год (медиана {np.median(margin):.1f})")
ax[0].set_xlabel("млн руб./год"); ax[0].set_ylabel("число сценариев")

ax[1].hist(payback, bins=40, color="#15417d", alpha=0.85)
ax[1].axvline(np.median(payback), color="k", ls="--", lw=1)
ax[1].set_title(f"Срок окупаемости, лет (медиана {np.median(payback):.2f})")
ax[1].set_xlabel("лет"); ax[1].set_ylabel("число сценариев")
fig.suptitle("КАРБОКУБАНЬ: двойная монетизация биоугля из лузги (мелиорант + CO2-единицы)")
fig.tight_layout()
fig.savefig("carbonkuban_economics.png", dpi=150)
print("медиана маржи: %.2f млн руб./год; окупаемость %.2f года"
      % (np.median(margin), np.median(payback)))
