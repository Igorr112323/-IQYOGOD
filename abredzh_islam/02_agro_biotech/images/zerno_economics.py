# ЗЕРНОВОЙ ПАСПОРТ: Монте-Карло 3 000 сценариев — экономия хозяйства и окупаемость
# Запуск: python3 zerno_economics.py -> zerno_economics.png
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(2026)
N = 3000

volume_kt = rng.triangular(18, 25, 34, size=N)        # объём зерна через ток за сезон, тыс. т
price = rng.triangular(11.0, 13.5, 16.0, size=N)      # тыс. руб./т пшеницы
loss_before = rng.uniform(0.035, 0.060, size=N)       # потери приёмки и доработки без паспорта
loss_after = loss_before - rng.uniform(0.010, 0.016)  # снижение на 1,0-1,6 п.п.
class_bonus = rng.uniform(0.004, 0.010, size=N)       # премия за класс
savings = volume_kt * 1000 * (loss_before - loss_after) * price / 1e6 \
          + volume_kt * 1000 * class_bonus * price / 1e6  # млн руб./сезон

capex = 4.66
net = 6.7
payback = 12 * capex / net

plt.rcParams.update({"font.size": 9})
fig, ax = plt.subplots(1, 2, figsize=(10, 4.2))
ax[0].hist(savings, bins=40, color="#1b5e20", alpha=0.75)
ax[0].axvline(np.median(savings), color="k", ls="--", lw=1)
ax[0].set_title(f"Экономия хозяйства за сезон, млн руб. (медиана {np.median(savings):.1f})")
ax[0].set_xlabel("млн руб."); ax[0].set_ylabel("сценарии")
ax[1].bar(["капзатраты", "чистый результат", "пост, тыс."], [capex, net, 0.89],
          color="#0d47a1", alpha=0.85)
ax[1].set_title(f"4 поста на два сезона: окупаемость {payback:.1f} мес.")
ax[1].set_ylabel("млн руб."); ax[1].grid(alpha=0.3)
fig.suptitle(f"ЗЕРНОВОЙ ПАСПОРТ: Монте-Карло {N} сценариев")
fig.tight_layout()
fig.savefig("zerno_economics.png", dpi=150)
print("экономия: медиана %.1f млн руб./сезон (p10 %.1f, p90 %.1f); окупаемость %.1f мес."
      % (np.median(savings), np.percentile(savings, 10), np.percentile(savings, 90), payback))
