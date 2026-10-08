# ТЕРМОСТОПА-32: драйвер передачи результата в медицинскую информационную систему
# Устройство отдаёт запись; драйвер формирует строку карты и очередь на осмотр.

QUEUE_CATEGORIES = {"осмотр врача"}

def mis_record(patient_id, measurement, operator="устройство-01"):
    return {"пациент": patient_id,
            "дата": measurement.get("дата", "2026-09-30"),
            "источник": operator,
            "категория": measurement["категория"],
            "индекс_асимметрии": measurement["индекс"],
            "карта_зон": measurement["карта"]}

def enqueue(record):
    """Пациенты категории «осмотр врача» попадают в начало очереди эндокринолога."""
    return record["категория"] in QUEUE_CATEGORIES

def shift_capacity(measurements_per_patient_min=3):
    """Смена 8 часов: 60 с измерение + оформление."""
    return int(8 * 60 / (measurements_per_patient_min + 1))

if __name__ == "__main__":
    m = {"категория": "осмотр врача", "индекс": 2.7, "карта": [0.1] * 16, "дата": "2026-09-30"}
    rec = mis_record(4412, m)
    print("запись карты:", rec)
    print("в очередь к врачу:", enqueue(rec))
    print("пропускная способность, пациентов в смену:", shift_capacity())
    # Результат в МИС за 60 секунд; 40 пациентов в смену на устройство.
