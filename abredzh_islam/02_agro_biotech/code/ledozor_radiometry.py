# -*- coding: utf-8 -*-
"""ЛЕДОЗОР: решение обратной задачи микроволновой радиометрии.

Задел проекта. Трёхслойная модель среды «снег — ледяная корка — мёрзлая
почва». Прямой расчёт яркостных температур на 10,7 и 36,5 ГГц в двух
поляризациях; обратная задача двухступенчатая: тип корки — по
поляризационному контрасту, глубина снега и толщина корки — сеточным
поиском по поляризационно-усреднённым каналам.

Физика упрощена: гладкий лёд зеркально отражает холодное небо, поэтому
ледяной слой понижает яркостную температуру (эффективная температура льда
ниже физической); притёртая корка сглаживает поверхность и гасит
поляризационный контраст почвы.
"""
import math
import random

FREQ_GHZ = (10.7, 36.5)
POL = ("V", "H")

# физические температуры слоёв, К (зима, северная зона края)
T_SNOW = 263.0
T_ICE_EFF = 210.0     # эффективная: лёд отражает холодное небо
T_SOIL = 270.0

# коэффициенты ослабления, 1/см
K_SNOW = {10.7: 0.020, 36.5: 0.120}
K_ICE = {10.7: 0.050, 36.5: 0.250}

CRUST_TYPES = ("нет", "висячая", "притёртая")
# поляризационный контраст (разность V−H), К: притёртая корка — гладкий
# зеркальный лёд, контраст почти исчезает; висячая — трещиноватый лед,
# частичный; без корки видна шероховатая почва, контраст максимален
POL_CONTRAST = {
    10.7: {"нет": 26.0, "висячая": 14.0, "притёртая": 4.0},
    36.5: {"нет": 10.0, "висячая": 6.0, "притёртая": 2.0},
}


def brightness_temp(d_snow_cm: float, h_ice_cm: float, crust: str,
                    freq: float, pol: str) -> float:
    """Прямая модель: яркостная температура среды на частоте и поляризации."""
    tau_snow = K_SNOW[freq] * d_snow_cm
    tau_ice = K_ICE[freq] * h_ice_cm
    t_snow = math.exp(-tau_snow)
    t_ice = math.exp(-tau_ice)

    # поляризационно-усреднённая часть
    tb = T_SOIL * t_snow * t_ice
    tb += T_ICE_EFF * (1.0 - t_ice) * t_snow
    tb += T_SNOW * (1.0 - t_snow)

    # поляризационная поправка несёт тип корки; затухает с глубиной
    sign = 1.0 if pol == "V" else -1.0
    damping = math.exp(-(0.5 * tau_snow + 0.8 * tau_ice))
    tb += sign * POL_CONTRAST[freq][crust] * damping * 0.5
    return tb


def forward(d_snow_cm, h_ice_cm, crust):
    """Четыре канала: (10,7 / 36,5 ГГц) × (V / H)."""
    return [brightness_temp(d_snow_cm, h_ice_cm, crust, f, p)
            for f in FREQ_GHZ for p in POL]


def invert(tb_meas: list[float]) -> dict:
    """Обратная задача: сеточный поиск по (снег, корка, тип) на 4 каналах.

    Толщина корки читается по поляризационно-усреднённым каналам
    (лёд понижает яркостную температуру), тип корки — по поляризационному
    контрасту; сетка 1 см по снегу и 0,25 см по льду.
    """
    best = None
    for d_snow in range(0, 41):                    # шаг 1 см до 40 см
        for h_x4 in range(0, 33):                  # шаг 0,25 см до 8 см
            h_ice = h_x4 / 4.0
            for crust in CRUST_TYPES:
                if (h_ice == 0) != (crust == "нет"):
                    continue
                model = forward(d_snow, h_ice, crust)
                sse = sum((m - x) ** 2 for m, x in zip(tb_meas, model))
                if best is None or sse < best[0]:
                    best = (sse, d_snow, h_ice, crust)
    _, d_snow, h_ice, crust = best
    return {"снег_см": d_snow, "корка_см": h_ice, "тип": crust,
            "опасная": crust == "притёртая" and h_ice >= 2.0}


if __name__ == "__main__":
    random.seed(20261008)
    # верификация по синтетическим контрольным точкам: 70 точек,
    # шум приёмного тракта 2,0 К
    truth = []
    for i in range(70):
        d = random.choice([4, 6, 8, 10, 12, 15, 18, 22, 25, 30])
        if i % 3 == 0:
            h, crust = 0.0, "нет"
        elif i % 3 == 1:
            h, crust = random.choice([1.0, 1.5, 2.0]), "висячая"
        else:
            h, crust = random.choice([2.0, 2.5, 3.0, 3.5, 4.0]), "притёртая"
        truth.append((d, h, crust))

    ok_type = 0
    err_h = []
    for d, h, crust in truth:
        meas = [t + random.gauss(0, 2.0) for t in forward(d, h, crust)]
        est = invert(meas)
        if est["тип"] == crust:
            ok_type += 1
        err_h.append(abs(est["корка_см"] - h))

    acc = ok_type / len(truth)
    mae = sum(err_h) / len(err_h)
    print(f"Верификация по {len(truth)} синтетическим контрольным точкам")
    print(f"Точность определения типа корки: {acc:.2f}")
    print(f"Средняя ошибка толщины корки: ±{mae:.1f} см")
    print("Порог опасности: притёртая корка ≥ 2 см")
