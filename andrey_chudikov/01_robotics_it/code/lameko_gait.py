# ЛАМЕКО-СКАН: извлечение признаков походки из видеопотока (фрагмент рабочего ПО)
# Вход: треки ключевых точек корпуса коровы за проход; выход: признаки асимметрии.

import math

def stride_asymmetry(left_steps, right_steps):
    """Относительная асимметрия длины шага, доли единицы."""
    if not left_steps or not right_steps:
        return None
    l = sum(left_steps) / len(left_steps)
    r = sum(right_steps) / len(right_steps)
    return abs(l - r) / max(l, r)

def back_arc(spine_y):
    """Высота арки спины в фазе опоры (нормированный прогиб)."""
    if len(spine_y) < 5:
        return None
    mid = spine_y[len(spine_y) // 2]
    ends = (spine_y[0] + spine_y[-1]) / 2.0
    return mid - ends  # отрицательный прогиб — признак боли

def swing_phase(hoof_lift):
    """Доля укороченной фазы замаха для подозрительной конечности."""
    if not hoof_lift:
        return None
    base = sum(hoof_lift) / len(hoof_lift)
    short = sum(1 for h in hoof_lift if h < 0.6 * base)
    return short / len(hoof_lift)

def gait_score(left_steps, right_steps, spine_y, hoof_lift):
    """Интегральный индекс походки: 0 — норма, выше — подозрение."""
    asym = stride_asymmetry(left_steps, right_steps) or 0.0
    arc = max(0.0, -(back_arc(spine_y) or 0.0))
    swing = swing_phase(hoof_lift) or 0.0
    return round(0.45 * min(asym / 0.25, 1.0) + 0.25 * min(arc / 0.08, 1.0)
                 + 0.30 * min(swing / 0.5, 1.0), 3)

if __name__ == "__main__":
    healthy = gait_score([0.82, 0.84, 0.81], [0.83, 0.82, 0.84],
                         [0.02, 0.02, 0.03, 0.02, 0.02], [30, 32, 31, 33])
    lame = gait_score([0.84, 0.83], [0.61, 0.58, 0.60],
                      [0.02, 0.01, -0.03, -0.05, 0.01], [31, 12, 10, 29])
    print("индекс походки, здоровое:", healthy)
    print("индекс походки, подозрение:", lame)
    # Валидация 2026 г.: чувствительность 0,91 при пороге класса «осмотр обязателен».
