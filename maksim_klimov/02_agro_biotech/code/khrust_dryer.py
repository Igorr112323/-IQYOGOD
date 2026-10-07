# КУБАНЬ-ХРУСТ: контроллер гибридной ИК-конвективной сушки (фрагмент рабочего кода)
# Логика: ИК-фаза до 60 % потери массы, затем конвективная доводка до влажности <= 6 %.

import time

IR_POWER = 2400.0        # Вт, суммарная мощность карбоновых ламп
SURF_T_LIMIT = 78.0      # °С, максимум температуры поверхности долек
HUM_TARGET = 6.0         # %, целевая остаточная влажность

class DryerState:
    def __init__(self, batch_kg):
        self.batch_kg = batch_kg
        self.mass = batch_kg
        self.phase = "IR"

def ir_phase_step(state, surface_t):
    """ИК-предсушка: снимаем до 40 % исходной массы за ~40 минут."""
    loss_pct = 100 * (state.batch_kg - state.mass) / state.batch_kg
    if surface_t > SURF_T_LIMIT:
        power = IR_POWER * 0.6          # щадящий режим против подгорания
    else:
        power = IR_POWER
    if loss_pct >= 40.0:
        state.phase = "CONV"
    return power

def conv_phase_step(state, humidity_pct):
    """Конвективная доводка с рекуперацией."""
    if humidity_pct <= HUM_TARGET:
        state.phase = "DONE"
        return 0.0
    return 1800.0 if humidity_pct > 12.0 else 1200.0

def simulate(batch_kg=20.0, steps=100):
    st = DryerState(batch_kg)
    log = []
    for i in range(steps):
        if st.phase == "IR":
            p = ir_phase_step(st, surface_t=70 + i * 0.05)
            st.mass -= 0.18                       # упрощённая кинетика
        elif st.phase == "CONV":
            hum = 100 * (st.mass / batch_kg - 0.15) / 0.85
            p = conv_phase_step(st, hum)
            st.mass -= 0.05
        else:
            break
        log.append((i, st.phase, round(st.mass, 2), p))
    return log

if __name__ == "__main__":
    log = simulate()
    print("фаза завершена:", log[-1][1], "; финальная масса:", log[-1][2], "кг")
    # По замерам цеха: 1,9 кВт·ч/кг готового продукта (протокол испытаний).
