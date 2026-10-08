# ВТОРАЯ ЛОЗА: планировщик партий и паспорт партии экстракта
# Каждая партия получает паспорт с метриками — пищевое производство принимает по цифрам.

from datetime import date, timedelta

POLYPHENOL_MIN = 24.0      # %, сумма полифенолов в пересчёте на галловую кислоту
MOISTURE_MAX = 5.0         # %, влажность сухого экстракта

class BatchPlanner:
    def __init__(self, capacity_t_per_day=4.0):
        self.capacity = capacity_t_per_day
        self.queue = []

    def add(self, variety, tons, day_offset=0):
        self.queue.append({"сорт": variety, "тонн": tons, "день": day_offset})

    def schedule(self):
        """Раскладка по дням с учётом производительности модуля."""
        plan, carry, day = [], 0.0, 0
        for item in sorted(self.queue, key=lambda x: x["день"]):
            carry += item["тонн"]
            while carry >= self.capacity:
                plan.append({"день": item["день"] + day, "сорт": item["сорт"],
                             "тонн": self.capacity})
                carry -= self.capacity
                day += 1
        if carry > 0:
            plan.append({"день": (self.queue[-1]["день"] if self.queue else 0) + day,
                         "сорт": item["сорт"] if self.queue else "-", "тонн": round(carry, 2)})
        return plan

def batch_passport(batch_id, variety, polyphenol_pct, moisture_pct, yield_kg_per_t):
    ok = polyphenol_pct >= POLYPHENOL_MIN and moisture_pct <= MOISTURE_MAX
    return {
        "партия": batch_id, "сорт": variety,
        "полифенолы_%": polyphenol_pct, "влажность_%": moisture_pct,
        "выход_кг_на_т": yield_kg_per_t,
        "статус": "годен" if ok else "отклонён",
        "дата": date.today().isoformat(),
    }

if __name__ == "__main__":
    p = BatchPlanner(capacity_t_per_day=4.0)
    p.add("Красностоп", 9.0)
    p.add("Шардоне", 5.5)
    print("план:", p.schedule())
    print("паспорт:", batch_passport("LZ-2026-014", "Саперави", 27.6, 4.1, 3.4))
    # 28 экстракций прототипа: все партии с паспортом, полифенолы 24-31 %.
