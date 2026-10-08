# КАРБОКУБАНЬ: логика ПИД-регулирования температуры реактора (фрагмент задела)
# Реализация для контроллера; проверена на макете в феврале–апреле 2026 г.
# Входы: 3 термопары ТХА; выход: мощность нагревателя (рециркуляция газа).

SP = 505.0            # уставка, °С
KP, KI, KD = 2.2, 0.08, 9.0
T_MIN, T_MAX = 440.0, 560.0   # допустимое окно пиролиза лузги
CO_ALARM_PPM = 30.0

class Pid:
    def __init__(self, kp, ki, kd, dt):
        self.kp, self.ki, self.kd, self.dt = kp, ki, kd, dt
        self.integral = 0.0
        self.prev_err = 0.0

    def step(self, err):
        self.integral += err * self.dt
        self.integral = max(-60.0, min(60.0, self.integral))  # anti-windup
        deriv = (err - self.prev_err) / self.dt
        self.prev_err = err
        return self.kp * err + self.ki * self.integral + self.kd * deriv

def control_step(temps, co_ppm, pid, power):
    """temps: три измерения по зонам реактора; возвращает новую мощность 0–100 %."""
    if co_ppm > CO_ALARM_PPM:
        return 0.0, "ALARM_CO"                  # аварийная остановка нагрева
    t = max(temps)
    if not (T_MIN <= t <= T_MAX + 40):
        return 0.0, "OUT_OF_WINDOW"
    err = SP - t
    p = pid.step(err)
    power = max(0.0, min(100.0, power + p * 0.05))
    return power, "OK"

if __name__ == "__main__":
    pid = Pid(KP, KI, KD, dt=1.0)
    power = 60.0
    temps = [480.0, 492.0, 501.0]   # стартовое состояние макета
    for i in range(30):
        power, status = control_step(temps, co_ppm=4.0, pid=pid, power=power)
        t = temps[-1] + (power - 60.0) * 0.15  # упрощённая модель объекта
        temps = [t - 25, t - 10, t]
    print(f"через 30 с: мощность {power:.1f} %, Tmax {temps[-1]:.1f} °С, статус {status}")
