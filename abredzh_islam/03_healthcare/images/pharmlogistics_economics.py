# ФАРМЛОГИСТИКА-ЮГ: экономика пилота и масштабирование
# Запуск: python3 pharmlogistics_economics.py -> pharmlogistics_economics.png
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(41)
N = 3000

turnover = rng.triangular(1.8, 2.1, 2.5, N)          # млрд руб./год оборот периметра 8 МО
saving_procurement = turnover * 1000 * 0.09          # млн руб. консолидация
saving_writeoff = rng.triangular(30, 45, 60, N)      # млн руб. списания
saving_staff = rng.triangular(28, 38, 50, N)         # млн руб. высвобождение ставок
total = saving_procurement + saving_writeoff + saving_staff

capex = 210.0
op_revenue = turnover * 1000 * 0.035                 # логистическая наценка, млн руб.
payback = capex / (op_revenue * 0.42)                # маржа оператора

plt.rcParams.update({"font.size": 9})
fig, ax = plt.subplots(1, 2, figsize=(10, 4.2))
parts = np.vstack([saving_procurement, saving_writeoff, saving_staff]).T
labels = ["закупки -9 %", "списания", "ставки"]
ax[0].boxplot(parts, tick_labels=labels)
ax[0].set_title("Состав эффекта периметра, млн руб./год")
ax[0].set_ylabel("млн руб./год")
ax[1].hist(total, bins=40, color="#15417d", alpha=0.85)
ax[1].axvline(np.median(total), color="k", ls="--", lw=1)
ax[1].set_title(f"Суммарный эффект, млн руб./год (медиана {np.median(total):.0f}); окупаемость хаба {payback:.1f} г.")
ax[1].set_ylabel("сценарии")
fig.suptitle("ФАРМЛОГИСТИКА-ЮГ: хаб 210 млн руб., наценка оператора 3,5 %")
fig.tight_layout()
fig.savefig("pharmlogistics_economics.png", dpi=150)
print("медиана эффекта %.0f млн руб./год" % np.median(total))
