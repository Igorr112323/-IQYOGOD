# СЕТЬ-КОНТРОЛЬ: индекс риска участков и ранжирование плана ремонтов
# Индекс риска Р = В х П: вероятность отказа на последствия для потребителей.

def failure_probability(age_years, material, prior_failures, acoustic_score):
    base = {"чугун": 0.45, "сталь": 0.35, "пэ": 0.10}.get(material, 0.30)
    age_k = min(age_years / 60.0, 1.5)
    hist_k = 1.0 + 0.25 * prior_failures
    ac_k = 1.0 + 0.5 * acoustic_score      # акустический фон утечек на участке
    return round(min(base * age_k * hist_k * ac_k, 0.95), 3)

def consequences(consumers, social_objects, main_line):
    score = consumers / 1000.0 + 0.4 * social_objects + (0.5 if main_line else 0.0)
    return round(min(score, 5.0), 2)

def risk_index(section):
    v = failure_probability(section["возраст"], section["материал"],
                            section["аварий"], section["акустика"])
    p = consequences(section["абоненты"], section["соцобъекты"], section["магистраль"])
    return {"участок": section["id"], "В": v, "П": p, "индекс": round(v * p, 3)}

def repair_plan(sections, budget_slots):
    ranked = sorted((risk_index(s) for s in sections), key=lambda r: -r["индекс"])
    return [{"очередь": i + 1, **r} for i, r in enumerate(ranked[:budget_slots])]

if __name__ == "__main__":
    zones = [{"id": "Т-04", "возраст": 48, "материал": "чугун", "аварий": 3,
              "акустика": 0.8, "абоненты": 5200, "соцобъекты": 2, "магистраль": True},
             {"id": "Т-11", "возраст": 21, "материал": "сталь", "аварий": 1,
              "акустика": 0.2, "абоненты": 1400, "соцобъекты": 0, "магистраль": False}]
    print("план ремонтов:", repair_plan(zones, budget_slots=2))
    # Пилот 2026: перечень 6 приоритетных участков передан владельцу сетей.
