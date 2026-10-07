# СВЕТЛЫЙ РАЙОН: экономика платформы на 12 поселений (Монте-Карло)
# Запуск: python3 svetly_economics.py -> svetly_economics.png
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(29)
N = 3000

points = rng.triangular(6000, 8000, 10000, N).astype(int)     # светоточек
old_w = rng.uniform(180, 250, N)        # Вт средняя старая лампа ДНаТ/ДРЛ
new_w = rng.uniform(55, 100, N)         # Вт новая с диммированием
hours = 4100.0                            # часов горения в год
tariff = rng.uniform(5.2, 7.4, N)         # руб/кВт-ч (сельский/город)

kwh_old = points * old_w * hours / 1e3
kwh_new = points * new_w * hours / 1e3
saving = (kwh_old - kwh_new) * tariff / 1e6    # млн руб/год

capex = points * rng.uniform(6.0, 7.0) / 1e3   # млн руб, 6-7 тыс/точка
payback = capex / (saving * 0.9)

plt.rcParams.update({"font.size": 9})
fig, ax = plt.subplots(1, 2, figsize=(10, 4.2))
ax[0].hist(saving, bins=40, color="#2e7d32", alpha=0.85)
ax[0].axvline(np.median(saving), color="k", ls="--", lw=1)
ax[0].set_title(f"Экономия 12 поселений, млн руб./год (медиана {np.median(saving):.0f})")
ax[0].set_ylabel("сценарии")
ax[1].hist(payback, bins=40, color="#15417d", alpha=0.85)
ax[1].axvline(7, color="#c62828", ls="--", lw=1.4)
ax[1].set_title(f"Окупаемость, лет (медиана {np.median(payback):.1f}; контракт 7 лет)")
ax[1].set_ylabel("сценарии")
fig.suptitle("СВЕТЛЫЙ РАЙОН: платит не бюджет, а неэффективная лампа")
fig.tight_layout()
fig.savefig("svetly_economics.png", dpi=150)
print("медиана экономии %.1f млн руб./год, окупаемость %.1f года"
      % (np.median(saving), np.median(payback)))
