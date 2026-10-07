# КУБАНЬ-УРОЖАЙ: грейдинг принятых партий в качественные лоты
# Правила пшеницы: протеин >= 13,5 -> лот А (мелькомбинат, премия),
# 12,0-13,4 -> лот Б, < 12,0 -> лот В (фураж/смесь).

def grade(protein, moisture, gluten):
    if moisture > 13.5:
        raise ValueError("партия требует сушки перед грейдингом")
    if protein >= 13.5 and gluten >= 23:
        return "А"
    if protein >= 12.0:
        return "Б"
    return "В"

def make_lots(deliveries):
    lots = {}
    for d in deliveries:
        lot = grade(d["protein"], d["moisture"], d["gluten"])
        rec = lots.setdefault(lot, {"т": 0.0, "хозяйств": 0})
        rec["т"] += d["т"]
        rec["хозяйств"] += 1
    return lots

if __name__ == "__main__":
    deliveries = [
        {"хозяйство": "КФХ-1", "т": 85, "protein": 14.1, "moisture": 12.8, "gluten": 26},
        {"хозяйство": "КФХ-2", "т": 210, "protein": 13.6, "moisture": 13.1, "gluten": 24},
        {"хозяйство": "ООО-3", "т": 190, "protein": 12.4, "moisture": 13.3, "gluten": 21},
        {"хозяйство": "КФХ-4", "т": 60, "protein": 11.8, "moisture": 12.9, "gluten": 19},
    ]
    lots = make_lots(deliveries)
    for lot, r in sorted(lots.items()):
        print(f"лот {lot}: {r['т']:.0f} т от {r['хозяйств']} хоз.")
    # Пилот: 1 200 т рассортированы в 3 лота; реализация +1 850 руб./т к цене "с колёс".
