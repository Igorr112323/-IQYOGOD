# -*- coding: utf-8 -*-
"""ИСКРА-СТОП: вольтметрическое детектирование ЭДС источника тока в потоке.

Физика: предмет с собственным зарядом (батарейка) при проходе над парой
измерительных электродов даёт отклик потенциала; пассивный металл — нет.
Задел проекта, исполнялся на лабораторном конвейере (март-сентябрь 2026 г.).
"""
import numpy as np

EMF_THRESHOLD_MV = 30.0      # порог отклика ЭДС, мВ
WINDOW_MS = 120              # окно наблюдения за проходом, мс


class VoltDetect:
    def __init__(self, sample_hz: int = 20_000):
        self.sample_hz = sample_hz
        self.baseline = 0.0

    def calibrate(self, empty_belt_mv: np.ndarray) -> None:
        """Нулевая точка по пустой ленте (дрейф компенсируется)."""
        self.baseline = float(np.median(empty_belt_mv))

    def detect(self, trace_mv: np.ndarray, metal_gate: bool) -> tuple[bool, float]:
        """Возвращает (событие, амплитуда отклика).

        Событие засчитывается только при открытом магнитоиндукционном
        затворе: так отклоняются фольга и немагнитный мусор.
        """
        if not metal_gate:
            return False, 0.0
        centered = trace_mv - self.baseline
        # двуполярный пик: ЭДС источника видна при входе и выходе из зоны
        peak = max(abs(centered.max()), abs(centered.min()))
        return bool(peak >= EMF_THRESHOLD_MV), float(peak)


def classify_cell(amplitude_mv: float) -> str:
    """Грубая классификация по амплитуде ЭДС для телеметрии оператора."""
    if amplitude_mv >= 2500:
        return "литиевый элемент"
    if amplitude_mv >= 1200:
        return "щелочной элемент"
    if amplitude_mv >= 300:
        return "разряженный/солевой"
    return "неклассифицировано"
