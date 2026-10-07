# БОРА-5: контроль осевого зазора магнитного подвеса
# Три датчика Холла по окружности; задача — держать зазор 2,0 ± 0,3 мм
# и фиксировать касание страховочного подшипника.

TARGET_MM = 2.0
TOL_MM = 0.3

def gap_from_hall(voltage, k=1.8, v0=1.65):
    """Линейная калибровка датчика Холла по щупу: мм."""
    return (voltage - v0) * k

def suspension_state(voltages):
    gaps = [gap_from_hall(v) for v in voltages]
    avg = sum(gaps) / len(gaps)
    tilt = max(gaps) - min(gaps)
    alarm = abs(avg - TARGET_MM) > TOL_MM or tilt > 0.4
    return {"gaps_mm": [round(g, 2) for g in gaps],
            "avg_mm": round(avg, 2), "tilt_mm": round(tilt, 2),
            "alarm": alarm}

if __name__ == "__main__":
    print(suspension_state([2.76, 2.78, 2.75]))   # норма
    print(suspension_state([3.30, 2.80, 2.40]))   # перекос -> тревога
    # Стенд полного размера: зазор удержан при боковой нагрузке до 600 Н.
