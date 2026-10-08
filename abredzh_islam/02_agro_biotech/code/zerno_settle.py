# ЗЕРНОВОЙ ПАСПОРТ: взаиморасчёты по данным паспорта партии
# Паспорт — первичный документ между хозяйством, перевозчиком и приёмщиком.

def settling_price(base_price, passport):
    """Корректировки цены: премия за класс, вычеты за влажность и примесь."""
    price = base_price
    if passport["протеин"] >= 13.5:
        price += 450                        # премия за высокопротеиновую, руб./т
    if passport["влажность"] > 14.0:
        price -= 120 * (passport["влажность"] - 14.0)   # вычет на сушку
    if passport["примесь"] > 2.0:
        price -= 200 * (passport["примесь"] - 2.0)
    return round(price, 0)

def settlement(passport, base_price, carrier_rate_t):
    price = settling_price(base_price, passport)
    total = price * passport["масса_т"]
    carrier = carrier_rate_t * passport["масса_т"]
    return {"партия": passport["партия"],
            "цена_руб_т": price,
            "итого_хозяйство_руб": round(total - carrier, 0),
            "перевозчик_руб": round(carrier, 0),
            "основание": "цифровой паспорт партии"}

if __name__ == "__main__":
    wet = {"партия": "ВЕС-2-К-114", "масса_т": 32.4, "влажность": 16.8,
           "протеин": 12.9, "примесь": 1.2}
    dry = {"партия": "ВЕС-2-К-201", "масса_т": 41.0, "влажность": 12.9,
           "протеин": 14.2, "примесь": 0.6}
    print("влажная:", settlement(wet, base_price=13000, carrier_rate_t=350))
    print("классная:", settlement(dry, base_price=13000, carrier_rate_t=350))
    # Споры о влажности и примеси решаются данными паспорта, а не переговорами.
