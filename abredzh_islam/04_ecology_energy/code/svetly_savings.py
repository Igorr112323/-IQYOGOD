# СВЕТЛЫЙ РАЙОН: калькулятор экономии энергосервисного контракта

HOURS_YEAR = 4100  # часов горения в год (референс-поселение)

def annual_saving(points, old_w, new_w, dimming_factor, tariff):
    """dimming_factor: доля средней мощности с учётом ночного диммирования."""
    kwh_old = points * old_w * HOURS_YEAR / 1000
    kwh_new = points * new_w * dimming_factor * HOURS_YEAR / 1000
    rub = (kwh_old - kwh_new) * tariff
    return {"кВт·ч было": round(kwh_old), "кВт·ч стало": round(kwh_new),
            "экономия, руб/год": round(rub)}

def payback(contract_value, saving_rub, share=0.9):
    return round(contract_value / (saving_rub * share), 1)

if __name__ == "__main__":
    r = annual_saving(points=412, old_w=205, new_w=78,
                      dimming_factor=0.82, tariff=6.4)
    print(r)
    print("окупаемость контракта 3,4 млн руб.:",
          payback(3_400_000, r["экономия, руб/год"]), "лет")
    # Модель (референс-поселение): -68 % потребления, освещённость 4,1 -> 9,3 лк по ГОСТ Р 55706-2013.
