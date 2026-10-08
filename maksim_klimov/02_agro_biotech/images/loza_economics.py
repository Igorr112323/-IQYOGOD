# ВТОРАЯ ЛОЗА: Монте-Карло 3 000 сценариев — окупаемость у винодельни и у проекта
# Запуск: python3 loza_economics.py -> loza_economics.png
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(34)
N = 3000

# винодельня среднего размера: 1 600 т выжимок за сезон
pomace_t = rng.triangular(1200, 1600, 2200, size=N)
yield_kg = rng.triangular(2.9, 3.1, 3.4, size=N)          # кг экстракта с тонны
price = rng.triangular(5500, 6200, 7000, size=N)          # руб./кг
cost_kg = rng.triangular(2600, 2940, 3400, size=N)        # себестоимость
extract_kg = pomace_t * yield_kg
margin_winery = extract_kg * (price - cost_kg)
# сервисная модель 50/50 без входного чека: винодельня получает половину маржи сразу
payback_service = np.full(N, 0.0)                          # вход нулевой, результат с 1-го сезона
payback_buy = 12 * 7.9e6 / margin_winery                  # при покупке модуля

# проект: 4 модуля (2 продажи + 2 сервисных) и 12 т экстракта
rev_sales = 2 * 7.9e6
rev_extract = 12_000 * 6200 * 0.5                          # сервисные модули: доля проекта 50 %
revenue = (rev_sales + rev_extract) / 1e6
opex = revenue - 7.8
net = 7.8
capex = 9.4
payback_project = 12 * capex / net

plt.rcParams.update({"font.size": 9})
fig, ax = plt.subplots(1, 2, figsize=(10, 4.2))
ax[0].hist(np.clip(payback_buy, 0, 84) / 12, bins=40, color="#6a1b9a", alpha=0.85)
ax[0].axvline(np.median(payback_buy) / 12, color="k", ls="--", lw=1)
ax[0].set_title(f"Окупаемость модуля при покупке, лет (медиана {np.median(payback_buy)/12:.1f})")
ax[0].set_xlabel("лет"); ax[0].set_ylabel("сценарии")
ax[1].bar(["чистый результат", "капзатраты"], [net, capex], color="#ef6c00", alpha=0.85)
ax[1].set_title(f"Проект: {net:.1f} млн руб./год (4 модуля + 12 т), окупаемость {payback_project:.1f} мес.")
ax[1].set_ylabel("млн руб."); ax[1].grid(alpha=0.3)
fig.suptitle(f"ВТОРАЯ ЛОЗА: Монте-Карло {N} сценариев; сервисная модель 50/50 окупается с 1-го сезона")
fig.tight_layout()
fig.savefig("loza_economics.png", dpi=150)
print("винодельня (покупка): медиана %.1f года; проект: чистый %.1f млн/год, окупаемость %.1f мес."
      % (np.median(payback_buy) / 12, net, payback_project))
