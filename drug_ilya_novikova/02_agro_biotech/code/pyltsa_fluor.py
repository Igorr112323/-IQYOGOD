# -*- coding: utf-8 -*-
"""ПЫЛЬЦА-ВЕКС: флуоресцентный спектр пролёта пчелы и классификация.

Задел проекта. УФ-возбуждение 365 нм; рабочая полоса флуоресценции
420–560 нм. Классификация «чистая пыльца / пестицидный стресс» —
упрощённая линейная стадия задела (полная свёрточная модель — на борту).
"""
import numpy as np

N_BINS = 28                 # спектральных каналов в рабочей полосе
BAND_NM = np.linspace(420, 560, N_BINS)


def normalize_spectrum(counts: np.ndarray) -> np.ndarray:
    total = counts.sum()
    return counts / total if total > 1e-9 else counts


def stress_features(spec_norm: np.ndarray) -> np.ndarray:
    """Признаки стресса: смещение центра массы и форма профиля.

    У загрязнённой пыльцы флуоресценция смещается к длинным волнам
    и теряет пик в полосе 440–470 нм (фенольные соединения).
    """
    center = float(np.sum(BAND_NM * spec_norm))
    peak_band = int(np.argmax(spec_norm[:12]))     # синяя область 420–480
    ratio_red_blue = spec_norm[18:].sum() / max(spec_norm[:10].sum(), 1e-9)
    return np.array([center, peak_band, ratio_red_blue, spec_norm.std()])


def classify_pass(features: np.ndarray, weights: np.ndarray, bias: float) -> float:
    """Вероятность пестицидного стресса для одного пролёта."""
    z = float(np.dot(weights, features) + bias)
    return 1.0 / (1.0 + np.exp(-z))
