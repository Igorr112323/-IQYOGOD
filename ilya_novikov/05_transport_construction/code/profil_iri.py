# ПРОФИЛЬ-ТР: расчёт IRI моделью «четверть автомобиля»
# Профиль дороги (шаг 0,05 м по оси) -> индекс ровности, м/км.

STEP = 0.05            # м, шаг профиля
V = 22.0               # м/с, эталонная скорость расчёта (80 км/ч)

# Параметры модели четверть автомобиля (подбор по ГОСТ-методике)
K1 = 6.53e6; C1 = 1.16e4; K2 = 6.5e5; M1 = 75.0; M2 = 15.0

def iri_m_per_km(profile_mm):
    """profile_mm: отсчёты неровности, мм; шаг STEP."""
    dt = STEP / V
    x1 = x2 = v1 = v2 = 0.0
    s = 0.0
    for i in range(1, len(profile_mm)):
        q = (profile_mm[i] - profile_mm[i - 1]) / 1000.0   # м
        a1 = (K2 * (x2 - x1) + C1 * (v2 - v1) - K1 * x1) / M1
        a2 = (K2 * (x1 - x2) + C1 * (v1 - v2) + K1 * (q / dt) ) / M2
        v1 += a1 * dt; v2 += a2 * dt
        x1 += v1 * dt; x2 += v2 * dt
        s += abs(v1 - v2) * dt
    length_km = max(len(profile_mm) - 1, 1) * STEP / 1000.0
    return s / length_km / 1000.0     # упрощённая нормировка до м/км

if __name__ == "__main__":
    import math, random
    random.seed(3)
    # Синтетический профиль: ровный участок + волна 20 мм на 20 м
    n = 16000
    prof = [0.4 * math.sin(i / 9.0) + random.gauss(0, 0.25) for i in range(n)]
    for i in range(6000, 6400):
        prof[i] += 10 * (1 + math.sin(math.pi * (i - 6000) / 400.0))
    print(f"IRI участка с волной: {iri_m_per_km(prof):.2f} м/км")
    # Полевой банк 2026: 14 участков, диапазон 1,9–5,8 м/км.
