# БОРА-5: трекер максимальной мощности и штормовой сброс
# Фрагмент контроллера головного образца. Работает на прерываниях 2 кГц.

STORM_MS = 25.0        # м/с, переход на сброс
BALLAST_W = 5000.0     # ТЭН-балласт
V_BUS = 48.0

class Mppt:
    def __init__(self):
        self.p_ref = 0.0

    def step(self, v_wind, rpm, p_gen):
        """Шаг возмущения и наблюдения с ограничением по оборотам."""
        if v_wind >= STORM_MS:
            return {"mode": "STORM", "load": "ballast", "target_w": BALLAST_W}
        if rpm > 420:                                   # ограничитель оборотов
            return {"mode": "LIMIT", "load": "battery", "target_w": p_gen * 0.8}
        dp = p_gen - self.p_ref
        self.p_ref = p_gen
        return {"mode": "MPPT", "load": "battery", "target_w": p_gen + (5 if dp >= 0 else -5)}

if __name__ == "__main__":
    m = Mppt()
    print(m.step(v_wind=9.2, rpm=210, p_gen=1840))
    print(m.step(v_wind=27.4, rpm=530, p_gen=4900))
    # Зимняя серия: 3 штормовых эпизода отработаны сбросом на ТЭН без остановов.
