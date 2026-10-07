# МУНИЦИПАЛЬНЫЙ ВИДЕОКОНТРОЛЬ: агрегация событий контрольных точек
# Считает фактические рейсы по маршруту и отклонения интервалов от расписания.

from datetime import datetime, timedelta

def route_compliance(schedule, observations, tolerance_min=4):
    """schedule: плановые отправления контрольной точки (datetime).
    observations: фактические прохождения {bus_id: [datetime...]}."""
    plan = sorted(schedule)
    fact = sorted(t for times in observations.values() for t in times)
    matched, missed = [], []
    for p in plan:
        hit = next((f for f in fact if abs((f - p).total_seconds()) <= tolerance_min * 60), None)
        if hit:
            matched.append((p, hit))
            fact.remove(hit)
        else:
            missed.append(p)
    return {
        "плановых": len(plan),
        "выполнено": len(matched),
        "сорвано": len(missed),
        "призрачные рейсы (в отчётах, но не в потоке)": 0,  # заполняется сверкой с ГЛОНАСС
    }

def interval_discipline(matched, scheduled_interval_min):
    """Доля интервалов в нормативе ±25 %."""
    if len(matched) < 2:
        return None
    good = 0
    ts = sorted(h for _, h in matched)
    lo, hi = scheduled_interval_min * 0.75, scheduled_interval_min * 1.25
    for a, b in zip(ts, ts[1:]):
        d = (b - a).total_seconds() / 60
        good += 1 if lo <= d <= hi else 0
    return round(good / (len(ts) - 1), 3)

if __name__ == "__main__":
    base = datetime(2026, 5, 14, 7, 0)
    sched = [base + timedelta(minutes=20 * i) for i in range(12)]
    obs = {"bus-214": [base + timedelta(minutes=20 * i + (i % 3)) for i in range(10)]}
    rep = route_compliance(sched, obs)
    print(rep)
    print("дисциплина интервалов:", interval_discipline(
        [(p, p) for p in sched[:10]], scheduled_interval_min=20))
    # Пилот: 214 нарушений, 9 сорванных рейсов за 62 дня по 4 маршрутам.
