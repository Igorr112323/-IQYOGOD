# -*- coding: utf-8 -*-
"""Генератор ЗАЯВКА.md для всех 25 папок.
Собирает: тексты разделов 1–11 из application.md (дословно), номинацию,
данные автора из шапки, mermaid/svg/код в п. 3 и 5, таблицы протокола в п. 9,
фактический вывод экономического скрипта в п. 11, самооценку и блок подписей.
"""
import glob
import os
import re
import subprocess
import sys

ROOT = "/home/user/-IQYOGOD"

NOMS = {
    "01_robotics_it": "«Лучший инновационный проект в сфере робототехники, компьютерных технологий и телекоммуникаций»",
    "02_agro_biotech": "«Лучший инновационный проект в сфере агропромышленного комплекса, биотехнологий и пищевой промышленности»",
    "03_healthcare": "«Лучший инновационный проект в сфере здравоохранения, биомедицины, фармацевтики»",
    "04_ecology_energy": "«Лучший инновационный проект в сфере охраны окружающей среды, энергосбережения и альтернативных источников энергии»",
    "05_transport_construction": "«Лучший инновационный проект в сфере транспорта, строительства и жилищно-коммунального хозяйства»",
}

HEAD = {
    1: "1. НАИМЕНОВАНИЕ ПРОЕКТА",
    2: "2. ОБОСНОВАНИЕ АКТУАЛЬНОСТИ ПРОЕКТА",
    3: "3. ИННОВАЦИОННАЯ СОСТАВЛЯЮЩАЯ ПРОЕКТА",
    4: "4. ЦЕЛИ ПРОЕКТА И ОСНОВНЫЕ ЗАДАЧИ",
    5: "5. ОСНОВНОЕ СОДЕРЖАНИЕ (КОНЦЕПЦИЯ, МЕТОДИКА, ТЕХНОЛОГИИ)",
    6: "6. ОСНОВНЫЕ ЭТАПЫ И СРОКИ РЕАЛИЗАЦИИ",
    7: "7. МЕСТО РЕАЛИЗАЦИИ ПРОЕКТА",
    8: "8. МЕХАНИЗМ РЕАЛИЗАЦИИ И КАДРОВОЕ ОБЕСПЕЧЕНИЕ",
    9: "9. РЕЗУЛЬТАТЫ, ДОСТИГНУТЫЕ К НАСТОЯЩЕМУ ВРЕМЕНИ",
    10: "10. ИНФОРМАЦИЯ О СОБСТВЕННЫХ РЕСУРСАХ",
    11: "11. ПРЕДПОЛАГАЕМЫЕ КОНЕЧНЫЕ РЕЗУЛЬТАТЫ, ЭКОНОМИКА",
}


def parse_app(text):
    """Возвращает (поля шапки {номер: значение}, {номер секции: текст}, самооценка, приложения)."""
    fields = {}
    for m in re.finditer(r"^\|\s*(\d+)\s*\|[^|]*\|\s*(.*?)\s*\|\s*$", text, re.M):
        fields.setdefault(int(m.group(1)), m.group(2))
    sections = {}
    marks = [(m.start(), int(m.group(1))) for m in re.finditer(r"^## (\d+)\. ", text, re.M)]
    other = re.search(r"^## Самооценка", text, re.M)
    end_all = other.start() if other else len(text)
    for i, (pos, num) in enumerate(marks):
        nxt = marks[i + 1][0] if i + 1 < len(marks) else end_all
        body = text[pos:nxt]
        body = re.sub(r"^## \d+\. [^\n]*\n", "", body, count=1)  # убрать старый заголовок секции
        sections[num] = body.strip()
    selfev = ""
    if other:
        pril = re.search(r"^## Приложения", text, re.M)
        selfev = text[other.start():pril.start() if pril else len(text)].strip()
        selfev = re.sub(r"^## Самооценка[^\n]*\n", "", selfev, count=1).strip()
    pril_text = ""
    pril = re.search(r"^## Приложения", text, re.M)
    if pril:
        pril_text = text[pril.start():].strip()
        pril_text = re.sub(r"^## Приложения[^\n]*\n", "", pril_text, count=1).strip()
    return fields, sections, selfev, pril_text


def code_block(path, lang, limit=150):
    rel = os.path.relpath(path, ROOT)
    src = open(path, encoding="utf-8").read()
    lines = src.splitlines()
    cut = len(lines) > limit
    body = "\n".join(lines[:limit])
    note = f"\n… (полный файл — {len(lines)} строк, см. `{rel}`)" if cut else ""
    return f"```{lang}\n{body}\n```{note}"


def extract_tables(proto):
    """Все markdown-таблицы протокола с ближайшим подписным заголовком."""
    lines = proto.splitlines()
    out, i, caption = [], 0, ""
    while i < len(lines):
        ln = lines[i]
        if ln.strip().startswith("|"):
            tbl = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                tbl.append(lines[i])
                i += 1
            if caption:
                if caption.startswith("#"):
                    caption = "**" + caption.lstrip("#").strip() + "**"
                out.append(caption)
            out.extend(tbl)
            out.append("")
            caption = ""
        else:
            if ln.strip().startswith(("**", "#")):
                caption = ln.strip()
            elif not ln.strip():
                pass
            i += 1
    return "\n".join(out).strip()


def run_economics(script):
    r = subprocess.run([sys.executable, script], cwd=ROOT, capture_output=True, text=True, timeout=120)
    return r.returncode, r.stdout.strip(), r.stderr.strip()


total = 0
for folder in sorted(glob.glob(os.path.join(ROOT, "*", "0*"))):
    author = os.path.basename(os.path.dirname(folder))
    nom_dir = os.path.basename(folder)
    if nom_dir not in NOMS:
        continue
    app = open(os.path.join(folder, "application.md"), encoding="utf-8").read()
    fields, sections, selfev, pril_text = parse_app(app)

    mmd = sorted(glob.glob(os.path.join(folder, "images", "*.mmd")))
    svg = sorted(glob.glob(os.path.join(folder, "images", "*.svg")))
    eco = sorted(glob.glob(os.path.join(folder, "images", "*.py")))
    codes = sorted([p for p in glob.glob(os.path.join(folder, "code", "*"))
                    if os.path.isfile(p) and not os.path.basename(p).startswith(".")])
    proto_path = os.path.join(folder, "docs", "протокол_испытаний.md")
    proto = open(proto_path, encoding="utf-8").read() if os.path.isfile(proto_path) else ""

    out = []
    out.append("# ЗАЯВКА НА УЧАСТИЕ В ГУБЕРНАТОРСКОМ КОНКУРСЕ «ПРЕМИЯ IQ ГОДА»")
    out.append("")
    out.append("## НОМИНАЦИЯ")
    out.append("")
    out.append(NOMS[nom_dir])
    out.append("")
    out.append("## ДАННЫЕ АВТОРА")
    out.append("")
    out.append(f"- Ф.И.О. автора: {fields.get(8, '[указать при подаче]')}")
    out.append(f"- Дата рождения: {fields.get(7, '[указать при подаче]')}")
    out.append(f"- Телефон: {fields.get(5, '[указать при подаче]')}")
    out.append(f"- E-mail: {fields.get(6, '[указать при подаче]')}")
    out.append(f"- Место регистрации: {fields.get(3, '[указать при подаче]')}")
    out.append(f"- Место фактического проживания: {fields.get(4, '[указать при подаче]')}")
    out.append(f"- Образовательная организация: {fields.get(11, '[указать при подаче]')}")
    out.append(f"- Муниципальное образование: {fields.get(13, '[указать при подаче]')}")
    out.append(f"- Консультант проекта: {fields.get(9, 'Богус Азамат Эдуардович').replace('**', '')}")
    out.append(f"- Член проектной группы: {fields.get(10, 'Шершнев Игорь Андреевич').replace('**', '')}")
    out.append("")
    out.append("---")
    out.append("")

    for num in range(1, 12):
        out.append(f"## {HEAD[num]}")
        out.append("")
        out.append(sections.get(num, "").strip())
        out.append("")
        if num == 3:
            for p in mmd:
                rel = os.path.relpath(p, folder)
                out.append(f"### Схема процесса (источник: `{rel}`)")
                out.append("")
                out.append("```mermaid")
                out.append(open(p, encoding="utf-8").read().strip())
                out.append("```")
                out.append("")
            for p in svg:
                rel = os.path.relpath(p, folder)
                out.append(f"### Схема устройства (источник: `{rel}`)")
                out.append("")
                out.append(f"![Схема]({rel})")
                out.append("")
            if codes:
                rel = os.path.relpath(codes[0], folder)
                ext = os.path.splitext(codes[0])[1].lstrip(".")
                lang = {"py": "python", "ino": "cpp", "scad": "openscad"}.get(ext, ext)
                out.append(f"### Ключевой код задела (источник: `{rel}`)")
                out.append("")
                out.append(code_block(codes[0], lang))
                out.append("")
        if num == 5 and len(codes) > 1:
            for p in codes[1:]:
                rel = os.path.relpath(p, folder)
                ext = os.path.splitext(p)[1].lstrip(".")
                lang = {"py": "python", "ino": "cpp", "scad": "openscad"}.get(ext, ext)
                out.append(f"### Код задела (источник: `{rel}`)")
                out.append("")
                out.append(code_block(p, lang))
                out.append("")
        if num == 9 and proto:
            tables = extract_tables(proto)
            if tables:
                out.append("### Ключевые таблицы протокола испытаний (источник: `docs/протокол_испытаний.md`)")
                out.append("")
                out.append(tables)
                out.append("")
        if num == 11 and eco:
            p = eco[0]
            rel = os.path.relpath(p, folder)
            rc, so, se = run_economics(p)
            out.append(f"### Экономический расчёт — фактический запуск `{rel}` (Монте-Карло)")
            out.append("")
            if rc == 0:
                out.append("```")
                out.append(so)
                out.append("```")
            else:
                out.append(f"Скрипт завершился с ошибкой (код {rc}): `{se}`")
            out.append("")

    out.append("---")
    out.append("")
    out.append("## САМООЦЕНКА ПО КРИТЕРИЯМ")
    out.append("")
    out.append("| Критерий | Балл |")
    out.append("|---|---|")
    out.append("| 8.1. Инновационная составляющая | 5 |")
    out.append("| 8.2. Актуальность | 5 |")
    out.append("| 8.3. Ожидаемый результат | 5 |")
    out.append("| 8.4. Эффективность внедрения | 3 |")
    out.append("| 8.5. Экономическая целесообразность | 5 |")
    out.append("| **ИТОГО** | **23** |")
    out.append("")
    if selfev:
        out.append("Обоснование баллов (из заявки, дословно):")
        out.append("")
        out.append(selfev)
        out.append("")
    out.append("---")
    out.append("")
    out.append("## ПОДПИСИ")
    out.append("")
    out.append("- Подпись автора проекта: __________")
    out.append("- Подпись консультанта проекта: __________")
    out.append("- Дата подачи заявки: __________")
    if pril_text:
        out.append("")
        out.append("---")
        out.append("")
        out.append("## Приложения (задел проекта)")
        out.append("")
        out.append(pril_text)

    dest = os.path.join(folder, "ЗАЯВКА.md")
    open(dest, "w", encoding="utf-8").write("\n".join(out) + "\n")
    total += 1
    print("OK:", os.path.relpath(dest, ROOT))

print("Создано файлов:", total)
