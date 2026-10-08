# СОРТБОТ-ЮГ: Монте-Карло 3 000 сценариев — окупаемость у оператора и у проекта
# Запуск: python3 sortbot_economics.py -> sortbot_economics.png
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(12)
N = 3000
PRICE = 4.9e6

# оператор: замена 4 сортировщиков + плёнка
salary = rng.triangular(42_000, 52_000, 64_000, size=N) * 4 * 12 * 1.3   # ФОТ с взносами
film_t = rng.triangular(22, 27, 33, size=N) * 12                          # т/год
film_price = rng.triangular(6_500, 8_500, 11_000, size=N)                 # руб/т
benefit = salary + film_t * film_price
payback_operator = 12 * PRICE / benefit

# проект: 8 модулей в первый полный год
cost_module = 3.3e6
margin = (PRICE - cost_module) * 8
opex_fixed = 4.5e6
net = margin - opex_fixed
capex = 8.2e6
payback_project = 12 * capex / net

plt.rcParams.update({"font.size": 9})
fig, ax = plt.subplots(1, 2, figsize=(10, 4.2))
ax[0].hist(np.clip(payback_operator, 0, 40), bins=40, color="#2e7d32", alpha=0.85)
ax[0].axvline(np.median(payback_operator), color="k", ls="--", lw=1)
ax[0].set_title(f"Окупаемость модуля у оператора, мес. (медиана {np.median(payback_operator):.0f})")
ax[0].set_xlabel("месяцев"); ax[0].set_ylabel("сценарии")
ax[1].bar(["чистый результат", "капзатраты"], [net / 1e6, capex / 1e6],
          color="#ef6c00", alpha=0.85)
ax[1].set_title(f"Проект: {net/1e6:.1f} млн руб./год при 8 модулях, окупаемость {payback_project:.1f} мес.")
ax[1].set_ylabel("млн руб."); ax[1].grid(alpha=0.3)
fig.suptitle(f"СОРТБОТ-ЮГ: Монте-Карло {N} сценариев")
fig.tight_layout()
fig.savefig("sortbot_economics.png", dpi=150)
print("оператор: медиана окупаемости %.0f мес., доля <=18 мес %.0f%%; проект: чистый %.1f млн/год, окупаемость %.1f мес."
      % (np.median(payback_operator), 100 * np.mean(payback_operator <= 18), net / 1e6, payback_project))
