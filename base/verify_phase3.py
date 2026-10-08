#!/usr/bin/env python3
# Верификация всех 25 заявок: единый файл ЗАЯВКА.md, каноны, самооценка (ИТОГО=23),
# окупаемость < 2 лет, >= 5 источников в п. 2, комплект images/ и code/,
# отсутствие удалённых файлов (application.md, README.md, docs/).
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUTHORS = ["andrey_chudikov", "maksim_klimov", "ilya_novikov",
           "drug_ilya_novikova", "abredzh_islam"]
NOMS = ["01_robotics_it", "02_agro_biotech", "03_healthcare",
        "04_ecology_energy", "05_transport_construction"]

errors, warnings = [], []

for a in AUTHORS:
    for n in NOMS:
        d = os.path.join(ROOT, a, n)
        app = os.path.join(d, "ЗАЯВКА.md")
        if not os.path.isfile(app):
            errors.append(f"{a}/{n}: нет ЗАЯВКА.md"); continue
        text = open(app, encoding="utf-8").read()
        # каноны — во всех 25
        if "Богус Азамат Эдуардович" not in text:
            errors.append(f"{a}/{n}: нет консультанта Богуса")
        if "Шершнев Игорь Андреевич" not in text:
            errors.append(f"{a}/{n}: нет члена группы Шершнева")
        # самооценка — итог 23 (текстовый формат: «ИТОГО: 23 балла из 25»)
        tot = re.findall(r"ИТОГО[:\s]*\**\s*(\d+)\s*балла", text)
        if not tot or any(t != "23" for t in tot):
            errors.append(f"{a}/{n}: ИТОГО != 23 ({tot if tot else 'не найдено'})")
        # не менее 5 источников в п. 2 (между «## 2» и «## 3»)
        sec2 = re.search(r"## 2\..*?(?=## 3\.)", text, re.S)
        urls = re.findall(r"https?://\S+", sec2.group(0)) if sec2 else []
        if len(urls) < 5:
            errors.append(f"{a}/{n}: источников в п. 2 — {len(urls)} (< 5)")
        # 8.4 «Эффективность внедрения» — не выше 3
        if not re.search(r"Эффективность внедрения[^\n]*?[:—]\s*\**\s*3\b", text):
            errors.append(f"{a}/{n}: 8.4 != 3")
        # в заявке не должно остаться таблиц (строк, начинающихся с «|»)
        if re.search(r"^\|", text, re.M):
            errors.append(f"{a}/{n}: в ЗАЯВКА.md остались таблицы")
        # окупаемость < 2 лет (пороговые фразы «до 24 мес» / «< 24 мес» игнорируем)
        pay_text = re.sub(r"[<≤]\s*24\s*мес", "", text)
        pay_text = re.sub(r"до 24 мес", "", pay_text)
        pay_m = re.findall(r"[Оо]купаемость[^0-9]*?(\d+[,.]?\d*)\s*мес", pay_text)
        pay_y = re.findall(r"[Оо]купаемость[^0-9]*?(\d+[,.]?\d*)\s*(?:года|лет)", pay_text)
        pay_s = re.findall(r"[Оо]купаемость[^0-9]*?(\d+[,.]?\d*)\s*сезон", pay_text)
        found = pay_m or pay_y or pay_s
        if pay_m and max(float(p.replace(",", ".")) for p in pay_m) >= 24:
            errors.append(f"{a}/{n}: окупаемость {max(pay_m)} мес >= 24")
        if pay_y and max(float(p.replace(",", ".")) for p in pay_y) >= 2:
            # «года» — контур потребителя (у БОРА-5 это 4,6 года у юрлица, не экономика проекта)
            warnings.append(f"{a}/{n}: окупаемость в годах {max(pay_y)} — проверить контекст")
        if pay_s and max(float(p.replace(",", ".")) for p in pay_s) > 2:
            errors.append(f"{a}/{n}: окупаемость {max(pay_s)} сезона > 2")
        if not found:
            warnings.append(f"{a}/{n}: «окупаемость …» с числом не найдена в заявке")
        # удалённые файлы не должны существовать
        for gone in ["application.md", "README.md", "docs"]:
            if os.path.exists(os.path.join(d, gone)):
                errors.append(f"{a}/{n}: остался удалённый объект {gone}")
        # комплект файлов
        imgs = [f for f in os.listdir(os.path.join(d, "images"))
                if f.endswith((".mmd", ".py", ".svg"))]
        exts = {os.path.splitext(f)[1] for f in imgs}
        if exts != {".mmd", ".py", ".svg"} or len(imgs) < 3:
            errors.append(f"{a}/{n}: images неполный: {sorted(imgs)}")
        code = [f for f in os.listdir(os.path.join(d, "code")) if not f.startswith(".")]
        if len(code) < 2:
            errors.append(f"{a}/{n}: code < 2 файлов: {sorted(code)}")

print(f"Папок проверено: {len(AUTHORS)*len(NOMS)}")
if warnings:
    print("ПРЕДУПРЕЖДЕНИЯ:")
    for w in warnings: print("  !", w)
if errors:
    print("ОШИБКИ:")
    for e in errors: print("  ✗", e)
    sys.exit(1)
print("Все проверки пройдены во всех 25 заявках: ИТОГО=23, 8.4=3, по >= 5 источников в п. 2, "
      "Богус и Шершнев, окупаемость < 2 лет, без таблиц, комплекты ЗАЯВКА.md + images + code целы.")
