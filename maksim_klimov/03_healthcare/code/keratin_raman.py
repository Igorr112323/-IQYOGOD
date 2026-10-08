# -*- coding: utf-8 -*-
"""КЕРАТИН-ГЛИК: предобработка рамановского спектра ногтевой пластины.

Задел проекта: вычитание флуоресцентного фона, нормировка, извлечение
признаков полос 1450 и 1650 см^-1 (амидные связи кератина).
"""
import numpy as np

SPECTR_RANGE = (200.0, 2000.0)      # см^-1
BAND_AMIDE3 = (1420.0, 1480.0)
BAND_AMIDE1 = (1620.0, 1690.0)


def baseline_subtract(wavenumbers: np.ndarray, intensity: np.ndarray,
                      poly_degree: int = 5) -> np.ndarray:
    """Полиномиальное вычитание флуоресцентного фона."""
    coef = np.polyfit(wavenumbers, intensity, poly_degree)
    return intensity - np.polyval(coef, wavenumbers)


def vector_normalize(intensity: np.ndarray) -> np.ndarray:
    norm = np.linalg.norm(intensity)
    return intensity / norm if norm > 1e-9 else intensity


def band_features(wavenumbers: np.ndarray, intensity: np.ndarray) -> dict:
    """Признаки амидных полос: площадь, пик, смещение центра массы."""
    feats = {}
    for name, (lo, hi) in {"amide3": BAND_AMIDE3, "amide1": BAND_AMIDE1}.items():
        mask = (wavenumbers >= lo) & (wavenumbers <= hi)
        x, y = wavenumbers[mask], intensity[mask]
        area = float(np.trapz(y, x))
        peak_wn = float(x[np.argmax(y)])
        com = float(np.sum(x * np.clip(y, 0, None)) / max(np.sum(np.clip(y, 0, None)), 1e-9))
        feats[f"{name}_area"] = area
        feats[f"{name}_peak"] = peak_wn
        feats[f"{name}_com_shift"] = com - (lo + hi) / 2.0
    feats["ratio_amide"] = feats["amide3_area"] / max(feats["amide1_area"], 1e-9)
    return feats


def preprocess(raw_spectra: list) -> list:
    """Конвейер предобработки для усреднения по 3 точкам ногтя."""
    processed = []
    for wn, inten in raw_spectra:
        inten = baseline_subtract(wn, inten)
        inten = vector_normalize(inten)
        processed.append((wn, inten))
    return processed
