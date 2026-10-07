# ПУЛЬС-ПОЙНТ: правила триажа пилотной версии
# Маршрутизация, не диагноз. Правила согласованы с клиническими
# рекомендациями по артериальной гипертензии; валидация — 1240 сеансов.

def triage(systolic: int, diastolic: int, pulse: int, spo2: int,
           temp_c: float, chest_pain: bool, answers: dict) -> dict:
    """Возвращает маршрут: green / yellow / red + пояснение."""
    if chest_pain or spo2 < 92 or temp_c >= 39.5:
        return {"route": "red", "why": "признаки неотложного состояния -> 103"}
    if systolic >= 180 or diastolic >= 110:
        return {"route": "red", "why": "гипертонический криз: инструкция + 103"}
    yellow = []
    if systolic >= 140 or diastolic >= 90:
        yellow.append("АД >= 140/90")
    if pulse > 110 or pulse < 45:
        yellow.append("пульс вне коридора 45-110")
    if temp_c >= 38.0:
        yellow.append("температура >= 38,0")
    if answers.get("diabetes") and answers.get("weakness"):
        yellow.append("диабет + слабость: контроль глюкозы")
    if yellow:
        return {"route": "yellow", "why": "; ".join(yellow) + " -> телемедицина/поликлиника"}
    return {"route": "green", "why": "норма: рекомендации и повторный чек-ап"}

if __name__ == "__main__":
    cases = [
        dict(systolic=190, diastolic=105, pulse=98, spo2=97, temp_c=36.7, chest_pain=False, answers={}),
        dict(systolic=146, diastolic=92, pulse=84, spo2=98, temp_c=36.6, chest_pain=False, answers={}),
        dict(systolic=118, diastolic=74, pulse=71, spo2=99, temp_c=36.5, chest_pain=False, answers={}),
        dict(systolic=132, diastolic=84, pulse=77, spo2=90, temp_c=36.8, chest_pain=False, answers={}),
    ]
    for c in cases:
        print(triage(**c))
    # Пилот: доля красных 1,9 %, ложных красных 0,4 % (врачебный контроль).
