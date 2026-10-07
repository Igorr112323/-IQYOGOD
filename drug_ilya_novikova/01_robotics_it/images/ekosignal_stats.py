# ЭКОСИГНАЛ КУБАНИ: результаты пилота (8 недель, Динской район)
# Запуск: python3 ekosignal_stats.py -> ekosignal_stats.png
import numpy as np
import matplotlib.pyplot as plt

cats = ["свалки и площадки", "водоёмы", "дым и гарь", "прочее"]
vals = [0.58, 0.21, 0.12, 0.09]
resolved = [0.67, 0.55, 0.61, 0.60]

weeks = np.arange(1, 9)
signals = np.array([14, 19, 24, 27, 31, 34, 33, 32])
reaction = np.array([19, 17, 14, 12, 10, 8, 7, 7])   # средний срок реакции, дней

plt.rcParams.update({"font.size": 9})
fig, ax = plt.subplots(1, 3, figsize=(12, 3.8))
ax[0].pie(vals, labels=cats, autopct="%.0f%%", colors=["#8d6e63", "#4fc3f7", "#ff8a65", "#bdbdbd"])
ax[0].set_title("Категории сигналов (214)")
ax[1].barh(cats, [r * 100 for r in resolved], color="#2e7d32", alpha=0.85)
ax[1].set_title("Доля подтверждённо решённых, %"); ax[1].set_xlim(0, 100)
ax2 = ax[2]
ax2.plot(weeks, signals, "o-", color="#1565c0", label="сигналов в неделю")
ax2b = ax2.twinx()
ax2b.plot(weeks, reaction, "s--", color="#c62828", label="срок реакции, дней")
ax2.set_xlabel("неделя"); ax2.set_title("Активность и скорость реакции")
lines1, labels1 = ax2.get_legend_handles_labels()
lines2, labels2 = ax2b.get_legend_handles_labels()
ax2.legend(lines1 + lines2, labels1 + labels2, fontsize=7, loc="upper left")
fig.suptitle("ЭКОСИГНАЛ КУБАНИ: пилот 04–06.2026 — 63 % сигналов закрыто результатом")
fig.tight_layout()
fig.savefig("ekosignal_stats.png", dpi=150)
print("всего сигналов:", signals.sum())
