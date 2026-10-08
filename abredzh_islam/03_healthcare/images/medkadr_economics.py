# МЕДКАДР-23: Монте-Карло 3 000 сценариев — предотвращённые потери отрасли и окупаемость
# Запуск: python3 medkadr_economics.py -> medkadr_economics.png
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(23)
N = 3000

vacancies = rng.triangular(3800, 5400, 7200, size=N)        # незакрытые вакансии в крае
share_closing = rng.uniform(0.12, 0.22, size=N)             # доля дефицита, закрываемая планированием
cost_vacancy = rng.triangular(220, 320, 460, size=N)        # тыс. руб./год потерь на вакансию
saving = vacancies * share_closing * cost_vacancy / 1000.0  # млн руб./год

capex = 3.1
net = 2.9
payback = 12 * capex / net

plt.rcParams.update({"font.size": 9})
fig, ax = plt.subplots(1, 2, figsize=(10, 4.2))
ax[0].hist(saving, bins=40, color="#1b5e20", alpha=0.75)
ax[0].axvline(np.median(saving), color="k", ls="--", lw=1)
ax[0].set_title(f"Предотвращённые потери отрасли, млн руб./год (медиана {np.median(saving):.0f})")
ax[0].set_xlabel("млн руб."); ax[0].set_ylabel("сценарии")
ax[1].bar(["капзатраты", "чистый результат", "внедрение/территория"],
          [capex, net, 1.9], color="#0d47a1", alpha=0.85)
ax[1].set_title(f"3 территории: окупаемость {payback:.1f} мес.")
ax[1].set_ylabel("млн руб."); ax[1].grid(alpha=0.3)
fig.suptitle(f"МЕДКАДР-23: Монте-Карло {N} сценариев")
fig.tight_layout()
fig.savefig("medkadr_economics.png", dpi=150)
print("потери: медиана %.0f млн руб./год (p10 %.0f, p90 %.0f); окупаемость %.1f мес."
      % (np.median(saving), np.percentile(saving, 10), np.percentile(saving, 90), payback))
