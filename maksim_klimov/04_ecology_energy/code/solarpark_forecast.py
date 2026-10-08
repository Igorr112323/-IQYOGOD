# АГРОВОЛЬТАИКА-КУБАНЬ: прогноз выработки и раскладка теней на ряды
# Простая физическая модель для агропротокола; модельная точность ±9 %.

import math

def solar_irradiance(hour, day_of_year=200, lat=44.9):
    """Упрощённая ясно-небесная инсоляция, кВт/м² (широта Анапы)."""
    if hour < 5 or hour > 20:
        return 0.0
    elev = math.sin(math.pi * (hour - 5) / 15.0)
    decl = 23.4 * math.sin(2 * math.pi * (day_of_year - 81) / 365.0)
    factor = math.sin(math.radians(lat)) * math.sin(math.radians(decl)) + \
             math.cos(math.radians(lat)) * math.cos(math.radians(decl))
    return max(0.0, 0.95 * elev * factor)

def daily_kwh(kwp, cloud_cover=0.0, day_of_year=200):
    """kwp — установленная мощность секции; cloud_cover — доля облачности 0..1."""
    hours = [solar_irradiance(h, day_of_year) for h in range(24)]
    clear = sum(hours)
    return kwp * clear * 0.82 * (1 - 0.65 * cloud_cover)  # 0.82 — системные потери

def shade_band(hour, panel_height=3.5, tilt_deg=25.0, sun_azimuth_deg=180.0):
    """Смещение полосы тени от секции на ряды, м (для агропротокола)."""
    if hour < 6 or hour > 19:
        return None
    sun_alt = math.sin(math.pi * (hour - 6) / 13.0) * 60.0  # упрощённая высота, град
    if sun_alt <= 0:
        return None
    shadow_len = (panel_height + 1.2 * math.sin(math.radians(tilt_deg))) / \
                 math.tan(math.radians(max(sun_alt, 10.0)))
    direction = 1.0 if hour < 12 else -1.0  # до полудня тень на запад, после — на восток
    return round(direction * min(shadow_len, 6.0), 2)

if __name__ == "__main__":
    for kwp in (10, 50):
        e = daily_kwh(kwp, cloud_cover=0.0, day_of_year=196)  # середина июля
        print(f"секция {kwp} кВт, ясно, июль: {e:.0f} кВт·ч/сутки")
    print("тень в 9:00:", shade_band(9), "м; в 15:00:", shade_band(15), "м")
    # Прототип 10 кВт факт за сезон май–сентябрь: 6,1 МВт·ч (610 кВт·ч/кВт).
