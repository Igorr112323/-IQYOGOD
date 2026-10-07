# КУБАНЬ-ХРУСТ: генератор QR-паспортов партий («история от сада»)
# Каждая пачка получает уникальный код партии и ссылку на страницу прослеживания.

import hashlib
import json

def party_id(garden, fruit, harvest_date, batch_no):
    raw = f"{garden}|{fruit}|{harvest_date}|{batch_no}"
    return "KH-" + hashlib.sha1(raw.encode()).hexdigest()[:10].upper()

def passport(garden, fruit, harvest_date, batch_no, dry_mode, ir_time_min,
             final_humidity, pack_date):
    pid = party_id(garden, fruit, harvest_date, batch_no)
    data = {
        "партия": pid,
        "сад": garden,
        "фрукт": fruit,
        "сбор": harvest_date,
        "режим": dry_mode,
        "ИК-фаза, мин": ir_time_min,
        "влажность_готового, %": final_humidity,
        "упаковано": pack_date,
        "страница": f"https://kuban-hrust.example/trace/{pid}",
    }
    return data

if __name__ == "__main__":
    p = passport("ООО «Сады Крымска», квартал 14", "яблоко «Гренни Смит», некондиция",
                 "2026-08-28", "042", "гибридная ИК+конвекция", 42, 5.6, "2026-09-01")
    print(json.dumps(p, ensure_ascii=False, indent=2))
    # Реестр партий хранится в таблице диспетчерской цеха и отдаётся по ссылке из QR.
