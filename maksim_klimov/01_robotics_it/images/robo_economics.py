# ЮЖНЫЙ РОБОКУРЬЕР: юнит-экономика флота
# Запуск: python3 robo_economics.py -> robo_economics.png
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(42)
N = 3000
SEASON = 150                     # дней активного сезона
PRICE = 190.0                    # руб./доставка
CAPEX = 680_000.0                # серийный ровер

deliveries = rng.triangular(8, 12, 18, N)          # доставок/день на ровер
util = rng.triangular(0.35, 0.55, 0.8, N)          # загрузка флота
revenue = deliveries * util * PRICE * SEASON       # руб./сезон
opex = 188_000 * SEASON / 365 + revenue * 0.06     # сервис, энергия, эквайринг
margin = (revenue - opex) / 1e3
payback = CAPEX / (margin * 1e3)

plt.rcParams.update({"font.size": 9})
fig, ax = plt.subplots(1, 2, figsize=(10, 4.2))
ax[0].hist(margin, bins=40, color="#ef6c00", alpha=0.85)
ax[0].axvline(np.median(margin), color="k", ls="--", lw=1)
ax[0].set_title(f"Маржа на ровер, тыс. руб./сезон (медиана {np.median(margin):.0f})")
ax[0].set_xlabel("тыс. руб./сезон"); ax[0].set_ylabel("сценарии")

fleet = np.arange(1, 31)
gp = np.median(margin) * fleet / 1e3
ax[1].plot(fleet, gp, "o-", color="#15417d")
ax[1].set_title("Валовая прибыль флота (к сезону-2028 — 30 роверов)")
ax[1].set_xlabel("роверов"); ax[1].set_ylabel("млн руб./сезон"); ax[1].grid(alpha=0.3)
fig.suptitle("ЮЖНЫЙ РОБОКУРЬЕР: Монте-Карло 3000 сценариев, сезон 150 дней")
fig.tight_layout()
fig.savefig("robo_economics.png", dpi=150)
print("медиана маржи %.0f тыс. руб./сезон; окупаемость %.2f года"
      % (np.median(margin), np.median(payback)))
