# ТРАНСПОРТНЫЙ КАРКАС: клиринг выручки между перевозчиками
# Распределение по фактически перевезённым пассажирам минус сбор оператора.

PROCESSING_FEE = 0.032

def clear(day_transactions):
    """day_transactions: [{перевозчик, пассажиров, тариф}]."""
    gross = sum(t["пассажиров"] * t["тариф"] for t in day_transactions)
    fee = gross * PROCESSING_FEE
    net = gross - fee
    shares = {}
    for t in day_transactions:
        v = t["пассажиров"] * t["тариф"]
        shares[t["перевозчик"]] = shares.get(t["перевозчик"], 0) + v / gross * net
    return {"оборот": round(gross, 2), "сбор оператора": round(fee, 2),
            "к выплате перевозчикам": {k: round(v, 2) for k, v in shares.items()}}

if __name__ == "__main__":
    day = [
        {"перевозчик": "МУП ПАТП", "пассажиров": 21400, "тариф": 40},
        {"перевозчик": "ИП-группа А", "пассажиров": 13600, "тариф": 40},
        {"перевозчик": "ООО Транслайн", "пассажиров": 27000, "тариф": 40},
    ]
    rep = clear(day)
    for k, v in rep.items():
        print(k, v)
    # Пилот: безнал 31 -> 78 %, сборы +17 %, льготные - по фактическим поездкам.
