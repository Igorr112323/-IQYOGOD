# ЖИВОЙ БЕРЕГ: Монте-Карло 3 000 сценариев — спасённые жизни и эффект
# Запуск: python3 bereg_effect.py -> bereg_effect.png
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(2026)
N = 3000

posts = 8
incidents = rng.triangular(2.0, 3.4, 6.0, size=N) * posts * 0.6   # эпизоды тонущих на участке за сезон
detect = rng.uniform(0.82, 0.90, size=N)                            # точность распознавания
launch = rng.uniform(0.85, 0.97, size=N)                            # успешная подача круга
survive_with = rng.uniform(0.75, 0.95, size=N)                      # выживание с кругом в первую минуту
survive_without = rng.uniform(0.25, 0.45, size=N)                   # без поста, вызов очевидцами
saved = incidents * detect * launch * (survive_with - survive_without)
saved = np.clip(saved, 0, None)

# эффект: жизнь — лечение реанимации, компенсации, следствие, закрытие пляжа
cost_case = rng.triangular(4.5, 6.4, 9.0, size=N)                  # млн руб. на случай
effect = saved * cost_case

net = 3.4
capex = 4.2
payback = 12 * capex / net

plt.rcParams.update({"font.size": 9})
fig, ax = plt.subplots(1, 2, figsize=(10, 4.2))
ax[0].hist(saved, bins=30, color="#1b5e20", alpha=0.75)
ax[0].axvline(np.median(saved), color="k", ls="--", lw=1)
ax[0].set_title(f"Спасённые жизни за сезон (медиана {np.median(saved):.0f})")
ax[0].set_xlabel("человек"); ax[0].set_ylabel("сценарии")
ax[1].hist(effect, bins=30, color="#0d47a1", alpha=0.75)
ax[1].axvline(np.median(effect), color="k", ls="--", lw=1)
ax[1].set_title(f"Эффект, млн руб./год (медиана {np.median(effect):.1f}); окупаемость {payback:.1f} мес.")
ax[1].set_xlabel("млн руб.")
fig.suptitle(f"ЖИВОЙ БЕРЕГ: Монте-Карло {N} сценариев")
fig.tight_layout()
fig.savefig("bereg_effect.png", dpi=150)
print("жизни: медиана %.0f (p10 %.0f, p90 %.0f); эффект: медиана %.1f млн руб./год"
      % (np.median(saved), np.percentile(saved, 10), np.percentile(saved, 90), np.median(effect)))
