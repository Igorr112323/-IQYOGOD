# ТЕНЬ КУБАНИ: индекс жаровой нагрузки и теневой коэффициент маршрута
# Индекс — композит температуры воздуха, влажности и радиационного фона.

def heat_index(t_c, rh):
    """Упрощённый индекс жары (аппроксимация Стедмана для 27-42 °С)."""
    if t_c < 27:
        return t_c
    c1 = -8.784; c2 = 1.611; c3 = 2.339; c4 = -0.146
    c5 = -0.012; c6 = -0.016; c7 = 0.002
    return c1 + c2 * t_c + c3 * rh + c4 * t_c * rh + \
           c5 * t_c ** 2 + c6 * rh ** 2 + c7 * t_c ** 2 * rh

def route_shade(segments):
    """segments: список (длина_м, в_тени: bool). Возвращает долю тени."""
    total = sum(s[0] for s in segments)
    shaded = sum(s[0] for s in segments if s[1])
    return shaded / total

def load_reduction(hi_open, hi_shade, shade_old, shade_new):
    """Оценка снижения жаровой нагрузки при переходе на теневой маршрут."""
    hi_old = hi_open * (1 - shade_old) + hi_shade * shade_old
    hi_new = hi_open * (1 - shade_new) + hi_shade * shade_new
    return 100 * (hi_old - hi_new) / hi_old

if __name__ == "__main__":
    hi_sun = heat_index(39.0, 35)          # полдень, открытая площадь
    hi_shade = heat_index(33.0, 45)        # затенённый двор
    r = load_reduction(hi_sun, hi_shade, shade_old=0.22, shade_new=0.58)
    print(f"индекс на площади: {hi_sun:.1f}, в тени: {hi_shade:.1f}")
    print(f"снижение нагрузки на маршруте: −{r:.0f} %")
    # Пилот: −18…−24 % на двух школьных маршрутах.
