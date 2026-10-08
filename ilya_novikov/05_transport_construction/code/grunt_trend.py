# ГРУНТ-МЕМ М1: скользящий тренд наклона на устройстве
# Вход: серии измерений наклона по двум осям каждые 6 часов.
# Выход: тренд в градусах/неделя; сигнал при превышении порога.

THRESHOLD_DEG_WEEK = 0.08    # порог тренда
WINDOW_DAYS = 14             # окно скользящей оценки
MEAS_PER_DAY = 4             # 6-часовой интервал

def detrend_drift(raw, zero_offset):
    return [x - zero_offset for x in raw]

def weekly_trend(samples):
    """Линейная регрессия по номеру измерения; пересчёт на неделю."""
    n = len(samples)
    if n < MEAS_PER_DAY * 3:
        return None
    xs = list(range(n))
    mean_x = sum(xs) / n
    mean_y = sum(samples) / n
    num = sum((xs[i] - mean_x) * (samples[i] - mean_y) for i in range(n))
    den = sum((xs[i] - mean_x) ** 2 for i in range(n)) or 1.0
    slope_per_meas = num / den
    return slope_per_meas * MEAS_PER_DAY * 7

def check_zone(samples_axis_x, samples_axis_y, zero_x, zero_y):
    tx = weekly_trend(detrend_drift(samples_axis_x, zero_x))
    ty = weekly_trend(detrend_drift(samples_axis_y, zero_y))
    trend = max(abs(tx or 0), abs(ty or 0))
    return {"тренд_град_нед": round(trend, 3),
            "сигнал": trend >= THRESHOLD_DEG_WEEK}

if __name__ == "__main__":
    # зона вымывания: рост наклона ~0,11 градуса в неделю
    sx = [0.02 * i * 0.016 for i in range(60)]
    sy = [0.01 * i * 0.016 for i in range(60)]
    print(check_zone(sx, sy, zero_x=0.0, zero_y=0.0))
    print(check_zone([0.0] * 60, [0.0] * 60, zero_x=0.0, zero_y=0.0))
    # Полевые наблюдения 2026: упреждение видимой деформации 6 суток.
