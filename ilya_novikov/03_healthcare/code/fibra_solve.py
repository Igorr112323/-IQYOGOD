# -*- coding: utf-8 -*-
"""ФИБРА-СТОПА: восстановление давления и температуры по спектру решёток Брэгга.

Задел проекта. Решётки разведены по длинам волн 1530–1565 нм; для каждой
точки решается система двух уравнений (деформация + температура).
"""
import numpy as np

P_E = 0.22                 # фотоупругий коэффициент волокна
ALPHA_SI = 0.55e-6         # 1/К, тепловой коэффициент расширения
XI = 8.6e-6                # 1/К, термооптический коэффициент
E_PU = 4.2e6               # Па, модуль Юнга полиуретановой матрицы стельки
GRID_LAMBDAS_NM = np.linspace(1530.0, 1565.0, 16)


def wavelength_shifts(lambda_ref_nm: np.ndarray, lambda_meas_nm: np.ndarray) -> np.ndarray:
    return lambda_meas_nm - lambda_ref_nm


def solve_point(dlambda_nm: float, dlambda_temp_ref_nm: float, lambda_b_nm: float) -> tuple[float, float]:
    """Возвращает (давление Па, температура дельта К) для одной решётки.

    Используется пара решёток: рабочая в зоне нагрузки и температурный
    референс вне зоны нагрузки той же номинальной длины волны.
    """
    # референс даёт чистую температурную составляющую
    dt = dlambda_temp_ref_nm / (lambda_b_nm * (ALPHA_SI + XI))
    # вычитаем температурный вклад из рабочей решётки
    strain = dlambda_nm / lambda_b_nm - (ALPHA_SI + XI) * dt
    strain /= (1.0 - P_E)
    pressure_pa = E_PU * strain
    return float(max(pressure_pa, 0.0)), float(dt)


def full_frame(lambda_ref: np.ndarray, lambda_meas: np.ndarray,
               temp_ref_shifts: np.ndarray) -> dict:
    """Кадр измерения: 16 точек давления и температура стельки."""
    shifts = wavelength_shifts(lambda_ref, lambda_meas)
    pressures, temps = [], []
    for i in range(16):
        p, t = solve_point(shifts[i], temp_ref_shifts[i % len(temp_ref_shifts)],
                           GRID_LAMBDAS_NM[i])
        pressures.append(p)
        temps.append(t)
    return {"pressure_kpa": [round(p / 1000, 1) for p in pressures],
            "temperature_c": [round(t, 2) for t in temps]}
