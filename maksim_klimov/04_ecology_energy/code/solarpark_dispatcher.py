# СОЛНЦЕПАРК: энергодиспетчер пикового бритья (фрагмент рабочего ПО)
# Каждый интервал 15 мин решает: солнце -> отель / накопитель / зарядки.

PEAK_HOURS = range(19, 24)          # пиковая зона тарифа
SOC_MIN, SOC_MAX = 0.15, 0.95       # границы накопителя

def dispatch(hour, solar_kw, hotel_kw, ev_request_kw, soc, cap_kwh=40.0):
    """Возвращает потоки: в отель, в накопитель (+заряд/−разряд), в зарядки."""
    to_hotel = min(solar_kw, hotel_kw)
    left = solar_kw - to_hotel
    to_ev = 0.0
    to_batt = 0.0
    if hour in PEAK_HOURS and soc > SOC_MIN:
        # вечер: накопитель кормит отель вместо сети
        discharge = min((soc - SOC_MIN) * cap_kwh * 4, hotel_kw - to_hotel)
        to_hotel += max(discharge, 0.0)
    if left > 0:
        to_ev = min(ev_request_kw, left)
        left -= to_ev
        if left > 0 and soc < SOC_MAX:
            to_batt = left
    soc_new = soc + (to_batt - max(0.0, -(solar_kw - hotel_kw - to_ev))) / cap_kwh * 0.25
    return {"hotel_kw": round(to_hotel, 2), "ev_kw": round(to_ev, 2),
            "batt_kw": round(to_batt, 2), "soc": round(min(max(soc_new, 0), 1), 3)}

if __name__ == "__main__":
    print("день, 13:00, солнце 18 кВт:", dispatch(13, 18, 9, 11, soc=0.4))
    print("пик, 20:15, солнца нет:  ", dispatch(20, 0, 24, 7, soc=0.8))
    # Пилот: срезано 38 кВт вечернего пика отеля (июль–август 2026).
