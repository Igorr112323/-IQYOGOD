# -*- coding: utf-8 -*-
"""ПОЛЯРИС-БЕРЕГ: разделение бликового и подповерхностного слоёв.

Задел проекта. Матрица 4-DoFP: четыре ориентации микрополяризаторов
(0/45/90/135) на пиксель; из них восстанавливаются параметры Стокса,
бликовый слой выделяется по высокой степени поляризации.
"""
import numpy as np


def stokes_from_channels(ch0: np.ndarray, ch45: np.ndarray,
                         ch90: np.ndarray, ch135: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """I, Q, U — параметры Стокса из четырёх ориентаций."""
    I = (ch0 + ch45 + ch90 + ch135) / 2.0
    Q = ch0 - ch90
    U = ch45 - ch135
    return I, Q, U


def degree_of_polarization(I: np.ndarray, Q: np.ndarray, U: np.ndarray) -> np.ndarray:
    return np.sqrt(Q ** 2 + U ** 2) / np.maximum(I, 1e-6)


def split_layers(I: np.ndarray, dop: np.ndarray, glare_thr: float = 0.35):
    """Бликовый слой — высокая степень поляризации (отражение от воды).

    Возвращает маски: блики и подповерхностный слой.
    """
    glare = dop > glare_thr
    subsurface = ~glare
    return glare, subsurface


def subsurface_image(I: np.ndarray, dop: np.ndarray, glare_thr: float = 0.35) -> np.ndarray:
    """Изображение с подавленными бликами — вход детектора."""
    glare, subsurface = split_layers(I, dop, glare_thr)
    out = I.copy()
    out[glare] = np.median(I[subsurface]) if subsurface.any() else 0.0
    return out
