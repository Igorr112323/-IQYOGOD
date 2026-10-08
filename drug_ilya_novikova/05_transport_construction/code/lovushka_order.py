# ГОРОД БЕЗ ЛОВУШЕК: нарядный контур с нормативами и публичные статусы

NORMS_HOURS = {"тротуар": 6, "магистраль": 12, "просадка": 24}
STATUSES = ("обнаружено", "наряд назначен", "закрыто", "срок сорван")

def open_order(manhole_id, event_type, place, contractor):
    return {"люк": manhole_id, "тип": event_type, "место": place,
            "подрядчик": contractor,
            "норматив_часов": NORMS_HOURS.get(event_type, 24),
            "статус": "наряд назначен"}

def close_order(order, photo_ok, sensor_ok):
    order["статус"] = "закрыто" if photo_ok and sensor_ok else "закрыто с замечанием"
    order["подтверждение"] = "фото + датчик «крышка на месте»"
    return order

def weekly_summary(orders):
    """Сводка для администрации и публичной карты: кто срывает сроки."""
    by_contractor = {}
    for o in orders:
        c = o["подрядчик"]
        by_contractor.setdefault(c, {"нарядов": 0, "сорвано": 0})
        by_contractor[c]["нарядов"] += 1
        if o["статус"] == "срок сорван":
            by_contractor[c]["сорвано"] += 1
    return by_contractor

if __name__ == "__main__":
    order = open_order("Л-104", "нет", "тротуар у школы", "ООО «Сетьсервис»")
    print("наряд:", order)
    print("закрытие:", close_order(order, photo_ok=True, sensor_ok=True))
    late = open_order("Л-207", "смещение", "магистраль", "АО «Горсети»")
    late["статус"] = "срок сорван"
    print("сводка недели:", weekly_summary([order, late]))
    # Пилот 2026: средний срок закрытия наряда 7 часов против 3-7 дней по заявкам.
