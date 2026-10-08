# АГРОВОЛЬТАИКА-КУБАНЬ: мониторинг секции над виноградником (фрагмент рабочего ПО)
# Телеметрия: выработка, температура под пологом и на открытом контроле, доступность.

HEAT_ALERT_C = 35.0        # порог жары для агроотчёта
SHADE_TARGET_C = 4.0       # ожидаемое снижение температуры под пологом, °С

def summarize_interval(solar_kw, plant_load_kw, t_canopy, t_control):
    """Один интервал 15 мин: потоки энергии и температурный статус."""
    to_plant = min(solar_kw, plant_load_kw)
    to_grid = max(solar_kw - to_plant, 0.0)
    delta_t = t_control - t_canopy
    heat_status = "норма"
    if t_control >= HEAT_ALERT_C:
        heat_status = "защита активна" if delta_t >= SHADE_TARGET_C else "тень ниже расчётной"
    return {"to_plant_kw": round(to_plant, 2), "to_grid_kw": round(to_grid, 2),
            "delta_t_c": round(delta_t, 1), "status": heat_status}

def hail_report(damage_covered_pct, damage_control_pct):
    """Сравнение повреждений после градового события."""
    shield = 100.0 * (1 - damage_covered_pct / damage_control_pct) if damage_control_pct else 0.0
    return {"покрытие_панелями": damage_covered_pct, "контроль": damage_control_pct,
            "эффективность_щита": round(shield, 1)}

if __name__ == "__main__":
    print("жара, 13:00:", summarize_interval(8.2, 6.5, 31.4, 35.9))
    print("утро, 8:00: ", summarize_interval(2.1, 4.0, 22.0, 23.1))
    print("град 12.06.2026:", hail_report(0.4, 17.0))
    # Прототип 10 кВт: сезон 2026 г., 6,1 МВт·ч, доступность 97,8 %.
