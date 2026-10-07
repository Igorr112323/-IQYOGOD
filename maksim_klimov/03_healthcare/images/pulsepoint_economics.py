# ПУЛЬС-ПОЙНТ: юнит-экономика станции и сеть
# Запуск: python3 pulsepoint_economics.py -> pulsepoint_economics.png
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(5)
N = 3000
CAPEX = 480_000.0

sessions = rng.triangular(10, 18, 30, N)          # чек-апов/день, станция в отеле
sub = 24_900 * 12                                  # подписка, руб./год
paid = sessions * 0.35 * 190 * 365                 # доля платных сверх подписки
tele = sessions * 0.06 * 490 * 365                 # телемедицинское плечо
revenue = sub + paid + tele
opex = 0.06 * revenue + 96_000                     # сервис, расходники, эквайринг
margin = (revenue - opex) / 1e3
payback = CAPEX / (margin * 1e3)

plt.rcParams.update({"font.size": 9})
fig, ax = plt.subplots(1, 2, figsize=(10, 4.2))
ax[0].hist(margin, bins=40, color="#00838f", alpha=0.85)
ax[0].axvline(np.median(margin), color="k", ls="--", lw=1)
ax[0].set_title(f"Маржа станции, тыс. руб./год (медиана {np.median(margin):.0f})")
ax[0].set_xlabel("тыс. руб./год"); ax[0].set_ylabel("сценарии")

n = np.arange(5, 51, 5)
gp = np.median(margin) * n / 1e3
ax[1].plot(n, gp, "o-", color="#15417d")
ax[1].set_title("Маржа сети к сезону-2027: 50 станций")
ax[1].set_xlabel("станций"); ax[1].set_ylabel("млн руб./год"); ax[1].grid(alpha=0.3)
fig.suptitle("ПУЛЬС-ПОЙНТ: Монте-Карло 3000 сценариев, станция в отеле")
fig.tight_layout()
fig.savefig("pulsepoint_economics.png", dpi=150)
print("медиана маржи станции %.0f тыс. руб./год; окупаемость %.2f года"
      % (np.median(margin), np.median(payback)))
