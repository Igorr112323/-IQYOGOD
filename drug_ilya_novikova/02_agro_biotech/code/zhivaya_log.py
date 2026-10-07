# ЖИВАЯ ЗЕМЛЯ: журнал сети вермикомпостеров
# Каждый модуль ежемесячно отдаёт сводку; район видит суммарную переработку.

class NetworkLog:
    def __init__(self):
        self.entries = []

    def add(self, site, month, waste_kg, humus_kg, temp_min, temp_max):
        self.entries.append(dict(site=site, month=month, waste=waste_kg,
                                 humus=humus_kg, tmin=temp_min, tmax=temp_max))

    def totals(self):
        return {
            "модулей": len({e["site"] for e in self.entries}),
            "органики, кг": sum(e["waste"] for e in self.entries),
            "биогумуса, кг": sum(e["humus"] for e in self.entries),
            "не доехало до полигона, кг": sum(e["waste"] for e in self.entries),
        }

if __name__ == "__main__":
    log = NetworkLog()
    for m, w, h in [("02", 140, 20), ("03", 165, 28), ("04", 190, 40),
                    ("05", 215, 48), ("06", 225, 62), ("07", 240, 80), ("08", 245, 102)]:
        log.add("школа № 83 + двор", m, w, h, 9, 27)
    t = log.totals()
    print(t)
    assert t["органики, кг"] == 1420
    print("журнал пилота сведён: 1,42 т органики, 380 кг биогумуса")
