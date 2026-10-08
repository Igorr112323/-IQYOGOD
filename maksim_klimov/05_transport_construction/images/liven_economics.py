# ЛИВЕНЬ-ПРО: Монте-Карло 3 000 сценариев — ущерб подтоплений и окупаемость проекта
# Запуск: python3 liven_economics.py -> liven_economics.png
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(2026)
N = 3000

# ущерб одного подтопления районного масштаба (дороги, трамваи, компенсации)
road = rng.triangular(3.0, 5.2, 9.0, size=N)          # ремонт полотна, млн
tram = rng.triangular(0.4, 1.1, 2.4, size=N)          # простой и инфраструктура
comp = rng.triangular(0.6, 2.4, 6.0, size=N)          # компенсации и внеплановые работы
damage = road + tram + comp                            # млн руб. за событие

# проект: 3 района в первый полный год
rev = 3 * 8.9 + 3 * 180_000 * 12 / 1e6                 # районы + платформа
net = 7.8
capex = 6.4
payback_project = 12 * capex / net
events_avoided = 3                                      # предотвращённых событий в год
city_saving = np.median(damage) * events_avoided

plt.rcParams.update({"font.size": 9})
fig, ax = plt.subplots(1, 2, figsize=(10, 4.2))
ax[0].hist(damage, bins=40, color="#b71c1c", alpha=0.75)
ax[0].axvline(np.median(damage), color="k", ls="--", lw=1)
ax[0].set_title(f"Ущерб одного потопа района, млн руб. (медиана {np.median(damage):.1f})")
ax[0].set_xlabel("млн руб."); ax[0].set_ylabel("сценарии")
ax[1].bar(["чистый результат", "капзатраты", "экономия города/год"],
          [net, capex, city_saving], color="#0d47a1", alpha=0.85)
ax[1].set_title(f"Проект: {net:.1f} млн/год, окупаемость {payback_project:.1f} мес.; "
                f"город экономит {city_saving:.0f} млн/год")
ax[1].set_ylabel("млн руб."); ax[1].grid(alpha=0.3)
fig.suptitle(f"ЛИВЕНЬ-ПРО: Монте-Карло {N} сценариев")
fig.tight_layout()
fig.savefig("liven_economics.png", dpi=150)
print("ущерб: медиана %.1f млн руб./потоп; проект: окупаемость %.1f мес.; город: %.0f млн руб./год"
      % (np.median(damage), payback_project, city_saving))
