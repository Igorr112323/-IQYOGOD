# АГРОВОЛЬТАИКА-КУБАНЬ: экономика проекта и клиента (винодельни)
# Запуск: python3 solarpark_economics.py -> solarpark_economics.png
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(23)
N = 3000

# --- клиент: секция 50 кВт на винограднике ---
kwh_year = rng.triangular(56, 60, 64) * 1e3      # кВт·ч/год (1 120–1 280 кВт·ч/кВт)
price_grid = rng.triangular(8.8, 9.5, 10.4)      # руб./кВт·ч для юрлиц
energy_saving = kwh_year * price_grid            # руб./год
# защита урожая: аналог противоградовой сетки (400–600 тыс./га на 0,7 га) + избежание потерь
shield_value = rng.triangular(0.25, 0.42, 0.65) * 1e6
client_benefit = energy_saving + shield_value
client_payback = 7.9e6 / client_benefit          # при покупке секции за 7,9 млн

# --- проект: маржа секции и окупаемость капзатрат ---
sections_year = 6
margin_section = 2.1e6                           # 7,9 − 5,8 млн руб.
revenue = sections_year * 7.9e6
opex = revenue - sections_year * margin_section + 8.4e6  # себестоимость + постоянные расходы
net = (revenue - opex) / 1e6
payback_project = 8.6 / net

plt.rcParams.update({"font.size": 9})
fig, ax = plt.subplots(1, 2, figsize=(10, 4.2))
ax[0].hist(client_payback, bins=40, color="#558b2f", alpha=0.85)
ax[0].axvline(np.median(client_payback), color="k", ls="--", lw=1)
ax[0].set_title(f"Окупаемость секции у винодельни, лет (медиана {np.median(client_payback):.1f})")
ax[0].set_xlabel("лет"); ax[0].set_ylabel("сценарии")
ax[1].hist(client_benefit / 1e6, bins=40, color="#ef6c00", alpha=0.85)
ax[1].axvline(np.median(client_benefit) / 1e6, color="k", ls="--", lw=1)
ax[1].set_title(f"Эффект клиента, млн руб./год (медиана {np.median(client_benefit)/1e6:.2f})")
ax[1].set_xlabel("млн руб./год"); ax[1].grid(alpha=0.3)
fig.suptitle(f"АГРОВОЛЬТАИКА-КУБАНЬ: Монте-Карло {N} сценариев; "
             f"проект: 6 секций, чистый {net:.1f} млн руб./год, окупаемость {payback_project:.1f} года")
fig.tight_layout()
fig.savefig("solarpark_economics.png", dpi=150)
print("клиент: медиана эффекта %.0f тыс. руб./год, окупаемость %.1f года; "
      "проект: чистый %.1f млн руб./год, окупаемость %.2f года"
      % (np.median(client_benefit)/1e3, np.median(client_payback), net, payback_project))
