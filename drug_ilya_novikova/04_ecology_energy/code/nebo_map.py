# ЧИСТОЕ НЕБО: карта риска полигона и наряды на пересыпку

RISK_LEVELS = ("фон", "разложение", "начало тления", "открытый очаг")
NORM_HOURS = 24          # срок пересыпки после подтверждения

def zone_risk(zone_probes):
    """Максимальный уровень риска по зондам зоны."""
    order = {st: i for i, st in enumerate(RISK_LEVELS)}
    best = max(zone_probes, key=lambda st: order[st])
    return best

def build_map(zones):
    """zones: {зона: [состояния зондов]}."""
    result = {}
    for zone, states in zones.items():
        result[zone] = zone_risk(states)
    return result

def work_orders(risk_map):
    orders = []
    for zone, level in risk_map.items():
        if level == "начало тления":
            orders.append({"зона": zone, "действие": "подтверждение дроном + пересыпка",
                           "срок_часов": NORM_HOURS})
        elif level == "открытый очаг":
            orders.append({"зона": zone, "действие": "немедленная пересыпка, вызов служб",
                           "срок_часов": 6})
    return orders

if __name__ == "__main__":
    zones = {"ЮГ-1": ["фон", "фон"], "СЕВ-2": ["риск тления", "риск тления"],
             "ЦЕНТР-3": ["открытый очаг", "фон"]}
    rmap = build_map(zones)
    print("карта риска:", rmap)
    print("наряды:", work_orders(rmap))
    # Пилот 2026: 3 очага пересыпаны в течение суток после подтверждения тепловизором.
