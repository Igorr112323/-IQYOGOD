# ДВОР БЕЗ СТУПЕНЕЙ: индексы доступности пилотных дворов
# Запуск: python3 dvor_index.py -> dvor_index.png
import numpy as np
import matplotlib.pyplot as plt

yards = ["Захарова, 23", "Ставропольская, 149", "Двор № 3", "Двор № 4"]
index = [34, 41, 47, 52]
top_barriers = ["бордюр 10-15 см", "ступени без пандуса", "тёмный проход",
                "лавочки без спинки", "ямы на тропах"]
counts = [4, 3, 3, 2, 2]

plt.rcParams.update({"font.size": 9})
fig, ax = plt.subplots(1, 2, figsize=(10, 4.0))
colors = ["#c62828" if v < 40 else "#ef6c00" if v < 55 else "#2e7d32" for v in index]
ax[0].barh(yards, index, color=colors)
ax[0].axvline(60, color="k", ls="--", lw=1)
ax[0].set_xlim(0, 100)
ax[0].set_title("Индекс доступности дворов (60 — минимально приличный)")
ax[0].invert_yaxis()
ax[1].barh(top_barriers, counts, color="#455a64")
ax[1].set_title("Топ-барьеры (14 дворовых кейсов)")
ax[1].set_xlabel("число барьеров")
fig.suptitle("ДВОР БЕЗ СТУПЕНЕЙ: пилот 02–04.2026 — 312 точек, 78 барьеров")
fig.tight_layout()
fig.savefig("dvor_index.png", dpi=150)
print("индексы:", dict(zip(yards, index)))
