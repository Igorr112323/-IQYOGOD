# НОС-КОД: Монте-Карло 3 000 сценариев — предотвращённые нападения и эффект
# Запуск: python3 noskod_effect.py -> noskod_effect.png
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(2026)
N = 3000

# базовые параметры трёх районов
pack_events = rng.triangular(38, 60, 92, size=N)        # событий стай за учебный год в районе
coverage = rng.uniform(0.55, 0.85, size=N)             # доля охваченных маршрутов
detect = rng.uniform(0.82, 0.90, size=N)               # точность обнаружения
attack_given_pack = rng.uniform(0.04, 0.11, size=N)    # вероятность нападения без раннего наряда
prevented = 3 * pack_events * coverage * detect * attack_given_pack

# эффект: лечение, компенсации, внеплановые работы на один случай
cost_case = rng.triangular(0.8, 1.4, 2.6, size=N)      # млн руб.
effect = prevented * cost_case

net = 2.2
capex = 2.4
payback = 12 * capex / net

plt.rcParams.update({"font.size": 9})
fig, ax = plt.subplots(1, 2, figsize=(10, 4.2))
ax[0].hist(prevented, bins=40, color="#1b5e20", alpha=0.75)
ax[0].axvline(np.median(prevented), color="k", ls="--", lw=1)
ax[0].set_title(f"Предотвращённые нападения за учебный год (медиана {np.median(prevented):.0f})")
ax[0].set_xlabel("случаев"); ax[0].set_ylabel("сценарии")
ax[1].hist(effect, bins=40, color="#0d47a1", alpha=0.75)
ax[1].axvline(np.median(effect), color="k", ls="--", lw=1)
ax[1].set_title(f"Эффект, млн руб./год (медиана {np.median(effect):.1f}); окупаемость {payback:.1f} мес.")
ax[1].set_xlabel("млн руб.")
fig.suptitle(f"НОС-КОД: Монте-Карло {N} сценариев")
fig.tight_layout()
fig.savefig("noskod_effect.png", dpi=150)
print("нападения: медиана %.0f (p10 %.0f, p90 %.0f); эффект: медиана %.1f млн руб./год"
      % (np.median(prevented), np.percentile(prevented, 10), np.percentile(prevented, 90), np.median(effect)))
