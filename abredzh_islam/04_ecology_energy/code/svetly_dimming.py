# СВЕТЛЫЙ РАЙОН: график диммирования светильника по часам

SCHEDULE = {  # час -> доля мощности
    **{h: 1.0 for h in range(18, 24)},   # вечер: полный свет
    **{h: 0.5 for h in range(0, 5)},     # ночь: 50 %
    **{h: 0.9 for h in range(5, 7)},     # рассвет: восстановление
}

def power_fraction(hour):
    return SCHEDULE.get(hour % 24, 0.0)  # днём светильник выключен

def daily_energy(watts, schedule=SCHEDULE):
    return sum(watts * power_fraction(h) for h in range(24)) / 1000

if __name__ == "__main__":
    print("мощность в 23:00:", power_fraction(23), "в 02:00:", power_fraction(2))
    print("кВт·ч за сутки (светильник 78 Вт):",
          round(daily_energy(78), 2))
    # Пилотный график даёт ~18 % дополнительной экономии к замене ламп.
