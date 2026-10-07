# БИОЩИТ-КУБАНЬ: обработка кривых роста и расчёт титра
# Рабочий модуль задела; проверен на данных ферментаций 5 л и 50 л (2026 г.).
import math

def cfu_from_dilution(colonies: int, dilution: float, volume_plated_ml: float = 0.1) -> float:
    """КОЕ/мл по чашечному посеву."""
    return colonies / (dilution * volume_plated_ml)

def logistic_fit(hours, od):
    """Аппроксимация логистической кривой роста (упрощённо):
    возвращает (r — уд. скорость роста 1/ч, K — плато оптической плотности)."""
    K = max(od)
    r_list = []
    for i in range(1, len(od) - 1):
        if od[i - 1] > 0.05 and od[i + 1] > 0.05 and od[i] < 0.9 * K:
            r_list.append(math.log(od[i + 1] / od[i - 1]) / 2.0)
    r = sum(r_list) / len(r_list) if r_list else 0.0
    return r, K

def titer_estimate(od600: float, calib_coef: float = 1.3e9) -> float:
    """Пересчёт OD600 в КОЕ/мл по калибровочному коэффициенту
    (откалиброван чашечным посевом для БК-12: 1,3×10⁹ КОЕ/мл на ед. OD)."""
    return od600 * calib_coef

def viability_after_storage(v0: float, days: int, k_per_day: float = 0.0009) -> float:
    """Экспоненциальная модель гибели спор при хранении (20–25 °С):
    константа подобрана по нашим данным 90 сут -> 92 %."""
    return v0 * math.exp(-k_per_day * days)

if __name__ == "__main__":
    # Данные ферментации 50 л, 18.06.2026 (фрагмент журнала)
    hours = [0, 6, 12, 18, 24, 30, 36, 48]
    od = [0.08, 0.21, 0.55, 1.10, 1.62, 1.88, 1.95, 1.97]
    r, K = logistic_fit(hours, od)
    titer = titer_estimate(K)
    print(f"уд. скорость роста r = {r:.3f} 1/ч; плато OD = {K:.2f}")
    print(f"титр по окончании ферментации: {titer:.2e} КОЕ/мл")
    v90 = viability_after_storage(1.0, 90)
    print(f"жизнеспособность после 90 сут: {v90*100:.0f} % (измерено 92 ± 3 %)")
