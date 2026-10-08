# КАПРЕМОНТ-КОНТРОЛЬ: Монте-Карло 3 000 сценариев — предотвращённые потери бюджета и окупаемость
# Запуск: python3 kaprem_economics.py -> kaprem_economics.png
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(615)
N = 3000

budget = rng.uniform(8.8, 9.2, size=N)               # млрд руб. годовая программа края
defect_share = rng.uniform(0.025, 0.055, size=N)      # доля работ с отклонениями без контроля
detect = rng.uniform(0.65, 0.85, size=N)              # доля отклонений, ловимая приёмкой
rework_cost = rng.uniform(0.5, 0.8, size=N)           # доля стоимости работ на переделку
warranty_loss = rng.uniform(0.008, 0.02, size=N)      # потери гарантийного периода без реестра
loss = budget * 1000 * (defect_share * detect * rework_cost + warranty_loss)  # млн руб./год

capex = 3.0
net = 3.7
payback = 12 * capex / net

plt.rcParams.update({"font.size": 9})
fig, ax = plt.subplots(1, 2, figsize=(10, 4.2))
ax[0].hist(loss, bins=40, color="#b71c1c", alpha=0.75)
ax[0].axvline(np.median(loss), color="k", ls="--", lw=1)
ax[0].set_title(f"Предотвращённые потери бюджета, млн руб./год (медиана {np.median(loss):.0f})")
ax[0].set_xlabel("млн руб."); ax[0].set_ylabel("сценарии")
ax[1].bar(["капзатраты", "чистый результат", "внедрение/муниципалитет"],
          [capex, net, 2.4], color="#0d47a1", alpha=0.85)
ax[1].set_title(f"3 муниципалитета: окупаемость {payback:.1f} мес.")
ax[1].set_ylabel("млн руб."); ax[1].grid(alpha=0.3)
fig.suptitle(f"КАПРЕМОНТ-КОНТРОЛЬ: Монте-Карло {N} сценариев")
fig.tight_layout()
fig.savefig("kaprem_economics.png", dpi=150)
print("потери: медиана %.0f млн руб./год (p10 %.0f, p90 %.0f); окупаемость %.1f мес."
      % (np.median(loss), np.percentile(loss, 10), np.percentile(loss, 90), payback))
