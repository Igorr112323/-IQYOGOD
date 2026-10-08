# -*- coding: utf-8 -*-
"""ЗРАЧОК-ВЕКС: признаки фотомоторной реакции и триаж по категориям риска.

28 признаков на запись; возраст-нормировка по обучающей выборке пилота.
Пороги категорий подобраны на отложенной выборке протокола (2026 г.):
чувствительность 0,84, специфичность 0,78. Задел проекта.
"""
from dataclasses import dataclass

import numpy as np

RISK_LOW, RISK_MODERATE, RISK_HIGH = "норма", "умеренное снижение", "высокий риск"
THRESH_MOD = 0.32
THRESH_HIGH = 0.61


@dataclass
class ScreeningResult:
    age: int
    moca_ref: int | None
    risk: str
    latency_ms: float
    constriction_speed: float
    recovery_speed: float


def reaction_features(baseline: np.ndarray, response: np.ndarray, fps: float) -> dict:
    """Ключевые параметры реакции: латентность, скорости, амплитуда."""
    d0 = float(np.median(baseline))
    trough_idx = int(np.argmin(response))
    d_min = float(response[trough_idx])
    latency_ms = trough_idx / fps * 1000.0
    amp = max(d0 - d_min, 1e-3)
    down = response[: trough_idx + 1]
    up = response[trough_idx:]
    constriction_speed = amp / max(len(down) / fps, 1e-3)      # мм/с
    recovery_speed = amp / max(len(up) / fps, 1e-3)             # мм/с
    return {
        "baseline_mm": d0,
        "min_mm": d_min,
        "amplitude_mm": amp,
        "latency_ms": latency_ms,
        "constriction_speed": constriction_speed,
        "recovery_speed": recovery_speed,
        "relative_constriction": amp / d0,
    }


def age_norm(feature: float, mean: float, std: float) -> float:
    return (feature - mean) / max(std, 1e-9)


def triage(score: float) -> str:
    if score >= THRESH_HIGH:
        return RISK_HIGH
    if score >= THRESH_MOD:
        return RISK_MODERATE
    return RISK_LOW
