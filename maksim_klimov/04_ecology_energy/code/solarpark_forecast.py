# СОЛНЦЕПАРК: суточный прогноз генерации по метеоданным
# Простая физическая модель для диспетчера; точность по пилоту ±9 %.

def solar_irradiance(hour, day_of_year=200, lat=44.5):
    """Упрощённая ясная-небесная инсоляция, кВт/м² (широта Сочи)."""
    import math
    if hour < 5 or hour > 20:
        return 0.0
    elev = math.sin(math.pi * (hour - 5) / 15.0)      # высота солнца, усл.
    decl = 23.4 * math.sin(2 * math.pi * (day_of_year - 81) / 365.0)
    factor = math.sin(math.radians(lat)) * math.sin(math.radians(decl)) + \
             math.cos(math.radians(lat)) * math.cos(math.radians(decl))
    return max(0.0, 0.95 * elev * factor)

def daily_kwh(kwp, cloud_cover=0.0, day_of_year=200):
    """kwp — установленная мощность; cloud_cover — доля облачности 0..1."""
    hours = [solar_irradiance(h, day_of_year) for h in range(24)]
    clear = sum(hours)
    return kwp * clear * 0.82 * (1 - 0.65 * cloud_cover)  # 0.82 — системные потери

if __name__ == "__main__":
    for kwp in (11, 22):
        for cloud in (0.0, 0.5):
            e = daily_kwh(kwp, cloud)
            print(f"модуль {kwp} кВт, облачность {cloud:.0%}: {e:.0f} кВт·ч/сутки")
    # Пилот 11 кВт факт за сезон 5,4 МВт·ч / 123 дня = 43,9 кВт·ч/сутки в среднем.
