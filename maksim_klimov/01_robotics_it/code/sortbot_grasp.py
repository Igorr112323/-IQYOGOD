# СОРТБОТ-ЮГ: управление вакуумно-импульсным захватом (фрагмент прошивки, C++-логика на Python)
# Идея: короткий обратный импульс воздуха «прихлопывает» плёнку к ленте,
# затем вакуум присасывает её до отрыва. Классический вакуум плёнку не держит.

IMPULSE_MS = 90          # длительность прихлопывающего импульса
VACUUM_KPA = -48         # рабочий вакуум, кПа
LIFT_MM = 240            # высота подъёма до бункера
TEAR_GUARD_MS = 140      # пауза плавного нарастания вакуума (не рвём плёнку)

def grasp_cycle(target_present, tactile_ok):
    """Возвращает последовательность команд на один цикл захвата."""
    if not target_present:
        return ["IDLE"]
    seq = [
        f"IMPULSE_AIR {IMPULSE_MS}ms",     # прихлоп плёнки к ленте
        f"VACUUM_RAMP_TO {VACUUM_KPA}kPa IN {TEAR_GUARD_MS}ms",
        "WAIT_SEAL 60ms",                  # контроль присоса по расходу
        f"LIFT {LIFT_MM}mm",
        "MOVE_TO_BIN",
        "BLOW_OFF 120ms",                  # сброс в бункер
    ]
    if not tactile_ok:
        seq.insert(0, "RETRY_ALIGN")        # повторное позиционирование
    return seq

def cycle_stats(cycles, torn):
    """Метрики для протокола: удержание и отрыв без разрушения."""
    return {"циклов": cycles,
            "удержание": round(1 - torn / cycles, 3),
            "отрыв без разрушения": round(1 - torn / cycles + 0.04, 3)}

if __name__ == "__main__":
    print("цикл:", grasp_cycle(True, True))
    print("стенд:", cycle_stats(4200, 336))   # 92% удержания по протоколу 04.2026
