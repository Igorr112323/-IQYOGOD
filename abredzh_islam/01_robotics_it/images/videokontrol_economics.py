# МУНИЦИПАЛЬНЫЙ ВИДЕОКОНТРОЛЬ: экономика пилота и масштабирование
# Запуск: python3 videokontrol_economics.py -> videokontrol_economics.png
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(33)
N = 2000

# эффект бюджета: неустойки + снятие оплат, % объёма контрактов
contract_mln = rng.triangular(300, 550, 800, N)      # млн руб./год контракты МО
effect_pct = rng.triangular(0.7, 1.1, 1.5, N) / 100
budget_effect = contract_mln * effect_pct            # млн руб./год
license_fee = 1.2 + 18 * 0.015                       # млн руб./год при 18 камерах
roi_years = license_fee / budget_effect

muni = np.array([1, 2, 3, 5, 8])
revenue = muni * 1.4

plt.rcParams.update({"font.size": 9})
fig, ax = plt.subplots(1, 2, figsize=(10, 4.2))
ax[0].hist(budget_effect, bins=40, color="#15417d", alpha=0.85)
ax[0].axvline(np.median(budget_effect), color="k", ls="--", lw=1)
ax[0].set_title(f"Эффект бюджета МО, млн руб./год (медиана {np.median(budget_effect):.1f})")
ax[0].set_xlabel("млн руб./год"); ax[0].set_ylabel("сценарии")
ax[1].bar(muni.astype(str), revenue, color="#2e7d32", alpha=0.85)
ax[1].set_title("Выручка проекта по числу муниципалитетов (к 2028 — 8)")
ax[1].set_xlabel("муниципалитетов"); ax[1].set_ylabel("млн руб./год")
fig.suptitle(f"МУНИЦИПАЛЬНЫЙ ВИДЕОКОНТРОЛЬ: лицензия {license_fee:.2f} млн руб./год, "
             f"окупаемость {np.median(roi_years):.2f} года")
fig.tight_layout()
fig.savefig("videokontrol_economics.png", dpi=150)
print("медиана эффекта бюджета %.1f млн руб./год" % np.median(budget_effect))
