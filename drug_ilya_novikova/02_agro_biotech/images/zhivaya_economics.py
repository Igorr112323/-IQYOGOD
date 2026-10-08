# БИОФИЛЬТР-СТОК: Монте-Карло 2 000 сценариев окупаемости у хозяйства
# Запуск: python3 zhivaya_economics.py -> zhivaya_economics.png
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(31)
N = 2000
MODULE_COST = 480_000            # руб., модуль под ключ для фермы 100–150 голов

# предотвращаемые потери: штрафы ст. 8.14 КоАП, иски о вреде водному объекту, платежи НВОС
fine = rng.choice([0, 60_000, 100_000, 150_000], size=N, p=[0.45, 0.25, 0.2, 0.1])
claim = rng.triangular(0, 350_000, 2_400_000) * rng.random(N) * 0.35   # риск иска в год
nvos = rng.triangular(30_000, 60_000, 110_000)                          # платежи НВОС
annual_benefit = fine + claim + nvos

payback_months = MODULE_COST / (annual_benefit / 12.0)
payback_months = np.clip(payback_months, 1, 60)

# проект: 8 модулей в первый полный год
proj_net = (8 * (480_000 - 340_000) + 8 * 12_000 * 12 - 1_050_000) / 1e6

plt.rcParams.update({"font.size": 9})
fig, ax = plt.subplots(1, 2, figsize=(10, 4.2))
ax[0].hist(payback_months, bins=40, color="#2e7d32", alpha=0.85)
ax[0].axvline(np.median(payback_months), color="k", ls="--", lw=1)
ax[0].set_title(f"Окупаемость модуля у фермы, мес. (медиана {np.median(payback_months):.0f})")
ax[0].set_xlabel("месяцев"); ax[0].set_ylabel("сценарии")
share = 100 * np.mean(payback_months <= 18)
ax[1].bar(["чистый результат", "капзатраты"], [proj_net, 0.65], color="#1565c0", alpha=0.85)
ax[1].set_title(f"Проект: {proj_net:.1f} млн руб./год при 8 модулях ({share:.0f}% сценариев ≤ 18 мес.)")
ax[1].set_ylabel("млн руб.")
fig.suptitle("БИОФИЛЬТР-СТОК: Монте-Карло 2 000 сценариев, ферма на 120 голов")
fig.tight_layout()
fig.savefig("zhivaya_economics.png", dpi=150)
print("медиана окупаемости у хозяйства: %.0f мес.; доля <=18 мес.: %.0f%%; "
      "чистый результат проекта: %.2f млн руб./год" % (np.median(payback_months), share, proj_net))
