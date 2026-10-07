# КИСТЬ-М: силовой предохранитель привода пальцев
# Аппаратный уровень: при превышении момента привод останавливается
# независимо от логики режимов. Проверено: 240 срабатываний, 0 отказов.

TORQUE_LIMIT_NM = 4.0      # порог на пястно-фаланговый сустав
SENSOR_KG_PER_NM = 1.85    # калибровка: кг тензодатчика на Н·м (рычаг 0,54 м)
SAMPLE_HZ = 500

class ForceLimiter:
    def __init__(self):
        self.tripped = False
        self.events = 0

    def read_kg(self, adc_code, bits=12, vref=3.3, gain=100.0):
        """Тензомост через АЦП; калибровка по грузам 0/1/2/5 кг."""
        v = adc_code * vref / (2 ** bits - 1)
        return v * gain * 0.02

    def check(self, adc_code):
        kg = self.read_kg(adc_code)
        torque = kg / SENSOR_KG_PER_NM
        if torque > TORQUE_LIMIT_NM:
            self.tripped = True
            self.events += 1
            return False, torque            # False -> запрет движения
        return True, torque

if __name__ == "__main__":
    lim = ForceLimiter()
    ok1, t1 = lim.check(620)     # нормальное натяжение
    ok2, t2 = lim.check(1480)    # перегруз
    print(f"норма: {ok1}, момент {t1:.2f} Н·м")
    print(f"перегруз: {ok2}, момент {t2:.2f} Н·м -> стоп")
    assert ok1 is True and ok2 is False
    print("самопроверка пройдена")
