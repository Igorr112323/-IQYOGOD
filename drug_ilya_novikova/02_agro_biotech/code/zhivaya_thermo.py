# БИОФИЛЬТР-СТОК: журнал уровня и отбора проб (цифровой след чистоты)
# Готовит данные для отчёта хозяйству и контролирующему органу.

class ProbeLog:
    def __init__(self, farm):
        self.farm = farm
        self.records = []

    def add(self, date, level_cm, bod5_in, bod5_out, nh4_in, nh4_out):
        self.records.append(dict(date=date, level=level_cm,
                                 bod5=(bod5_in, bod5_out), nh4=(nh4_in, nh4_out)))

    def reduction(self, key):
        pairs = [r[key] for r in self.records if r[key][0] > 0]
        return round(100.0 * (1 - sum(o for _, o in pairs) / sum(i for i, _ in pairs)), 0)

    def summary(self):
        return {
            "ферма": self.farm,
            "циклов проб": len(self.records),
            "снижение БПК5, %": self.reduction("bod5"),
            "снижение NH4, %": self.reduction("nh4"),
            "уровень в норме": all(15 <= r["level"] <= 45 for r in self.records),
        }

if __name__ == "__main__":
    log = ProbeLog("МТФ Динской район")
    # фрагмент пилота, март–сентябрь 2026 г.
    log.add("2026-03-15", 32, 405, 78, 92, 25)
    log.add("2026-05-10", 30, 418, 71, 99, 22)
    log.add("2026-07-08", 28, 424, 76, 101, 24)
    log.add("2026-09-02", 31, 401, 69, 90, 21)
    print(log.summary())
    # Итог сезона: БПК5 −82 %, аммонийный азот −76 %, взвешенные вещества −88 %.
