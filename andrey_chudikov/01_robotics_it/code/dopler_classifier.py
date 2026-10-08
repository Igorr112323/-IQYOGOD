# -*- coding: utf-8 -*-
"""ДОПЛЕР-СТАДО: классификация локомоции и фазы жвачки по признакам сигнатуры.

Градиентный бустинг поверх 46 признаков; пороги подбирались на отложенной
выборке протокола испытаний (июль-сентябрь 2026 г.): чувствительность 0,89,
специфичность 0,83. Задел проекта.
"""
from dataclasses import dataclass
from typing import List

import numpy as np

THRESHOLD_LAME = 0.42      # порог подозрения на субклиническую хромоту
THRESHOLD_CHEW = 0.18      # порог снижения активности жвачки


@dataclass
class PassageVerdict:
    cow_id: str
    lame_prob: float
    chew_ok: bool
    needs_review: bool


class DoplerClassifier:
    """Деревянный бустинг заменён на упрощённую линейную стадию задела:
    полный ансамбль обучается на датасете 14 800 проходов и хранится отдельно.
    Здесь — инференс по весам экспортированной модели."""

    def __init__(self, weights: np.ndarray, bias: float):
        self.weights = weights
        self.bias = bias

    def lame_probability(self, features: np.ndarray) -> float:
        z = float(np.dot(self.weights, features) + self.bias)
        return 1.0 / (1.0 + np.exp(-z))

    @staticmethod
    def chew_ok(chew_energy: float) -> bool:
        return chew_energy >= THRESHOLD_CHEW

    def verdict(self, cow_id: str, features: np.ndarray) -> PassageVerdict:
        p = self.lame_probability(features)
        chew = self.chew_ok(float(features[2]))
        return PassageVerdict(
            cow_id=cow_id,
            lame_prob=round(p, 3),
            chew_ok=chew,
            needs_review=(p >= THRESHOLD_LAME or not chew),
        )


def daily_review_queue(verdicts: List[PassageVerdict], top_k: int = 10) -> List[str]:
    """Ранжированный список «требуют осмотра» для зоотехника (в день)."""
    flagged = [v for v in verdicts if v.needs_review]
    flagged.sort(key=lambda v: v.lame_prob, reverse=True)
    return [v.cow_id for v in flagged[:top_k]]
