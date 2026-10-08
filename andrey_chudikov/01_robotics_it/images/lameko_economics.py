# ЛАМЕКО-СКАН: Монте-Карло 3 000 итераций — предотвращённый ущерб и окупаемость
# Запуск: python3 lameko_economics.py -> lameko_economics.png
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(2026)
N = 3000
HERD = 600                  # голов
PRICE_MILK = 34.0           # руб./кг (закупочная, центральная зона края, 2026)

# параметры раннего выявления
cases = rng.binomial(HERD, rng.triangular(0.15, 0.22, 0.30, size=N))  # доля хромоты в стаде
kg_loss = rng.triangular(1.8, 2.4, 3.1, size=N)          # потеря кг/сутки при позднем выявлении
days_saved = rng.triangular(12, 21, 30, size=N)          # дней потери, которые предотвращаются
vet_cost_saved = rng.triangular(1500, 2600, 4200, size=N) * cases  # руб. на лечение

benefit = cases * kg_loss * days_saved * PRICE_MILK + vet_cost_saved
system_cost = 1.15e6
payback_months = 12 * system_cost / benefit

plt.rcParams.update({"font.size": 9})
fig, ax = plt.subplots(1, 2, figsize=(10, 4.2))
ax[0].hist(benefit / 1e6, bins=40, color="#4527a0", alpha=0.85)
ax[0].axvline(np.median(benefit) / 1e6, color="k", ls="--", lw=1)
ax[0].set_title(f"Предотвращённый ущерб, млн руб./год (медиана {np.median(benefit)/1e6:.2f})")
ax[0].set_xlabel("млн руб./год"); ax[0].set_ylabel("сценарии")
ax[1].hist(np.clip(payback_months, 0, 40), bins=40, color="#2e7d32", alpha=0.85)
ax[1].axvline(np.median(payback_months), color="k", ls="--", lw=1)
ax[1].set_title(f"Окупаемость, мес. (медиана {np.median(payback_months):.1f})")
ax[1].set_xlabel("месяцев"); ax[1].grid(alpha=0.3)
fig.suptitle(f"ЛАМЕКО-СКАН: стадо {HERD} голов, Монте-Карло {N} итераций")
fig.tight_layout()
fig.savefig("lameko_economics.png", dpi=150)
print("медиана пользы %.2f млн руб./год; окупаемость %.1f мес.; доля сценариев <24 мес: %.0f%%"
      % (np.median(benefit)/1e6, np.median(payback_months), 100*np.mean(payback_months < 24)))
