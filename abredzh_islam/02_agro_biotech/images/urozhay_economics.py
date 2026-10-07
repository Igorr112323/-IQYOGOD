# КУБАНЬ-УРОЖАЙ: экономика хаба и эффект хозяйств (Монте-Карло цены)
# Запуск: python3 urozhay_economics.py -> urozhay_economics.png
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(17)
N = 3000

volume = 30_000.0                       # т за сезон
price_harvest = rng.triangular(10500, 11500, 12500, N)     # цена "с колёс" в уборку
price_peak = price_harvest + rng.triangular(500, 1400, 2500, N)  # пик февраль-март
gross_gain = volume * (price_peak - price_harvest) / 1e6   # млн руб.
fee = volume * 0.9 / 1e3 * 1.0 + price_peak * volume * 0.025 / 1e6  # услуги хаба
farm_net = gross_gain - fee            # чистый эффект хозяйств

revenue_hub = volume * 0.9 / 1e3 + price_peak.mean() * volume * 0.025 / 1e6
capex, opex = 240, revenue_hub * 0.62
payback = capex / (revenue_hub - opex)

plt.rcParams.update({"font.size": 9})
fig, ax = plt.subplots(1, 2, figsize=(10, 4.2))
ax[0].hist(farm_net, bins=40, color="#2e7d32", alpha=0.85)
ax[0].axvline(np.median(farm_net), color="k", ls="--", lw=1)
ax[0].set_title(f"Чистый эффект хозяйств, млн руб./сезон (медиана {np.median(farm_net):.0f})")
ax[0].set_ylabel("сценарии")
ax[1].bar(["выручка хаба", "опер. расходы", "маржа"],
          [revenue_hub, opex, revenue_hub - opex], color=["#15417d", "#c62828", "#2e7d32"])
ax[1].set_title(f"Хаб: выручка {revenue_hub:.0f} млн руб., окупаемость капитальных {payback:.1f} года")
ax[1].set_ylabel("млн руб./сезон")
fig.suptitle("КУБАНЬ-УРОЖАЙ: хаб 30 тыс. т, эффект без роста посевов")
fig.tight_layout()
fig.savefig("urozhay_economics.png", dpi=150)
print("медиана эффекта хозяйств %.0f млн руб." % np.median(farm_net))
