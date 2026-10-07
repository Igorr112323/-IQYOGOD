# КАРДИОКЛИМАТ-КУБАНЬ: сценарная экономика предотвращения госпитализаций
# Запуск: python3 kardioklimat_economics.py -> kardioklimat_economics.png
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(2025)
N = 3000
RED_DAYS = 23               # дней «красного» уровня в сезоне 2025, 5 муниципалитетов
BASE_HOSP = 1400            # базовое число «пиковых» госпитализаций за эти дни
COST = rng.triangular(100, 125, 150, N) * 1e3   # руб. за случай
PREVENT = rng.triangular(0.05, 0.075, 0.10, N)  # доля предотвращённых (консервативно)

saved = BASE_HOSP * PREVENT * COST / 1e6        # млн руб./сезон
dev_cost = 2.4 + 0.6 * np.arange(0, 5)          # млн руб. накопленные затраты системы по годам

plt.rcParams.update({"font.size": 9})
fig, ax = plt.subplots(1, 2, figsize=(10, 4.2))
ax[0].hist(saved, bins=40, color="#b71c1c", alpha=0.8)
ax[0].axvline(np.median(saved), color="k", ls="--", lw=1)
ax[0].set_title(f"Предотвращённые расходы ОМС, млн руб./сезон (медиана {np.median(saved):.0f})")
ax[0].set_xlabel("млн руб./сезон"); ax[0].set_ylabel("число сценариев")

cum_effect = np.cumsum(np.full(5, np.median(saved)))
ax[1].plot(np.arange(2026, 2031), cum_effect, "o-", color="#15417d", label="эффект накопленный")
ax[1].plot(np.arange(2026, 2031), dev_cost, "s--", color="#b71c1c", label="затраты системы")
ax[1].set_title("Окупаемость в первый же сезон")
ax[1].set_xlabel("год"); ax[1].set_ylabel("млн руб."); ax[1].grid(alpha=0.3); ax[1].legend(fontsize=8)
fig.suptitle("КАРДИОКЛИМАТ-КУБАНЬ: Монте-Карло, 3000 сценариев, 5 пилотных муниципалитетов")
fig.tight_layout()
fig.savefig("kardioklimat_economics.png", dpi=150)
print("медиана предотвращённых расходов: %.1f млн руб./сезон" % np.median(saved))
