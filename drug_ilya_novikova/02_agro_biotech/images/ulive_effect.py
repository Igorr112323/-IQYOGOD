# ЖИВОЙ УЛЕЙ: Монте-Карло 3 000 сценариев — сохранённые пчелосемьи и эффект
# Запуск: python3 ulive_effect.py -> ulive_effect.png
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(46)
N = 3000

hives = 200                                            # ульев в развёртывании
stress_events = rng.triangular(1.5, 2.4, 4.0, size=N)  # эпизодов риска на пасеку за сезон
detect = rng.uniform(0.80, 0.88, size=N)               # точность обнаружения
save_share = rng.uniform(0.55, 0.80, size=N)           # доля семей, сохранённых при раннем предупреждении
colonies = rng.triangular(4, 7, 12, size=N)            # семей на пасеку
apiaries = hives / colonies.mean()

saved = apiaries * stress_events * detect * save_share * colonies * rng.uniform(0.30, 0.55, size=N)

# эффект: семья даёт мёд + опыление; плюс предотвращённые судебные издержки
value_colony = rng.triangular(140, 190, 260, size=N)   # тыс. руб. за семью за сезон
effect = saved * value_colony / 1000.0                 # млн руб./год

net = 2.2
capex = 3.1
payback = 12 * capex / net

plt.rcParams.update({"font.size": 9})
fig, ax = plt.subplots(1, 2, figsize=(10, 4.2))
ax[0].hist(saved, bins=40, color="#1b5e20", alpha=0.75)
ax[0].axvline(np.median(saved), color="k", ls="--", lw=1)
ax[0].set_title(f"Сохранённые семьи за сезон (медиана {np.median(saved):.0f})")
ax[0].set_xlabel("семей"); ax[0].set_ylabel("сценарии")
ax[1].hist(effect, bins=40, color="#0d47a1", alpha=0.75)
ax[1].axvline(np.median(effect), color="k", ls="--", lw=1)
ax[1].set_title(f"Эффект, млн руб./год (медиана {np.median(effect):.1f}); окупаемость {payback:.1f} мес.")
ax[1].set_xlabel("млн руб.")
fig.suptitle(f"ЖИВОЙ УЛЕЙ: Монте-Карло {N} сценариев")
fig.tight_layout()
fig.savefig("ulive_effect.png", dpi=150)
print("семьи: медиана %.0f (p10 %.0f, p90 %.0f); эффект: медиана %.1f млн руб./год"
      % (np.median(saved), np.percentile(saved, 10), np.percentile(saved, 90), np.median(effect)))
