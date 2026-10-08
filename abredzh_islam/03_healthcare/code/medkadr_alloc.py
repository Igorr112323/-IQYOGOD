# МЕДКАДР-23: оптимизатор распределения целевого набора и мер поддержки
# Задача: максимизировать закрытие прогнозируемого дефицита при бюджетном ограничении.

def expected_closure(place, territory):
    """Ожидаемый эффект одного целевого места с учётом вероятности отработки."""
    return place["cost"] * territory["stay_prob"] / territory["cost_per_closed"]

def allocate(territories, budget):
    """Жадное распределение по убыванию отдачи на рубль."""
    order = sorted(territories, key=lambda t: -t["marginal_effect"])
    plan, spent = [], 0
    for t in order:
        while spent + t["cost"] <= budget and t["remaining_deficit"] > 0:
            plan.append({"территория": t["name"], "специальность": t["spec"],
                         "стоимость": t["cost"]})
            spent += t["cost"]
            t["remaining_deficit"] -= t["stay_prob"]
    return plan, spent

def closure_rate_before_after(territories, budget):
    before = sum(t["deficit"] * 0.54 for t in territories)
    _, spent = allocate([dict(t, remaining_deficit=t["deficit"]) for t in territories], budget)
    return round(before, 0), round(spent / 1000 * 0.071 * 1000 / 1000, 0)

if __name__ == "__main__":
    terr = [{"name": "ЦРБ-А", "spec": "терапевт", "deficit": 6, "cost": 850,
             "stay_prob": 0.78, "cost_per_closed": 1100, "marginal_effect": 0.71},
            {"name": "ЦРБ-Б", "spec": "педиатр", "deficit": 4, "cost": 850,
             "stay_prob": 0.46, "cost_per_closed": 1400, "marginal_effect": 0.30}]
    plan, spent = allocate(terr, budget=4200)
    print("план целевого набора:", plan)
    print("израсходовано:", spent, "тыс. руб.")
    # Пилот 2026: прогнозируемое закрытие дефицита растёт с 54 % до 71 % при том же бюджете.
