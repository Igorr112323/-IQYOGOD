# СЕТЬ-КОНТРОЛЬ: Монте-Карло 3 000 сценариев — предотвращённые потери и окупаемость
# Запуск: python3 set_economics.py -> set_economics.png
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(44)
N = 3000

# потери и ущерб без контроля, млн руб./год на зону подачи
water = rng.triangular(9, 16, 26, size=N)        # потери воды по тарифу
outage = rng.triangular(5, 9, 16, size=N)        # аварийные отключения, раскопки, компенсации
ground = rng.triangular(2, 6, 14, size=N)        # размывы, провалы, восстановление благоустройства
loss = water + outage + ground

detect = rng.uniform(0.65, 0.85, size=N)         # доля потерь, переводимых в управляемые
saved = loss * detect

capex = 6.44
net = 6.3
payback = 12 * capex / net

plt.rcParams.update({"font.size": 9})
fig, ax = plt.subplots(1, 2, figsize=(10, 4.2))
ax[0].hist(loss, bins=40, color="#b71c1c", alpha=0.7, label="без контроля")
ax[0].hist(saved, bins=40, color="#1b5e20", alpha=0.7, label="под контролем")
ax[0].axvline(np.median(saved), color="k", ls="--", lw=1)
ax[0].set_title(f"Потери зоны, млн руб./год; предотвращено — медиана {np.median(saved):.1f}")
ax[0].set_xlabel("млн руб."); ax[0].set_ylabel("сценарии"); ax[0].legend()
ax[1].bar(["капзатраты", "чистый результат", "сопровождение/год"],
          [capex, net, 3 * 210 / 100, ], color="#0d47a1", alpha=0.85)
ax[1].set_title(f"2 зоны: окупаемость {payback:.1f} мес.")
ax[1].set_ylabel("млн руб."); ax[1].grid(alpha=0.3)
fig.suptitle(f"СЕТЬ-КОНТРОЛЬ: Монте-Карло {N} сценариев")
fig.tight_layout()
fig.savefig("set_economics.png", dpi=150)
print("потери без контроля: медиана %.1f млн руб./год; предотвращено: медиана %.1f; окупаемость %.1f мес."
      % (np.median(loss), np.median(saved), payback))
