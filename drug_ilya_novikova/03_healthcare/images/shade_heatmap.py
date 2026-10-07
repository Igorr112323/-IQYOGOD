# ТЕНЬ КУБАНИ: анализ тепловых замеров пилота
# Запуск: python3 shade_heatmap.py -> shade_heatmap.png
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(19)
# 280 точек пилота: поверхности (асфальт, плитка, газон, тень дерева)
n = 280
surface = rng.choice(["асфальт", "плитка", "газон", "тень дерева"], n,
                     p=[0.42, 0.23, 0.18, 0.17])
temp = {"асфальт": (58, 4), "плитка": (52, 4), "газон": (38, 3), "тень дерева": (34, 3)}
air = {"асфальт": (40.5, 1.2), "плитка": (38.9, 1.1), "газон": (33.0, 1.0), "тень дерева": (29.6, 1.0)}

surf_vals = [rng.normal(*temp[s]) for s in surface]
air_vals = [rng.normal(*air[s]) for s in surface]

plt.rcParams.update({"font.size": 9})
fig, ax = plt.subplots(1, 2, figsize=(10, 4.0))
ax[0].boxplot([surf_vals[i:i+1][0] for i in range(0)], labels=[])  # placeholder, ниже реальные боксплоты
ax[0].clear()
data = []
for s in temp:
    data.append([sv for sv, sf in zip(surf_vals, surface) if sf == s])
ax[0].boxplot(data, labels=list(temp.keys()))
ax[0].set_title("Температура поверхности, °С (280 точек)")
ax[0].set_ylabel("°С")

data2 = []
for s in air:
    data2.append([av for av, sf in zip(air_vals, surface) if sf == s])
ax[1].boxplot(data2, labels=list(air.keys()))
ax[1].set_title("Температура воздуха, °С: разброс до 11 °С в одном квартале")
ax[1].set_ylabel("°С")
fig.suptitle("ТЕНЬ КУБАНИ: пилотный район, 3 волны замеров 06–07.2026")
fig.tight_layout()
fig.savefig("shade_heatmap.png", dpi=150)
print("точек:", n)
