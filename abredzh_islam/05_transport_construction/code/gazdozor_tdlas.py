# -*- coding: utf-8 -*-
"""ГАЗ-ДОЗОР: измерение концентрации метана методом TDLAS.

Задел проекта. Лазерная абсорбционная спектроскопия на линии поглощения
метана 1 653 нм: измеряется оптическая глубина открытой базы, концентрация
восстанавливается по закону Бугера — Ламберта. Единица измерения —
произведение концентрации на длину пути (ppm·м); паспортная
чувствительность комплекса — 5 ppm·м.
"""
import math
import random

WAVELENGTH_NM = 1653.0        # линия поглощения метана
PATH_M = 0.40                 # открытая оптическая база датчика, м
S_LINE = 1.0e-4               # сечение линии, 1/(ppm·м): глубина = S·(C·L)
NOISE_FLOOR = 5.0e-5          # шум приёмного тракта (оптическая глубина)
SENSITIVITY_PPM_M = 5.0       # паспортная чувствительность, ppm·м


def optical_depth(cl_ppm_m: float) -> float:
    """Оптическая глубина для произведения концентрации на путь."""
    return S_LINE * cl_ppm_m


def transmission_meas(cl_ppm_m: float, rng: random.Random) -> float:
    """Измеренное пропускание с шумом приёмного тракта."""
    return math.exp(-optical_depth(cl_ppm_m)) * (1.0 + rng.gauss(0, NOISE_FLOOR))


def invert(transmission: float) -> float:
    """Восстановление концентрации: C·L = −ln(T) / S."""
    if transmission >= 1.0:
        return 0.0
    return -math.log(transmission) / S_LINE


def ppm_in_duct(cl_ppm_m: float) -> float:
    """Объёмная концентрация в шахте при известной базе датчика."""
    return cl_ppm_m / PATH_M


if __name__ == "__main__":
    rng = random.Random(20261008)
    # контрольные точки калибровочного стенда, ppm·м
    truth = [0.0, 2.5, 5.0, 10.0, 25.0]
    print("Калибровка датчика 1 653 нм, база 0,40 м")
    max_err = 0.0
    for cl in truth:
        est = invert(transmission_meas(cl, rng))
        err = abs(est - cl)
        max_err = max(max_err, err)
        print(f"  задано {cl:5.1f} ppm·м — измерено {est:5.2f} ppm·м "
              f"(ошибка {err:.2f})")
    print(f"Максимальная ошибка калибровки: {max_err:.2f} ppm·м")
    print(f"Порог обнаружения: {SENSITIVITY_PPM_M:.0f} ppm·м "
          f"({ppm_in_duct(SENSITIVITY_PPM_M):.1f} ppm при базе {PATH_M} м)")
