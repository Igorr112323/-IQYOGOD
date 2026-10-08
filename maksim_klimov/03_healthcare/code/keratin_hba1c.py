# -*- coding: utf-8 -*-
"""КЕРАТИН-ГЛИК: регрессия спектральных признаков на эквивалент HbA1c.

Задел проекта: линейный этап инференса (полный ансамбль обучается на
датасете 226 измерений и хранится отдельно). Порог скрининга 7,0 %.
"""
from dataclasses import dataclass

import numpy as np

SCREEN_THRESHOLD = 7.0      # % эквивалент HbA1c


@dataclass
class ScreeningOutcome:
    glycation_index: float
    hba1c_equiv: float
    referral_needed: bool


class Hba1cRegressor:
    def __init__(self, weights: np.ndarray, bias: float):
        self.weights = weights
        self.bias = bias

    def predict_hba1c(self, features: np.ndarray) -> float:
        z = float(np.dot(self.weights, features) + self.bias)
        # калибровка на физиологический диапазон 4,5–12,0 %
        return float(min(max(z, 4.5), 12.0))

    def screen(self, features: np.ndarray) -> ScreeningOutcome:
        hba1c = self.predict_hba1c(features)
        index = float(np.dot(self.weights, features) + self.bias)
        return ScreeningOutcome(
            glycation_index=round(index, 3),
            hba1c_equiv=round(hba1c, 2),
            referral_needed=hba1c >= SCREEN_THRESHOLD,
        )


def batch_report(outcomes: list[ScreeningOutcome]) -> dict:
    """Сводка для кабинета: доля направленных на лабораторный анализ."""
    n = len(outcomes)
    referral = sum(1 for o in outcomes if o.referral_needed)
    mean_eq = sum(o.hba1c_equiv for o in outcomes) / n if n else 0.0
    return {"измерений": n, "направлено": referral,
            "доля_направленных": round(referral / n, 3) if n else 0.0,
            "средний_эквивалент": round(mean_eq, 2)}
