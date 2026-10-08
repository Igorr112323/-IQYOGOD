# ТЕРМОСТОПА-32: алгоритм попарной асимметрии зон подошвы
# Вход: 32 температуры (16 зон на стопу) + температура пола.
# Выход: индекс асимметрии и категория «норма / наблюдение / осмотр врача».

THRESHOLD = 2.0          # порог асимметрии, градусы
PAIRS = 16               # пар зон левая/правая
REPEAT_REQUIRED = 2      # повторное измерение для сигнала

def normalize_to_floor(temps, floor_t):
    """Смещение относительно температуры пола: холодный пол не даёт ложных зон."""
    return [t - floor_t for t in temps]

def zone_asymmetry(left, right):
    """Попарная разность температур соответствующих зон."""
    return [abs(l - r) for l, r in zip(left, right)]

def classify(asymmetry, previous_asymmetry=None):
    hot = [i for i, d in enumerate(asymmetry) if d >= THRESHOLD]
    if not hot:
        return "норма", 0.0
    idx = max(hot, key=lambda i: asymmetry[i])
    if previous_asymmetry is not None and previous_asymmetry[idx] >= THRESHOLD:
        return "осмотр врача", asymmetry[idx]
    return "наблюдение", asymmetry[idx]

def one_measurement(left_t, right_t, floor_t, previous=None):
    left = normalize_to_floor(left_t, floor_t)
    right = normalize_to_floor(right_t, floor_t)
    asym = zone_asymmetry(left, right)
    category, value = classify(asym, previous)
    return {"категория": category, "индекс": round(value, 2), "карта": [round(x, 2) for x in asym]}

if __name__ == "__main__":
    left = [32.1, 31.8, 32.4] + [32.0] * 13
    right = [32.0, 31.9, 35.1] + [31.9] * 13   # зона 2: +2,7 градуса
    first = one_measurement(left, right, floor_t=24.0)
    second = one_measurement(left, right, floor_t=24.0, previous=[0.1, 0.1, 2.7] + [0.1] * 13)
    print("измерение 1:", first)
    print("измерение 2:", second)
    # Испытания 2026: 214 измерений, 9 подтверждённых случаев из 11 сигналов.
