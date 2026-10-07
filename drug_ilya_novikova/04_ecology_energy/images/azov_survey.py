# ЧИСТЫЙ АЗОВ: статистика экспедиций 2026 г.
# Запуск: python3 azov_survey.py -> azov_survey.png
import numpy as np
import matplotlib.pyplot as plt

trips = ["Э-1, июнь", "Э-2, июль", "Э-3, август"]
km_traverse = [26, 18, 21]          # км галсов
targets = [14, 9, 7]                # целей по локатору
confirmed = [3, 2, 2]               # подтверждено водолазно
nets_kg = [0, 150, 190]             # поднято, кг

x = np.arange(len(trips))
plt.rcParams.update({"font.size": 9})
fig, ax = plt.subplots(1, 2, figsize=(10, 4.0))
ax[0].bar(x - 0.2, targets, 0.4, label="цели локатора", color="#455a64")
ax[0].bar(x + 0.2, confirmed, 0.4, label="подтверждено", color="#2e7d32")
ax[0].set_xticks(x); ax[0].set_xticklabels(trips)
ax[0].set_title("Обнаружение и подтверждение целей")
ax[0].legend(fontsize=8); ax[0].set_ylabel("целей")
ax[1].bar(trips, nets_kg, color="#01579b")
ax[1].set_title("Поднято сетей, кг (итог: 340 кг; 200 кг переработано)")
ax[1].set_ylabel("кг")
fig.suptitle("ЧИСТЫЙ АЗОВ: экспедиции 06–08.2026, 28 волонтёров, 9 дайверов")
fig.tight_layout()
fig.savefig("azov_survey.png", dpi=150)
print("поднято суммарно:", sum(nets_kg), "кг")
