# ЧИСТЫЙ АЗОВ: детектор «сетевых» текстур на аэроснимках мелководий
# Признаки сети на грунте: вытянутые линейные структуры с регулярным шагом.
# Фрагмент рабочей обработки ортофотопланов (контраст + линейные фильтры).

import math

def local_contrast(tile):
    """tile: квадратный фрагмент яркости 0..255."""
    n = len(tile)
    mean = sum(sum(row) for row in tile) / (n * n)
    var = sum((v - mean) ** 2 for row in tile for v in row) / (n * n)
    return math.sqrt(var)

def line_score(row_contrasts):
    """Доля строк/столбцов с повышенным контрастом — признак ячеистой сети."""
    if not row_contrasts:
        return 0.0
    hi = sum(1 for c in row_contrasts if c > 14.0)
    return hi / len(row_contrasts)

def classify_tile(tile, thr_contrast=12.0, thr_line=0.35):
    c = local_contrast(tile)
    if c < thr_contrast:
        return {"вердикт": "дно", "контраст": round(c, 1)}
    rows = [local_contrast([row]) for row in tile]
    cols = [local_contrast([[tile[r][i] for r in range(len(tile))]]) for i in range(len(tile[0]))]
    ls = max(line_score(rows), line_score(cols))
    return {"вердикт": "сеть?" if ls >= thr_line else "дно",
            "контраст": round(c, 1), "линейность": round(ls, 2)}

if __name__ == "__main__":
    # Синтетический тайл с «сеткой» и тайл однородного грунта
    net = [[(i * 7 + j * 13) % 40 + (90 if i % 6 == 0 else 0) + (60 if j % 6 == 0 else 0)
            for j in range(24)] for i in range(24)]
    sand = [[118 + (i + j) % 3 for j in range(24)] for i in range(24)]
    print(classify_tile(net))
    print(classify_tile(sand))
    # На 12 км² пилота: 9 кандидатов, 3 подтверждены водолазно (на мелководье до 1,5 м — 4 из 5).
