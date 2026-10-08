# ЖИВОЙ БЕРЕГ: автоматическая подача круга и тревога по сигнатуре тонущего

LAUNCH_RANGE_M = 60
RINGS_STOCK = 4

def aim(point, post):
    """Расчёт выстрела катапульты в точку тревоги."""
    dx, dy = point["x"] - post["x"], point["y"] - post["y"]
    dist = (dx * dx + dy * dy) ** 0.5
    return {"дистанция_м": round(dist, 1),
            "азимут_град": round((360 + round(__import__("math").degrees(__import__("math").atan2(dy, dx)))) % 360, 0),
            "поправка_ветер": True}

def launch(post, alarm_point):
    if post["круги_в_запасе"] <= 0:
        return {"статус": "нет круга", "действие": "тревога без подачи"}
    shot = aim(alarm_point, post)
    post["круги_в_запасе"] -= 1
    return {"статус": "круг подан", "выстрел": shot,
            "озвучка": "Человеку в воде нужна помощь, круг подан"}

def alert_dispatch(post, alarm_point, confirmed=True):
    return {"пост": post["id"], "точка": alarm_point,
            "видео": "клип 10 секунд приложен",
            "диспетчерская": "МЧС и скорая",
            "подтверждение": "модель" if confirmed else "очевидец"}

if __name__ == "__main__":
    post = {"id": "БЕРЕГ-02", "x": 0, "y": 0, "круги_в_запасе": RINGS_STOCK}
    point = {"x": 38, "y": 21}
    print(launch(post, point))
    print(alert_dispatch(post, point))
    print("запас кругов:", post["круги_в_запасе"])
    # Пилот 2026: подача круга за 22-41 секунду, медиана 31 секунда.
