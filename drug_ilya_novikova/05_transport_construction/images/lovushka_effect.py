# ГОРОД БЕЗ ЛОВУШЕК: Монте-Карло 3 000 сценариев — предотвращённые травмы и потери
# Запуск: python3 lovushka_effect.py -> lovushka_effect.png
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(2026)
N = 3000

manholes = 500
events_per_year = manholes * rng.uniform(0.35, 0.75, size=N)     # событий смещения/просадки/кражи
detect = rng.uniform(0.86, 0.93, size=N)                          # доля обнаруженных датчиками
share_open = rng.uniform(0.18, 0.35, size=N)                      # доля, что стало бы открытой ловушкой
injury_per_open = rng.uniform(0.02, 0.06, size=N)                 # вероятность травмы/аварии за год
prevented = events_per_year * detect * share_open * injury_per_open

# потери на случай: лечение/ремонт авто/компенсации/аварийные работы
cost_case = rng.triangular(1.6, 3.0, 5.5, size=N)                # млн руб.
effect = prevented * cost_case

net = 3.5
capex = 3.8
payback = 12 * capex / net

plt.rcParams.update({"font.size": 9})
fig, ax = plt.subplots(1, 2, figsize=(10, 4.2))
ax[0].hist(prevented, bins=30, color="#1b5e20", alpha=0.75)
ax[0].axvline(np.median(prevented), color="k", ls="--", lw=1)
ax[0].set_title(f"Предотвращённые случаи за год (медиана {np.median(prevented):.0f})")
ax[0].set_xlabel("случаев"); ax[0].set_ylabel("сценарии")
ax[1].hist(effect, bins=30, color="#0d47a1", alpha=0.75)
ax[1].axvline(np.median(effect), color="k", ls="--", lw=1)
ax[1].set_title(f"Предотвращённые потери, млн руб./год (медиана {np.median(effect):.1f}); окупаемость {payback:.1f} мес.")
ax[1].set_xlabel("млн руб.")
fig.suptitle(f"ГОРОД БЕЗ ЛОВУШЕК: Монте-Карло {N} сценариев")
fig.tight_layout()
fig.savefig("lovushka_effect.png", dpi=150)
print("случаи: медиана %.0f (p10 %.0f, p90 %.0f); потери: медиана %.1f млн руб./год"
      % (np.median(prevented), np.percentile(prevented, 10), np.percentile(prevented, 90), np.median(effect)))
