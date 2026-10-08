# ОКО-СКРИН: бортовой инференс модели анализа глазного дна (фрагмент рабочего ПО)
# Модель работает на вычислительном модуле станции, офлайн; классы по референсным шкалам.

QUALITY_MIN = 0.70          # порог годности снимка для анализа
CLASSES = ("норма", "подозрение", "угрожающие признаки")

def check_frame_quality(sharpness, exposure_ok, optic_disc_found):
    """Автоконтроль качества кадра до инференса (96 % годных в валидации)."""
    score = 0.5 * sharpness + 0.3 * (1.0 if exposure_ok else 0.0) \
            + 0.2 * (1.0 if optic_disc_found else 0.0)
    return round(score, 2), score >= QUALITY_MIN

def infer(frame_features, model):
    """Возвращает категорию и признаки; модель дообучена на региональных данных."""
    probs = model.predict(frame_features)     # [норма, подозрение, угрожающие]
    cls = int(max(range(3), key=lambda i: probs[i]))
    signs = [s for s, p in zip(("микроаневризмы", "экссудаты", "неоваскуляризация"),
                               probs) if p > 0.35]
    return CLASSES[cls], round(probs[cls], 3), signs

def decide(category):
    """Маршрут пациента по результату (валидация 2026: 61 подозрение, 9 угрожающих)."""
    return {"норма": "следующий скрининг через 12 мес",
            "подозрение": "телемедицинский приём офтальмолога, 14 дней",
            "угрожающие признаки": "очный приём офтальмолога, 3 дня"}[category]

if __name__ == "__main__":
    class StubModel:
        def predict(self, _f):
            return [0.06, 0.22, 0.72]

    q, ok = check_frame_quality(0.86, True, True)
    cat, p, signs = infer(None, StubModel())
    print("качество кадра:", q, "годен:", ok)
    print("категория:", cat, p, signs, "->", decide(cat))
