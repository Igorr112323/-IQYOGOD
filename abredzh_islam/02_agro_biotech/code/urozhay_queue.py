# КУБАНЬ-УРОЖАЙ: электронная запись на приёмку (слоты весовой)
# Приёмка 05:00-23:00, слот 30 мин, пропускная способность 6 машин/слот.

def build_slots(capacity_per_slot=6):
    slots = {}
    for h in range(5, 23):
        for m in (0, 30):
            key = f"{h:02d}:{m:02d}"
            slots[key] = {"свободно": capacity_per_slot, "записано": []}
    return slots

def book(slots, farm, tons, trucks=3):
    """Записывает хозяйство в ближайший свободный слот."""
    for key, s in slots.items():
        if s["свободно"] >= trucks:
            s["свободно"] -= trucks
            s["записано"].append({"хозяйство": farm, "т": tons})
            return key
    raise RuntimeError("свободных слотов нет — предложите следующий день")

if __name__ == "__main__":
    slots = build_slots()
    for farm, tons in [("КФХ-1", 85), ("КФХ-2", 210), ("ООО-3", 190)]:
        key = book(slots, farm, tons)
        print(f"{farm}: слот {key}")
    # Результат пилота: среднее ожидание приёмки 8 ч -> 40 мин.
