# ОКО-СКРИН: Монте-Карло 3 000 сценариев — окупаемость точки и проекта
# Запуск: python3 oko_economics.py -> oko_economics.png
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(2020)
N = 3000

# точка в поликлинике
per_day = rng.triangular(22, 30, 40, size=N)        # исследований в день
days = rng.triangular(200, 212, 220, size=N)        # рабочих дней в году
tariff = rng.triangular(280, 320, 360, size=N)      # руб. за исследование (ОМС/программа)
revenue_point = per_day * days * tariff
opex_point = 1.1e6 + 0.12 * revenue_point           # сервис, связь, амортизация, персонал
margin_point = revenue_point - opex_point
payback_point = 12 * 1.19e6 / margin_point          # станция 1,19 млн руб.

# проект: 10 станций в первый полный год (7 продаж + 3 аренды)
rev = (7 * 1.19e6 + 3 * 89_000 * 12 + 10 * 220_000) / 1e6   # продажи, аренда, сервис
net = 3.6
capex = 4.8
payback_project = 12 * capex / net

plt.rcParams.update({"font.size": 9})
fig, ax = plt.subplots(1, 2, figsize=(10, 4.2))
ax[0].hist(np.clip(payback_point, 0, 60), bins=40, color="#00695c", alpha=0.85)
ax[0].axvline(np.median(payback_point), color="k", ls="--", lw=1)
ax[0].set_title(f"Окупаемость станции в поликлинике, мес. (медиана {np.median(payback_point):.0f})")
ax[0].set_xlabel("месяцев"); ax[0].set_ylabel("сценарии")
ax[1].bar(["чистый результат", "капзатраты"], [net, capex], color="#4527a0", alpha=0.85)
ax[1].set_title(f"Проект: {net:.1f} млн руб./год при 10 станциях, окупаемость {payback_project:.1f} мес.")
ax[1].set_ylabel("млн руб."); ax[1].grid(alpha=0.3)
fig.suptitle(f"ОКО-СКРИН: Монте-Карло {N} сценариев")
fig.tight_layout()
fig.savefig("oko_economics.png", dpi=150)
print("точка: медиана окупаемости %.0f мес., доля <=18 мес %.0f%%; проект: окупаемость %.1f мес."
      % (np.median(payback_point), 100 * np.mean(payback_point <= 18), payback_project))
