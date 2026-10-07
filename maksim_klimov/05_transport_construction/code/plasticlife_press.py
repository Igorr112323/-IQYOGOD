# ВТОРАЯ ЖИЗНЬ ПЛАСТИКА: контроллер температурных зон термопресса
# Фрагмент рабочего ПО мобильного комплекса (этап 2-4).
# Режимы: нагрев до уставки, выдержка под давлением, остывание под прижимом.

import time

ZONES = {"mixer": 210.0, "plate_top": 185.0, "plate_bottom": 185.0}
PRESS_T = 40.0          # т, усилие
HOLD_MIN = 4.0          # мин выдержки
COOL_TO = 60.0          # °С, распалубка

class Press:
    def __init__(self):
        self.temps = {z: 25.0 for z in ZONES}
        self.state = "IDLE"

    def heat(self, power_frac=1.0, dt_s=60.0):
        for z, target in ZONES.items():
            self.temps[z] += power_frac * (target - self.temps[z]) * 0.35
        return all(self.temps[z] >= target - 3 for z, target in ZONES.items())

    def cycle(self, simulate_minutes=30):
        """Упрощённая симуляция цикла прессования плитки."""
        log = []
        while not self.heat():
            log.append(("heat", round(self.temps["mixer"], 1)))
        self.state = "PRESS"
        for _ in range(int(HOLD_MIN)):
            log.append(("hold", PRESS_T))
        self.state = "COOL"
        while self.temps["plate_top"] > COOL_TO:
            self.temps["plate_top"] *= 0.86
            self.temps["plate_bottom"] *= 0.86
            log.append(("cool", round(self.temps["plate_top"], 1)))
        self.state = "IDLE"
        return log

if __name__ == "__main__":
    p = Press()
    log = p.cycle()
    print("фаз цикла:", len(log), "; финальное состояние:", p.state)
    # По протоколу: партия плитки без брака при уставках 210/185 °С.
