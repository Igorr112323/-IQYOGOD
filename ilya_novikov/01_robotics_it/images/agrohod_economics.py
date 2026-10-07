# АГРОХОД-2: экономия СЗР и окупаемость платформы
# Запуск: python3 agrohod_economics.py -> agrohod_economics.png
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(8)
N = 2000
AREA = 250.0            # га в обслуживании
TRIPS = 12              # обработок за сезон
PRICE = 2500.0          # руб./обработку/га
COST_SERIES = 1.9e6     # руб. серийная платформа

save_frac = rng.triangular(0.26, 0.31, 0.36, N)     # экономия жидкости
base_l = 452.0                                       # л/га базовый расход
chem_rub_ha = rng.triangular(2600, 3200, 3900, N)   # руб./га СЗР+вода, сезон
save_ha = save_frac * chem_rub_ha                    # руб./га/сезон

rev = AREA * TRIPS * PRICE * rng.triangular(0.5, 0.6, 0.75, N)
opex = 1.1e6
margin = rev - opex + save_ha * AREA * 0.0           # эффект хозяйства отдельно
payback = COST_SERIES / margin

plt.rcParams.update({"font.size": 9})
fig, ax = plt.subplots(1, 2, figsize=(10, 4.2))
ax[0].hist(save_ha, bins=40, color="#33691e", alpha=0.85)
ax[0].axvline(np.median(save_ha), color="k", ls="--", lw=1)
ax[0].set_title(f"Экономия хозяйства, руб./га/сезон (медиана {np.median(save_ha):.0f})")
ax[0].set_xlabel("руб./га"); ax[0].set_ylabel("сценарии")
ax[1].hist(payback, bins=40, color="#0d47a1", alpha=0.85)
ax[1].axvline(np.median(payback), color="k", ls="--", lw=1)
ax[1].set_title(f"Окупаемость платформы, сезонов (медиана {np.median(payback):.2f})")
ax[1].set_xlabel("сезонов"); ax[1].set_ylabel("сценарии")
fig.suptitle("АГРОХОД-2: Монте-Карло 2000 сценариев, 250 га, 12 обработок")
fig.tight_layout()
fig.savefig("agrohod_economics.png", dpi=150)
print("медиана экономии %.0f руб./га/сезон; окупаемость %.2f сезона"
      % (np.median(save_ha), np.median(payback)))
