# АГРОСПЕКТР-К: модель эффекта и окупаемости
# Модель Монте-Карло, 2500 сезонов (упрощённая версия модуля задела).
# Запуск: python3 agrospectr_economics.py  -> файл agrospectr_economics.png
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(2026)
N = 2500
AREA = 500.0            # га, пилотное хозяйство
PRICE = 13500.0         # руб./т продовольственная пшеница
SERVICE = 290.0         # руб./га стоимость мониторинга
FUNG_SAVE = 1200.0 * 0.85  # экономия фунгицида, руб./га (адресность)

# предотвращённые потери, т/га: без комплекса (визуальный контроль) и с комплексом
loss_base = rng.triangular(0.15, 0.55, 1.10, N)     # сезонный разброс болезней
detection_gain = rng.triangular(0.25, 0.35, 0.45, N)  # доля предотвращённых потерь
saved_t = loss_base * detection_gain
effect = AREA * saved_t * PRICE + AREA * FUNG_SAVE   # руб./сезон
cost_service = AREA * SERVICE

plt.rcParams.update({"font.size": 9})
fig, ax = plt.subplots(1, 2, figsize=(10, 4.2))

ax[0].hist(effect / 1e6, bins=40, color="#2f7d32", alpha=0.85)
ax[0].axvline(np.median(effect) / 1e6, color="k", ls="--", lw=1)
ax[0].set_title(f"Эффект хозяйства, млн руб./сезон (медиана {np.median(effect)/1e6:.2f})")
ax[0].set_xlabel("млн руб./сезон"); ax[0].set_ylabel("число сезонов")

years = np.arange(0, 4.1, 0.1)
cum = np.median(effect) * years - 690000  # против покупки комплекса
ax[1].plot(years, cum / 1e6, color="#15417d", lw=2)
ax[1].axhline(0, color="gray", lw=0.8)
ax[1].axvline(690000 / np.median(effect), color="r", ls="--", lw=1)
ax[1].set_title(f"Окупаемость комплекса 690 тыс. руб.: {690000/np.median(effect):.2f} сезона")
ax[1].set_xlabel("сезоны"); ax[1].set_ylabel("кумулятивно, млн руб.")
ax[1].grid(alpha=0.3)

fig.suptitle("АГРОСПЕКТР-К: экономика пилотного хозяйства (500 га), Монте-Карло 2500 сезонов")
fig.tight_layout()
fig.savefig("agrospectr_economics.png", dpi=150)
print("медиана эффекта: %.1f млн руб.; доля сезонов с эффектом > 1 млн: %.1f%%"
      % (np.median(effect) / 1e6, 100 * np.mean(effect > 1e6)))
