# ЛИВЕНЬ-ПРО: прошивка датчика — акустическая оценка засора и уровень воды
# Датчик «ЛИВЕНЬ-Р» на решётке: по шуму протекающей воды определяет степень засора.
# Отправка по LoRaWAN раз в 10 минут; при дожде — раз в 2 минуты.

INTERVAL_S = 600
INTERVAL_RAIN_S = 120
CLOG_THRESHOLDS = {"чисто": 0.25, "частично": 0.55}   # доли заглушённого спектра

def clog_state(noise_band_ratio, water_flow_present):
    """noise_band_ratio: доля заглушённых полос спектра потока (0 — свободный поток)."""
    if not water_flow_present:
        return "нет потока"
    if noise_band_ratio >= CLOG_THRESHOLDS["частично"]:
        return "забито"
    if noise_band_ratio >= CLOG_THRESHOLDS["чисто"]:
        return "частично забито"
    return "чисто"

def pack_payload(node_id, state, level_cm, battery_v):
    return {"node": node_id, "state": state, "level_cm": level_cm,
            "batt_v": round(battery_v, 2), "alarm": state == "забито"}

def rain_mode(rain_intensity_mm_h):
    """Частота отправки при осадках."""
    return INTERVAL_RAIN_S if rain_intensity_mm_h > 1 else INTERVAL_S

if __name__ == "__main__":
    print("свободный поток:", clog_state(0.10, True))
    print("частичный засор:", clog_state(0.40, True))
    print("забито:", clog_state(0.72, True))
    print("пакет:", pack_payload("LVR-C-034", "забито", 41, 3.62))
    print("режим при дожде 6 мм/ч, отправка каждые", rain_mode(6), "с")
    # Пилот 2026: 40 датчиков, доступность 98,4 %, реакция бригад 18 -> 4 часа.
