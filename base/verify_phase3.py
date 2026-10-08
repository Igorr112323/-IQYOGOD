#!/usr/bin/env python3
# Верификация фазы 3: комплектность, каноны, самооценка, окупаемость.
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUTHORS = ["andrey_chudikov", "maksim_klimov", "ilya_novikov",
           "drug_ilya_novikova", "abredzh_islam"]
NOMS = ["01_robotics_it", "02_agro_biotech", "03_healthcare",
        "04_ecology_energy", "05_transport_construction"]
# 8 папок фазы 2 — не тронуты (другой формат самооценки, проверка только канонов)
UNTOUCHED = {("andrey_chudikov", "02_agro_biotech"), ("andrey_chudikov", "04_ecology_energy"),
             ("andrey_chudikov", "05_transport_construction"), ("maksim_klimov", "04_ecology_energy"),
             ("ilya_novikov", "01_robotics_it"), ("ilya_novikov", "02_agro_biotech"),
             ("ilya_novikov", "04_ecology_energy"), ("abredzh_islam", "04_ecology_energy")}
errors, warnings = [], []

for a in AUTHORS:
    for n in NOMS:
        d = os.path.join(ROOT, a, n)
        app = os.path.join(d, "application.md")
        if not os.path.isfile(app):
            errors.append(f"{a}/{n}: нет application.md"); continue
        text = open(app, encoding="utf-8").read()
        # каноны — во всех 25
        if "Богус Азамат Эдуардович" not in text:
            errors.append(f"{a}/{n}: нет консультанта Богуса")
        if "Шершнев Игорь Андреевич" not in text:
            errors.append(f"{a}/{n}: нет члена группы Шершнева")
        if (a, n) in UNTOUCHED:
            continue
        # самооценка — только 17 переписанных
        m = re.search(r"\*\*ИТОГО\*\*\s*\|\s*\*\*(\d+)\*\*", text)
        if not m or m.group(1) != "23":
            errors.append(f"{a}/{n}: ИТОГО != 23 ({m.group(1) if m else 'не найдено'})")
        if re.search(r"Эффективность внедрения \| 3", text) is None:
            errors.append(f"{a}/{n}: 8.4 != 3")
        # окупаемость < 2 лет
        pay = re.findall(r"[Оо]купаемость[^0-9]*?(\d+[,\.]?\d*)\s*мес", text)
        if pay:
            vals = [float(p.replace(",", ".")) for p in pay]
            if max(vals) >= 24:
                errors.append(f"{a}/{n}: окупаемость {max(vals)} мес >= 24")
        else:
            warnings.append(f"{a}/{n}: слово «окупаемость … мес» не найдено в заявке")
        # комплект файлов
        need = ["README.md", "docs/протокол_испытаний.md"]
        for f in need:
            if not os.path.isfile(os.path.join(d, f)):
                errors.append(f"{a}/{n}: нет {f}")
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
print("Все проверки пройдены: ИТОГО=23 и 8.4=3 в 17 переписанных заявках, "
      "Богус и Шершнев — во всех 25, окупаемость < 2 лет, комплекты целы.")
