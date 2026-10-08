# -*- coding: utf-8 -*-
"""РИТМ-КАДРЫ: регламенты реакции и кадровые КПЭ подразделения.

Задел проекта. Индекс состояния сотрудника входит в управленческий
контур: реакция старшей медсестры, корректировка плана смен,
КПЭ подразделения для контракта.
"""
from dataclasses import dataclass

REACTIONS = {
    "зелёный": "работа по графику",
    "жёлтый": "наблюдение, контроль на следующей смене",
    "красный": "перераспределение нагрузки, отдых, направление к психологу",
}


@dataclass
class UnitDay:
    red_share: float          # доля «красных» индексов за день
    overtime_hours: float     # сверхурочные по табелю
    coverage: float           # доля прошедших тест


def unit_kpi(day: UnitDay) -> dict:
    """КПЭ дня для отчётности по контракту."""
    return {
        "охват_тестом": day.coverage,
        "доля_красных": day.red_share,
        "сверхурочные_часы": day.overtime_hours,
        "цель_красных": "< 0,05",
    }


def shift_plan_adjustment(red_share: float, plan_hours: float) -> float:
    """Корректировка плановой нагрузки при высокой доле «красных»."""
    if red_share >= 0.15:
        return plan_hours * 0.85          # снижение нагрузки на 15 %
    if red_share >= 0.05:
        return plan_hours * 0.95
    return plan_hours


def ministry_report(month_days: list[UnitDay]) -> dict:
    reds = [d.red_share for d in month_days]
    overtime = [d.overtime_hours for d in month_days]
    return {
        "средняя_доля_красных_за_месяц": round(sum(reds) / max(len(reds), 1), 3),
        "сверхурочные_всего_часов": round(sum(overtime), 1),
        "рекомендация": "включить индекс в кадровые КПЭ подразделения",
    }
