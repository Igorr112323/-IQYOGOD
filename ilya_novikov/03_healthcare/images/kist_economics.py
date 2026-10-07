# КИСТЬ-М: окупаемость у медорганизации и экономика серии
# Запуск: python3 kist_economics.py -> kist_economics.png
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(2)
N = 2000
PRICE = 149_000.0
patients = rng.triangular(5, 8, 12, N)              # пациентов/мес
sessions = 12
rate = rng.triangular(300, 350, 450, N)             # руб./сеанс возмещения
monthly = patients * sessions * rate
payback_m = PRICE / monthly

# серия
units = np.arange(10, 51, 5)
margin_series = units * (PRICE - 78_000) / 1e6

plt.rcParams.update({"font.size": 9})
fig, ax = plt.subplots(1, 2, figsize=(10, 4.2))
ax[0].hist(payback_m, bins=40, color="#00695c", alpha=0.85)
ax[0].axvline(np.median(payback_m), color="k", ls="--", lw=1)
ax[0].set_title(f"Окупаемость у центра, мес (медиана {np.median(payback_m):.1f})")
ax[0].set_xlabel("месяцев"); ax[0].set_ylabel("сценарии")
ax[1].plot(units, margin_series, "o-", color="#15417d")
ax[1].set_title("Маржа серии: 50 аппаратов/год")
ax[1].set_xlabel("аппаратов/год"); ax[1].set_ylabel("млн руб./год"); ax[1].grid(alpha=0.3)
fig.suptitle("КИСТЬ-М: Монте-Карло 2000 сценариев")
fig.tight_layout()
fig.savefig("kist_economics.png", dpi=150)
print("медиана окупаемости %.1f мес" % np.median(payback_m))
