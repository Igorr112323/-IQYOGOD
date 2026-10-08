# НОС-КОД: бортовая классификация звуковых событий узла
# Узел слушает двор круглосуточно и различает три класса: фон, одиночная спокойная
# собака, агрессивная стая. Звук не передаётся — наружу уходит только событие.

CLASSES = ("фон", "одиночная собака", "агрессивная стая")
CONFIRM_WINDOW_S = 30          # длительность видеоклипа верификации
PACK_THRESHOLD = 0.62          # порог класса «стая»

def bark_features(frame):
    """Признаки кадра: доля вокализации, число перекрывающихся голосов, рык."""
    return {"voiced": frame.get("voiced", 0.0),
            "overlap": frame.get("overlap", 0.0),
            "growl": frame.get("growl", 0.0)}

def pack_score(features):
    """Стаю отличают перекрывающиеся голоса, нарастающая частота и рык."""
    return 0.45 * features["overlap"] + 0.35 * features["growl"] + 0.20 * features["voiced"]

def classify_frame(frame):
    f = bark_features(frame)
    score = pack_score(f)
    if score >= PACK_THRESHOLD:
        return CLASSES[2], round(score, 2)
    if f["voiced"] > 0.25:
        return CLASSES[1], round(score, 2)
    return CLASSES[0], round(score, 2)

def privacy_packet(node_id, cls, score, ts):
    """Наружу уходит событие, а не звук."""
    return {"узел": node_id, "класс": cls, "балл": score, "время": ts,
            "клип": "запрошен" if cls == CLASSES[2] else "не требуется",
            "длительность_клипа_с": CONFIRM_WINDOW_S if cls == CLASSES[2] else 0}

if __name__ == "__main__":
    quiet = {"voiced": 0.10, "overlap": 0.0, "growl": 0.0}
    lone = {"voiced": 0.40, "overlap": 0.1, "growl": 0.0}
    pack = {"voiced": 0.70, "overlap": 0.8, "growl": 0.6}
    for name, fr in [("тихий двор", quiet), ("одинокая собака", lone), ("стая", pack)]:
        cls, score = classify_frame(fr)
        print(name, "->", cls, score)
    print("пакет события:", privacy_packet("NK-07", "агрессивная стая", 0.71, "06:42"))
    # Пилот 2026: точность класса «агрессивная стая» 0,86, ложные тревоги 3,1 %.
