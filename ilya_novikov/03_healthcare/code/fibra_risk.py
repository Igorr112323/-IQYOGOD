# -*- coding: utf-8 -*-
"""ФИБРА-СТОПА: предиктивный алгоритм трофического риска.

Задел проекта. Критерии: разность температур стоп ΔT > 2,2 °C
и/или пиковое давление > 450 кПа в динамике 3 измерений подряд.
"""
from dataclasses import dataclass, field

DT_THRESHOLD_C = 2.2
PRESSURE_THRESHOLD_KPA = 450.0
TREND_LEN = 3


@dataclass
class PatientDailyFrame:
    day: int
    pressure_kpa: list[float]
    temperature_c: list[float]          # средняя по стельке
    contralateral_temp_c: float         # температура парной стопы


@dataclass
class RiskState:
    frames: list[PatientDailyFrame] = field(default_factory=list)

    def delta_t(self) -> float:
        f = self.frames[-1]
        return abs(f.temperature_c and sum(f.temperature_c) / len(f.temperature_c)
                   - f.contralateral_temp_c)

    def pressure_over(self) -> bool:
        return any(p > PRESSURE_THRESHOLD_KPA for p in self.frames[-1].pressure_kpa)

    def evaluate(self) -> dict:
        """Наряд формируется при тренде из 3 измерений."""
        if len(self.frames) < TREND_LEN:
            return {"риск": "данных недостаточно", "наряд": False}
        dt_growing = all(self.frames[i].contralateral_temp_c is not None
                         for i in range(-TREND_LEN, 0))
        dt_last = [abs(sum(f.temperature_c) / len(f.temperature_c) - f.contralateral_temp_c)
                   for f in self.frames[-TREND_LEN:]]
        dt_flag = dt_last[-1] > DT_THRESHOLD_C and dt_last[-1] >= dt_last[0]
        p_flag = all(any(p > PRESSURE_THRESHOLD_KPA for p in f.pressure_kpa)
                     for f in self.frames[-TREND_LEN:])
        zone = max(range(len(self.frames[-1].pressure_kpa)),
                   key=lambda i: self.frames[-1].pressure_kpa[i])
        risk = bool(dt_flag or p_flag)
        return {
            "риск": "высокий" if risk else "норма",
            "наряд": risk,
            "зона": zone + 1,
            "dT": round(dt_last[-1], 2),
        }
