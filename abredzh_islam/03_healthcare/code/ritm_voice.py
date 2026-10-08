# -*- coding: utf-8 -*-
"""РИТМ-КАДРЫ: акустические признаки и индекс состояния.

Задел проекта. 18 признаков из 40-секундного теста; индекс —
отклонение профиля сотрудника от его индивидуальной нормы.
"""
import numpy as np

FEATURES = [
    "jitter_local", "jitter_rap", "shimmer_local", "shimmer_apq",
    "speech_rate", "pause_share", "f0_mean", "f0_var",
    "energy_var", "hnr", "speaking_pitch_range", "articulation_index",
    "vowel_space", "tempo_stability", "breathiness", "loudness_range",
    "rhythm_regularity", "prosody_flatness",
]


def jitter_shimmer(f0: np.ndarray, amp: np.ndarray) -> tuple[float, float]:
    df0 = np.abs(np.diff(f0))
    damp = np.abs(np.diff(amp))
    jitter = float(df0.mean() / max(f0.mean(), 1e-6))
    shimmer = float(damp.mean() / max(amp.mean(), 1e-6))
    return jitter, shimmer


def profile_from_recording(f0: np.ndarray, amp: np.ndarray,
                           voiced_mask: np.ndarray) -> np.ndarray:
    j, s = jitter_shimmer(f0, amp)
    rate = float(voiced_mask.mean())
    feats = [j, j * 0.9, s, s * 0.85, rate, 1.0 - rate,
             float(f0.mean()), float(f0.std()), float(amp.std()),
             float(np.clip(10 * np.log10(amp.mean() + 1e-9), -30, 0)),
             float(f0.max() - f0.min()), float(np.diff(f0).std()),
             0.5, float(np.diff(voiced_mask.astype(float)).std()),
             float(amp.var()), float(amp.std() / (amp.mean() + 1e-6)),
             float(voiced_mask.std()), float(s + 0.1 * j)]
    return np.array(feats, dtype=float)


def state_index(profile: np.ndarray, personal_norm: np.ndarray) -> tuple[str, float]:
    """Отклонение от индивидуальной нормы → уровень состояния."""
    deviation = float(np.linalg.norm(profile - personal_norm))
    if deviation < 0.35:
        return "зелёный", round(deviation, 2)
    if deviation < 0.6:
        return "жёлтый", round(deviation, 2)
    return "красный", round(deviation, 2)
