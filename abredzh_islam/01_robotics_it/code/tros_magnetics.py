# -*- coding: utf-8 -*-
"""ТРОС-ВЕКС: расчёт потери сечения и обрывов проволок по магнитному потоку.

Задел проекта. Прогон каната через кольцо; базовый поток соответствует
полному сечению, дефицит потока — потере металла (LF), локальные
всплески — обрывам проволок (LMA).
"""

WIRE_BREAK_SPIKE = 0.045      # относительный всплеск на обрыв проволоки
LF_LIMIT_PCT = 8.0            # предел потери сечения по регламенту


def median(values: list[float]) -> float:
    """Медиана ряда измерений."""
    s = sorted(values)
    n = len(s)
    if n == 0:
        return 0.0
    mid = n // 2
    return s[mid] if n % 2 else (s[mid - 1] + s[mid]) / 2.0


def loss_of_section(flux_series: list[float], baseline_flux: float) -> float:
    """LF, %: средний дефицит потока относительно базового сечения."""
    if baseline_flux <= 0 or not flux_series:
        return 0.0
    deficit = 1.0 - median(flux_series) / baseline_flux
    return round(max(deficit, 0.0) * 100, 2)


def count_wire_breaks(flux_series: list[float], baseline_flux: float) -> int:
    """LMA: число локальных всплесков выше порога."""
    if baseline_flux <= 0:
        return 0
    peaks = 0
    above = False
    for v in flux_series:
        rel = abs(v - baseline_flux) / baseline_flux
        if rel >= WIRE_BREAK_SPIKE and not above:
            peaks += 1
            above = True
        elif rel < WIRE_BREAK_SPIKE * 0.6:
            above = False
    return peaks


def section_status(lf_pct: float, lma: int) -> str:
    """Статус каната по тренду для телеметрии."""
    if lf_pct >= LF_LIMIT_PCT * 0.8 or lma >= 6:
        return "критический: планировать замену"
    if lf_pct >= LF_LIMIT_PCT * 0.5 or lma >= 3:
        return "наблюдение: внеочередной осмотр"
    return "в ресурсе"


if __name__ == "__main__":
    # модельный прогон: ночной режим 0,1 м/с, 8 датчиков Холла, один проход
    baseline = 1.00
    series = [0.985, 0.984, 0.986, 0.983, 0.985, 0.984, 0.986, 0.985]
    # три обрыва проволок на разных метрах каната
    for i in (2, 5, 7):
        series[i] -= 0.05
    lf = loss_of_section(series, baseline)
    lma = count_wire_breaks(series, baseline)
    print(f"Базовый поток: {baseline:.2f} Вб, точек прогона: {len(series)}")
    print(f"Потеря сечения LF: {lf:.2f} % (предел {LF_LIMIT_PCT:.0f} %)")
    print(f"Обрывов проволок LMA: {lma}")
    print(f"Статус: {section_status(lf, lma)}")
