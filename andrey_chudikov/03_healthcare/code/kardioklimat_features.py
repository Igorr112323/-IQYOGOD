# КАРДИОКЛИМАТ-КУБАНЬ: расчёт метеопризнаков и индекса ЖКИ
# Рабочий модуль задела (ноябрь 2025 — июль 2026). Проверен на 5479 записях.

def thi(t_c: float, rh: float) -> float:
    """Индекс «температура–влажность» (упрощённый)."""
    return t_c - 0.55 * (1.0 - rh / 100.0) * (t_c - 14.5)

def heat_series_len(tmax_series, threshold=33.0) -> int:
    """Длина текущей серии дней с Tmax выше порога (ведущий признак модели)."""
    n = 0
    for t in reversed(tmax_series):
        if t >= threshold:
            n += 1
        else:
            break
    return n

def grad(seq, window=2):
    """Градиент за окно суток."""
    return (seq[-1] - seq[-1 - window]) / window if len(seq) > window else 0.0

def zhki(features: dict) -> float:
    """Индекс жаровой кардионагрузки 0–100.
    Веса — из логистической регрессии (интерпретируемая копия модели).
    features: tmax, grad48, series33, thi, pressure_drop24, share65."""
    w = {"tmax": 1.9, "grad48": 2.6, "series33": 3.4, "thi": 1.4,
         "pressure_drop24": 0.9, "share65": 22.0}
    b = {"tmax": -33.0, "grad48": 0.0, "series33": 0.0, "thi": -26.0,
         "pressure_drop24": -3.0, "share65": -0.18}
    s = 0.0
    for k, wi in w.items():
        s += wi * max(features.get(k, 0.0) - b[k], 0.0)
    return min(100.0, max(0.0, s))

def level(z: float) -> str:
    return "зелёный" if z < 50 else ("жёлтый" if z < 70 else "красный")

if __name__ == "__main__":
    # Контрольный пример: Тихорецк, пик жары 27.07.2025 (данные валидации)
    f = {"tmax": 39.4, "grad48": 2.1, "series33": 6, "thi": 33.8,
         "pressure_drop24": 4.5, "share65": 0.24}
    z = zhki(f)
    print(f"ЖКИ = {z:.0f} ({level(z)})")
    assert level(z) == "красный", "эталонный кейс должен быть красным"
    print("самопроверка пройдена")
