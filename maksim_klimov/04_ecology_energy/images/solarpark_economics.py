# СОЛНЦЕПАРК: экономика модуля и сети
# Запуск: python3 solarpark_economics.py -> solarpark_economics.png
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(17)
N = 3000
CAPEX = 2.1e6                       # руб., коммерческий модуль

season_kwh = rng.triangular(26, 30, 34) * 1e3     # МВт·ч -> кВт·ч за сезон
selfuse = rng.triangular(0.85, 0.92, 0.97)
price_hotel = 13.5                                  # руб./кВт·ч (ниже пикового тарифа)
charge_money = rng.triangular(240, 340, 460) * 1e3  # руб./сезон, зарядки
winter = 210_000                                    # межсезонье, руб./год

revenue = season_kwh * selfuse * price_hotel + charge_money + winter
opex = 85_000 + 0.03 * revenue
margin = (revenue - opex) / 1e3
payback = CAPEX / (margin * 1e3)

plt.rcParams.update({"font.size": 9})
fig, ax = plt.subplots(1, 2, figsize=(10, 4.2))
ax[0].hist(margin, bins=40, color="#ef6c00", alpha=0.85)
ax[0].axvline(np.median(margin), color="k", ls="--", lw=1)
ax[0].set_title(f"Маржа модуля, тыс. руб./год (медиана {np.median(margin):.0f})")
ax[0].set_xlabel("тыс. руб./год"); ax[0].set_ylabel("сценарии")

n = np.arange(3, 16)
ax[1].plot(n, np.median(margin) * n / 1e3, "o-", color="#15417d")
ax[1].set_title(f"Маржа сети: 15 модулей к сезону-2027 (окупаемость {np.median(payback):.1f} года)")
ax[1].set_xlabel("модулей"); ax[1].set_ylabel("млн руб./год"); ax[1].grid(alpha=0.3)
fig.suptitle("СОЛНЦЕПАРК: Монте-Карло 3000 сценариев, отель побережья")
fig.tight_layout()
fig.savefig("solarpark_economics.png", dpi=150)
print("медиана маржи %.0f тыс. руб./год; окупаемость %.2f года"
      % (np.median(margin), np.median(payback)))
