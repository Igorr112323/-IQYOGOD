# АГРОХОД-2: удержание в ряду по лидару (фрагмент рабочего стека)
# Кластеризация отражений стволов -> ось ряда -> ошибка курса для ПИД.

import math

def fit_row_axis(points, cx, cy):
    """points: [(x, y), ...] отражения стволов/шпалеры в СК платформы.
    Возвращает (ошибку смещения от оси ряда, угол курса ряда)."""
    if len(points) < 3:
        return None, None
    xs = [p[0] for p in points]; ys = [p[1] for p in points]
    n = len(points)
    mx = sum(xs) / n; my = sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    syy = sum((y - my) ** 2 for y in ys)
    sxy = sum((xs[i] - mx) * (ys[i] - my) for i in range(n))
    ang = 0.5 * math.atan2(2 * sxy, sxx - syy)     # направление главной оси
    # ошибка = расстояние от центра платформы до оси ряда по нормали
    err = (cy - my) * math.cos(ang) - (cx - mx) * math.sin(ang)
    return err, ang

def pid(err, integral, prev_err, kp=0.9, ki=0.04, kd=1.4, dt=0.1):
    integral = max(-1.5, min(1.5, integral + err * dt))
    out = kp * err + ki * integral + kd * (err - prev_err) / dt
    return out, integral

if __name__ == "__main__":
    # Синтетика: стволы вдоль оси ряда со смещением +0,4 м влево
    pts = [(0.4, y) for y in range(0, 20, 2)]
    err, ang = fit_row_axis(pts, cx=0.0, cy=10.0)
    print(f"ошибка от оси ряда: {err:+.3f} м; угол ряда: {math.degrees(ang):.1f}°")
    # Полевой замер этапа 2: отклонение от оси ряда 58 мм макс, 27 мм СКЗ.
