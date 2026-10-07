# БИОЩИТ-КУБАНЬ: экономика хозяйства, Монте-Карло 1000 псевдосезонов
# Запуск: python3 bioshchit_economics.py -> bioshchit_economics.png
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(7)
N = 1000
AREA = 1000.0           # га
PRICE_WHEAT = 13500.0   # руб./т
YIELD = 48.0            # ц/га базовая
CHEM = 550.0            # руб./га химический протравитель
BIO = 85.0              # руб./га БИОЩИТ-КУБАНЬ

# биологическая эффективность био относительно химии (консервативно 0,5–1,0)
rel_eff = rng.triangular(0.5, 0.8, 1.0, N)
# предотвращённые потери всходов, % площади (эталон-химия): 0,8–1,6 %
saved_pct_chem = rng.triangular(0.8, 1.2, 1.6, N)
saved_pct = saved_pct_chem * rel_eff

revenue_saved = AREA * YIELD * 100 / 1e6 * (saved_pct / 100) * PRICE_WHEAT  # млн
direct_save = AREA * (CHEM - BIO) / 1e6                                      # млн
total = revenue_saved + direct_save

plt.rcParams.update({"font.size": 9})
fig, ax = plt.subplots(1, 2, figsize=(10, 4.2))
ax[0].hist(total, bins=36, color="#5b3a9e", alpha=0.85)
ax[0].axvline(np.median(total), color="k", ls="--", lw=1)
ax[0].set_title(f"Суммарный эффект, млн руб./сезон (медиана {np.median(total):.2f})")
ax[0].set_xlabel("млн руб./сезон"); ax[0].set_ylabel("число сезонов")

price = np.linspace(60, 120, 61)
margin = (price - 28) * 10000 / 1e6   # 10 тыс. га-доз/год, себестоимость 28 руб/дозу
ax[1].plot(price, margin, color="#15417d", lw=2)
ax[1].axhline(0.98, color="r", ls="--", lw=1, label="CAPEX линии 0,98 млн руб.")
ax[1].set_title("Маржа производителя при 10 тыс. га-доз/год")
ax[1].set_xlabel("отпускная цена, руб./га-дозу"); ax[1].set_ylabel("млн руб./год")
ax[1].grid(alpha=0.3); ax[1].legend(fontsize=8)
fig.suptitle("БИОЩИТ-КУБАНЬ: экономическая модель (1000 га озимой пшеницы)")
fig.tight_layout()
fig.savefig("bioshchit_economics.png", dpi=150)
print("медиана эффекта хозяйства: %.2f млн руб./сезон" % np.median(total))
