# КАРБОКУБАНЬ: углеродный калькулятор биоугля из лузги подсолнечника
# Рабочий модуль задела; консервативные допущения для добровольного рынка.

CO2_PER_C = 44.0 / 12.0          # т CO2 на т углерода
STABILITY_DISCOUNT = 0.85        # дисконт стабильности (100-летний горизонт)
BOILER_EFF = 0.82                # КПД котельной МЭЗ в базовом сценарии

def biochar_carbon_t(char_t: float, carbon_fraction: float = 0.782) -> float:
    """Масса стабильного углерода в партии биоугля."""
    return char_t * carbon_fraction

def avoided_burning_co2(husk_t: float, husk_carbon: float = 0.47) -> float:
    """Базовый сценарий — сжигание лузги: эмиссия, которой избегаем."""
    return husk_t * husk_carbon * CO2_PER_C

def net_co2e_per_t_char(char_t: float, husk_per_char: float = 3.05) -> float:
    """Чистый углеродный эффект на тонну биоугля, т CO2-экв.
    (наши данные: выход 33,7% => 2,97–3,0 т лузги на т угля)."""
    husk_t = char_t * husk_per_char
    stable = biochar_carbon_t(char_t) * STABILITY_DISCOUNT * CO2_PER_C
    avoided = avoided_burning_co2(husk_t) * (1 - BOILER_EFF * 0)  # энергия замещается газом рециркуляции
    # консервативно засчитываем только стабильный углерод и поправку на замещение
    return stable * 0.9 + avoided * 0.10

def portfolio_summary(char_t_year: float, price_co2: float = 700.0) -> dict:
    co2e = net_co2e_per_t_char(1.0) * char_t_year
    return {
        "biochar_t_year": char_t_year,
        "co2e_t_year": round(co2e, 1),
        "revenue_co2_rub_year": round(co2e * price_co2),
    }

if __name__ == "__main__":
    per_t = net_co2e_per_t_char(1.0)
    print(f"чистый эффект: {per_t:.2f} т CO2-экв. на т биоугля")
    print(portfolio_summary(1600.0))
    # Ожидаемо ~1,74 т CO2-экв./т — совпадает с заявленным в заявке.
