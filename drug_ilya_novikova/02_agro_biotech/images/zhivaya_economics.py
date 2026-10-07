# ЖИВАЯ ЗЕМЛЯ: динамика пилота и экономика модуля
# Запуск: python3 zhivaya_economics.py -> zhivaya_economics.png
import numpy as np
import matplotlib.pyplot as plt

months = ["02", "03", "04", "05", "06", "07", "08"]
processed_kg = np.array([140, 165, 190, 215, 225, 240, 245])   # данные журнала
humus_kg = np.array([20, 28, 40, 48, 62, 80, 102])             # накопленный сбор

CAPEX = 34_000.0
saving = 4.8e3          # вывоз органики, руб./год
humus_money = 21.6e3    # применение/реализация биогумуса, руб./год
payback = CAPEX / (saving + humus_money)

plt.rcParams.update({"font.size": 9})
fig, ax = plt.subplots(1, 2, figsize=(10, 4.0))
ax[0].bar(months, processed_kg, color="#6d4c41", alpha=0.85, label="переработано, кг/мес")
ax[0].plot(months, humus_kg, "o-", color="#2e7d32", label="биогумус накопленно, кг")
ax[0].set_title("Пилот: 1,42 т органики и 380 кг биогумуса за 7 мес")
ax[0].legend(fontsize=8); ax[0].set_ylabel("кг")

yrs = np.linspace(0, 3, 31)
cum = (saving + humus_money) * yrs - CAPEX
ax[1].plot(yrs, cum / 1e3, color="#1565c0", lw=2)
ax[1].axhline(0, color="gray", lw=0.8)
ax[1].set_title(f"Окупаемость модуля: {payback*12:.0f} мес")
ax[1].set_xlabel("лет"); ax[1].set_ylabel("тыс. руб."); ax[1].grid(alpha=0.3)
fig.suptitle("ЖИВАЯ ЗЕМЛЯ: школа № 83, № 100 и двор-пилот, 2026")
fig.tight_layout()
fig.savefig("zhivaya_economics.png", dpi=150)
print(f"окупаемость модуля: {payback*12:.1f} мес")
