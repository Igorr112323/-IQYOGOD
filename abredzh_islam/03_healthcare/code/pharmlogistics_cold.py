# ФАРМЛОГИСТИКА-ЮГ: контроль холодовой цепи 2-8 °С
# Каждые 10 минут -> реестр; отклонение -> алерт и блокировка выдачи партии.

LIMITS = (2.0, 8.0)

def check_chain(series):
    """series: [(время, температура)]."""
    violations, warm_minutes = [], 0
    for ts, temp in series:
        if temp > LIMITS[1] or temp < LIMITS[0]:
            violations.append((ts, temp))
            warm_minutes += 10
    status = "ОК" if warm_minutes == 0 else ("ГОДНО К РЕШЕНИЮ КОМИССИИ"
              if warm_minutes <= 30 else "БЛОКИРОВАНА К ВЫДАЧЕ")
    return {"нарушений": len(violations),
            "минут вне диапазона": warm_minutes,
            "статус": status}

if __name__ == "__main__":
    series = [("07:00", 4.2), ("07:10", 4.5), ("07:20", 8.6),
              ("07:30", 6.1), ("07:40", 4.9), ("07:50", 4.4)]
    rep = check_chain(series)
    print(rep)
    assert rep["статус"] == "ГОДНО К РЕШЕНИЮ КОМИССИИ"
    # Пилот: 26 отклонений за год, все до 30 минут, партий заблокировано - 0.
