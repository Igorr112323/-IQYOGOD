# -*- coding: utf-8 -*-
"""ЗАМОР-СТОП: детекция эпизодов «плавания у поверхности».

Задел проекта. В ИК-кадре всплытие — компактная цель у границы воды
с характерной динамикой головы (заглатывание воздуха). Утки, волны
и блики отсеиваются по форме и скорости движения.
"""
from dataclasses import dataclass

WINDOW_MIN = 40
BASELINE_FACTOR = 3.0


@dataclass
class SurfaceEvent:
    t_sec: float
    x_m: float
    y_m: float
    head_dips: int          # число характерных «кивков» головы
    speed_m_s: float
    aspect: float


def is_gulp_event(ev: SurfaceEvent) -> bool:
    """Критерии эпизода заглатывания воздуха рыбой."""
    return (ev.head_dips >= 2
            and ev.speed_m_s <= 0.35
            and 1.8 <= ev.aspect <= 5.5)


def is_false_target(ev: SurfaceEvent) -> bool:
    """Утки и крупные плавающие цели: крупный размер, высокая скорость."""
    return ev.aspect > 5.5 or ev.speed_m_s > 0.6


def window_rate(events: list[SurfaceEvent], t_now_sec: float) -> float:
    """Частота эпизодов за окно 40 минут."""
    start = t_now_sec - WINDOW_MIN * 60
    return sum(1 for e in events if e.t_sec >= start and is_gulp_event(e))


def threshold(baseline_per_window: float) -> float:
    """Порог тревоги: ×3 к базовой линии водоёма."""
    return max(3.0, baseline_per_window * BASELINE_FACTOR)
