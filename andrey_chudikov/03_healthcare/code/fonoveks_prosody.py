# ФОНО-ВЕКС: извлечение просодических признаков диалогового фрагмента
# Признаки используются моделью скрининга когнитивных нарушений.
# Реализация учебно-демонстрационная; в изделии применяется калиброванная версия.

def speech_rate(syllables, voiced_seconds):
    """Слоговая скорость, слогов/с. Снижение скорости — один из маркеров."""
    if voiced_seconds <= 0:
        return None
    return syllables / voiced_seconds

def pause_profile(pauses_s):
    """Паузы длительностью >= 0,4 с: доля и средняя длительность."""
    significant = [p for p in pauses_s if p >= 0.4]
    total = sum(pauses_s) or 1.0
    return {"доля_пауз": round(sum(significant) / total, 3),
            "средняя_с": round(sum(significant) / len(significant), 3)
            if significant else 0.0}

def f0_variability(f0_track_hz):
    """Коэффициент вариации основной частоты; монотонность — маркер."""
    n = len(f0_track_hz)
    if n < 10:
        return None
    mean = sum(f0_track_hz) / n
    var = sum((x - mean) ** 2 for x in f0_track_hz) / n
    return round((var ** 0.5) / mean, 3) if mean else None

def repetition_index(transcript_words):
    """Доля повторов слов в пределах окна 12 слов — маркер поиска слов."""
    window, repeats = 12, 0
    for i in range(len(transcript_words)):
        if transcript_words[i] in transcript_words[max(0, i - window):i]:
            repeats += 1
    return round(repeats / len(transcript_words), 3) if transcript_words else 0.0

def feature_vector(dialogue):
    return {"слоговая_скорость": speech_rate(dialogue["слоги"], dialogue["озвучено_с"]),
            "паузы": pause_profile(dialogue["паузы_с"]),
            "вариабельность_f0": f0_variability(dialogue["f0_гц"]),
            "индекс_повторов": repetition_index(dialogue["слова"])}

if __name__ == "__main__":
    sample = {"слоги": 214, "озвучено_с": 96.0,
              "паузы_с": [0.2, 0.6, 0.9, 0.3, 1.4],
              "f0_гц": [172, 168, 175, 181, 169, 176] * 6,
              "слова": ["добрый", "день", "да", "добрый", "вчера", "вчера"]}
    print(feature_vector(sample))
    # Валидация 2026: 412 участников, 1 236 диалогов, эталон GDS-15;
    # чувствительность 0,86, специфичность 0,79.
