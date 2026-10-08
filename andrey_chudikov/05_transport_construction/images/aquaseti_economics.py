# АКУСТИК-СЕТИ: экономика обнаружения утечек, Монте-Карло 3000 сценариев
# Запуск: python3 aquaseti_economics.py -> aquaseti_economics.png
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(3)
N = 3000
LENGTH_KM = 200.0
TARIFF = 47.0            # руб./м³, Новороссийск
NODES = 900
CAPEX = NODES * 7200 + 1.4e6   # узлы + сервер/внедрение

leaks_year = rng.poisson(np.clip(rng.normal(46, 9, N), 20, 90))      # скрытых утечек/год
q_m3h = rng.triangular(0.6, 1.2, 2.4, N)                              # средний дебит
months_hidden = rng.triangular(1.0, 3.0, 6.0, N)                      # без системы
saved_m3 = leaks_year * q_m3h * 24 * 30.4 * months_hidden
water_money = saved_m3 * TARIFF / 1e6
avaria = rng.poisson(10, N) * rng.triangular(300, 400, 600, N) * 1e3 / 1e6
total = water_money + avaria
payback_years = CAPEX / 1e6 / total

plt.rcParams.update({"font.size": 9})
fig, ax = plt.subplots(1, 2, figsize=(10, 4.2))
ax[0].hist(total, bins=40, color="#01579b", alpha=0.85)
ax[0].axvline(np.median(total), color="k", ls="--", lw=1)
ax[0].set_title(f"Эффект, млн руб./год (медиана {np.median(total):.1f})")
ax[0].set_xlabel("млн руб./год"); ax[0].set_ylabel("число сценариев")
ax[1].hist(payback_years, bins=40, color="#2e7d32", alpha=0.85)
ax[1].axvline(np.median(payback_years), color="k", ls="--", lw=1)
ax[1].set_title(f"Окупаемость, лет (медиана {np.median(payback_years):.2f})")
ax[1].set_xlabel("лет"); ax[1].set_ylabel("число сценариев")
fig.suptitle("АКУСТИК-СЕТИ: 200 км магистралей Новороссийска, 900 узлов")
fig.tight_layout()
fig.savefig("aquaseti_economics.png", dpi=150)
print("медиана эффекта %.1f млн руб./год; окупаемость %.2f года"
      % (np.median(total), np.median(payback_years)))
