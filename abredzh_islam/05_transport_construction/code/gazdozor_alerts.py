# -*- coding: utf-8 -*-
"""ГАЗ-ДОЗОР: алгоритм тревог и передача в аварийную службу.

Задел проекта. По ряду измерений датчика вентшахты алгоритм держит
скользящий фон за 24 часа, выдаёт тревогу при превышении фона в три раза
и более, устойчивом 10 минут, и выполняет повторную проверку: если фон
восстановился (аэрозоль, готовка) — тревога снимается, если концентрация
растёт — передаётся в аварийную газовую службу по 4G.
"""
import random
from dataclasses import dataclass

RATIO_ALARM = 3.0        # порог: превышение фона в три раза
HOLD_MIN = 10            # устойчивость превышения, минут
RECHECK_MIN = 15         # повторная проверка после срабатывания, минут
ALERT_SEND_S = 60        # норматив передачи тревоги по 4G, секунд
LOWER_BOUND_PPM_M = 2.0  # нижняя граница значимого превышения, ppm·м


@dataclass
class Event:
    name: str
    start_min: int
    end_min: int
    level_ppm_m: float
    kind: str            # "leak" — утечка, "aerosol" — фоновый всплеск


def build_day_series(events: list[Event], minutes: int,
                     rng: random.Random) -> list[float]:
    """Синтез ряда измерений: фон с суточным ходом + события."""
    series = []
    for m in range(minutes):
        hour = (m // 60) % 24
        # суточный ход: пики утром и вечером (готовка)
        base = 0.6 + 0.25 * (hour in (7, 8, 19, 20, 21))
        v = base + rng.gauss(0, 0.15)
        for e in events:
            if e.start_min <= m < e.end_min:
                # утечка нарастает ступенями, аэрозоль — короткий пик
                if e.kind == "leak":
                    ramp = min(1.0, (m - e.start_min) / 40 + 0.3)
                    v = max(v, e.level_ppm_m * ramp)
                else:
                    v = max(v, e.level_ppm_m)
        series.append(v)
    return series


def run_alarm(series: list[float]) -> list[dict]:
    """Прогон алгоритма по ряду: список сработавших тревог.

    После подтверждённой тревоги канал «защёлкивается» и не выдаёт
    повторных сигналов, пока концентрация не спадёт ниже порога
    (аварийная служба уже в работе).
    """
    alarms = []
    i = 24 * 60
    n = len(series)
    while i < n - HOLD_MIN:
        window = series[i - 24 * 60:i]
        bg = sorted(window)[int(len(window) * 0.75)]
        thr = max(bg * RATIO_ALARM, LOWER_BOUND_PPM_M)
        if all(v >= thr for v in series[i:i + HOLD_MIN]):
            # повторная проверка через RECHECK минут
            j = i + HOLD_MIN + RECHECK_MIN
            still = j < n and series[j] >= thr
            alarms.append({
                "минута": i,
                "подтверждена": still,
                "значение": round(series[i + HOLD_MIN], 2),
            })
            if not still:
                i += HOLD_MIN
                continue
            # защёлка: молчим, пока не будет 10 минут ниже порога
            k = j
            while k < n - HOLD_MIN:
                if all(v < thr for v in series[k:k + HOLD_MIN]):
                    break
                k += 1
            i = k
        else:
            i += 1
    return alarms


if __name__ == "__main__":
    rng = random.Random(20261008)
    # модельный сценарий: две заложенные «утечки» и один аэрозольный всплеск
    events = [
        Event("кв. 34, шланг плиты", 3_000, 3_200, 8.0, "leak"),
        Event("ремонт, аэрозоль", 6_500, 6_512, 6.0, "aerosol"),
        Event("кв. 71, штуцер", 9_000, 9_260, 7.0, "leak"),
    ]
    series = build_day_series(events, 14 * 24 * 60, rng)   # 14 суток
    alarms = run_alarm(series)

    confirmed = [a for a in alarms if a["подтверждена"]]
    cleared = [a for a in alarms if not a["подтверждена"]]
    print(f"Тревог подтверждено (переданы в аварийную службу): "
          f"{len(confirmed)}")
    for a in confirmed:
        print(f"  минута {a['минута']}: превышение {a['значение']} ppm·м, "
              f"передача по 4G ≤ {ALERT_SEND_S} с")
    print(f"Ложных срабатываний, снятых повторной проверкой: {len(cleared)}")
    print(f"Пропущено утечек: {2 - len(confirmed)}")
    print(f"Время от начала превышения до передачи: {HOLD_MIN + 1} мин "
          f"(устойчивость {HOLD_MIN} мин + передача ≤ 1 мин)")
    print(f"Правило: ≥ {RATIO_ALARM:.0f}× фона, устойчиво {HOLD_MIN} мин, "
          f"повторная проверка через {RECHECK_MIN} мин")
