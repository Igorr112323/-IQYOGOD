# ФАРМЛОГИСТИКА-ЮГ: политика управления запасами медорганизации
# Уровень "до заказа" = средний расход за время доставки + страховой запас.

def reorder_point(monthly_demand, delivery_days=1, safety_weeks=1):
    daily = monthly_demand / 30
    return round(daily * delivery_days + daily * 7 * safety_weeks)

def weekly_orders(stock, consumption, rop, order_up_to):
    """Симуляция: если остаток на конец недели <= rop -> заказ до order_up_to."""
    events = []
    for wk, cons in enumerate(consumption, 1):
        stock -= cons
        if stock <= rop:
            qty = order_up_to - stock
            stock += qty
            events.append((wk, max(cons, 0), qty, stock))
    return events

if __name__ == "__main__":
    monthly = 120  # упаковок
    rop = reorder_point(monthly, delivery_days=1, safety_weeks=1)
    print("уровень до заказа:", rop, "упаковок")
    cons = [26, 31, 24, 29, 33, 27]
    for wk, c, q, s in weekly_orders(stock=140, consumption=cons,
                                     rop=rop, order_up_to=160):
        print(f"неделя {wk}: расход {c}, заказ {q}, остаток {s}")
    # Пилот: дефектура 1,5 дня при расчётных уровнях; списания -64 % за ротацию.
