# ГРУНТ-МЕМ М1: сервер приёма пакетов и формирование заявок
# Пакет датчика: 46 байт (идентификатор, наклон по двум осям, заряд, температура).

DELIVERY_TARGET = 0.995
ALERT_STATE = "заявка"

def parse_packet(raw):
    return {"датчик": raw["id"],
            "наклон_x": raw["tx"],
            "наклон_y": raw["ty"],
            "батарея": raw["bat"],
            "температура": raw["temp"]}

def zone_status(sensor, trend, threshold=0.08):
    if trend is None:
        return "набор данных"
    if trend >= threshold:
        return ALERT_STATE
    return "фоновое наблюдение"

def dispatch(zone_id, trend, owner):
    return {"участок": zone_id,
            "владелец_сети": owner,
            "тренд_град_нед": round(trend, 3),
            "действие": "обследование участка, перекрытие при подтверждении"}

def delivery_rate(received, sent):
    return received / sent if sent else 0.0

if __name__ == "__main__":
    pkt = parse_packet({"id": "GM-066-04", "tx": 0.14, "ty": 0.05, "bat": 3.61, "temp": 17.4})
    print("пакет:", pkt)
    print("статус зоны:", zone_status(pkt["датчик"], trend=0.11))
    print("заявка:", dispatch("Московская-66", 0.11, "водоканал"))
    print("доставка за 47 суток:", delivery_rate(6048, 6066))
    # Полевые наблюдения: 12 датчиков, доставка 99,7 %, ложных срабатываний 0.
