# БИОФИЛЬТР-СТОК: расчёт секций биофильтра под поголовье фермы
# Методика пилота 2026 г.: ориентир 0,8–1,2 м² на условную голову для молочного скота,
# удержание стоков 8–10 суток, каскад из трёх секций.

SECTION_AREA_M2 = {S: a for S, a in [("усреднитель", 0.17), ("тростник", 0.42), ("рогоз_осока", 0.41)]}
AREA_PER_HEAD = (0.8, 1.2)     # м² на условную голову

def total_area(heads, factor="средний"):
    per_head = {"минимум": AREA_PER_HEAD[0], "средний": 1.0, "максимум": AREA_PER_HEAD[1]}[factor]
    return round(heads * per_head, 1)

def cascade(heads, factor="средний"):
    """Раскладка каскада по секциям (доли из пилота 24 м²)."""
    area = total_area(heads, factor)
    return {"итого, м²": area,
            **{name: round(area * share, 1) for name, share in SECTION_AREA_M2.items()}}

def daily_flow_m3(heads, liters_per_head_day=55.0):
    """Суточный объём стоков, м³ (вода + мойка, молочная ферма)."""
    return round(heads * liters_per_head_day / 1000.0, 1)

if __name__ == "__main__":
    print("ферма 120 голов:", cascade(120))
    print("суточный объём стоков:", daily_flow_m3(120), "м³/сут")
    print("ферма 150 голов, максимум:", cascade(150, "максимум"))
    # Пилот: 24 м² при ~120 головах — 0,2 м²/гол. на частичной загрузке;
    # для полной очистки проектируем 0,8–1,2 м²/гол.
