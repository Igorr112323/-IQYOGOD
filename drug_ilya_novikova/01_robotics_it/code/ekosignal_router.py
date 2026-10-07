# ЭКОСИГНАЛ КУБАНИ: маршрутизация сигналов по полномочиям
# По координатам и категории сигнала определяется ответственный орган
# и нормативный срок реакции. Фрагмент рабочей логики платформы.

AUTHORITY_LAYERS = {
    "свалка": ("администрация района", 10),
    "контейнеры": ("региональный оператор ТКО", 3),
    "водоём": ("Минприроды края", 14),
    "дым": ("администрация района + МЧС", 1),
    "шум": ("администрация района", 7),
}

def resolve_authority(category: str, point: tuple, layers) -> dict:
    """layers: ГИС-слои границ с атрибутом органа; точка попадает в один слой."""
    base, days = AUTHORITY_LAYERS.get(category, ("администрация района", 14))
    for layer in layers:
        if inside(point, layer["bbox"]):
            return {"орган": layer.get("authority", base), "срок_дней": days,
                    "территория": layer["name"]}
    return {"орган": base, "срок_дней": days, "территория": "вне слоёв"}

def inside(point, bbox):
    x, y = point
    return bbox[0] <= x <= bbox[2] and bbox[1] <= y <= bbox[3]

if __name__ == "__main__":
    demo_layers = [
        {"name": "Динское сельское поселение", "bbox": (38.6, 45.1, 39.4, 45.5),
         "authority": "администрация Динского района"},
    ]
    print(resolve_authority("свалка", (39.0, 45.25), demo_layers))
    print(resolve_authority("дым", (39.0, 45.25), demo_layers))
    # В пилоте 8 недель: средний срок реакции снизился с 19 до 7 дней.
