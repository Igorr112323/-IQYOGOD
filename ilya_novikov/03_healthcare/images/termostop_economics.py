# ТЕРМОСТОПА-32: Монте-Карло 3 000 итераций — предотвращённые затраты и окупаемость
# Запуск: python3 termostop_economics.py -> termostop_economics.png
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(2323)
N = 3000

screened = rng.integers(1200, 2600, size=N)            # измерений в год на отделение
rate_early = rng.uniform(0.025, 0.055, size=N)         # доля выявленных ранних случаев
avoided_share = rng.uniform(0.35, 0.60, size=N)        # доля случаев, где лечение упрощено
save_per_case = rng.triangular(180, 260, 380, size=N)  # тыс. руб. на случай (госпитализация, курс)
savings = screened * rate_early * avoided_share * save_per_case / 1000.0  # млн руб./год

devices = 90
margin = 27                                            # тыс. руб./шт.
capex = 2.9                                            # млн руб.
net = 3.3                                              # млн руб./год
payback = 12 * capex / net

plt.rcParams.update({"font.size": 9})
fig, ax = plt.subplots(1, 2, figsize=(10, 4.2))
ax[0].hist(savings, bins=40, color="#1b5e20", alpha=0.75)
ax[0].axvline(np.median(savings), color="k", ls="--", lw=1)
ax[0].set_title(f"Предотвращённые затраты отделения, млн руб./год (медиана {np.median(savings):.1f})")
ax[0].set_xlabel("млн руб."); ax[0].set_ylabel("итерации")
ax[1].bar(["маржа на устройство, тыс.", "капзатраты, млн", "чистый результат, млн"],
          [margin, capex, net], color="#0d47a1", alpha=0.85)
ax[1].set_title(f"{devices} устройств в год, окупаемость {payback:.1f} мес.")
ax[1].set_ylabel("значение"); ax[1].grid(alpha=0.3)
fig.suptitle(f"ТЕРМОСТОПА-32: Монте-Карло {N} итераций")
fig.tight_layout()
fig.savefig("termostop_economics.png", dpi=150)
print("затраты: медиана %.1f млн руб./год (p10 %.1f, p90 %.1f); окупаемость %.1f мес."
      % (np.median(savings), np.percentile(savings, 10), np.percentile(savings, 90), payback))
