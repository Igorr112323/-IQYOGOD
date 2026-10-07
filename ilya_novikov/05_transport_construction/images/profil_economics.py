# ПРОФИЛЬ-ТР: экономика услуги и карты IRI из полевого банка
# Запуск: python3 profil_economics.py -> profil_economics.png
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(27)
N = 2000
PRICE_KM = 1200.0
SERIES = 520_000.0

km_year = rng.triangular(700, 1100, 1600, N)     # км/год на один прибор
revenue = km_year * PRICE_KM / 1e3                # тыс. руб.
opex = 96.0                                        # топливо, амортизация авто, ТО
margin = revenue - opex
payback = SERIES / 1e3 / margin

# Карта IRI 14 участков (банк задела)
sections = np.array([1.9, 2.2, 2.4, 2.6, 2.9, 3.1, 3.3, 3.4, 3.8, 4.1, 4.4, 4.9, 5.3, 5.8])

plt.rcParams.update({"font.size": 9})
fig, ax = plt.subplots(1, 2, figsize=(10, 4.2))
ax[0].hist(payback, bins=40, color="#4527a0", alpha=0.85)
ax[0].axvline(np.median(payback), color="k", ls="--", lw=1)
ax[0].set_title(f"Окупаемость 520 тыс. руб., сезонов (медиана {np.median(payback):.2f})")
ax[0].set_xlabel("сезонов"); ax[0].set_ylabel("сценарии")
ax[1].bar(np.arange(1, len(sections) + 1), sections,
          color=np.where(sections <= 3.5, "#2e7d32", "#c62828"))
ax[1].axhline(3.5, color="k", ls="--", lw=1)
ax[1].set_title("Банк задела: IRI 14 участков, 83 км (порог 3,5 м/км)")
ax[1].set_xlabel("участок"); ax[1].set_ylabel("м/км")
fig.suptitle("ПРОФИЛЬ-ТР: Монте-Карло 2000 сценариев + полевые данные 2026")
fig.tight_layout()
fig.savefig("profil_economics.png", dpi=150)
print("медиана окупаемости %.2f сезона" % np.median(payback))
