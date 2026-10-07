# ТРАНСПОРТНЫЙ КАРКАС: пересадочный тариф "90 минут"

BASE_FARE = 40.0        # руб.
TRANSFER_DISCOUNT = 0.5  # вторая поездка в окне
WINDOW_MIN = 90

def fare(trips, window_min=WINDOW_MIN):
    """trips: отсортированные времена поездок в минутах от первой."""
    total = 0.0
    window_start = None
    for t in trips:
        if window_start is None or t - window_start > window_min:
            total += BASE_FARE
            window_start = t
        else:
            total += BASE_FARE * (1 - TRANSFER_DISCOUNT)
    return round(total, 2)

if __name__ == "__main__":
    print("одна поездка:", fare([0]))
    print("две в окне 90 мин:", fare([0, 35]))
    print("две вне окна:", fare([0, 120]))
    assert fare([0, 35]) == 60.0 and fare([0, 120]) == 80.0
    # Пилот: +9 % поездок на жителя за 4 месяца пересадочного тарифа.
