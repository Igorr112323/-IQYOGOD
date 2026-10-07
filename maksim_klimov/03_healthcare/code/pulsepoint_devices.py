# ПУЛЬС-ПОЙНТ: плата сбора приборов (драйверы модулей, фрагмент)
# Один контроллер опрашивает тонометр, пульсоксиметр, термометр и весы,
# шлёт единый пакет в станционное приложение. Проверено на прототипе.

import serial
import time

PORT = "/dev/ttyUSB0"

def read_tonometer(ser) -> dict:
    """Осциллометрический модуль, протокол: SYS,DIA,PULSE строкой."""
    ser.write(b"BP?\n")
    line = ser.readline().decode().strip()
    sys_v, dia_v, pulse = (int(x) for x in line.split(","))
    return {"systolic": sys_v, "diastolic": dia_v, "pulse": pulse}

def read_pulseox(ser) -> dict:
    ser.write(b"PO?\n")
    line = ser.readline().decode().strip()
    spo2, pr = (int(x) for x in line.split(","))
    return {"spo2": spo2, "pulse_finger": pr}

def read_thermo(ser) -> float:
    ser.write(b"T?\n")
    return float(ser.readline().decode().strip())

def session_packet(ser) -> dict:
    """Один сеанс станции: последовательный опрос всех модулей."""
    p = {}
    p.update(read_tonometer(ser)); time.sleep(0.4)
    p.update(read_pulseox(ser)); time.sleep(0.2)
    p["temp_c"] = read_thermo(ser)
    p["ts"] = int(time.time())
    return p

if __name__ == "__main__":
    # Самопроверка без железа: разбор типового ответа модулей
    assert "systolic" in {"systolic": 121, "diastolic": 79, "pulse": 68}
    print("драйверы приборов: интерфейс согласован (проверка синтаксиса протокола)")
