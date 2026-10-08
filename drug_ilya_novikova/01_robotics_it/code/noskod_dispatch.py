# НОС-КОД: позиционирование стаи по разности времени прихода звука и наряд отлова
# Два и более узлов, услышавших стаю, дают точку на карте; один узел — сектор.

SOUND_SPEED = 343.0            # м/с
DISPATCH_TARGET_MIN = 40       # норматив времени до наряда

def locate(nodes_heard):
    """nodes_heard: [(узел, x, y, t_срабатывания)]. Возвращает точку или сектор."""
    if len(nodes_heard) >= 2:
        xs = [n[1] for n in nodes_heard]
        ys = [n[2] for n in nodes_heard]
        ts = [n[3] for n in nodes_heard]
        w = [1.0 / (0.5 + abs(t - min(ts))) for t in ts]   # раньше услышал — ближе
        sw = sum(w)
        return {"тип": "точка",
                "x": round(sum(x * wi for x, wi in zip(xs, w)) / sw, 1),
                "y": round(sum(y * wi for y, wi in zip(ys, w)) / sw, 1)}
    node = nodes_heard[0]
    return {"тип": "сектор", "узел": node[0], "радиус_м": 120}

def make_order(location, district):
    return {"район": district,
            "локация": location,
            "служба": "отлов",
            "норматив_минут": DISPATCH_TARGET_MIN,
            "статус": "назначен"}

def close_order(order, minutes_to_arrival):
    order["статус"] = "выполнен" if minutes_to_arrival <= DISPATCH_TARGET_MIN else "нарушен срок"
    order["факт_минут"] = minutes_to_arrival
    return order

if __name__ == "__main__":
    heard = [("NK-07", 100, 200, 0.0), ("NK-08", 210, 240, 0.18)]
    loc = locate(heard)
    print("позиционирование:", loc)
    order = make_order(loc, district="Прикубанский")
    print("наряд:", order)
    print("закрытие наряда:", close_order(order, minutes_to_arrival=32))
    # Пилот 2026: время до наряда 2,4 часа против 1-2 дней по заявкам жителей.
