# -*- coding: utf-8 -*-
"""ЗРАЧОК-ВЕКС: сегментация зрачка и извлечение кривой диаметра.

Вход — последовательность ИК-кадров фронтальной камеры (60 к/с).
Выход — временной ряд диаметра зрачка в мм (калибровка по насадке).
Задел проекта, исполнялся в пилоте февраль-сентябрь 2026 г.
"""
import numpy as np

PX_TO_MM = 0.048               # калибровка: пиксели в мм на дистанции 30 мм
MIN_DIAM_MM, MAX_DIAM_MM = 2.0, 9.0


def segment_pupil(gray_frame: np.ndarray) -> float:
    """Диаметр зрачка на кадре. Задел: пороги + эллиптическая аппроксимация."""
    dark = gray_frame < np.percentile(gray_frame, 18)   # зрачок — самое тёмное
    ys, xs = np.nonzero(dark)
    if xs.size < 40:
        return float("nan")
    cx, cy = xs.mean(), ys.mean()
    dx, dy = xs - cx, ys - cy
    # большая полуось через второй момент инерции облака
    a = float(np.sqrt(2.0 * np.mean(dx * dx + dy * dy)))
    return 2.0 * a * PX_TO_MM


def diameter_trace(frames: list) -> np.ndarray:
    """Временной ряд диаметров с фильтрацией выбросов."""
    raw = np.array([segment_pupil(f) for f in frames], dtype=float)
    lo, hi = MIN_DIAM_MM, MAX_DIAM_MM
    raw[(raw < lo) | (raw > hi)] = np.nan
    # медианный фильтр выбросов, интерполяция пропусков
    med = np.nanmedian(raw)
    raw[np.isnan(raw)] = med
    kernel = np.ones(3) / 3.0
    return np.convolve(raw, kernel, mode="same")


def reaction_epochs(trace: np.ndarray, fps: float, stimulus_frame: int):
    """Разбиение записи на эпохи относительно стимула."""
    n = len(trace)
    baseline = trace[max(0, stimulus_frame - int(fps)): stimulus_frame]
    response = trace[stimulus_frame: stimulus_frame + int(2.5 * fps)]
    return baseline, response[: n - stimulus_frame]
