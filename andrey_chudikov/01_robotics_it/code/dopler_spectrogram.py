# -*- coding: utf-8 -*-
"""ДОПЛЕР-СТАДО: извлечение микродоплеровской сигнатуры прохода.

Вход — отсчёты промежуточной частоты радара 24 ГГц (ЛЧМ).
Выход — КВЧФ-представление прохода и вектор из 46 признаков.
Задел проекта, фрагмент исполнялся на прототипе (ферма-партнёр, 2026 г.).
"""
import numpy as np

FS = 2048          # частота дискретизации ПЧ, Гц
FRAME = 256        # окно КВПФ
HOP = 64           # сдвиг окна
BAND_HZ = 250      # полоса анализа микродоплера, Гц

def stft_pass(if_signal: np.ndarray) -> np.ndarray:
    """Коротковременное преобразование Фурье сигнала прохода."""
    win = np.hanning(FRAME)
    n_frames = (len(if_signal) - FRAME) // HOP
    spec = np.zeros((n_frames, FRAME // 2))
    for i in range(n_frames):
        seg = if_signal[i * HOP : i * HOP + FRAME] * win
        spec[i] = np.abs(np.fft.rfft(seg))[: FRAME // 2]
    return spec

def crop_band(spec: np.ndarray, fs: int, max_hz: float = BAND_HZ) -> np.ndarray:
    """Оставляет только микродоплеровскую полосу (шаг + жвачка)."""
    k_max = int(max_hz / (fs / FRAME)) + 1
    return spec[:, :k_max]

def passage_features(spec: np.ndarray) -> np.ndarray:
    """46 признаков сигнатуры: периодика шага, асимметрия, энергия жвачки."""
    t = spec.mean(axis=1)                      # огибающая энергии
    t = t - t.mean()
    # автокорреляция огибающей -> период шага
    ac = np.correlate(t, t, mode="full")[len(t) - 1 :]
    ac = ac / (ac[0] + 1e-9)
    search = ac[40:200]
    step_period = (np.argmax(search) + 40) * HOP / FS
    # спектральная асимметрия левой/правой фаз шага
    half = spec.shape[1] // 2
    asym = np.abs(spec[:, :half].mean() - spec[:, half:].mean()) / (spec.mean() + 1e-9)
    # энергия микровибраций жвачки (40-90 Гц)
    k_lo, k_hi = int(40 / (FS / FRAME)), int(90 / (FS / FRAME))
    chew_energy = spec[:, k_lo:k_hi].mean()
    feats = [step_period, asym, chew_energy,
             spec.std(), t.std(), np.percentile(t, 90) - np.percentile(t, 10)]
    # дополняем до 46 признаков статистиками по частотным поддиапазонам
    bands = np.array_split(spec, 8, axis=1)
    for b in bands:
        feats += [b.mean(), b.std(), np.median(b), b.max(),
                  np.percentile(b, 75) - np.percentile(b, 25)]
    return np.asarray(feats[:46], dtype=float)
