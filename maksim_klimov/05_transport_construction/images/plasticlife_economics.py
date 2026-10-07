# ВТОРАЯ ЖИЗНЬ ПЛАСТИКА: экономика трёх потоков дохода
# Запуск: python3 plasticlife_economics.py -> plasticlife_economics.png
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(31)
N = 3000
CAPEX = 3.4e6

tons = rng.triangular(380, 480, 560, N)            # т пластика в год
gate = tons * 6500                                  # приём отходов, руб.
benches = rng.triangular(450, 600, 720, N)
furniture = benches * 9500 + tons * 8 * 1000       # мебель + плитка/урны (руб./т продукции)
rop = rng.triangular(0.9, 1.5, 2.2, N) * 1e6        # брендированные контракты
revenue = (gate + furniture + rop) / 1e6
costs = (0.38 * revenue + 3.1)                      # переменные + постоянные, млн/год
margin = revenue - costs
payback = CAPEX / 1e6 / margin

plt.rcParams.update({"font.size": 9})
fig, ax = plt.subplots(1, 2, figsize=(10, 4.2))
ax[0].hist(margin, bins=40, color="#2e7d32", alpha=0.85)
ax[0].axvline(np.median(margin), color="k", ls="--", lw=1)
ax[0].set_title(f"Маржа, млн руб./год (медиана {np.median(margin):.1f})")
ax[0].set_xlabel("млн руб./год"); ax[0].set_ylabel("сценарии")
ax[1].hist(payback, bins=40, color="#15417d", alpha=0.85)
ax[1].axvline(np.median(payback), color="k", ls="--", lw=1)
ax[1].set_title(f"Окупаемость комплекса 3,4 млн руб., лет (медиана {np.median(payback):.2f})")
ax[1].set_xlabel("лет"); ax[1].set_ylabel("сценарии")
fig.suptitle("ВТОРАЯ ЖИЗНЬ ПЛАСТИКА: Монте-Карло 3000 сценариев, 480 т/год")
fig.tight_layout()
fig.savefig("plasticlife_economics.png", dpi=150)
print("медиана маржи %.2f млн руб./год; окупаемость %.2f года"
      % (np.median(margin), np.median(payback)))
