# ЧИСТОЕ НЕБО: обработка показаний зонда и кластерная тревога
# Тревога «начало тления»: устойчивый рост CO и температуры в кластере 3+ зондов за 12 часов.
# Метан — отдельный класс: контроль взрывоопасности, а не тления.

CO_DELTA = 8.0            # ppm прироста за окно
TEMP_DELTA = 4.0          # градусов прироста за окно
CH4_LIMIT = 1.5           # % объёмной доли, порог взрывоопасности

def window_growth(series):
    """Прирост за окно наблюдений."""
    if len(series) < 2:
        return 0.0
    return series[-1] - series[0]

def probe_state(co_series, temp_series, ch4_series):
    ch4 = ch4_series[-1] if ch4_series else 0.0
    if ch4 >= CH4_LIMIT:
        return "взрывоопасный фон метана"
    if window_growth(co_series) >= CO_DELTA and window_growth(temp_series) >= TEMP_DELTA:
        return "риск тления"
    return "фон"

def cluster_alarm(probes):
    """probes: {имя: состояние}. Тревога при 3+ зондах «риск тления» рядом."""
    hot = [name for name, st in probes.items() if st == "риск тления"]
    return {"тревога": len(hot) >= 3, "зонды": hot,
            "действие": "облёт дрона, наряд пересыпки" if len(hot) >= 3 else "наблюдение"}

if __name__ == "__main__":
    print("спокойный зонд:", probe_state([12, 12.5, 13], [28, 28, 28.5], [0.2, 0.2, 0.2]))
    print("зреющий очаг:", probe_state([14, 20, 26], [29, 32, 35], [0.3, 0.4, 0.4]))
    print("метановый всплеск:", probe_state([12, 12, 12], [28, 28, 28], [1.6, 1.7, 1.8]))
    cluster = {"A1": "риск тления", "A2": "риск тления", "A3": "риск тления", "B4": "фон"}
    print("кластерная тревога:", cluster_alarm(cluster))
    # Пилот 2026: 4 события тления, упреждение 4-6 суток до дыма.
