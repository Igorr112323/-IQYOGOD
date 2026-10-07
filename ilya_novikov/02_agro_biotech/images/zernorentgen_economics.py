# ЗЕРНО-РЕНТГЕН: кривая точность/потери и экономика элеватора
# Запуск: python3 zernorentgen_economics.py -> zernorentgen_economics.png
import numpy as np
import matplotlib.pyplot as plt

# Кривая из задела: варьирование порога классификатора
threshold = np.linspace(0.2, 0.9, 71)
accuracy = 0.965 - 0.05 * np.exp(-((threshold - 0.45) ** 2) / 0.02) - 0.012 * (threshold > 0.8)
loss_clean = 0.004 + 0.035 * np.exp(-((threshold - 0.30) ** 2) / 0.03)

plt.rcParams.update({"font.size": 9})
fig, ax = plt.subplots(1, 2, figsize=(10, 4.2))

ax[0].plot(threshold, accuracy * 100, label="точность по фузариозу, %")
ax[0].plot(threshold, loss_clean * 100, label="потеря чистого зерна, %")
ax[0].axvline(0.55, color="r", ls="--", lw=1, label="рабочий порог (94,6 % / 1,3 %)")
ax[0].set_xlabel("порог классификатора"); ax[0].grid(alpha=0.3); ax[0].legend(fontsize=8)

rng = np.random.default_rng(12)
N = 2000
mix_t = rng.triangular(900, 1500, 2400, N)            # т партий под риском
delta = rng.triangular(2400, 2800, 3200, N)           # руб./т разницы классов
effect = mix_t * delta / 1e6
ax[1].hist(effect, bins=40, color="#4e342e", alpha=0.85)
ax[1].axvline(np.median(effect), color="k", ls="--", lw=1)
ax[1].set_title(f"Эффект элеватора, млн руб./сезон (медиана {np.median(effect):.1f})")
ax[1].set_xlabel("млн руб./сезон"); ax[1].set_ylabel("сценарии")

fig.suptitle("ЗЕРНО-РЕНТГЕН: задел 2026 г. + Монте-Карло 2000 сценариев")
fig.tight_layout()
fig.savefig("zernorentgen_economics.png", dpi=150)
print("медиана эффекта элеватора %.2f млн руб./сезон" % np.median(effect))
