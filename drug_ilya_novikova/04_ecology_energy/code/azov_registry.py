# ЧИСТЫЙ АЗОВ: реестр «паспортов сетей»
# Каждая поднятая сеть получает паспорт: координаты, масса, тип, судьба.

class NetRegistry:
    def __init__(self):
        self.nets = []

    def add(self, net_id, lat, lon, mass_kg, net_type, date, fate="на переработку"):
        self.nets.append(dict(id=net_id, lat=lat, lon=lon, mass_kg=mass_kg,
                              type=net_type, date=date, fate=fate))

    def report(self):
        total = sum(n["mass_kg"] for n in self.nets)
        recycled = sum(n["mass_kg"] for n in self.nets if n["fate"] == "переработана")
        return {
            "сетей": len(self.nets),
            "масса, кг": total,
            "переработано, кг": recycled,
            "рыбы сохранено, т (оценка 1-1,5 т на т сетей в год)":
                round(total / 1000 * 1.0, 1),
        }

if __name__ == "__main__":
    r = NetRegistry()
    r.add("AZ-001", 45.21, 36.87, 120, "ставная", "2026-07-19", "переработана")
    r.add("AZ-002", 45.24, 36.92, 150, "ставная", "2026-08-02", "переработана")
    r.add("AZ-003", 45.31, 37.05, 70, "донная, фрагмент", "2026-08-21")
    print(r.report())
    # Итог экспедиций: 340 кг поднято, 200 кг переработано в гранулу.
