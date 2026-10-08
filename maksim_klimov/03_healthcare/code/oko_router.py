# ОКО-СКРИН: маршрутизация пациентов и шлюз в МИС/телемедицину (фрагмент рабочего ПО)

from datetime import date, timedelta

SLA_DAYS = {"норма": 365, "подозрение": 14, "угрожающие признаки": 3}

def route(patient_id, category, eye_center, mis_write):
    """Формирует пакет маршрутизации и запись в карту пациента."""
    deadline = date.today() + timedelta(days=SLA_DAYS[category])
    packet = {
        "пациент": patient_id,
        "категория": category,
        "назначение": eye_center if category != "норма" else "плановый скрининг",
        "срок_до": deadline.isoformat(),
        "телемедицина": category == "подозрение",
    }
    mis_write(packet)   # запись в МИС поликлиники
    return packet

def queue_load(queue, ophthalmologist_slots_per_day=6):
    """Оценка загрузки очереди телеконсультаций офтальмологического центра."""
    if not queue:
        return {"очередь": 0, "дней_до_приёма": 0}
    days = max(1, -(-len(queue) // ophthalmologist_slots_per_day))
    return {"очередь": len(queue), "дней_до_приёма": days}

if __name__ == "__main__":
    written = []
    pkt = route("P-090143", "угрожающие признаки", "Краевой офтальмологический центр",
                lambda p: written.append(p))
    print("пакет:", pkt)
    print("загрузка центра:", queue_load(["q1"] * 34))
    # Пилот 2026: телемедицинское плечо отработано на 34 случаях, среднее время 9 дней.
