# ЭКОСИГНАЛ КУБАНИ: акустический классификатор событий сброса мусора
# Вход: аудиофрагмент 10 с (16 кГц, моно). Признаки: мел-спектрограмма 64×40.
# Классы: 0 — фон, 1 — сброс мусора (самосвал/бой/манипулятор), 2 — техника без сброса.
# Обучение: датасет 4 200 фрагментов (июль–август 2026 г.), отложенная выборка 20 %.

import math

SR = 16000
WINDOW_S = 10.0
N_MELS = 64
N_FRAMES = 40
THRESHOLD = 0.62          # порог вероятности класса «сброс» для создания сигнала
MAX_FALSE_PER_DAY = 3     # эксплуатационное ограничение на пост

def mel_spectrogram(samples, n_mels=N_MELS, n_frames=N_FRAMES):
    """Упрощённое мел-представление: энергия по полосам (заглушка для стенда)."""
    block = max(1, len(samples) // n_frames)
    frames = []
    for i in range(n_frames):
        chunk = samples[i * block:(i + 1) * block] or [0]
        e = math.sqrt(sum(x * x for x in chunk) / len(chunk))
        frames.append([e] * n_mels)
    return frames

def classify(spectrogram, model):
    """Логистический выход модели; возвращает вероятности трёх классов."""
    # в продакшене — свёрточная сеть на мел-спектрограммах; здесь интерфейс
    return model.predict(spectrogram)

def on_event(node_id, probs, ts, send_signal):
    """Пороговая логика: при высокой вероятности сброса создаём черновик сигнала."""
    if probs[1] >= THRESHOLD:
        send_signal({
            "node": node_id,
            "type": "acoustic_dump",
            "p_dump": round(probs[1], 3),
            "audio_ref": f"{node_id}_{ts}.wav",
            "ts": ts,
            "status": "draft",  # волонтёр подтверждает перед отправкой в органы
        })
        return True
    return False

if __name__ == "__main__":
    class StubModel:
        def predict(self, _spec):
            return [0.08, 0.87, 0.05]  # пример: эпизод сброса

    created = []
    spec = mel_spectrogram([0.2, -0.1, 0.3] * 1600)
    fired = on_event("post-07", classify(spec, StubModel()), 1767268800,
                     lambda s: created.append(s))
    print("сигнал создан:", fired, created[0]["p_dump"] if fired else "-")
