# ФОНО-ВЕКС: Монте-Карло 3 000 итераций — эффект района и окупаемость проекта
# Запуск: python3 fonoveks_economics.py -> fonoveks_economics.png
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(77)
N = 3000
POP = 1200                      # участников 65+ на район

prevalence = rng.triangular(0.10, 0.15, 0.22, size=N)     # невыявленная симптоматика в группе
detection = rng.triangular(0.55, 0.70, 0.85, size=N)      # доля, выявленная скринингом
cases_avoided_frac = rng.triangular(0.06, 0.11, 0.18, size=N)  # доля предотвращаемых случаев
annual_cases_per_person = 0.9                              # эпизодов обращения на участника в год
case_cost = rng.triangular(18_000, 26_000, 40_000, size=N)  # руб. на случай (скорая/госпитализация)

cases_prevented = POP * annual_cases_per_person * prevalence * detection * cases_avoided_frac
savings = cases_prevented * case_cost                       # руб./год на район

capex = 1.8e6
revenue = 12 * 68_000 * 12       # 12 районов × 68 тыс./мес × 12 мес
opex = 6.2e6
net = revenue - opex
payback_months = 12 * capex / net

plt.rcParams.update({"font.size": 9})
fig, ax = plt.subplots(1, 2, figsize=(10, 4.2))
ax[0].hist(savings / 1e6, bins=40, color="#00695c", alpha=0.85)
ax[0].axvline(np.median(savings) / 1e6, color="k", ls="--", lw=1)
ax[0].set_title(f"Эффект района, млн руб./год (медиана {np.median(savings)/1e6:.1f})")
ax[0].set_xlabel("млн руб./год"); ax[0].set_ylabel("сценарии")
ax[1].hist(np.clip(payback_months, 0, 24), bins=30, color="#4527a0", alpha=0.85)
ax[1].axvline(payback_months, color="k", ls="--", lw=1)
ax[1].set_title(f"Окупаемость проекта, мес. ({payback_months:.1f}); чистый {net/1e6:.1f} млн руб./год")
ax[1].set_xlabel("месяцев"); ax[1].grid(alpha=0.3)
fig.suptitle(f"ФОНО-ВЕКС: {POP} участников на район, Монте-Карло {N} итераций")
fig.tight_layout()
fig.savefig("fonoveks_economics.png", dpi=150)
print("медиана эффекта района %.2f млн руб./год; чистый %.2f млн руб./год; окупаемость %.1f мес."
      % (np.median(savings) / 1e6, net / 1e6, payback_months))
