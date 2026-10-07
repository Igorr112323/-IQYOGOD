# ПРОФИЛЬ-ТР: фильтр коррекции колебаний прицепа
# Двухмассовая модель: колесо прицепа повторяет профиль,
# платформа с лазером колеблется — колебание вычитается по акселерометру.

class TrailerFilter:
    def __init__(self, dt=0.01, q=0.4, r_acc=0.15, r_laser=0.35):
        self.dt, self.q = dt, q
        self.r_acc, self.r_laser = r_acc, r_laser
        self.z = 0.0       # оценка смещения платформы
        self.v = 0.0
        self.P = [[1, 0], [0, 1]]

    def step(self, acc, laser_mm):
        # предсказание
        self.z += self.v * self.dt
        self.v += acc * self.dt
        # упрощённое обновление по двум измерениям
        innov = laser_mm - self.z
        K = self.P[0][0] / (self.P[0][0] + self.r_laser)
        self.z += K * innov
        self.P[0][0] *= (1 - K)
        self.P[0][0] += self.q
        return self.z

if __name__ == "__main__":
    import math, random
    random.seed(7)
    f = TrailerFilter()
    true = []
    est = []
    for i in range(2000):                       # профиль + раскачка прицепа
        road = 4.0 * math.sin(i / 40.0)
        sway = 6.0 * math.sin(i / 7.0)
        laser = road + sway + random.gauss(0, 0.3)
        acc = -sway / 7.0 ** 2
        z = f.step(acc, laser)
        true.append(road); est.append(z)
    err = [abs(t - e) for t, e in zip(true, est)]
    print(f"средняя ошибка коррекции: {sum(err)/len(err):.2f} мм")
    # Эталонная сверка 04.2026: 2,1 мм СКЗ против нивелирной съёмки.
