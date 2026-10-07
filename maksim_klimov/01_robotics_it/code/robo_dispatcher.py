# ЮЖНЫЙ РОБОКУРЬЕР: диспетчер заказов (фрагмент рабочего облака)
# Задача: назначить заказ ближайшему свободному роверу с учётом батареи и очереди.

import heapq

BATTERY_LIMIT = 25.0      # %, ниже — ровер уходит на станцию
K_WH_PER_DELIVERY = 0.35  # кВт·ч на среднюю доставку

class Rover:
    def __init__(self, rid, pos, battery, free=True):
        self.rid, self.pos, self.battery, self.free = rid, pos, battery, free

def distance(a, b):
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5

def assign(order, fleet):
    """order: dict(pos_pickup, pos_dropoff). Возвращает ровер или плановую очередь."""
    cand = []
    for r in fleet:
        if not r.free:
            continue
        dist_pick = distance(r.pos, order["pos_pickup"])
        trip = distance(order["pos_pickup"], order["pos_dropoff"])
        if r.battery - (dist_pick + trip) * K_WH_PER_DELIVERY < BATTERY_LIMIT:
            continue
        heapq.heappush(cand, (dist_pick + trip, r.rid))
    if not cand:
        return None  # все заняты/разряжены -> очередь и алерт оператору
    return heapq.heappop(cand)[1]

if __name__ == "__main__":
    fleet = [Rover("R-01", (100, 120), 82), Rover("R-02", (400, 300), 64),
             Rover("R-03", (350, 100), 23)]
    order = {"pos_pickup": (360, 110), "pos_dropoff": (500, 140)}
    rid = assign(order, fleet)
    print("назначен:", rid)
    assert rid == "R-03" or rid == "R-01"  # ближайший с достаточной батареей
