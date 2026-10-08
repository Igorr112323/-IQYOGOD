# ЧИСТОЕ НЕБО: Монте-Карло 3 000 сценариев — предотвращённые затраты на пожар полигона
# Запуск: python3 nebo_effect.py -> nebo_effect.png
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(2026)
N = 3000

# затраты на один допущенный пожар полигона (млн руб.)
extinguish = rng.triangular(8, 16, 30, size=N)        # техника, недели пересыпки, грунт
fines = rng.triangular(3, 8, 18, size=N)             # штрафы надзора и иски
health = rng.triangular(4, 10, 22, size=N)           # ущерб здоровью, дым над жильём
damage = extinguish + fines + health

# сеть на двух полигонах предотвращает часть пожаров
fires_per_year = rng.triangular(1.0, 2.2, 4.0, size=N)   # без сети на два объекта
prevent_share = rng.uniform(0.6, 0.85, size=N)           # доля предотвращённых сетью
prevented = fires_per_year * prevent_share
saved = prevented * damage

net = 5.6
capex = 5.6
payback = 12 * capex / net

plt.rcParams.update({"font.size": 9})
fig, ax = plt.subplots(1, 2, figsize=(10, 4.2))
ax[0].hist(damage, bins=40, color="#b71c1c", alpha=0.75)
ax[0].axvline(np.median(damage), color="k", ls="--", lw=1)
ax[0].set_title(f"Затраты на один пожар, млн руб. (медиана {np.median(damage):.1f})")
ax[0].set_xlabel("млн руб."); ax[0].set_ylabel("сценарии")
ax[1].hist(saved, bins=40, color="#1b5e20", alpha=0.75)
ax[1].axvline(np.median(saved), color="k", ls="--", lw=1)
ax[1].set_title(f"Предотвращённые затраты/год, млн руб. (медиана {np.median(saved):.1f}); окупаемость {payback:.1f} мес.")
ax[1].set_xlabel("млн руб.")
fig.suptitle(f"ЧИСТОЕ НЕБО: Монте-Карло {N} сценариев")
fig.tight_layout()
fig.savefig("nebo_effect.png", dpi=150)
print("пожар: медиана %.1f млн руб. (p10 %.1f, p90 %.1f); предотвращено: медиана %.1f млн руб./год"
      % (np.median(damage), np.percentile(damage, 10), np.percentile(damage, 90), np.median(saved)))
