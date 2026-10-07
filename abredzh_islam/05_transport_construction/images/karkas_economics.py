# ТРАНСПОРТНЫЙ КАРКАС: экономика пилота и тиражирование (Монте-Карло)
# Запуск: python3 karkas_economics.py -> karkas_economics.png
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(51)
N = 3000

# пилот: сборы до/после (млн руб./мес)
base = rng.triangular(9.5, 11.0, 12.5, N)
after = base * rng.triangular(1.12, 1.17, 1.23, N)
uplift = after - base

# тираж на 6 городов: оборот тарифной системы и сбор оператора 3,2 %
cities = 6
turnover_city = rng.triangular(1.1, 1.5, 2.0, N) * 12 * cities  # млрд руб/год
fee = turnover_city * 1000 * 0.032                              # млн руб/год

plt.rcParams.update({"font.size": 9})
fig, ax = plt.subplots(1, 2, figsize=(10, 4.2))
ax[0].hist(uplift, bins=40, color="#2e7d32", alpha=0.85)
ax[0].axvline(np.median(uplift), color="k", ls="--", lw=1)
ax[0].set_title(f"Прирост сборов пилота, млн руб./мес (медиана {np.median(uplift):.1f})")
ax[0].set_ylabel("сценарии")
ax[1].hist(fee, bins=40, color="#15417d", alpha=0.85)
ax[1].axvline(np.median(fee), color="k", ls="--", lw=1)
ax[1].set_title(f"Выручка оператора при тираже на 6 городов, млн руб./год (медиана {np.median(fee):.0f})")
ax[1].set_ylabel("сценарии")
fig.suptitle("ТРАНСПОРТНЫЙ КАРКАС: сбор 3,2 %, концессия 1,9 млрд руб. на 12 лет")
fig.tight_layout()
fig.savefig("karkas_economics.png", dpi=150)
print("медиана прироста сборов %.1f млн руб./мес" % np.median(uplift))
