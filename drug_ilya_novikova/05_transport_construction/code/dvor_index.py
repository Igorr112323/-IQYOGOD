# ДОСТУПНЫЙ КУРОРТ: индекс доступности курортной территории
# Взвешенная доля доступных объектов по категориям; публикуется ежеквартально.

WEIGHTS = {
    "пляжи": 0.25,
    "набережные": 0.20,
    "размещение": 0.25,
    "аптеки_медицина": 0.15,
    "транспортные_узлы": 0.15,
}

def category_share(statuses):
    """statuses: список статусов объектов категории ('доступно' и т.д.)."""
    if not statuses:
        return None
    full = sum(1 for s in statuses if s == "доступно")
    half = sum(1 for s in statuses if s == "доступно с помощью")
    return (full + 0.5 * half) / len(statuses)

def territory_index(by_category):
    """by_category: {категория: [статусы]}. Возвращает индекс 0..100."""
    score, weight_used = 0.0, 0.0
    detail = {}
    for cat, w in WEIGHTS.items():
        share = category_share(by_category.get(cat, []))
        if share is None:
            continue
        detail[cat] = round(share * 100, 1)
        score += share * w
        weight_used += w
    return round(100 * score / weight_used if weight_used else 0.0, 1), detail

if __name__ == "__main__":
    pilot = {
        "пляжи": ["доступно", "доступно с помощью", "недоступно", "доступно"],
        "набережные": ["доступно", "доступно с помощью"],
        "размещение": ["доступно", "недоступно", "доступно с помощью", "доступно", "недоступно"],
        "аптеки_медицина": ["доступно", "доступно"],
        "транспортные_узлы": ["доступно с помощью"],
    }
    idx, detail = territory_index(pilot)
    print("индекс территории:", idx, "из 100")
    print("по категориям:", detail)
    # Пилот Анапа/Геленджик/Ейск 2026 г.: 11 из 40 аудированных объектов полностью доступны.
