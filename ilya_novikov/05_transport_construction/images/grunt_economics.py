# ГРУНТ-МЕМ М1: Монте-Карло 3 000 итераций — предотвращённый ущерб провала и окупаемость
# Запуск: python3 grunt_economics.py -> grunt_economics.png
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(100)
N = 3000

# ущерб одного провала районного масштаба (млн руб.): аварийный ремонт, перекрытие, сети
excav = rng.triangular(4.0, 7.5, 14.0, size=N)      # раскопки и восстановление коллектора
road = rng.triangular(2.0, 4.2, 8.0, size=N)       # дорожное полотно и перекрытие
util = rng.triangular(1.0, 2.6, 6.5, size=N)       # повреждённые смежные сети
social = rng.triangular(0.5, 1.4, 3.0, size=N)     # компенсации, простой, объезды
damage = excav + road + util + social

points = 190                                         # точек мониторинга в первый полный год
margin = 27                                          # тыс. руб./точка
capex = 3.4                                          # млн руб.
net = 5.2                                            # млн руб./год
payback = 12 * capex / net

plt.rcParams.update({"font.size": 9})
fig, ax = plt.subplots(1, 2, figsize=(10, 4.2))
ax[0].hist(damage, bins=40, color="#b71c1c", alpha=0.75)
ax[0].axvline(np.median(damage), color="k", ls="--", lw=1)
ax[0].set_title(f"Ущерб одного провала, млн руб. (медиана {np.median(damage):.1f})")
ax[0].set_xlabel("млн руб."); ax[0].set_ylabel("итерации")
ax[1].bar(["маржа/точка, тыс.", "капзатраты, млн", "чистый результат, млн"],
          [margin, capex, net], color="#0d47a1", alpha=0.85)
ax[1].set_title(f"{points} точек в год, окупаемость {payback:.1f} мес.")
ax[1].set_ylabel("значение"); ax[1].grid(alpha=0.3)
fig.suptitle(f"ГРУНТ-МЕМ М1: Монте-Карло {N} итераций")
fig.tight_layout()
fig.savefig("grunt_economics.png", dpi=150)
print("ущерб провала: медиана %.1f млн руб. (p10 %.1f, p90 %.1f); окупаемость %.1f мес."
      % (np.median(damage), np.percentile(damage, 10), np.percentile(damage, 90), payback))
