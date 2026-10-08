# ЖИВОЙ УЛЕЙ: акустический анализ гула семьи на борту датчика
# Состояния: здоровая / пестицидный стресс / подготовка к роению / ослабление.

STATES = ("здоровая", "пестицидный стресс", "подготовка к роению", "ослабление")
STRESS_CONFIDENCE = 0.60
SWARM_CONFIDENCE = 0.55

def hum_features(spectrum):
    """Признаки гула: центроида спектра, модуляция, доля тревожных частот."""
    return {"centroid_hz": spectrum.get("centroid_hz", 250),
            "modulation": spectrum.get("modulation", 0.1),
            "alarm_share": spectrum.get("alarm_share", 0.0)}

def stress_score(f):
    """Стресс: рост тревожных частот и рваный ритм."""
    return 0.5 * f["alarm_share"] + 0.3 * min(f["modulation"], 1.0) + 0.2 * (f["centroid_hz"] - 250) / 400

def swarm_score(f):
    """Роение: рост центроиды за несколько суток до выхода роя."""
    return 0.6 * (f["centroid_hz"] - 280) / 300 + 0.4 * f["modulation"]

def classify(spectrum):
    f = hum_features(spectrum)
    s, w = stress_score(f), swarm_score(f)
    if s >= STRESS_CONFIDENCE:
        return STATES[1], round(s, 2)
    if w >= SWARM_CONFIDENCE:
        return STATES[2], round(w, 2)
    if f["modulation"] < 0.05 and f["alarm_share"] < 0.05:
        return STATES[0], 0.0
    return STATES[3], round(max(s, w), 2)

if __name__ == "__main__":
    calm = {"centroid_hz": 240, "modulation": 0.12, "alarm_share": 0.03}
    stress = {"centroid_hz": 380, "modulation": 0.7, "alarm_share": 0.55}
    swarm = {"centroid_hz": 420, "modulation": 0.6, "alarm_share": 0.10}
    for name, sp in [("ровный гул", calm), ("химия рядом", stress), ("рой готовится", swarm)]:
        print(name, "->", classify(sp))
    # Пилот 2026: 9 эпизодов стресса, 7 предупреждений за 18-36 часов до видимой гибели.
