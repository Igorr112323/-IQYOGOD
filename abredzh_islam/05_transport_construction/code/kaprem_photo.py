# КАПРЕМОНТ-КОНТРОЛЬ: фотоверификация этапов по чек-листам
# Некомплект (нет геометки, съёмка вне объекта, не все ракурсы) отклоняется до акта.

CHECKLIST = {
    "кровля": ["общий план", "примыкания", "водоотведение"],
    "фасад": ["общий план", "цоколь", "откосы"],
    "инженерные системы": ["стояки", "узлы учёта", "разводка"]}

def validate_shot(shot, object_geopoint):
    errors = []
    if not shot.get("геометка"):
        errors.append("нет геометки")
    elif shot["геометка"] != object_geopoint:
        errors.append("съёмка вне объекта")
    if not shot.get("ракурс") or shot["ракурс"] not in sum(CHECKLIST.values(), []):
        errors.append("ракурс вне чек-листа")
    return errors

def validate_stage(kind, shots, object_geopoint):
    required = set(CHECKLIST[kind])
    got = {s["ракурс"] for s in shots}
    errors = [e for s in shots for e in validate_shot(s, object_geopoint)]
    missing = required - got
    ok = not errors and not missing
    return {"этап": kind, "статус": "принят" if ok else "отклонён",
            "ошибки": errors, "не хватает": sorted(missing)}

if __name__ == "__main__":
    geo = "45.03, 38.97"
    shots_ok = [{"ракурс": "общий план", "геометка": geo},
                {"ракурс": "примыкания", "геометка": geo},
                {"ракурс": "водоотведение", "геометка": geo}]
    print(validate_stage("кровля", shots_ok, geo))
    shots_bad = [{"ракурс": "общий план", "геометка": "44.70, 37.77"}]
    print(validate_stage("кровля", shots_bad, geo))
    # Пилот 2026: отклонено 23 некомплекта фото до подписания актов.
