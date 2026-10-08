# ДОСТУПНЫЙ КУРОРТ: Монте-Карло 2 000 сценариев прироста доступного турпотока
# Запуск: python3 dvor_index.py -> dvor_index.png
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(41)
N = 2000

# базовая аудитория: доля туристов, которым важна доступная среда (ВОЗ: до 15 %)
share = rng.triangular(0.08, 0.12, 0.15, size=N)
# прирост приездов за два сезона при работающей карте и планах адаптации
uplift = rng.triangular(0.02, 0.06, 0.11, size=N)
guests = 1_000_000  # курорт с 1 млн гостей в год

extra_guests = guests * share * uplift * 2          # за два сезона, накопленно
extra_guests_med = np.median(extra_guests)

# экономика проекта
passport_rev = 180 * 38_000                         # 180 паспортов × 38 тыс. руб.
sub_rev = 4 * 45_000 * 12                           # 4 муниципалитета × 45 тыс./мес × 12
revenue = (passport_rev + sub_rev) / 1e6
net = revenue - 5.6
payback_months = 0.89 / net * 12

plt.rcParams.update({"font.size": 9})
fig, ax = plt.subplots(1, 2, figsize=(10, 4.2))
ax[0].hist(uplift * 100, bins=40, color="#00838f", alpha=0.85)
ax[0].axvline(np.median(uplift) * 100, color="k", ls="--", lw=1)
ax[0].set_title(f"Прирост доступного турпотока, % за два сезона (медиана {np.median(uplift)*100:.0f})")
ax[0].set_xlabel("%"); ax[0].set_ylabel("сценарии")
ax[1].hist(extra_guests / 1000, bins=40, color="#ef6c00", alpha=0.85)
ax[1].axvline(extra_guests_med / 1000, color="k", ls="--", lw=1)
ax[1].set_title(f"Доп. приезды на курорт с 1 млн гостей, тыс. (медиана {extra_guests_med/1000:.0f})")
ax[1].set_xlabel("тыс. гостей"); ax[1].grid(alpha=0.3)
fig.suptitle(f"ДОСТУПНЫЙ КУРОРТ: Монте-Карло {N} сценариев; проект: {net:.1f} млн руб./год, "
             f"окупаемость {payback_months:.1f} мес.")
fig.tight_layout()
fig.savefig("dvor_index.png", dpi=150)
print("медиана прироста %.1f%%; доп. приезды %.0f тыс.; чистый %.2f млн руб./год; окупаемость %.1f мес."
      % (np.median(uplift) * 100, extra_guests_med / 1000, net, payback_months))
